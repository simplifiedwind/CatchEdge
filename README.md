# CatchEdge

按「研究方向」增量抓取 arXiv 新论文，用大模型读摘要判断**值不值得读**，最后给出一份排好序的日报（Markdown + Excel）。

解决的是一件很具体的事：每天不用再翻几十条标题，只看排名最前的几篇；而且只抓上次之后的新论文，不重复、不遗漏。

---

## 功能

- **研究方向配置**：关键词、分类、打分词、排除词、兴趣描述都写在 `profiles.yaml` 里，界面上选一下就行。
- **增量抓取**：`state/seen.json` 记录已看过的论文，`last_fetch` 记录抓到哪天；再点一次只抓新的。
- **两级打分**
  - 规则分：关键词命中标题/摘要、是否 Accepted、是否有开源代码。
  - LLM 精判：读摘要给出相关度、创新度、**精读 / 扫读 / 跳过**，以及一句具体理由。
- **结果缓存**：`cache/scores/` 里一篇一份，同一篇论文只花一次钱；重跑、换日期范围都不重复计费。
- **一次抓取一个文件夹**：`report.md` 和 `report.xlsx` 放在同一个目录里，不再散落。
- **判定前置**：Markdown 标题行直接标 `【精读】`，Excel 判定在第 2 列，扫一眼就能筛。
- **GUI + 命令行**：手动挑日期看全量，或者用增量按钮/命令行跑每日更新。

---

## 安装

推荐 conda：

```bash
conda env create -f environment.yml
conda activate CatchEdge
```

或者已有 Python 环境时：

```bash
python -m pip install -r requirements.txt
```

---

## 配置

### 1. 研究方向：`profiles.yaml`

```yaml
profiles:
  3dad:
    name: 3D 异常检测
    keywords: ["3d anomaly detection", "point cloud anomaly"]   # 用来搜索
    terms: ["3d-ad", "point cloud", "industrial anomaly", "mvtec"]  # 用来打分
    categories: [cs.CV, cs.LG]
    exclude: ["medical"]        # 命中即剔除
    interest: "工业质检中的无监督 3D 异常检测，关注跨域泛化与统一模型"
```

| 字段 | 作用 | 备注 |
|---|---|---|
| `keywords` | 发给 arXiv 的检索词，多个用逗号分隔 | 要宽，否则召回不够 |
| `terms` | 打分用的领域专有词 | 要窄，用同行绕不开的说法；不填则退回用 `keywords` |
| `categories` | arXiv 分类，不填 = 不限 | 注意 `cat:` 会匹配交叉挂载 |
| `exclude` | 命中即剔除 | 可选 |
| `interest` | 会放进 LLM 的 prompt | 写得越具体，判断越准 |

`terms` 是打分准不准的关键。换了方向之后，先想「这个领域的人写论文一定会提到哪几个词」。

> 界面里的「新建 / 保存 / 删除」会重写整个 `profiles.yaml`：字段说明保留在文件头，
> 但你手写在文件里的行内注释会被覆盖。想保留自定义注释就只改文件、不用界面按钮。

### 2. 大模型：环境变量

```powershell
setx CATCHEDGE_LLM_API_KEY "sk-..."
setx CATCHEDGE_LLM_BASE_URL "https://api.deepseek.com"
setx CATCHEDGE_LLM_MODEL "deepseek-flash"
```

设完要**新开一个终端**才生效。没有配置 key 时会自动退回只用规则分，不会崩。

---

## 使用

### 图形界面

三种启动方式，任选：

1. 双击 `src\start_cmd.bat`
2. 双击项目根目录的 `CatchEdge.lnk`（可拖到桌面或固定到任务栏）
3. `python src/ui.py`

窗口顶部是研究方向选择，下面三个按钮用来管理它：

| 按钮 | 作用 |
|---|---|
| **新建方向** | 填一个短标识（如 `vlm`）和显示名，写入 `profiles.yaml` |
| **保存当前设置** | 把输入框里的关键词和勾选的分类存回当前方向 |
| **删除方向** | 从配置文件里移除该方向（不会删已导出的结果；至少保留一个） |

关键词改完直接点搜索也会自动保存，不用特意去点保存。

再往下是两个执行按钮：

