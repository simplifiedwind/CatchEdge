# src/profile.py
import os
from dataclasses import dataclass, field

import yaml


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PATH = os.path.join(PROJECT_ROOT, "profiles.yaml")

# 每次保存都会重写这个头，字段含义不至于丢
HEADER = """\
# 每个研究方向一份配置。本文件会由 CatchEdge 界面改写，也可以手动编辑。
#
# keywords   发给 arXiv 的检索词（多个用逗号分隔，也可写成列表）
# terms      打分用的领域专有词；留空则退回用 keywords
# categories arXiv 分类，留空 = 不限
# exclude    命中即剔除
# interest   交给模型的兴趣描述，写得越具体判断越准
"""


@dataclass
class Profile:
    """一个研究方向：搜什么、排除什么、为什么关注。

    keywords 用来搜索（arXiv 的检索词），terms 用来打分（领域专有词）。
    两者分开是因为检索要宽（否则召回不够），打分要准（用别人绕不开的专业说法）。
    terms 为空时退回用 keywords 打分。
    """
    name: str
    keywords: list = field(default_factory=list)
    terms: list = field(default_factory=list)
    categories: list = field(default_factory=list)
    exclude: list = field(default_factory=list)
    interest: str = ""

    @property
    def relevance_terms(self):
        return self.terms or self.keywords


def load_profiles(path=DEFAULT_PATH):
    """
    读取 profiles.yaml，返回 {key: Profile}。

    配置文件缺失或格式不对时抛 ValueError，消息里直接说明要怎么改，
    避免把原始 traceback 甩给用户。
    """
    if not os.path.exists(path):
        raise ValueError(
            f"找不到配置文件：{path}\n"
            f"请新建该文件，格式见 PLAN.md 的步骤 1.3。"
        )

    with open(path, encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"配置文件格式有误：{path}\n{e}") from e

    if not isinstance(data, dict) or not isinstance(data.get("profiles"), dict):
        raise ValueError(
            f"配置文件缺少顶层 profiles 段落：{path}\n"
            f"正确格式是：\nprofiles:\n  某个key:\n    name: ...\n    keywords: [...]"
        )

    profiles = {}
    for key, item in data["profiles"].items():
        item = item or {}
        profiles[key] = Profile(
            name=item.get("name") or key,
            keywords=item.get("keywords") or [],
            terms=item.get("terms") or [],
            categories=item.get("categories") or [],
            exclude=item.get("exclude") or [],
            interest=item.get("interest") or "",
        )
    return profiles


def save_profiles(profiles, path=DEFAULT_PATH):
    """把全部研究方向写回 profiles.yaml。

    会重写整个文件：界面上新增/删除的方向、改过的关键词都靠它落盘。
    手写在文件里的行内注释会在保存后丢失，所以字段说明放在文件头。
    """
    data = {"profiles": {}}
    for key, profile in profiles.items():
        data["profiles"][key] = {
            "name": profile.name,
            "keywords": list(profile.keywords),
            "terms": list(profile.terms),
            "categories": list(profile.categories),
            "exclude": list(profile.exclude),
            "interest": profile.interest,
        }

    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(HEADER)
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False)
