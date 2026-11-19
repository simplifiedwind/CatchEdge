# src/ui.py
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.arxiv_api import ArxivSearcher, paper_id
from src.excel_exporter import ExcelExporter
from src.markdown_exporter import MarkdownExporter
from src.profile import load_profiles
from src.state import load_state, mark_seen


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
        self.root.geometry(f"{w}x{h}")

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
        self.search_btn.pack(pady=(14, 18))

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

        self.search_btn.config(state="disabled")
        self.cancel_event = threading.Event()
        self.progress_win = ProgressWindow(self.root, on_cancel=self.cancel_event.set)

        threading.Thread(
            target=self._do_search,
            args=(profile_key, keywords, start_ym, end_ym, categories,
                  self.only_new.get(), self.cancel_event.is_set),
            daemon=True,
        ).start()

    def _do_search(self, profile_key, keywords, start_ym, end_ym, categories,
                   only_new, should_stop=None):
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
                # 抓取中断时不要把"接口失败"误报成"没搜到论文"
                msg = errors[0] if errors else "未找到相关论文，请调整关键词、日期或分类。"
                self.root.after(0, lambda: self._on_finish(False, msg, None, None))
                return

            seen = load_state(profile_key)["seen_ids"]
            new_papers = [p for p in papers_all if paper_id(p) not in seen]
            papers = new_papers if only_new else papers_all

            # 抓到的全部记账，不论这次是否展示，否则关掉"只看新增"再打开会重复
            mark_seen(profile_key, list(fetched), date.today())

            if not papers:
                msg = f"抓取到 {len(papers_all)} 篇，新增 0 篇（这些论文都已看过）。"
                self.root.after(0, lambda: self._on_finish(True, msg, None, None))
                return

            base_name = f"daily_{profile_key}_{date.today():%Y-%m-%d}"
            excel_path = ExcelExporter.export(papers, filename=f"{base_name}.xlsx")

            meta = {
                'keyword': ", ".join(keywords),
                'start_ym': start_ym,
                'end_ym': end_ym,
                'categories': categories,
            }
            md_path = MarkdownExporter.export(papers, meta, filename=f"{base_name}.md")

            if excel_path and md_path:
                seen_count = len(papers_all) - len(new_papers)
                msg = (f"共抓取 {len(papers_all)} 篇：新增 {len(new_papers)} 篇，"
                       f"已见过 {seen_count} 篇，本次导出 {len(papers)} 篇\n\n"
                       f"Excel: {excel_path}\n"
                       f"Markdown: {md_path}")
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

        if success:
            messagebox.showinfo("完成", message)
        else:
            messagebox.showerror("错误", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()