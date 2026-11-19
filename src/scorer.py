# src/scorer.py
"""规则初筛：纯关键词计分，不调模型、不花钱。

分数只反映"字面命中"，不理解语义。明显不相关的挡掉、明显强相关的顶上来，
真正的语义判断留给阶段 3 的 LLM。
"""
import re


# 权重集中在这里，试跑之后按感觉调就行
KEYWORD_TITLE = 10      # 关键词出现在标题：说明就是讲这件事的
KEYWORD_SUMMARY = 4     # 只出现在摘要：可能只是顺带提一句
ACCEPTED_BONUS = 8      # comment 里有 Accepted
CODE_BONUS = 6          # 有开源代码（用户明确要求提高权重）

CODE_RE = re.compile(r"https?://(?:www\.)?(?:github|gitlab)\.com/\S+", re.I)


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
