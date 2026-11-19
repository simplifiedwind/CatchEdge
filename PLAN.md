# CatchEdge 改进计划

> 本文件是唯一的计划依据。每完成一个步骤，就把对应的 `- [ ]` 改成 `- [x]`，
> 并在文末「进度记录」表里追加一行。开工前先读「当前状态」。

## 当前状态

- 最后更新：2026-11-19
- 当前阶段：**阶段 3 已完成**（阶段 1~3 全部完成，阶段 4 按计划暂缓）
- 下一件要做的事：无；等前三个阶段稳定运行两周后再评估是否启动阶段 4

---

## 一、目标（初心）

每天自动拿到**自己研究领域内最新出现的论文**，读到的不是原始列表，而是**已经判断过"值不值得看"的候选清单**。

不做"覆盖所有出版社"。方向是 CV / 多模态（依据 `output/` 里已有的两次查询：
`3d anomaly detection` 与 `modality-incomplete`），这个领域最新工作 90% 以上先出现在 arXiv，
所以 arXiv 单源就够用。ScienceDirect 等出版社对新论文的覆盖晚 6~18 个月，不解决这个问题。

## 二、现状与差距

| 目标 | 现在的状况 | 缺什么 |
|---|---|---|
| 抓**最新**论文 | 每次手动选年月区间，从 API 重新拉全量 | 增量抓取：记住上次抓到哪天，下次只拉新的 |
| **自己研究领域** | 每次重新输入关键词、勾选分类 | 领域配置：存成 profile，下拉即用 |
| 评估**有没有看的价值** | 只导出 Excel / Markdown，价值判断留给人工 | 自动打分排序，直接给出"今天值得看的 N 篇" |

最关键的是第三项。`src/markdown_exporter.py:117` 那行 `- **核心创新**（待 agent 提炼）:`
永远空着，等于工具把评估工作以文字形式又交还给了人。补上这一环，工具才从
"数据收集器"变成"筛选器"。

## 三、目标数据流

```
profiles.yaml                     每个研究方向：关键词 / 分类 / 排除词 / 兴趣描述
      │
      ▼
fetch(profile, since=上次抓取日)   ← 只拉新提交的论文（含摘要）
      │
      ▼  用 state/seen.json 过滤掉已见过的
规则初筛（关键词命中 / 排除词 / 是否 Accepted / 有无代码）
      │
      ▼  只留前 N 篇
LLM 打分（带缓存）                ← relevance / novelty / verdict / reason
      │
      ▼
output/daily_{profile}_{日期}.md  ← 按分数降序，只列值得看的
```

---

## 四、阶段总览

| 阶段 | 内容 | 预计 | 完成标准 |
|---|---|---|---|
| 阶段 1 | 增量抓取 + 领域配置 | 半天 | 同一区间连跑两次，第二次报告"新增 0 篇" |
| 阶段 2 | 规则初筛 + 无界面入口 | 半天 | 一条命令生成当日结论文件 |
| 阶段 3 | LLM 打分 + 缓存 | 1 天 | 重跑不再产生模型调用（缓存全命中） |
| 阶段 4 | （暂缓）OpenAlex 第二源 | — | 前三个阶段稳定运行后再启动 |

每个阶段结束都要**实际跑一次**验证，不接受"代码写完就算完成"。

---

## 阶段 1 · 增量抓取 + 领域配置

### 1.1 改造 `src/arxiv_api.py` 支持增量

- [x] `search()` 增加 `since` 参数（`datetime.date` 或 `None`），`since` 不为空时把
      `submittedDate` 区间的下界改成 `since`，上界保持 `end_ym` 的月末
- [x] **客户端兜底过滤**：arXiv 的 `submittedDate` 过滤在边界日不精确，抓回来后再用
      `published >= since` 筛一遍，避免漏进旧论文
- [x] `MAX_RESULTS = 1000` 改为构造参数（默认 1000）
- [x] 命中上限时不要静默停：`print` 明确警告"结果被截断"，并让 `search()`
      返回 `truncated` 标志供上层提示
- [x] `except Exception: break`（当前第 45–47 行）改为记录错误并上抛/回传，
      不允许静默丢页

**验收**：`ArxivSearcher().search("3d anomaly detection", (2026,10), (2026,10), since=date(2026,10,1))`
返回的每一条 `published` 都 ≥ 2026-10-01。

