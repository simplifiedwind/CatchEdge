# src/ui.py
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date, datetime, timedelta

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src import llm
from src.arxiv_api import ArxivSearcher, paper_id
from src.excel_exporter import ExcelExporter
from src.markdown_exporter import MarkdownExporter
from src.profile import Profile, load_profiles, save_profiles
from src.scorer import LLMScorer, llm_score
from src.state import last_fetch, load_state, mark_seen


CATEGORY_OPTIONS = [
    ("cs.CV", "计算机视觉"),
    ("cs.LG", "机器学习"),
    ("cs.AI", "人工智能"),
    ("cs.CL", "自然语言处理"),
    ("cs.RO", "机器人"),
    ("cs.GR", "图形学"),
    ("cs.NE", "神经与进化计算"),
    ("eess.IV", "图像视频处理"),
    ("stat.ML", "统计机器学习"),
]


# 每个关键词最多抓多少篇。1000 条 = 10 页 × 3 秒，光等待就半分钟，
# 碰上限流重试能拖到几分钟；对"看最新的"来说 300 条（3 页）足够。
MAX_RESULTS_PER_KEYWORD = 300

# 每次抓取的结果单独放一个文件夹，避免 md/xlsx 在 output 里堆成一坨
OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "output")


def open_with_default_app(path):
    """用系统默认程序打开文件；Windows 上是 os.startfile。"""
    try:
        os.startfile(path)
    except (AttributeError, OSError) as e:
        messagebox.showerror("打不开", f"无法打开：\n{path}\n\n{e}")


