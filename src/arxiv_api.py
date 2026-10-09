# src/arxiv_api.py
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime


class ArxivSearcher:
    BASE_URL = "http://export.arxiv.org/api/query?"
    PAGE_SIZE = 100
    MAX_RESULTS = 1000
    REQUEST_INTERVAL = 3

    def search(self, keyword, year, progress_callback=None):
        """
        搜索指定年份的论文，按提交日期降序排列。
        :param keyword: 搜索关键词
        :param year: 论文年份 (int)
        :param progress_callback: 可选，回调函数(current_count)，用于更新进度
        :return: 论文信息列表
        """
        query = self._build_query(keyword, year)

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
                progress_callback(len(all_papers))

            start += self.PAGE_SIZE

            if len(papers) < self.PAGE_SIZE:
                break

        return all_papers

    def _build_query(self, keyword, year):
        """按 arXiv 网页的语义构造查询：每个词分别 AND 匹配。"""
        date_range = f"submittedDate:[{year}01010000 TO {year}12312359]"
        terms = keyword.split()
        term_query = " AND ".join(f'all:"{t}"' for t in terms)
        return f"{term_query} AND {date_range}"

    def _parse_response(self, xml_content):
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        root = ET.fromstring(xml_content)
        entries = []

        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns)
            summary = entry.find('atom:summary', ns)
            link = entry.find('atom:id', ns)
            published = entry.find('atom:published', ns)

            if all(x is not None for x in (title, summary, link, published)):
                entries.append({
                    'title': title.text.strip().replace('\n', ' '),
                    'summary': summary.text.strip().replace('\n', ' '),
                    'link': link.text.strip(),
                    'published': published.text.strip()[:10],
                })
        return entries