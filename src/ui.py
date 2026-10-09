# src/ui.py
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.arxiv_api import ArxivSearcher
from src.excel_exporter import ExcelExporter


# 常用分类，可按需扩展
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


class ProgressWindow:
    """点击搜索后弹出的独立进度窗口，居中显示。"""

    WIDTH = 360
    HEIGHT = 140

    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("正在抓取...")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()  # 模态
        # 屏蔽关闭按钮，防止误关
        self.top.protocol("WM_DELETE_WINDOW", lambda: None)

        # ---- 居中定位 ----
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

        tk.Label(self.top, text="请勿关闭本窗口", fg="#aaaaaa",
                 font=("", 8)).pack()

    def update_count(self, n):
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
        # 先画一遍控件再自适应大小，避免底部留白
        self._build_widgets()
        self.root.update_idletasks()
        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        self.root.geometry(f"{w}x{h}")

    def _build_widgets(self):
        # ---- 关键词 ----
        tk.Label(self.root, text="搜索关键词 (例如: 3d anomaly detection):",
                 anchor="w").pack(fill="x", padx=20, pady=(18, 4))
        self.keyword_entry = tk.Entry(self.root, width=70)
        self.keyword_entry.pack(padx=20, fill="x")
        self.keyword_entry.focus_set()

        # ---- 日期范围 ----
        date_frame = tk.LabelFrame(self.root, text="选择文章提交日期范围（精确到月）",
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

        # ---- 分类多选 ----
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

        # ---- 按钮 ----
        self.search_btn = tk.Button(
            self.root, text="确定并导出 Excel",
            command=self.start_search,
            bg="#4CAF50", fg="white",
            padx=24, pady=6, relief="flat"
        )
        self.search_btn.pack(pady=(14, 18))

    # ---------- 事件 ----------
    def start_search(self):
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("输入错误", "请输入搜索关键词。")
            return

        start_ym = (int(self.start_year.get()), int(self.start_month.get()))
        end_ym = (int(self.end_year.get()), int(self.end_month.get()))

        if start_ym > end_ym:
            messagebox.showwarning("日期错误", "起始年月不能晚于结束年月。")
            return

        categories = [code for code, var in self.cat_vars.items() if var.get()]

        self.search_btn.config(state="disabled")
        self.progress_win = ProgressWindow(self.root)

        threading.Thread(
            target=self._do_search,
            args=(keyword, start_ym, end_ym, categories),
            daemon=True,
        ).start()

    def _do_search(self, keyword, start_ym, end_ym, categories):
        try:
            searcher = ArxivSearcher()

            def on_progress(count, _total):
                self.root.after(0, lambda: self.progress_win.update_count(count))

            papers = searcher.search(
                keyword, start_ym, end_ym,
                categories=categories,
                progress_callback=on_progress,
            )

            if not papers:
                self.root.after(0, lambda: self._on_finish(
                    False, "未找到相关论文，请调整关键词、日期或分类。", None))
                return

            kw = keyword.replace(' ', '_').replace('/', '_')
            ym = f"{start_ym[0]}{start_ym[1]:02d}-{end_ym[0]}{end_ym[1]:02d}"
            filename = f"arxiv_{kw}_{ym}.xlsx"
            filepath = ExcelExporter.export(papers, filename=filename)

            if filepath:
                msg = f"下载成功！共 {len(papers)} 篇，已保存至:\n{filepath}"
                self.root.after(0, lambda: self._on_finish(True, msg, filepath))
            else:
                self.root.after(0, lambda: self._on_finish(
                    False, "导出 Excel 时发生错误。", None))

        except Exception as e:
            self.root.after(0, lambda: self._on_finish(False, f"发生错误: {e}", None))

    def _on_finish(self, success, message, filepath):
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