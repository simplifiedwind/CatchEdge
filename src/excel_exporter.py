# src/excel_exporter.py
import os
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# 颜色（ARGB，不带 #）
COLOR_ACCEPTED = "FF2E7D32"      # 深绿：已接收
COLOR_UNDER_REVIEW = "FFED7D31"  # 橙：审稿中

# 列顺序：判定紧跟在标题后面，别让人往右翻才知道该不该看
COL_TITLE = 1
COL_VERDICT = 2
COL_RELEVANCE = 3
COL_NOVELTY = 4
COL_REASON = 5
COL_SUMMARY = 6
COL_LINK = 7
COL_PUBLISHED = 8
COL_CATEGORY = 9
COL_COMMENT = 10

HEADERS = ["标题", "判定", "相关度", "创新度", "理由", "摘要",
           "arXiv 链接", "发布日期", "分类", "Comment"]

WIDTHS = {COL_TITLE: 50, COL_VERDICT: 10, COL_RELEVANCE: 8, COL_NOVELTY: 8,
          COL_REASON: 60, COL_SUMMARY: 80, COL_LINK: 35, COL_PUBLISHED: 15,
          COL_CATEGORY: 12, COL_COMMENT: 45}


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

        ws.append(HEADERS)

        header_font = Font(bold=True)
        for col_num in range(1, len(HEADERS) + 1):
            cell = ws.cell(row=1, column=col_num)
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center')

        for paper in papers:
            ws.append([
                paper.get('title', ''),
                paper.get('verdict', ''),
                paper.get('relevance', ''),
                paper.get('novelty', ''),
                paper.get('reason', ''),
                paper.get('summary', ''),
                paper.get('link', ''),
                paper.get('published', ''),
                paper.get('category', ''),
                paper.get('comment', ''),
            ])

        for col, width in WIDTHS.items():
            ws.column_dimensions[get_column_letter(col)].width = width

        # 需要自动换行的列：标题 / 理由 / 摘要 / Comment
        for col in (COL_TITLE, COL_REASON, COL_SUMMARY, COL_COMMENT):
            for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
                for cell in row:
                    cell.alignment = Alignment(wrap_text=True, vertical='top')

        # 判定列加粗居中，扫一眼就能看出该不该看
        for row in ws.iter_rows(min_row=2, min_col=COL_VERDICT, max_col=COL_VERDICT):
            for cell in row:
                cell.alignment = Alignment(horizontal='center', vertical='top')
                if cell.value == "精读":
                    cell.font = Font(bold=True, color=COLOR_ACCEPTED)
                elif cell.value == "跳过":
                    cell.font = Font(color="FF9E9E9E")

        # arXiv 链接超链接化
        for row in ws.iter_rows(min_row=2, min_col=COL_LINK, max_col=COL_LINK):
            for cell in row:
                if cell.value:
                    cell.hyperlink = cell.value
                    cell.font = Font(color="0563C1", underline="single")

        # Comment 关键词高亮
        for row_idx in range(2, len(papers) + 2):
            cell = ws.cell(row=row_idx, column=COL_COMMENT)
            text = (cell.value or '').lower()
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