class ProgressWindow:
    WIDTH = 360
    HEIGHT = 200

    def __init__(self, parent, on_cancel=None):
        self.top = tk.Toplevel(parent)
        self.top.title("正在抓取...")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.protocol("WM_DELETE_WINDOW", self._cancel)
        self._on_cancel = on_cancel

        parent.update_idletasks()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = px + (pw - self.WIDTH) // 2
        y = py + (ph - self.HEIGHT) // 2
        self.top.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

        tk.Label(self.top, text="正在从 arXiv 抓取论文...",
                 font=("", 11)).pack(pady=(18, 8))
        self.progress = ttk.Progressbar(self.top, mode="indeterminate", length=300)
        self.progress.pack(pady=5)
        self.progress.start(12)
        self.count_label = tk.Label(self.top, text="已抓取 0 篇", fg="gray")
        self.count_label.pack(pady=4)
        tk.Label(self.top, text="arXiv 限流时会自动等待重试，可能需要几分钟",
                 fg="#aaaaaa", font=("", 8)).pack(pady=(0, 6))
        self.cancel_btn = tk.Button(self.top, text="取消", width=10,
                                    command=self._cancel)
        self.cancel_btn.pack()

    def _cancel(self):
        if self._on_cancel:
            self._on_cancel()
        self.cancel_btn.config(state="disabled", text="正在取消...")
        self.count_label.config(text="正在取消，请稍候...")

    def update_count(self, n, page=None):
        if page:
            self.count_label.config(text=f"已抓取 {n} 篇 · 第 {page} 页")
        else:
            self.count_label.config(text=f"已抓取 {n} 篇")

    def set_phase(self, text):
        self.count_label.config(text=text)

    def close(self):
        self.progress.stop()
        self.top.grab_release()
        self.top.destroy()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CatchEdge - arXiv 论文搜索导出")
        self.root.resizable(False, False)

        self.profiles = {}
        try:
            self.profiles = load_profiles()
        except ValueError as e:
            # 配置坏了也不要把窗口崩掉，把可读原因摆到用户面前
            messagebox.showerror("配置文件错误", str(e))

        self._build_widgets()
        self.root.update_idletasks()
        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        # 放到屏幕正中间，否则会由窗口管理器随意摆放
        x = max((self.root.winfo_screenwidth() - w) // 2, 0)
        y = max((self.root.winfo_screenheight() - h) // 2, 0)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_widgets(self):
        profile_frame = tk.Frame(self.root)
        profile_frame.pack(fill="x", padx=20, pady=(18, 0))
        tk.Label(profile_frame, text="研究方向:").pack(side="left")
        self.profile_combo = ttk.Combobox(
            profile_frame, state="readonly", width=26,
            values=[self._profile_label(k, p) for k, p in self.profiles.items()],
        )
        self.profile_combo.pack(side="left", padx=(6, 16))
        self.profile_combo.bind("<<ComboboxSelected>>", self._on_profile_change)

        self.only_new = tk.BooleanVar(value=True)
        tk.Checkbutton(profile_frame, text="只看新增",
                       variable=self.only_new).pack(side="left")

        # 研究方向的增删改：改完立刻写回 profiles.yaml
        manage = tk.Frame(self.root)
        manage.pack(fill="x", padx=20, pady=(4, 0))
        tk.Button(manage, text="新建方向", command=self._on_new_profile,
                  relief="flat", padx=8).pack(side="left")
        tk.Button(manage, text="保存当前设置", command=self._on_save_profile,
                  relief="flat", padx=8).pack(side="left", padx=6)
        tk.Button(manage, text="删除方向", command=self._on_delete_profile,
                  relief="flat", padx=8).pack(side="left")

        tk.Label(self.root, text="搜索关键词（多个用逗号分隔）:",
                 anchor="w").pack(fill="x", padx=20, pady=(12, 4))
        self.keyword_entry = tk.Entry(self.root, width=70)
        self.keyword_entry.pack(padx=20, fill="x")
        self.keyword_entry.focus_set()

        # 日期
        date_frame = tk.LabelFrame(self.root, text="提交日期范围（精确到月）",
                                   padx=10, pady=8)
        date_frame.pack(fill="x", padx=20, pady=(14, 6))

        current_year = datetime.now().year
        years = [str(y) for y in range(current_year, 2005, -1)]
        months = [f"{m:02d}" for m in range(1, 13)]

        tk.Label(date_frame, text="从").grid(row=0, column=0, padx=(0, 4))
        self.start_year = ttk.Combobox(date_frame, values=years, width=6, state="readonly")
        self.start_year.set(str(current_year))
        self.start_year.grid(row=0, column=1)
        tk.Label(date_frame, text="年").grid(row=0, column=2, padx=(2, 6))
        self.start_month = ttk.Combobox(date_frame, values=months, width=4, state="readonly")
        self.start_month.set("01")
        self.start_month.grid(row=0, column=3)
        tk.Label(date_frame, text="月").grid(row=0, column=4, padx=(2, 20))

        tk.Label(date_frame, text="到").grid(row=0, column=5, padx=(0, 4))
        self.end_year = ttk.Combobox(date_frame, values=years, width=6, state="readonly")
        self.end_year.set(str(current_year))
        self.end_year.grid(row=0, column=6)
        tk.Label(date_frame, text="年").grid(row=0, column=7, padx=(2, 6))
        self.end_month = ttk.Combobox(date_frame, values=months, width=4, state="readonly")
        self.end_month.set(f"{datetime.now().month:02d}")
        self.end_month.grid(row=0, column=8)
        tk.Label(date_frame, text="月").grid(row=0, column=9, padx=(2, 0))

        # 分类
        cat_frame = tk.LabelFrame(self.root, text="分类筛选（不勾选 = 不限）",
                                  padx=10, pady=8)
        cat_frame.pack(fill="x", padx=20, pady=(6, 6))

        self.cat_vars = {}
        for idx, (code, name) in enumerate(CATEGORY_OPTIONS):
            var = tk.BooleanVar(value=False)
            self.cat_vars[code] = var
            row = idx // 3
            col = idx % 3
            cb = tk.Checkbutton(cat_frame, text=f"{code} ({name})",
                                variable=var, anchor="w")
            cb.grid(row=row, column=col, sticky="w", padx=6, pady=2)

        # 按钮
        self.search_btn = tk.Button(
            self.root, text="确定并导出（Excel + Markdown）",
            command=self.start_search,
            bg="#4CAF50", fg="white",
            padx=24, pady=6, relief="flat"
        )
        self.search_btn.pack(pady=(14, 8))

        # 「只导出前 N 篇」对两个按钮都生效；默认不勾，绿色按钮保持导出全部
        quick_frame = tk.Frame(self.root)
        quick_frame.pack(pady=(0, 16))
        self.limit_on = tk.BooleanVar(value=False)
        tk.Checkbutton(quick_frame, text="只导出前",
                       variable=self.limit_on).pack(side="left")
        self.limit_top = tk.StringVar(value="20")
        ttk.Spinbox(quick_frame, from_=1, to=200, width=5,
                    textvariable=self.limit_top).pack(side="left", padx=4)
        tk.Label(quick_frame, text="篇").pack(side="left")

        self.quick_btn = tk.Button(
            quick_frame, text="增量跑一轮（上次之后，前 N 篇）",
            command=self.start_quick,
            bg="#2196F3", fg="white", padx=12, pady=3, relief="flat"
        )
        self.quick_btn.pack(side="left", padx=(14, 0))

        if self.profiles:
            first = next(iter(self.profiles))
            self.profile_combo.set(self._profile_label(first, self.profiles[first]))
            self._apply_profile(first)
        else:
            self.search_btn.config(state="disabled")

    @staticmethod
    def _profile_label(key, profile):
        return f"{key}（{profile.name}）"

    def _selected_profile_key(self):
        text = self.profile_combo.get()
        for key, profile in self.profiles.items():
            if text == self._profile_label(key, profile):
                return key
        return None

    def _on_profile_change(self, _event=None):
        key = self._selected_profile_key()
        if key:
            self._apply_profile(key)

    def _apply_profile(self, key):
        """把 profile 的关键词和分类填进界面；日期保持用户自己选的不动。"""
        profile = self.profiles[key]
        self.keyword_entry.delete(0, "end")
        self.keyword_entry.insert(0, ", ".join(profile.keywords))
        for code, var in self.cat_vars.items():
            var.set(code in profile.categories)

    def _score_with_llm(self, papers, profile):
        """给论文补上 LLM 判定。失败时论文不带 score，导出按日期排。"""
        scorer = LLMScorer()

        def on_batch(index, total):
            self.root.after(0, lambda: self.progress_win.set_phase(
                f"正在精判第 {index}/{total} 批"))

        results = scorer.score_many(papers, profile, progress=on_batch)
        for paper in papers:
            hit = results.get(paper_id(paper))
            if not hit:
                continue
            paper.update(
                score=llm_score(hit["relevance"], hit["novelty"]),
                relevance=hit["relevance"],
                novelty=hit["novelty"],
                verdict=hit["verdict"],
                reason=hit["reason"],
            )
        return scorer.last_error

    def _limit_value(self, always=False):
        """返回要截断的篇数；返回 None 表示不限制。

        always=True 用于增量按钮：它必须有个上限，所以无视复选框。
        """
        if not always and not self.limit_on.get():
            return None
        try:
            value = int(self.limit_top.get())
        except (TypeError, ValueError):
            raise ValueError("「只导出前 N 篇」要填一个正整数。")
        if value < 1:
            raise ValueError("「只导出前 N 篇」要填一个正整数。")
        return value

    def _persist_keywords(self, profile_key, keywords):
        """把界面上改过的关键词写回 profiles.yaml，避免下次启动又被还原。"""
        profile = self.profiles.get(profile_key)
        if not profile or list(profile.keywords) == list(keywords):
            return
        profile.keywords = list(keywords)
        try:
            save_profiles(self.profiles)
        except OSError as e:
            print(f"[CatchEdge] 保存关键词失败：{e}")

    def _refresh_profiles(self, select=None):
        values = [self._profile_label(k, p) for k, p in self.profiles.items()]
        self.profile_combo.config(values=values)
        key = select or next(iter(self.profiles))
        self.profile_combo.set(self._profile_label(key, self.profiles[key]))
        self._apply_profile(key)

    def _on_new_profile(self):
        key = simpledialog.askstring(
            "新建研究方向", "短标识（英文/数字，例如 vlm）：", parent=self.root)
        if not key:
            return
        key = key.strip()
        if not key:
            return
        if key in self.profiles:
            messagebox.showwarning("重名", f"已经有一个叫「{key}」的方向了。")
            return

        name = simpledialog.askstring(
            "新建研究方向", "显示名称（例如 视觉语言模型）：", parent=self.root)
        name = (name or "").strip() or key

        self.profiles[key] = Profile(name=name)
        try:
            save_profiles(self.profiles)
        except OSError as e:
            messagebox.showerror("保存失败", f"写不进 profiles.yaml：\n{e}")
            return
        self._refresh_profiles(select=key)
        messagebox.showinfo(
            "已创建",
            f"已新增「{name}」。\n\n关键词还是空的，填好后点「保存当前设置」。")

    def _on_delete_profile(self):
        key = self._selected_profile_key()
        if not key:
            return
        if len(self.profiles) <= 1:
            messagebox.showwarning("不能删", "至少要留一个研究方向。")
            return
        profile = self.profiles[key]
        if not messagebox.askyesno(
                "删除方向",
                f"确定删除「{profile.name}」？\n\n只删配置，不会删已导出的结果。"):
            return
        del self.profiles[key]
        try:
            save_profiles(self.profiles)
        except OSError as e:
            messagebox.showerror("保存失败", f"写不进 profiles.yaml：\n{e}")
            return
        self._refresh_profiles()

    def _on_save_profile(self):
        key = self._selected_profile_key()
        if not key:
            return
        keywords = [k.strip() for k in self.keyword_entry.get().split(",")]
        keywords = [k for k in keywords if k]
        if not keywords:
            messagebox.showwarning("不能保存", "关键词不能为空。")
            return

        profile = self.profiles[key]
        profile.keywords = keywords
        profile.categories = [code for code, var in self.cat_vars.items() if var.get()]
        try:
            save_profiles(self.profiles)
        except OSError as e:
            messagebox.showerror("保存失败", f"写不进 profiles.yaml：\n{e}")
            return
        messagebox.showinfo(
            "已保存",
            f"「{profile.name}」已写入 profiles.yaml：\n"
            f"关键词 {len(keywords)} 个，分类 {len(profile.categories)} 个。\n\n"
            f"terms / exclude / interest 需要直接编辑文件。")

    def start_search(self):
        profile_key = self._selected_profile_key()
        if not profile_key:
            messagebox.showwarning("配置缺失", "请选择一个研究方向。")
            return

        keywords = [k.strip() for k in self.keyword_entry.get().split(",")]
        keywords = [k for k in keywords if k]
        if not keywords:
            messagebox.showwarning("输入错误", "请输入搜索关键词。")
            return

        start_ym = (int(self.start_year.get()), int(self.start_month.get()))
        end_ym = (int(self.end_year.get()), int(self.end_month.get()))

        if start_ym > end_ym:
            messagebox.showwarning("日期错误", "起始年月不能晚于结束年月。")
            return

        categories = [code for code, var in self.cat_vars.items() if var.get()]

        try:
            top = self._limit_value()
        except ValueError as e:
            messagebox.showwarning("输入错误", str(e))
            return

        self._persist_keywords(profile_key, keywords)

        self.search_btn.config(state="disabled")
        self.quick_btn.config(state="disabled")
        self.cancel_event = threading.Event()
        self.progress_win = ProgressWindow(self.root, on_cancel=self.cancel_event.set)

        threading.Thread(
            target=self._do_search,
            args=(profile_key, keywords, start_ym, end_ym, categories,
                  self.only_new.get(), self.cancel_event.is_set, None, top),
            daemon=True,
        ).start()

    def start_quick(self):
        """增量模式：不选日期，从上次抓取日之后抓，只导出分数最高的前 N 篇。"""
        profile_key = self._selected_profile_key()
        if not profile_key:
            messagebox.showwarning("配置缺失", "请选择一个研究方向。")
            return

        keywords = [k.strip() for k in self.keyword_entry.get().split(",")]
        keywords = [k for k in keywords if k]
        if not keywords:
            messagebox.showwarning("输入错误", "请输入搜索关键词。")
            return

        try:
            top = self._limit_value(always=True)
        except ValueError as e:
            messagebox.showwarning("输入错误", str(e))
            return

        since = last_fetch(profile_key)
        if since is None:
            since = date.today() - timedelta(days=7)
            print(f"[CatchEdge] 没有抓取记录，本次抓最近 7 天（{since} 起）")

        today = date.today()
        categories = [code for code, var in self.cat_vars.items() if var.get()]

        self._persist_keywords(profile_key, keywords)

        self.search_btn.config(state="disabled")
        self.quick_btn.config(state="disabled")
        self.cancel_event = threading.Event()
        self.progress_win = ProgressWindow(self.root, on_cancel=self.cancel_event.set)

        threading.Thread(
            target=self._do_search,
            args=(profile_key, keywords, (since.year, since.month),
                  (today.year, today.month), categories, True,
                  self.cancel_event.is_set, since, top),
            daemon=True,
        ).start()

    def _do_search(self, profile_key, keywords, start_ym, end_ym, categories,
                   only_new, should_stop=None, since=None, top=None):
        try:
            searcher = ArxivSearcher(max_results=MAX_RESULTS_PER_KEYWORD)

            def on_progress(count, page):
                self.root.after(0, lambda: self.progress_win.update_count(count, page))

            # 一个方向可能配了多个关键词：分别搜，再按 arXiv id 合并去重
            fetched = {}
            errors = []
            truncated = False
            cancelled = False
            for kw in keywords:
                if should_stop and should_stop():
                    cancelled = True
                    break
                result = searcher.search(
                    kw, start_ym, end_ym,
                    categories=categories,
                    progress_callback=on_progress,
                    should_stop=should_stop,
                    since=since,
                )
                if result.cancelled:
                    cancelled = True
                    break
                if result.error:
                    errors.append(result.error)
                truncated = truncated or result.truncated
                for paper in result.papers:
                    fetched.setdefault(paper_id(paper), paper)

            if cancelled:
                self.root.after(0, lambda: self._on_finish(
                    False, "已取消本次抓取（没有导出，也没记进「已看过」）。",
                    None, None))
                return

            papers_all = list(fetched.values())
            if not papers_all:
                if errors:
                    # 抓取中断时不要把"接口失败"误报成"没搜到论文"
                    msg = errors[0]
                    self.root.after(0, lambda: self._on_finish(False, msg, None, None))
                elif since is not None:
                    msg = (f"增量窗口是 {since} 之后，这段时间没有新论文。\n\n"
                           f"如果你刚刚跑过一次，这是正常的——"
                           f"改天再点，或者用上面的「确定并导出」按日期范围抓。")
                    self.root.after(0, lambda: self._on_finish(True, msg, None, None))
                else:
                    msg = "未找到相关论文，请调整关键词、日期或分类。"
                    self.root.after(0, lambda: self._on_finish(False, msg, None, None))
                return

            seen = load_state(profile_key)["seen_ids"]
            new_papers = [p for p in papers_all if paper_id(p) not in seen]
            papers = new_papers if only_new else papers_all

            # 抓到的全部记账，不论这次是否展示，否则关掉"只看新增"再打开会重复
            # 有请求失败时不推进 last_fetch，否则增量模式会永久漏掉那段时间
            mark_seen(profile_key, list(fetched), date.today(),
                      advance_date=not errors)

            if not papers:
                msg = f"抓取到 {len(papers_all)} 篇，新增 0 篇（这些论文都已看过）。"
                self.root.after(0, lambda: self._on_finish(True, msg, None, None))
                return

            llm_error = self._score_with_llm(papers, self.profiles[profile_key])
            papers.sort(key=lambda p: p.get('published', ''), reverse=True)
            papers.sort(key=lambda p: p.get('score', -1), reverse=True)
            if top:
                papers = papers[:top]

            base_name = f"daily_{profile_key}_{date.today():%Y-%m-%d}"
            if top:
                base_name += f"_top{top}"
            run_dir = os.path.join(OUTPUT_ROOT, base_name)
            excel_path = ExcelExporter.export(papers, filename="report.xlsx",
                                              output_dir=run_dir)

            meta = {
                'keyword': ", ".join(keywords),
                'start_ym': start_ym,
                'end_ym': end_ym,
                'categories': categories,
            }
            md_path = MarkdownExporter.export(papers, meta, filename="report.md",
                                              output_dir=run_dir)

            if excel_path and md_path:
                seen_count = len(papers_all) - len(new_papers)
                if since is not None:
                    head = (f"增量模式：抓取 {len(papers_all)} 篇，"
                            f"新增 {len(new_papers)} 篇")
                else:
                    head = (f"共抓取 {len(papers_all)} 篇：新增 {len(new_papers)} 篇，"
                            f"已见过 {seen_count} 篇")
                if top:
                    head += f"，只保留最值得看的前 {len(papers)} 篇"
                else:
                    head += f"，本次导出 {len(papers)} 篇"
                msg = f"{head}\n\nExcel: {excel_path}\nMarkdown: {md_path}"
                if llm.USAGE["prompt_tokens"]:
                    msg += (f"\n\n模型用量 {llm.USAGE['prompt_tokens']} 输入 / "
                            f"{llm.USAGE['completion_tokens']} 输出 tokens，"
                            f"约 {llm.estimate_cost():.4f} 元")
                if llm_error:
                    msg += f"\n\n注意：模型调用有问题，部分论文只有规则分。\n{llm_error}"
                if truncated:
                    msg += (f"\n\n注意：结果被截断（已达 {searcher.max_results} 条上限），"
                            f"可能还有更多论文。")
                if errors:
                    msg += f"\n\n有 {len(errors)} 次请求失败：\n" + "\n".join(errors)
                self.root.after(0, lambda: self._on_finish(True, msg, excel_path, md_path))
            else:
                self.root.after(0, lambda: self._on_finish(
                    False, "部分文件导出失败，请查看控制台输出。", excel_path, md_path))

        except Exception as e:
            self.root.after(0, lambda: self._on_finish(False, f"发生错误: {e}", None, None))

    def _on_finish(self, success, message, excel_path, md_path):
        if hasattr(self, "progress_win") and self.progress_win:
            self.progress_win.close()
            self.progress_win = None

        self.search_btn.config(state="normal")
        self.quick_btn.config(state="normal")

        if success:
            if md_path:
                # 直接把 Markdown 打开，省得去文件夹里翻
                if messagebox.askyesno("完成", message + "\n\n要现在打开 Markdown 吗？"):
                    open_with_default_app(md_path)
            else:
                messagebox.showinfo("完成", message)
        else:
            messagebox.showerror("错误", message)


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
    except Exception:
        # 双击 .bat 用 pythonw 启动时没有控制台，异常只能落盘
        import traceback
        log_dir = os.path.join(PROJECT_ROOT, "output")
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, "ui_error.log"), "a", encoding="utf-8") as f:
            f.write(traceback.format_exc() + "\n")
        raise