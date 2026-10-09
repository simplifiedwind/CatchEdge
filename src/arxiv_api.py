# src/arxiv_api.py
import time
import datetime as _dt
import requests
import xml.etree.ElementTree as ET


class ArxivSearcher:
    BASE_URL = "http://export.arxiv.org/api/query?"
    PAGE_SIZE = 100
    MAX_RESULTS = 1000
    REQUEST_INTERVAL = 3

    def search(self, keyword, start_ym, end_ym, categories=None, progress_callback=None):
        """
        :param keyword: 关键词，如 "3d anomaly detection"
        :param start_ym: (year, month) 起始年月
        :param end_ym:   (year, month) 结束年月
        :param categories: 分类代码列表，如 ['cs.CV', 'cs.LG']；None 或空表示不限
        :param progress_callback: 可选，函数签名 (current_count, estimated_total) -> None
        :return: 论文列表
        """
        query = self._build_query(keyword, start_ym, end_ym, categories)

        all_papers = []
        start = 0
        last_request_time = 0

        while start < self.MAX_RESULTS:
            elapsed = time.time() - last_request_time
            if last_request_time > 0 and elapsed < self.REQUEST_INTERVAL:
                time.sleep(self.REQUEST_INTERVAL - elapsed)

            params = {
                "search_query": query,
                "start": start,
                "max_results": self.PAGE_SIZE,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }

            try:
                response = requests.get(self.BASE_URL, params=params, timeout=30)
                response.raise_for_status()
            except Exception as e:
                print(f"[arXiv] 请求失败 (start={start}): {e}")
                break

            last_request_time = time.time()
            papers = self._parse_response(response.text)

            if not papers:
                break

            all_papers.extend(papers)

            if progress_callback:
                progress_callback(len(all_papers), None)

            start += self.PAGE_SIZE

            if len(papers) < self.PAGE_SIZE:
                break

        return all_papers

    def _build_query(self, keyword, start_ym, end_ym, categories):
        """构造 arXiv API 查询语句。"""
        # 1) 关键词：分词后每个词单独 AND
        terms = keyword.split()
        parts = [f'all:"{t}"' for t in terms]

        # 2) 分类：多个用 OR 连接，整体加括号
        if categories:
            cat_part = "(" + " OR ".join(f"cat:{c}" for c in categories) + ")"
            parts.append(cat_part)

        # 3) 日期范围：精确到月
        start_date = f"{start_ym[0]:04d}{start_ym[1]:02d}010000"
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

            primary = entry.find('arxiv:primary_category', ns)
            category = primary.get('term') if primary is not None else ''

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