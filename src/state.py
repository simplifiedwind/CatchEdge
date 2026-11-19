# src/state.py
import json
import os
import tempfile
from datetime import date


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PATH = os.path.join(PROJECT_ROOT, "state", "seen.json")


def _load_all(path):
    """读出整个状态文件。文件不存在视为首次运行，返回空结构。"""
    if not os.path.exists(path):
        return {"version": 1, "profiles": {}}

    with open(path, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"状态文件损坏：{path}\n{e}\n"
                f"删掉这个文件即可从零开始（代价是下次会把已看过的论文当成新的）。"
            ) from e

    if not isinstance(data, dict) or not isinstance(data.get("profiles"), dict):
        raise ValueError(f"状态文件结构不对，缺少 profiles 段：{path}")
    return data


def _write_atomic(data, path):
    """先写临时文件再替换，避免中途崩溃留下半个 JSON。"""
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".seen-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def load_state(profile_key, path=DEFAULT_PATH):
    """返回 {"last_fetch": date|None, "seen_ids": set[str]}。每个 profile 各自独立。"""
    entry = _load_all(path)["profiles"].get(profile_key) or {}
    raw_ids = entry.get("seen_ids") or []
    return {
        "last_fetch": date.fromisoformat(entry["last_fetch"]) if entry.get("last_fetch") else None,
        "seen_ids": set(raw_ids),
    }


def last_fetch(profile_key, path=DEFAULT_PATH):
    """上次抓取到哪一天；没有记录返回 None。"""
    return load_state(profile_key, path)["last_fetch"]


def mark_seen(profile_key, ids, fetch_date, path=DEFAULT_PATH, advance_date=True):
    """把一批 id 记进某个 profile。重复调用不会产生重复项，日期只增不减。

    advance_date=False 时只记 id、不推进 last_fetch：抓取过程中出过错时用这个，
    否则 --since last 会永久跳过一个时间缺口，那段时间再也抓不回来。
    """
    data = _load_all(path)
    entry = data["profiles"].get(profile_key) or {}

    # dict.fromkeys 既去重又保留先后顺序
    merged = list(dict.fromkeys(list(entry.get("seen_ids") or []) + list(ids)))

    prev = entry.get("last_fetch")
    if advance_date:
        newest = max(date.fromisoformat(prev), fetch_date) if prev else fetch_date
        last = newest.isoformat()
    else:
        last = prev

    data["profiles"][profile_key] = {
        "last_fetch": last,
        "seen_ids": merged,
    }
    _write_atomic(data, path)
