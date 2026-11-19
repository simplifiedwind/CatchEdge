# src/run.py
"""命令行入口：抓取 → 去重 → 规则打分 → 导出。

刻意不 import tkinter，否则挂到计划任务里会因为没有显示环境而失败。
"""
import argparse
import datetime as dt
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.arxiv_api import ArxivSearcher, paper_id
from src.profile import load_profiles
from src.scorer import RuleScorer
from src.state import last_fetch, load_state, mark_seen


OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
LOG_PATH = os.path.join(OUTPUT_DIR, "last_run.log")
MAX_RESULTS = 300
DEFAULT_LOOKBACK_DAYS = 7


def build_parser():
    parser = argparse.ArgumentParser(
        description="抓取 arXiv 新论文，按规则分排序后导出")
    parser.add_argument("--profile", required=True, help="profiles.yaml 里的方向 key")
    parser.add_argument("--since", default="last",
                        help="last（默认，从上次抓取日之后）或 YYYY-MM-DD")
    parser.add_argument("--top", type=int, default=20, help="导出前 N 篇，默认 20")
    parser.add_argument("--no-llm", action="store_true",
                        help="阶段 2 只有规则分，此参数暂为占位")
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


def score_all(papers, profile):
    """返回 (按分数降序的 [(score, paper, hits)], 被排除的 [(paper, hits)])。"""
    scored, excluded = [], []
    for paper in papers:
        score, hits = RuleScorer.score(paper, profile)
        if score is None:
            excluded.append((paper, hits))
        else:
            scored.append((score, paper, hits))

    # 两趟排序：先按日期降序，再按分数降序（Python 排序稳定，同分保持日期序）
    scored.sort(key=lambda item: item[1].get('published', ''), reverse=True)
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored, excluded


def render(profile_key, profile, since, today, stats, ranked):
    new_count, excluded, truncated, errors, shown = stats
    lines = [f"# {profile.name} · {today}", ""]
    lines.append(f"- 方向：`{profile_key}`（{profile.name}）")
    lines.append(f"- 抓取下界：{since}；关键词：{', '.join(profile.keywords)}")
    lines.append(f"- 新增：{new_count} 篇")
    lines.append(f"- 被排除：{len(excluded)} 篇")
    lines.append(f"- 候选：{len(ranked)} 篇，导出前 {shown} 篇")
    if truncated:
        lines.append(f"- 注意：抓取达到 {MAX_RESULTS} 篇上限，可能还有更多")
    if errors:
        lines.append(f"- 注意：{len(errors)} 次请求失败")
        for error in errors:
            lines.append(f"  - {error}")
    lines.append("")
    lines.append("> 本文件是**规则分**：关键词命中、是否 Accepted、是否有开源代码。"
                 "不含语义判断，按分数从高到低读前几篇即可。")
    lines.append("")

    for index, (score, paper, hits) in enumerate(ranked[:shown], 1):
        link = paper.get('link', '')
        lines.append(f"## {index}. {paper.get('title') or '(无标题)'}（{score} 分）")
        lines.append("")
        lines.append(f"- **命中**：{'；'.join(hits) or '无'}")
        lines.append(f"- **arXiv**：[{link.rsplit('/', 1)[-1]}]({link})")
        lines.append(f"- **提交日期**：{paper.get('published', '')}")
        lines.append(f"- **分类**：{paper.get('category', '')}")
        lines.append(f"- **Comment**：{paper.get('comment') or '—'}")
        lines.append(f"- **摘要**：{paper.get('summary', '')}")
        lines.append("")

    return "\n".join(lines)


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
    searcher = ArxivSearcher(max_results=MAX_RESULTS)
    papers, errors, truncated = fetch_all(searcher, profile, since, today)

    if not papers and errors:
        for error in errors:
            print(f"[run] 抓取失败 {error}")
        log(f"{args.profile} 抓取失败：{errors[0]}")
        return 1

    seen = load_state(args.profile)["seen_ids"]
    new_papers = [p for p in papers if paper_id(p) not in seen]
    ranked, excluded = score_all(new_papers, profile)

    # 有请求失败时只记 id、不推进 last_fetch，否则缺口以后再补不回来
    mark_seen(args.profile, [paper_id(p) for p in papers], today,
              advance_date=not errors)

    if not ranked:
        summary = (f"新增 {len(new_papers)} 篇，"
                   f"无可导出候选（被排除 {len(excluded)} 篇）")
        print(f"[run] {summary}")
        log(f"{args.profile} {summary}")
        return 0

    shown = min(args.top, len(ranked))
    text = render(args.profile, profile, since, today,
                  (len(new_papers), excluded, truncated, errors, shown), ranked)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR,
                        f"daily_{args.profile}_{today}_top{args.top}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"[run] 新增 {len(new_papers)} 篇，候选 {len(ranked)} 篇，"
          f"导出 {shown} 篇 → {path}")
    log(f"{args.profile} 新增 {len(new_papers)} 候选 {len(ranked)} "
        f"导出 {shown} 失败 {len(errors)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
