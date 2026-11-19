# src/run.py
"""命令行入口：抓取 → 去重 → 规则粗筛 → LLM 精判 → 导出。

刻意不 import tkinter，否则挂到计划任务里会因为没有显示环境而失败。
"""
import argparse
import datetime as dt
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src import llm
from src.arxiv_api import ArxivSearcher, paper_id
from src.excel_exporter import ExcelExporter
from src.profile import load_profiles
from src.scorer import PROMPT_VERSION, LLMScorer, RuleScorer, llm_score
from src.state import last_fetch, load_state, mark_seen


OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
LOG_PATH = os.path.join(OUTPUT_DIR, "last_run.log")
MAX_RESULTS = 300
DEFAULT_LOOKBACK_DAYS = 7


def build_parser():
    parser = argparse.ArgumentParser(
        description="抓取 arXiv 新论文，打分排序后导出")
    parser.add_argument("--profile", required=True, help="profiles.yaml 里的方向 key")
    parser.add_argument("--since", default="last",
                        help="last（默认，从上次抓取日之后）或 YYYY-MM-DD")
    parser.add_argument("--top", type=int, default=20, help="导出前 N 篇，默认 20")
    parser.add_argument("--no-llm", action="store_true",
                        help="只跑规则分，不调用模型")
    return parser


def log(line):
    """计划任务没有控制台，失败信息只能落盘。"""
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {line}\n")
    except OSError:
        pass


def resolve_since(value, profile_key):
    if value != "last":
        return dt.date.fromisoformat(value)

    last = last_fetch(profile_key)
    if last:
        return last

    fallback = dt.date.today() - dt.timedelta(days=DEFAULT_LOOKBACK_DAYS)
    print(f"[run] 没有抓取记录，默认从 {fallback} 起（最近 {DEFAULT_LOOKBACK_DAYS} 天）")
    return fallback


def fetch_all(searcher, profile, since, today):
    fetched = {}
    errors = []
    truncated = False

    for keyword in profile.keywords:
        result = searcher.search(keyword, None, (today.year, today.month),
                                 categories=profile.categories, since=since)
        if result.error:
            errors.append(f"{keyword}: {result.error}")
        truncated = truncated or result.truncated
        for paper in result.papers:
            fetched.setdefault(paper_id(paper), paper)

    return list(fetched.values()), errors, truncated


def rule_score_all(papers, profile):
    """规则粗筛。命中排除词的直接剔除，其余变成待精判的记录。"""
    records, excluded = [], []
    for paper in papers:
        score, hits = RuleScorer.score(paper, profile)
        if score is None:
            excluded.append((paper, hits))
            continue
        records.append({
            "paper": paper, "score": score, "hits": hits,
            "relevance": None, "novelty": None,
            "verdict": None, "reason": "", "source": "rule",
        })
    return records, excluded


def apply_llm(records, profile, on_batch=None):
    """用 LLM 结果覆盖规则分。拿不到结果的记录保留规则分。返回 (用上了没, 错误)。"""
    if not records:
        return False, None

    scorer = LLMScorer()
    results = scorer.score_many([r["paper"] for r in records], profile,
                                progress=on_batch)
    if not results:
        return False, scorer.last_error

    for record in records:
        hit = results.get(paper_id(record["paper"]))
        if not hit:
            continue
        record.update(
            score=llm_score(hit["relevance"], hit["novelty"]),
            relevance=hit["relevance"],
            novelty=hit["novelty"],
            verdict=hit["verdict"],
            reason=hit["reason"],
            source="llm",
        )
    return True, scorer.last_error


def rank(records):
    """先按日期降序，再按分数降序：同分时新的在前。"""
    records.sort(key=lambda r: r["paper"].get("published", ""), reverse=True)
    records.sort(key=lambda r: r["score"], reverse=True)
    return records


