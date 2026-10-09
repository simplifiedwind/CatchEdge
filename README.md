# CatchEdge

一个用来抓取 arXiv 论文并导出为 Excel / Markdown 的桌面小工具，
主要用于快速收集某一方向的最新论文，供后续的科研趋势分析使用
（例如把 Markdown 直接喂给 LLM，让它总结创新点分布与竞争态势）。

## 功能

- **关键词搜索**：支持多词，例如 `3d anomaly detection`。
- **日期精确到月**：选择起始年月 ~ 结束年月，而不是只能选年份。
- **分类筛选**：可多选 `cs.CV` / `cs.LG` / `cs.AI` 等常用 arXiv 分类，不勾选 = 不限。
- **按提交日期排序**：结果从新到旧。
- **双格式导出**：
  - `Excel (.xlsx)`：给你自己看，带列宽、自动换行、链接可点击。
  - `Markdown (.md)`：给 agent / LLM 看，按「Accepted / Under review / 其他」分组，
    文件头部自带一段“给分析 agent 的指令”，复制粘贴即用。
- **Comment 高亮**：Excel 中 Comment 含 `Accepted` 显示深绿色加粗，
  含 `Under review` 显示橙色加粗。
- **文件名带时间戳**：多次搜索不会互相覆盖。
- **进度提示**：点击搜索后弹出居中进度窗，实时显示已抓取条数。

## 快速开始

### 方式一：conda（推荐）

```bash
conda env create -f environment.yml
conda activate CatchEdge
python src/ui.py