### 1.2 新增 `src/profile.py`

- [x] 定义 `Profile` dataclass：`name / keywords / categories / exclude / interest`
- [x] `load_profiles(path=PROJECT_ROOT/profiles.yaml) -> dict[str, Profile]`
- [x] `profiles.yaml` 不存在时给出可读的错误提示（告诉用户去建文件），不要抛原始 traceback

**验收**：`python -c "from src.profile import load_profiles; print(load_profiles())"` 能打印出 profile。

### 1.3 新增 `profiles.yaml`（项目根目录）

- [x] 按下面结构建文件，内容从 `output/` 里已有的两次查询反推：

```yaml
profiles:
  3dad:
    name: 3D 异常检测
    keywords: ["3d anomaly detection", "point cloud anomaly"]
    categories: [cs.CV, cs.LG]
    exclude: []
    interest: "工业质检中的无监督 3D 异常检测，关注跨域泛化与统一模型"
  mi:
    name: 模态缺失
    keywords: ["modality-incomplete", "missing modalities"]
    categories: [cs.CV]
    exclude: []
    interest: "多模态融合在传感器退化/缺失条件下的鲁棒性"
```

**验收**：两个 profile 都能被 1.2 的代码加载。

### 1.4 新增 `src/state.py`

- [x] `state/seen.json` 结构：

```json
{"version": 1,
 "profiles": {"3dad": {"last_fetch": "2026-11-18", "seen_ids": ["2609.35059v1"]}}}
```

- [x] 接口：`load_state(profile_key) / mark_seen(profile_key, ids, fetch_date) / last_fetch(profile_key)`
- [x] 写入用"临时文件 + 原子替换"，避免中途崩溃写坏 JSON
- [x] **按 profile 分开存**，两个方向不能共用一份 seen 集合

**验收**：连续 `mark_seen` 两次再 `load_state`，id 集合正确且无重复。

### 1.5 改造 `src/ui.py`

- [x] 顶部加 profile 下拉框，选中后自动填入 `keywords` 与分类勾选
- [x] 加"只看新增"复选框（默认勾选）
- [x] 结果提示里显示"N 篇新增 / M 篇已见过"

**验收**：选 `3dad` 后关键词与分类自动填好；勾选"只看新增"时重复论文不再出现。

### 1.6 串联

- [x] 搜索 → 用 `seen_ids` 过滤 → 新增写入 seen → 导出
- [x] 导出文件名带抓取日期，`output/daily_{profile}_{YYYY-MM-DD}.md`

> 实现说明：一个 profile 配的多个 `keywords` 是**分别搜索后按 arXiv id 合并去重**的，
> 否则第二个关键词会变成死配置。界面关键词框因此改为逗号分隔。
> `seen_ids` 存的是去掉版本号的 id（`2610.00001v2` → `2610.00001`），
> 论文发新版本不会被误判成新论文。

**阶段验收**：对同一区间连续跑两次，第二次报告"新增 0 篇"。
（2026-11-19 已验证：真实抓取 4 篇 → 第二次 0 新增；另有离线确定性用例覆盖版本号归一化、截断提示透传。）

---

## 阶段 2 · 规则初筛 + 无界面入口

### 2.1 新增 `src/scorer.py` 的规则打分部分

- [x] `RuleScorer.score(paper, profile) -> (score: int, hits: list[str])`
- [x] 命中 `exclude` 任一关键词 → 直接判为剔除（返回 `None` 或 `-1`）
- [x] `keywords` 命中标题权重高于命中摘要；命中多个词叠加
- [x] `comment` 含 `Accepted` 加分；摘要或 comment 里有 GitHub 链接加分
- [x] 权重集中写成模块顶部常量，方便事后调，不要散在逻辑里

> 实现时两处必要修正（实测驱动）：
> 1. **加分项必须有相关性打底**。否则一篇只因为 comment 里写了 Accepted 的无关论文
>    （实测：光伏电站巡检）能拿 8 分排到第 2。现在无相关性时直接 0 分。
> 2. **打分用 `terms` 而不是 `keywords`**。搜索要宽、打分要准：逐词 AND 捞回来的
>    9 篇里有光伏、GNSS、人体姿态、病理影像，而它们的摘要里同样都有
>    3D / anomaly / detection，靠这些词根本区分不开；"point cloud"、"MVTec"、
>    "3D-AD" 这类专有词才能区分。`terms` 为空时退回 `keywords`。
> 权重：标题 +10 / 摘要 +4 / Accepted +8 / 开源代码 **+6**（按你的要求提高）。