def render(profile_key, profile, since, today, stats, records):
    new_count, excluded, truncated, errors, shown, used_llm, llm_error = stats

    lines = [f"# {profile.name} · {today}", ""]
    lines.append(f"- 方向：`{profile_key}`（{profile.name}）")
    lines.append(f"- 抓取下界：{since}；关键词：{', '.join(profile.keywords)}")
    lines.append(f"- 新增：{new_count} 篇")
    lines.append(f"- 被排除：{len(excluded)} 篇")
    lines.append(f"- 候选：{len(records)} 篇，导出前 {shown} 篇")

    if used_llm:
        model = llm.current_model()
        lines.append(f"- 打分：LLM 精判（{model}，prompt {PROMPT_VERSION}）")
        if llm.USAGE["prompt_tokens"] or llm.USAGE["completion_tokens"]:
            lines.append(f"- 本次用量：输入 {llm.USAGE['prompt_tokens']} tokens / "
                         f"输出 {llm.USAGE['completion_tokens']} tokens，"
                         f"约 {llm.estimate_cost():.4f} 元（空闲时段价）")
        else:
            lines.append("- 本次全部命中缓存，未产生模型调用（0 元）")
        fallback = sum(1 for r in records if r["source"] == "rule")
        if fallback:
            lines.append(f"- 注意：{fallback} 篇模型没给出结果，已退回规则分")
    else:
        lines.append("- 打分：**规则分**（关键词命中/是否 Accepted/是否开源），未使用语义判断")

    if truncated:
        lines.append(f"- 注意：抓取达到 {MAX_RESULTS} 篇上限，可能还有更多")
    if errors:
        lines.append(f"- 注意：{len(errors)} 次请求失败")
        for error in errors:
            lines.append(f"  - {error}")
    if llm_error:
        lines.append(f"- 注意：模型调用有问题：{llm_error}")

    lines.append("")
    lines.append("> 按分数从高到低读前几篇即可。")
    lines.append("")

    for index, record in enumerate(records[:shown], 1):
        paper = record["paper"]
        tag = f"【{record['verdict']}】" if record["source"] == "llm" else ""
        link = paper.get('link', '')
        lines.append(f"## {index}. {tag}{paper.get('title') or '(无标题)'}")
        lines.append("")
        if record["source"] == "llm":
            lines.append(f"- **理由**：{record['reason'] or '—'}")
            lines.append(f"- **相关度**：{record['relevance']} · "
                         f"**创新度**：{record['novelty']}")
        else:
            lines.append(f"- **命中**：{'；'.join(record['hits']) or '无'}"
                         f"（{record['score']} 分）")
        lines.append(f"- **arXiv**：[{link.rsplit('/', 1)[-1]}]({link})")
        lines.append(f"- **提交日期**：{paper.get('published', '')}")
        lines.append(f"- **分类**：{paper.get('category', '')}")
        lines.append(f"- **Comment**：{paper.get('comment') or '—'}")
        lines.append(f"- **摘要**：{paper.get('summary', '')}")
        lines.append("")

    return "\n".join(lines)


def flatten(records):
    """把记录摊平成导出器认识的 paper dict。"""
    out = []
    for record in records:
        paper = dict(record["paper"])
        paper.update(score=record["score"], relevance=record["relevance"],
                     novelty=record["novelty"], verdict=record["verdict"],
                     reason=record["reason"])
        out.append(paper)
    return out


def main(argv=None):
    args = build_parser().parse_args(argv)

    profiles = load_profiles()
    if args.profile not in profiles:
        print(f"[run] 没有这个方向：{args.profile}；"
              f"可选：{', '.join(profiles) or '（空）'}")
        return 2

    profile = profiles[args.profile]
    try:
        since = resolve_since(args.since, args.profile)
    except ValueError:
        print(f"[run] --since 只能是 last 或 YYYY-MM-DD，收到：{args.since}")
        return 2

    today = dt.date.today()
    llm.reset_usage()

    searcher = ArxivSearcher(max_results=MAX_RESULTS)
    papers, errors, truncated = fetch_all(searcher, profile, since, today)

    if not papers and errors:
        for error in errors:
            print(f"[run] 抓取失败 {error}")
        log(f"{args.profile} 抓取失败：{errors[0]}")
        return 1

    seen = load_state(args.profile)["seen_ids"]
    new_papers = [p for p in papers if paper_id(p) not in seen]
    records, excluded = rule_score_all(new_papers, profile)

    used_llm = False
    llm_error = None
    if not args.no_llm and records:
        def on_batch(index, total):
            print(f"[run] 精判 {index}/{total} 批")

        used_llm, llm_error = apply_llm(records, profile, on_batch)
        if llm_error:
            print(f"[run] 模型调用有问题：{llm_error}")

    rank(records)

    # 有请求失败时只记 id、不推进 last_fetch，否则缺口以后再补不回来
    mark_seen(args.profile, [paper_id(p) for p in papers], today,
              advance_date=not errors)

    if not records:
        summary = (f"新增 {len(new_papers)} 篇，"
                   f"无可导出候选（被排除 {len(excluded)} 篇）")
        print(f"[run] {summary}")
        log(f"{args.profile} {summary}")
        return 0

    shown = min(args.top, len(records))
    text = render(args.profile, profile, since, today,
                  (len(new_papers), excluded, truncated, errors, shown,
                   used_llm, llm_error), records)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # 每次抓取单独一个文件夹，md 和 xlsx 都放进去
    run_dir = os.path.join(OUTPUT_DIR,
                           f"daily_{args.profile}_{today}_top{args.top}")
    os.makedirs(run_dir, exist_ok=True)
    path = os.path.join(run_dir, "report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    ExcelExporter.export(flatten(records[:shown]), filename="report.xlsx",
                         output_dir=run_dir)

    cost = llm.estimate_cost() if used_llm else 0
    print(f"[run] 新增 {len(new_papers)} 篇，候选 {len(records)} 篇，"
          f"导出 {shown} 篇，花费约 {cost:.4f} 元 → {run_dir}")
    log(f"{args.profile} 新增 {len(new_papers)} 候选 {len(records)} "
        f"导出 {shown} 失败 {len(errors)} llm={used_llm} 费用={cost:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
