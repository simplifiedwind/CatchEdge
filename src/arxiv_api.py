# src/arxiv_api.py
import time
import re
import datetime as _dt
from dataclasses import dataclass
import requests
import xml.etree.ElementTree as ET


@dataclass
class SearchResult:
    """一次搜索的结果。truncated / error / cancelled 供上层判断结果是否完整。"""
    papers: list
    truncated: bool = False
    error: str = None
    cancelled: bool = False


def paper_id(paper):
    """arXiv id，去掉版本号：同一篇论文的 v2 不应该被当成新论文。"""
    raw = (paper.get('link') or '').rsplit('/', 1)[-1]
    return re.sub(r'v\d+$', '', raw)


class ArxivSearcher:
    BASE_URL = "https://export.arxiv.org/api/query?"
    PAGE_SIZE = 100
    REQUEST_INTERVAL = 3   # arXiv 要求同一 IP 两次请求至少间隔 3 秒
    MAX_ATTEMPTS = 3
    RETRY_BACKOFF = 15     # 秒；限流/服务端错误时退避 15、30 秒，太短等于继续撞墙

    def __init__(self, max_results=1000):
        self.max_results = max_results
        self._last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "CatchEdge/0.1"})

    def _throttle(self):
        """节流放在实例上：多关键词是连续调用 search()，每次重置就会连发。"""
        elapsed = time.time() - self._last_request_time
        if self._last_request_time and elapsed < self.REQUEST_INTERVAL:
            time.sleep(self.REQUEST_INTERVAL - elapsed)

    def _get(self, params):
        """带退避重试。429/503 是 arXiv 限流的常规表现，不该直接当失败。"""
        for attempt in range(self.MAX_ATTEMPTS):
            self._throttle()
            try:
                response = self.session.get(self.BASE_URL, params=params, timeout=30)
            except requests.RequestException:
                if attempt == self.MAX_ATTEMPTS - 1:
                    raise
                time.sleep(self.RETRY_BACKOFF * (attempt + 1))
                continue
            finally:
                self._last_request_time = time.time()

            if response.status_code in (429, 503) and attempt < self.MAX_ATTEMPTS - 1:
                delay = self.RETRY_BACKOFF * (attempt + 1)
                retry_after = response.headers.get("Retry-After", "")
                if retry_after.isdigit():
                    delay = min(int(retry_after), 60)
                print(f"[arXiv] {response.status_code} 限流，{delay} 秒后重试"
                      f"（第 {attempt + 1}/{self.MAX_ATTEMPTS} 次）")
                time.sleep(delay)
                continue

            if response.status_code == 429:
                raise requests.RequestException(
                    "arXiv 限流(429)：请求太频繁，已被临时拒绝。\n"
                    "请等 5~10 分钟再试；期间不要反复点击。")
            if response.status_code == 503:
                raise requests.RequestException(
                    "arXiv 服务暂时不可用(503)，通常几分钟后恢复。")
            response.raise_for_status()
            return response

        raise requests.RequestException("请求重试后仍然失败")

    def search(self, keyword, start_ym, end_ym, categories=None, since=None,
               progress_callback=None, should_stop=None):
        """
        :param keyword: 关键词，如 "3d anomaly detection"
        :param start_ym: (year, month) 起始年月；给了 since 时可传 None
        :param end_ym:   (year, month) 结束年月
        :param categories: 分类代码列表，如 ['cs.CV', 'cs.LG']；None 或空表示不限
        :param since: datetime.date 或 None。给出后作为抓取下界（优先于 start_ym），
                      并会在客户端按 published 再筛一次：arXiv 的 submittedDate
                      过滤在边界日不精确，不筛会混进更早的论文
        :param progress_callback: 函数签名 (current_count, page_index) -> None
        :param should_stop: 可选，无参函数；返回 True 时尽快结束并标记 cancelled
        :return: SearchResult
        """
        query = self._build_query(keyword, start_ym, end_ym, categories, since)

        all_papers = []
        start = 0
        truncated = False
        exhausted = False
        cancelled = False
        error = None

        while start < self.max_results:
            if should_stop and should_stop():
                cancelled = True
                break

            params = {
                "search_query": query,
                "start": start,
                "max_results": self.PAGE_SIZE,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }

            try:
                response = self._get(params)
            except Exception as e:
                error = f"请求失败 (start={start}): {e}"
                print(f"[arXiv] {error}")
                break

            papers = self._parse_response(response.text)

            if not papers:
                exhausted = True
                break

            all_papers.extend(papers)

            if progress_callback:
                progress_callback(len(all_papers), start // self.PAGE_SIZE + 1)

            start += self.PAGE_SIZE

            if len(papers) < self.PAGE_SIZE:
                exhausted = True
                break

        # 只拿到不足一页（或空页）说明结果已取完；循环因 start >= max_results
        # 结束才是被上限截断
        if error is None and not exhausted and start >= self.max_results:
            truncated = True
            print(f"[arXiv] 结果被截断：已达上限 {self.max_results} 条，可能还有更多论文。")

        # 客户端按 since 兜底过滤（ISO 日期字符串可直接比较先后）
        if since is not None:
            all_papers = [p for p in all_papers if p['published'] >= since.isoformat()]

        return SearchResult(papers=all_papers, truncated=truncated, error=error,
                            cancelled=cancelled)

    def _build_query(self, keyword, start_ym, end_ym, categories, since=None):
        """构造 arXiv API 查询语句。"""
        # 1) 关键词：分词后每个词单独 AND
        terms = keyword.split()
        parts = [f'all:"{t}"' for t in terms]

        # 2) 分类：多个用 OR 连接，整体加括号
        if categories:
            cat_part = "(" + " OR ".join(f"cat:{c}" for c in categories) + ")"
            parts.append(cat_part)

        # 3) 日期范围：精确到月；给了 since 就以它作为下界
        if since is not None:
            start_date = since.strftime("%Y%m%d") + "0000"
        elif start_ym is not None:
            start_date = f"{start_ym[0]:04d}{start_ym[1]:02d}010000"
        else:
            raise ValueError("start_ym 与 since 至少要给一个")
        y, m = end_ym
        if m == 12:
            ny, nm = y + 1, 1
        else:
            ny, nm = y, m + 1
        last_day = (_dt.date(ny, nm, 1) - _dt.timedelta(days=1)).day
        end_date = f"{y:04d}{m:02d}{last_day:02d}2359"

        parts.append(f"submittedDate:[{start_date} TO {end_date}]")

        return " AND ".join(parts)

    def _parse_response(self, xml_content):
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom',
        }
        root = ET.fromstring(xml_content)
        entries = []

        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns)
            summary = entry.find('atom:summary', ns)
            link = entry.find('atom:id', ns)
            published = entry.find('atom:published', ns)

            if not all(x is not None for x in (title, summary, link, published)):
                continue

            # arXiv 的 cat: 过滤匹配全部分类（含交叉挂载）。只显示主分类会让人
            # 以为筛选失效，所以把全部分类一并记下，主分类排在最前
            primary = entry.find('arxiv:primary_category', ns)
            primary_term = primary.get('term') if primary is not None else ''
            terms = [c.get('term') for c in entry.findall('atom:category', ns)
                     if c.get('term')]
            if primary_term:
                terms = [primary_term] + [t for t in terms if t != primary_term]
            category = ", ".join(terms) if terms else primary_term

            # 新增：解析 comment 字段
            comment = entry.find('arxiv:comment', ns)
            comment_text = ''
            if comment is not None and comment.text:
                comment_text = comment.text.strip().replace('\n', ' ')

            entries.append({
                'title': title.text.strip().replace('\n', ' '),
                'summary': summary.text.strip().replace('\n', ' '),
                'link': link.text.strip(),
                'published': published.text.strip()[:10],
                'category': category,
                'comment': comment_text,
            })
        return entries