# src/scorer.py
"""两级打分。

第一级 RuleScorer：纯关键词计分，不调模型、不花钱，负责粗筛。
第二级 LLMScorer：让模型读摘要判断值不值得读，结果带缓存，一篇只付一次钱。
"""
import datetime as dt
import json
import os
import re

from src import llm
from src.arxiv_api import paper_id
from src.llm import LLMError


# 权重集中在这里，试跑之后按感觉调就行
KEYWORD_TITLE = 10      # 关键词出现在标题：说明就是讲这件事的
KEYWORD_SUMMARY = 4     # 只出现在摘要：可能只是顺带提一句
ACCEPTED_BONUS = 8      # comment 里有 Accepted
CODE_BONUS = 6          # 有开源代码（用户明确要求提高权重）

CODE_RE = re.compile(r"https?://(?:www\.)?(?:github|gitlab)\.com/\S+", re.I)

# ---- LLM 精判相关 ----
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CACHE_DIR = os.path.join(PROJECT_ROOT, "cache", "scores")
PROMPT_VERSION = "v1"
BATCH_SIZE = 15

SYSTEM_PROMPT = (
    "你是资深的学术文献筛选助手。用户会给出研究兴趣和一批论文的标题与摘要。\n"
    "只输出 JSON，格式为数组，不要任何解释性文字：\n"
    '[{"id":"<原样返回给定 id>","relevance":1-5,"novelty":1-5,'
    '"verdict":"精读|扫读|跳过","reason":"<中文一句话>"}]\n'
    "relevance：与该研究兴趣的相关度，5 为高度相关。\n"
    "novelty：相对该领域的创新程度，5 为明显新贡献。\n"
    "verdict：是否值得读。\n"
    "reason：必须指出具体的方法、任务或结论；禁止「提出了一种新颖的方法」这类空话，不超过 60 字。"
)

VERDICT_ALIASES = {
    "精读": ("精读", "仔细读", "深读", "read in detail", "deep"),
    "扫读": ("扫读", "略读", "泛读", "skim", "scan"),
    "跳过": ("跳过", "不必读", "不读", "skip"),
}


class RuleScorer:
    @staticmethod
    def score(paper, profile):
        """
        :return: (score, hits)；score 为 None 表示命中排除词、应直接剔除
        """
        title = (paper.get('title') or '').lower()
        summary = (paper.get('summary') or '').lower()
        comment = (paper.get('comment') or '').lower()

        for term in profile.exclude:
            needle = term.lower().strip()
            if needle and (needle in title or needle in summary):
                return None, [f"排除词命中「{term}」"]

        relevance = 0
        hits = []

        for term in profile.relevance_terms:
            needle = term.lower().strip()
            if not needle:
                continue
            if needle in title:
                relevance += KEYWORD_TITLE
                hits.append(f"标题命中「{term}」+{KEYWORD_TITLE}")
            elif needle in summary:
                relevance += KEYWORD_SUMMARY
                hits.append(f"摘要命中「{term}」+{KEYWORD_SUMMARY}")

        # 加分项必须有相关性打底：否则一篇只因为"被接收"或"有代码"的无关论文
        # 会排到真正相关的论文前面（实测过：光伏电站巡检排到了第 2）
        if relevance == 0:
            return 0, ["未命中关键词"]

        score = relevance

        if 'accepted' in comment:
            score += ACCEPTED_BONUS
            hits.append(f"comment 含 Accepted +{ACCEPTED_BONUS}")

        if CODE_RE.search(summary) or CODE_RE.search(comment):
            score += CODE_BONUS
            hits.append(f"有开源代码 +{CODE_BONUS}")

        return score, hits


def normalize_verdict(text):
    low = (text or "").strip().lower()
    for canonical, aliases in VERDICT_ALIASES.items():
        for alias in aliases:
            if alias in low:
                return canonical
    return "扫读"   # 认不出来时给个中性值，不让它变成空


def llm_score(relevance, novelty):
    """把两个 1-5 分压成一个可排序的数：相关度为主，创新度为辅。"""
    return relevance * 10 + novelty * 2


class LLMScorer:
    def __init__(self, batch_size=BATCH_SIZE, cache_dir=DEFAULT_CACHE_DIR):
        self.batch_size = batch_size
        self.cache_dir = cache_dir
        self.last_error = None

    # ---- 缓存 ----
    def _cache_file(self, pid):
        return os.path.join(self.cache_dir, f"{pid.replace('/', '_')}.json")

    def _load_cache(self, pid, model):
        path = self._cache_file(pid)
        if not os.path.exists(path):
            return None
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return None
        # prompt 改了或换了模型，旧结果一律作废
        if data.get("prompt_version") != PROMPT_VERSION or data.get("model") != model:
            return None
        return data

    def _save_cache(self, pid, model, item):
        record = {
            "prompt_version": PROMPT_VERSION,
            "model": model,
            "relevance": item["relevance"],
            "novelty": item["novelty"],
            "verdict": item["verdict"],
            "reason": item["reason"],
            "scored_at": dt.date.today().isoformat(),
        }
        os.makedirs(self.cache_dir, exist_ok=True)
        with open(self._cache_file(pid), "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        return record

    # ---- 打分 ----
    def score_many(self, papers, profile, progress=None):
        """返回 {paper_id: 记录}。没拿到结果的论文不会出现在返回值里，由上层降级。"""
        model = llm.current_model()
        results = {}
        todo = []
        for paper in papers:
            pid = paper_id(paper)
            cached = self._load_cache(pid, model)
            if cached:
                results[pid] = cached
            else:
                todo.append(paper)

        total = (len(todo) + self.batch_size - 1) // self.batch_size
        for index in range(total):
            batch = todo[index * self.batch_size:(index + 1) * self.batch_size]
            if progress:
                progress(index + 1, total)
            try:
                items = self._score_batch(batch, profile)
            except LLMError as e:
                self.last_error = str(e)
                continue
            for item in items:
                results[item["id"]] = self._save_cache(item["id"], model, item)

        return results

    def _score_batch(self, batch, profile):
        payload = [{"id": paper_id(p),
                    "title": p.get("title", ""),
                    "abstract": p.get("summary", "")} for p in batch]
        user = (f"研究兴趣：{profile.interest}\n\n论文：\n"
                + json.dumps(payload, ensure_ascii=False))

        data = llm.chat_json(SYSTEM_PROMPT, user)
        items = data
        if isinstance(data, dict):
            items = next((v for v in data.values() if isinstance(v, list)), [])
        if not isinstance(items, list):
            raise LLMError("模型返回的不是数组")

        allowed = {p["id"] for p in payload}
        parsed = []
        for entry in items:
            if not isinstance(entry, dict):
                continue
            pid = str(entry.get("id", "")).strip()
            if pid not in allowed:
                continue
            try:
                relevance = max(1, min(5, int(entry.get("relevance"))))
                novelty = max(1, min(5, int(entry.get("novelty"))))
            except (TypeError, ValueError):
                continue
            parsed.append({
                "id": pid,
                "relevance": relevance,
                "novelty": novelty,
                "verdict": normalize_verdict(entry.get("verdict")),
                "reason": str(entry.get("reason", "")).strip()[:120],
            })

        if not parsed:
            raise LLMError("模型返回的条目无法解析")
        return parsed