| 按钮 | 用途 |
|---|---|
| **确定并导出**（绿） | 按你选的年月范围抓。勾了「只导出前 N 篇」就只留分数最高的 N 篇，否则导出全部 |
| **增量跑一轮**（蓝） | 自动从上次抓取日之后抓，强制只看新增；始终按「前 N 篇」截断 |

抓取成功后可以直接点"是"打开 Markdown。

> 「只导出前 N 篇」对两个按钮都生效，但默认不勾——绿色按钮保持"导出全部"，蓝色按钮无视勾选状态、始终截断。

### 命令行

```bash
python -m src.run --profile 3dad --since last --top 20
```

| 参数 | 默认 | 说明 |
|---|---|---|
| `--profile` | 必填 | `profiles.yaml` 里的 key |
| `--since` | `last` | `last` 表示从上次抓取日之后，也可以写 `2026-11-01` |
| `--top` | 20 | 只导出前 N 篇 |
| `--no-llm` | — | 只用规则分，不调用模型 |

想每天早上自动跑，可以挂计划任务：

```powershell
schtasks /create /tn "CatchEdge 日报" /tr "cmd /c cd /d D:\practice\CatchEdge && python -m src.run --profile 3dad --since last --top 20" /sc daily /st 08:30 /f
```

### 输出

```
output/
└── daily_3dad_2026-11-20_top20/
    ├── report.md
    └── report.xlsx
```

Markdown 片段：

```markdown
## 1. 【精读】AggCLIP: Aggregating CLIP for Zero-Shot Multimodal Anomaly Detection

- **理由**：冻结CLIP做零样本多模态异常检测，几何感知聚合与双流提示对比损失，含跨数据集零样本实验。
- **相关度**：5 · **创新度**：4
- **arXiv**：[2611.24643v1](http://arxiv.org/abs/2611.24643v1)
- **摘要**：...
```

---

## 花费

按 `deepseek-flash` 空闲时段价实测：

| 规模 | 花费 |
|---|---|
| 单篇 | 约 0.0006 元 |
| 10 篇 | 约 0.6 分 |
| 85 篇 | 约 5 分 |
| 一年（7200 篇） | 约 5 元 |

一篇论文只判一次，之后都走缓存。想更省就在空闲时段跑（工作日晚间、周末全天，价格是高峰的一半）。

---

## 常见问题

**提示「arXiv 限流(429)」**
请求太频繁被临时拒绝。等 5~10 分钟再试，别反复点。程序内部已做 3 次退避重试（15/30 秒）和实例级 3 秒间隔。

**增量跑一轮提示「这段时间没有新论文」**
正常。你当天已经跑过一次的话，增量窗口里确实没有新东西。想看历史就用绿色按钮。

**窗口打不开 / 闪退**
用 `pythonw` 启动时没有控制台，异常会写进 `output/ui_error.log`，先看那个文件。

**想从头开始**
删掉 `state/` 目录即可（会重新把历史论文当成新的）。

---

## 项目结构

```
src/
├── ui.py               # 图形界面
├── run.py              # 命令行入口（不依赖 tkinter）
├── arxiv_api.py        # arXiv API 封装：查询构造、分页、限流重试
├── profile.py          # 读取 profiles.yaml
├── state.py            # 已看过的论文、增量进度
├── scorer.py           # 规则打分 + LLM 精判 + 结果缓存
├── llm.py              # DeepSeek 请求封装
├── excel_exporter.py   # Excel 导出
└── markdown_exporter.py# Markdown 导出
```

`state/`、`cache/`、`output/` 都是本地产物，已在 `.gitignore` 中忽略。

---

## 已知限制

- **只有 arXiv 一个来源**。CV/多模态方向的最新工作基本都先上 arXiv，其他领域的覆盖会弱一些。
- **规则分只看字面**，语义判断靠 LLM；不配置 key 时排序质量会明显下降。
- **同一天同一方向重复跑会覆盖同名文件夹**（按日期命名）。
- **每个关键词最多抓 300 篇**，超出会提示"结果被截断"——对"只看最新的"够用，要更多得改 `src/ui.py` 里的 `MAX_RESULTS_PER_KEYWORD`。
- 论文的"Accepted / Under review"来自 arXiv 的 comment 字段，是自由文本，信息不全。

开发过程与后续计划见 [PLAN.md](PLAN.md)。
