# src/excel_exporter.py
import os
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, Alignment


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# 颜色（ARGB，不带 #）
COLOR_ACCEPTED = "FF2E7D32"      # 深绿：已接收
COLOR_UNDER_REVIEW = "FFED7D31"  # 橙：审稿中


class ExcelExporter:
    @staticmethod
    def export(papers, filename=None, output_dir=DEFAULT_OUTPUT_DIR):
        if not papers:
            print("[Excel] 没有数据可导出。")
            return None

        os.makedirs(output_dir, exist_ok=True)
        if filename is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"arxiv_results_{ts}.xlsx"
        filepath = os.path.join(output_dir, filename)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "ArXiv Papers"

        headers = ["标题", "摘要", "arXiv 链接", "发布日期", "分类", "Comment"]
        ws.append(headers)

        header_font = Font(bold=True)
        for col_num in range(1, len(headers) + 1):
            cell = ws.cell(row=1, column=col_num)
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center')

        for paper in papers:
            ws.append([
                paper.get('title', ''),
                paper.get('summary', ''),
                paper.get('link', ''),
                paper.get('published', ''),
                paper.get('category', ''),
                paper.get('comment', ''),
            ])

        # 列宽
        ws.column_dimensions['A'].width = 50
        ws.column_dimensions['B'].width = 80
        ws.column_dimensions['C'].width = 35
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 12
        ws.column_dimensions['F'].width = 45

        # 摘要列自动换行
        for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical='top')

        # Comment 列自动换行
        for row in ws.iter_rows(min_row=2, min_col=6, max_col=6):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical='top')

        # arXiv 链接超链接化
        for row in ws.iter_rows(min_row=2, min_col=3, max_col=3):
            for cell in row:
                if cell.value:
                    cell.hyperlink = cell.value
                    cell.font = Font(color="0563C1", underline="single")

        # Comment 关键词高亮
        for row_idx in range(2, len(papers) + 2):
            cell = ws.cell(row=row_idx, column=6)
            text = (cell.value or '').lower()

            # 先清掉默认颜色干扰（如果你后续给 Comment 加了其他格式，这里保留字体加粗即可）
            if 'accepted' in text:
                cell.font = Font(color=COLOR_ACCEPTED, bold=True)
            elif 'under review' in text:
                cell.font = Font(color=COLOR_UNDER_REVIEW, bold=True)

        try:
            wb.save(filepath)
            print(f"[Excel] 已写入: {filepath}")
            return filepath
        except Exception as e:
            print(f"[Excel] 写入失败: {e}")
            return None