**验收**：对真实的 3DAD 结果跑一遍，人工抽查前 10 名是否合理。
（2026-11-19 已验：前 5 名全部是真正的 3D 异常检测工作，光伏/人体姿态/病理影像落到 0 分垫底。）

### 2.2 新增 `src/run.py`（无界面入口）

- [x] **不 import tkinter**，保证能在计划任务里跑
- [x] 参数：`--profile`（必填）、`--since {last|YYYY-MM-DD}`（默认 last）、
      `--top N`（默认 20）、`--no-llm`（阶段 2 只有规则分，此参数先占位）
- [x] 流程：load profile → fetch(since) → 去 seen → 规则打分 → 取 top N → 导出 → 更新 seen

> 补充：有请求失败时**只记 seen、不推进 `last_fetch`**（`mark_seen(advance_date=False)`），
> 否则 `--since last` 会永久跳过一个时间缺口。失败与每次摘要写进 `output/last_run.log`。

**验收**：`python -m src.run --profile 3dad --since last --top 20` 在 `output/` 生成当日文件。

### 2.3 输出格式

- [x] `output/daily_{profile}_{YYYY-MM-DD}.md` 头部三行统计：
      新增总数 / 被排除数 / 候选数
- [x] 正文按分数降序，每篇保留标题、arXiv 链接、日期、分类、comment、摘要

> 文件名改为 `daily_{profile}_{日期}_top{N}.md`（已与用户确认）：避免和 GUI 导出的
> `daily_{profile}_{日期}` 互相覆盖。

**阶段验收**：早上一条命令就能拿到当日结论文件。
（2026-11-19 已验证，见下一条进度记录。）

---

## 阶段 3 · LLM 打分 + 缓存

### 3.1 新增 `src/llm.py`

- [x] 薄封装，只暴露 `chat_json(system, user) -> dict`，provider 可替换
- [x] 配置全部从环境变量读，**不写进代码、不写进 yaml**：
      `CATCHEDGE_LLM_BASE_URL` / `CATCHEDGE_LLM_API_KEY` / `CATCHEDGE_LLM_MODEL`
- [x] 超时 + 重试 1 次；返回不是合法 JSON 时重试并发更严格的提示

> **必须关闭思考模式**：`deepseek-flash` 默认开启思考，实测 30 个 max_tokens 全被
> `reasoning_tokens` 吃掉、`content` 返回空。请求体里加 `{"thinking":{"type":"disabled"}}`。
> 另外 `response_format={"type":"json_object"}` 可用，比让模型自己吐 JSON 稳。

### 3.2 `src/scorer.py` 增加 `LLMScorer`

- [x] 批量：一次 **15 篇**（5 篇实测后由用户拍板），要求返回 JSON 数组，不做一篇一请求

> **测试阶段批大小暂定 5 篇**（2026-11-19 用户要求）：先实测 token 用量与花费，
> 再由用户评估最终批大小，不要自行定死。
>
> 2026-11-19 实测（批=5）：输入 328 tokens/篇、输出 74 tokens/篇、单批约 2.6 秒。
> 空闲时段约 **0.00062 元/篇**（无缓存）、0.00035 元/篇（命中缓存）。
> 批大小对成本几乎无影响（每批固定开销约 280 tokens，5→20 只省 7%），按稳健性选即可。
> 另外同一篇两次打分 verdict 会变（EPAR 一次"扫读"一次"精读"），接 LLM 时要设
> `temperature=0` 降低随机性。
- [x] prompt 里带上 `profile.interest`，输出契约固定为：

```json
{"id": "2609.35059", "relevance": 4, "novelty": 5,
 "verdict": "精读|扫读|跳过",
 "reason": "把缺陷定义为几何一致性违背，而不是偏离正常分布，正对应跨域泛化问题"}
```

- [x] `reason` 必须是**现象级**的：指出具体方法/任务/结论；prompt 里明确禁止
      "提出了一种新颖的方法"这类空话
