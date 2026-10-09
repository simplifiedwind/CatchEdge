# src/ui.py
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# 把项目根目录加入 sys.path，保证从任意位置运行都能 import src.xxx
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.arxiv_api import ArxivSearcher
from src.excel_exporter import ExcelExporter


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CatchEdge - arXiv 论文搜索导出")
        self.root.geometry("520x320")
        self.root.resizable(False, False)

        # 关键词输入
        tk.Label(root, text="搜索关键词 (例如: 3d anomaly detection):").pack(pady=(20, 5))
        self.keyword_entry = tk.Entry(root, width=60)
        self.keyword_entry.pack(pady=5)
        self.keyword_entry.focus_set()

        # 年份选择
        tk.Label(root, text="选择年份:").pack(pady=(15, 5))
        current_year = datetime.now().year
        self.year_var = tk.StringVar(value=str(current_year))
        years = [str(y) for y in range(current_year, 2010, -1)]
        self.year_combo = ttk.Combobox(
            root, textvariable=self.year_var, values=years, state="readonly", width=20
        )
        self.year_combo.pack(pady=5)

        # 搜索按钮
        self.search_btn = tk.Button(
            root, text="确定并导出 Excel",
            command=self.start_search,
            bg="#4CAF50", fg="white",
            padx=20, pady=5, relief="flat"
        )
        self.search_btn.pack(pady=25)

        # 状态标签
        self.status_label = tk.Label(root, text="就绪", fg="gray")
        self.status_label.pack(pady=5)

    def start_search(self):
        keyword = self.keyword_entry.get().strip()
        year = self.year_var.get()

        if not keyword:
            messagebox.showwarning("输入错误", "请输入搜索关键词。")
            return

        self.search_btn.config(state="disabled")
        self.status_label.config(text="正在搜索 arXiv，请稍候...", fg="blue")
        self.root.update_idletasks()

        threading.Thread(target=self._do_search, args=(keyword, year), daemon=True).start()

    def _do_search(self, keyword, year):
        try:
            searcher = ArxivSearcher()
            papers = searcher.search(keyword, int(year))

            if not papers:
                self.root.after(0, lambda: self._on_finish(
                    False, "未找到相关论文，请尝试其他关键词或年份。", None))
                return

            # 文件名：关键词 + 年份
            safe_kw = keyword.replace(' ', '_').replace('/', '_')
            filename = f"arxiv_{safe_kw}_{year}.xlsx"
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
        self.search_btn.config(state="normal")
        self.status_label.config(
            text="下载成功" if success else "失败",
            fg="green" if success else "red"
        )
        if success:
            messagebox.showinfo("完成", message)
        else:
            messagebox.showerror("错误", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()