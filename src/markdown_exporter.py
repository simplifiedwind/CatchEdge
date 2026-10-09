# src/markdown_exporter.py
import os
from datetime import datetime


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# 顶部附带的"给 agent 的提示词"，可按需修改
AGENT_PROMPT = (
    "> 请你阅读下面这份论文快照，完成以下任务：\n"
    "> 1. 按「研究子方向」对论文聚类，给出每个子方向的核心创新点；\n"
    "> 2. 标出哪些创新点已经被 Accepted 论文占据（= 已被抢先）；\n"
    "> 3. 指出在 Under review 论文中，哪些方向竞争最激烈；\n"
    "> 4. 给出 2-3 个「目前还空着、值得下注」的方向。\n"
    "> 5. 对于 Under review 的论文，请特别注意它们的创新点是否与 Accepted 论文高度重叠——这类意味着窗口期已基本关闭。\n"
)


class MarkdownExporter:
    @staticmethod
    def export(papers, meta, filename=None, output_dir=DEFAULT_OUTPUT_DIR):
        """
        :param papers: 论文列表（与 ExcelExporter 相同的结构）
        :param meta: 元信息 dict，包含 keyword / start_ym / end_ym / categories
        :param filename: 输出文件名；None 则自动生成
        :param output_dir: 输出目录
        :return: 完整文件路径，失败返回 None
        """
        if not papers:
            print("[Markdown] 没有数据可导出。")
            return None

        os.makedirs(output_dir, exist_ok=True)
        if filename is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"arxiv_results_{ts}.md"
        filepath = os.path.join(output_dir, filename)

        # ---- 按状态分组 ----
        accepted, under_review, others = [], [], []
        for p in papers:
            text = (p.get('comment') or '').lower()
            if 'accepted' in text:
                accepted.append(p)
            elif 'under review' in text:
                under_review.append(p)
            else:
                others.append(p)

        keyword = meta.get('keyword', '')
        start_ym = meta.get('start_ym', ('', ''))
        end_ym = meta.get('end_ym', ('', ''))
        categories = meta.get('categories') or []
        cat_str = ", ".join(categories) if categories else "不限"
        ym_str = (f"{start_ym[0]}-{start_ym[1]:02d} ~ "
                  f"{end_ym[0]}-{end_ym[1]:02d}")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        lines = []
        # ---- 头部元信息 ----
        lines.append("# arXiv 科研趋势快照\n")
        lines.append(f"- 查询关键词：`{keyword}`")
        lines.append(f"- 时间范围：{ym_str}")
        lines.append(f"- 分类：{cat_str}")
        lines.append(f"- 抓取时间：{now}")
        lines.append(f"- 论文总数：{len(papers)}")
        lines.append(f"- 状态分布：Accepted {len(accepted)} 篇 / "
                     f"Under review {len(under_review)} 篇 / "
                     f"其他 {len(others)} 篇\n")
        lines.append("---\n")

        # ---- 给 agent 的提示词 ----
        lines.append("## 给分析 agent 的指令\n")
        lines.append(AGENT_PROMPT)
        lines.append("\n---\n")

        # ---- 分组内容 ----
        lines.extend(MarkdownExporter._render_group(
            "✅ 已接收（Accepted）— 创新点已定局", accepted))
        lines.extend(MarkdownExporter._render_group(
            "🟡 审稿中（Under review）— 创新点竞争窗口", under_review))
        lines.extend(MarkdownExporter._render_group(
            "⚪ 其他", others))

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            print(f"[Markdown] 已写入: {filepath}")
            return filepath
        except Exception as e:
            print(f"[Markdown] 写入失败: {e}")
            return None

    @staticmethod
    def _render_group(title, papers):
        """渲染一个分组（Accepted / Under review / 其他）。"""
        out = [f"## {title}\n"]
        if not papers:
            out.append("_（本组为空）_\n")
            return out

        for idx, p in enumerate(papers, 1):
            title_text = p.get('title', '').strip() or '(无标题)'
            link = p.get('link', '')
            published = p.get('published', '')
            category = p.get('category', '')
            comment = p.get('comment', '') or '—'
            summary = p.get('summary', '').strip()

            out.append(f"### {idx}. {title_text}\n")
            out.append(f"- **arXiv**: [{link.split('/')[-1]}]({link})")
            out.append(f"- **提交日期**: {published}")
            out.append(f"- **分类**: {category}")
            out.append(f"- **Comment**: {comment}")
            out.append(f"- **摘要**: {summary}")
            out.append("- **核心创新**（待 agent 提炼）: \n")
        return out