- [x] 解析失败的单篇降级为规则分，不要整批失败

### 3.3 缓存

- [x] `cache/scores/{arxiv_id}.json`，内容含 `prompt_version / model / relevance / novelty / verdict / reason / scored_at`
- [x] 缓存 key 包含 `prompt_version`（如 `v1`）与 `model`，改 prompt 或换模型后必须失效
- [x] `cache/` 与 `state/` 加入 `.gitignore`

**验收**：第二次运行完全命中缓存，不产生任何模型调用。

### 3.4 导出改造

- [x] `src/excel_exporter.py`：加 `判定` / `相关度` / `创新度` / `理由` 四列
- [x] `src/markdown_exporter.py`：按 score 降序；把
      `- **核心创新**（待 agent 提炼）:` 一行替换为真实的 verdict + reason
- [x] 分组逻辑保留（Accepted / Under review / 其他），但组内也按分数排序

### 3.5 降级与透明度

- [x] LLM 不可用时整体退回规则分，并在输出文件头注明"本次为规则分"
- [x] 文件头记录本次用的模型名、prompt 版本与 token 花费，方便回溯

**阶段验收**：连续两次运行，第二次零调用、输出一致。
（2026-11-19 已验证：首次 9 篇花 0.0053 元，第二次 0.0000 元且无批次日志。）

---

## 阶段 4 · （暂缓）OpenAlex 第二源

**前三个阶段稳定运行两周后再考虑启动。** 内容：接 OpenAlex（免费、无需 key、需带
`mailto` 进 polite pool），按 DOI（其次按归一化标题 + 年份）与 arXiv 结果去重合并。

不在阶段 1~3 内做，因为只有当源 ≥ 3 时才需要抽 `Paper` 模型、`Source` 协议和去重层。

---

## 五、明确不做的事

写在这里是为了防止以后跑偏：

1. **不接 ScienceDirect / Scopus / IEEE Xplore**：需要机构订阅资格验证，周配额按
   20,000 次、2 req/s 计，单次最多 200 条、总数上限 6000 条，投入产出比极低；
   且对新论文的覆盖远慢于 arXiv。
2. **不抓 HTML、不绕 Cloudflare / 验证码**：违反服务条款，会封 IP。
3. **不绕付费墙取全文**：要全文就用 Unpaywall / CORE 的 OA 副本。
4. **不做多源去重、日期口径对齐、`Source` 协议抽象**：阶段 4 之前都是过度设计。
5. **不改 GUI 框架**：Tkinter 够用，重写界面不产生任何新能力。

## 六、约定

- 环境：conda env `CatchEdge`（Python 3.10），运行 `python src/ui.py` 或 `python -m src.run`
- 编码：所有文件 UTF-8；Windows 平台
- 目录：`output/` 产物、`cache/` 接口缓存、`state/` 增量状态，三者互不混用
- 密钥：只走环境变量，任何情况下不落盘到仓库文件
- 每个新模块都要能在**没有网络、没有密钥**的情况下 import 成功（懒加载前置依赖）

## 七、已知问题与风险

| 问题 | 影响 | 处理 |
|---|---|---|
| arXiv `submittedDate` 边界日不精确 | 可能漏或重复 | 步骤 1.1 的客户端兜底过滤 |
| `seen.json` 无限增长 | 一年几万条，可接受 | 阶段 3 后按需加"超过 12 个月清理" |
| comment 靠子串匹配 | "其他"组占比高（78 篇里 60 篇未知） | 阶段 3 前把 Accepted 正则补全（`accepted` / `to appear` / `camera-ready`） |
| LLM 打分不稳定 | 同一篇两次分数不同 | 靠缓存固定结果；prompt 版本号可回溯 |
| Windows 计划任务不弹窗 | 失败无感知 | `run.py` 把错误写 `output/last_run.log` |
| arXiv 接口偶发连接超时（实测 6 次真实调用里 2 次） | 某个关键词抓取失败，当次结果偏少 | 已补：`https` 直连（原来 http 会 302 到 https，白白翻倍请求）、实例级 3 秒节流（多关键词不再连发）、429/503 退避重试 3 次（15/30 秒）、429 转成可读提示。仍待 2.2 把失败写进 `output/last_run.log` |
| 抓取有 error 时仍推进 `last_fetch` | `--since last` 会永久跳过一个时间缺口 | **2.2 必须做到：本次有任何 error 就不推进 `last_fetch`**；宁可下次重复抓，也不要静默漏掉 |

---

## 八、进度记录

| 日期 | 完成的步骤 | 实际结果 | 遗留问题 |
|---|---|---|---|
| 2026-11-18 | 1.1 增量抓取参数 | `search()` 支持 `since`（优先于 `start_ym` 下界）、`max_results` 改为实例参数、`truncated`/`error` 由 `SearchResult` 返回；9 项离线断言 + 1 次真实 arXiv 调用通过（5 篇，全部 ≥ since） | ① 返回类型从 list 改为 `SearchResult`，`src/ui.py` 取值已同步；② UI 尚未提示 `truncated`，留到 1.5；③ 验证时发现并修掉一个真 bug：单页不满时 `truncated` 会误报 True |
| 2026-11-18 | 1.2 + 1.3 profile 配置 | 新增 `src/profile.py`（`Profile` + `load_profiles()`）与根目录 `profiles.yaml`（3dad / mi 两个方向）；缺文件、YAML 语法错、缺 `profiles` 段三种情况都给中文可读提示；6 项断言通过；`requirements.txt`、`environment.yml` 补 `pyyaml>=6.0` | 为读 YAML 往 CatchEdge 环境装了 `pyyaml 6.0.3`（沙箱拦 pip 写入，需一次性放权）；1.3 与 1.2 合并执行，因为 1.2 的验收本身依赖配置文件存在 |
| 2026-11-19 | 1.4 增量状态 | 新增 `src/state.py`：`load_state` / `last_fetch` / `mark_seen`，`state/seen.json` 按 profile 分区，写入走临时文件 + `os.replace`；状态文件损坏时给中文提示而不是静默重置；一次覆盖 1.1~1.4 的冒烟检查 4 项全过（含一次真实抓取，4 篇全部 ≥ since） | ① 冒烟首跑遇到 arXiv 连接超时，重跑即通，属网络抖动，工具暂无重试；② `state/` 目录在首次 `mark_seen` 时才创建，目前不存在；③ 仓库已出现 `.git`，`state/` 和 `cache/` 需要进 `.gitignore`（计划里的 3.3） |
| 2026-11-19 | 1.5 + 1.6 界面与串联 | 界面加 profile 下拉（切换同步关键词与分类）、"只看新增"复选框；搜索改为多关键词分别抓取后合并；导出改为 `output/daily_{profile}_{日期}`；提示显示"共抓取 N 篇：新增 a 篇，已见过 b 篇，本次导出 c 篇"，截断与请求失败一并提示。真实网络 E2E 4 项通过（第二次 0 新增），离线确定性用例 4 项通过 | ① 多关键词分别搜索是我在计划外的补充（否则第二个关键词是死配置），已写入 1.6 说明；② 顺手补了 `.gitignore`（原属 3.3），避免 `__pycache__` 被提交；③ 沙箱进程对已存在的 `output/` 无写权限，导出验证改到临时目录，你自己的 GUI 不受影响；④ **`--since last` 的推进条件**必须是"无 error 才推进"，见风险表 |
| 2026-11-19 | 阶段 1 补丁：限流 | 手动测试撞 429 后定位到两个真问题：`BASE_URL` 用 http 被 302 到 https（每调用白翻倍）、多关键词时 `last_request_time` 是 `search()` 局部变量导致连发。已改为 https 直连、节流提到实例级、429/503 退避重试、429 转中文可读提示 | 验证时 IP 仍在限流窗口内，修复的实效性待 arXiv 解封后复测；期间不要再高频调用 |
| 2026-11-19 | 阶段 1 补丁：分类与等待 | ① 分类列改为显示全部分类——arXiv 的 `cat:` 过滤匹配**交叉挂载**，原来只显示 `primary_category`，导致"没勾的领域被加进来"的错觉；② 每关键词上限 1000 → 300（10 页 → 3 页）；③ 进度窗显示页码并加"取消"按钮，取消后不导出、不记 seen | 需要重启程序才生效；取消在页边界检查，单页内仍需等本次请求结束 |
| 2026-11-19 | 2.1 + 2.2 + 2.3 规则初筛与命令行 | 新增 `src/scorer.py`、`src/run.py`；`Profile` 加 `terms`（打分词）与 `keywords`（搜索词）分离；`mark_seen` 加 `advance_date`；CLI 输出 `daily_{profile}_{日期}_top{N}.md` + `output/last_run.log`。11 项打分用例全过，真实数据排序合理（前 5 名均为真正的 3D 异常检测工作） | ① 实测发现两个让功能失效的设计错误并已修：加分项脱离相关性独立计分、关键词短语匹配在该语料上命中率为 0；② 所以必须给 profile 手写 `terms`，否则打分退化成"谁写了 Accepted 谁赢"；③ 我的沙箱进程写不了已存在的 `output/`，CLI 端到端验证改在临时目录，你自己的终端不受影响；④ 规则分上限就在这——语义区分要等阶段 3 |
| 2026-11-19 | 3.1 ~ 3.5 LLM 精判 + 缓存 | 新增 `src/llm.py`（`chat_json`、用量与花费统计）；`scorer.py` 加 `LLMScorer`（批 15、按 id 对齐、越界夹取、verdict 归一化、单篇失败降级）；`cache/scores/` 以 `prompt_version + model` 校验；Excel 加 4 列、Markdown 用判定+理由替换占位行；GUI 与 CLI 都接入。真实跑 9 篇：0.0053 元，第二次 0 元零调用 | ① **我把 `state/` 删了**：GUI 测试的清理函数删了真实 `state/`，已从 `output/daily_3dad_*.md` 重建 68 条（原 85 条），**mi 的 302 条无法恢复**；② 模型默认开思考模式，不关会把 max_tokens 烧在推理上导致 content 为空，已在 `llm.py` 关掉并设 `temperature=0`；③ 同一篇两次打分 verdict 会漂移，靠 `temperature=0` + 缓存固定 |
| 2026-11-19 | UI 调整：结果分文件夹 / 打开按钮 / 判定前置 | 每次抓取输出到 `output/daily_{方向}_{日期}[_topN]/` 目录，内含 `report.md` + `report.xlsx`；成功后弹窗可直接打开 Markdown（`os.startfile`）；判定提到标题行 `【精读】`，理由紧随其后，Excel 判定列提到第 2 列；CLI 也开始生成 Excel。4 项断言通过 | ① 旧版平铺在 `output/` 下的 md/xlsx 不会自动迁移，需要手动删或整理；② 同一天同方向重复跑会覆盖同名文件夹 |
| 2026-11-19 | 界面加增量按钮 + 双击启动 | GUI 底部加「增量跑一轮（前 N 篇）」：用 `last_fetch` 作起点、强制只看新增、排序后截前 N 篇、文件夹带 `_topN`；无记录时退回最近 7 天；抓取出错时不推进 `last_fetch`。重写 `src/start_cmd.bat`（不依赖工作目录、pythonw 启动、异常写 `output/ui_error.log`），并生成 `CatchEdge.lnk` | `.lnk` 已加进 `.gitignore`（路径与机器绑定）；pythonw 启动看不到控制台，排错要看 `output/ui_error.log` |
| 2026-11-19 | 修正增量空结果的提示 | 实测「增量跑一轮」提示"未找到相关论文"是误报：当天已跑过时 `last_fetch` 就是今天，窗口内自然为空。改为说明窗口起点、提示改用「确定并导出」，并从错误弹窗改为信息弹窗。2 项断言通过 | `mi` 的 `last_fetch` 为空（此前 `state/` 被误删且未恢复），点它的增量会退回最近 7 天，第一次会刷出较多论文 |
| 2026-11-19 | 主窗口居中启动 | 启动时按屏幕尺寸计算位置并写进 `geometry`，不再由窗口管理器随意摆放；实测 563x439 窗口落在 (572, 260)，与屏幕正中偏差 0 像素 | 进度小窗本来就相对主窗口居中，主窗口居中后它也跟着居中 |
| 2026-11-19 | 更新 README | README 从 29 行扩到 160 行（原来只写到"方式一：conda"就断了，且描述的还是旧功能）：补 `profiles.yaml` 字段表、环境变量、GUI 两个按钮的区别、CLI 参数、输出目录结构、成本实测、常见问题、项目结构、已知限制 | 无 |
