# src/llm.py
"""DeepSeek 薄封装：只负责发一次请求、拿回一份 JSON。

配置来自环境变量，不落盘：
  CATCHEDGE_LLM_BASE_URL（默认 https://api.deepseek.com）
  CATCHEDGE_LLM_API_KEY
  CATCHEDGE_LLM_MODEL（默认 deepseek-flash）
"""
import json
import os
import time

import requests


DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-flash"

# 本次进程累计用量，供上层估算花费
USAGE = {"prompt_tokens": 0, "completion_tokens": 0}

# 官方价：元 / 百万 tokens（空闲时段 / 高峰时段）
PRICE_IN = (1, 2)
PRICE_OUT = (4, 8)


class LLMError(RuntimeError):
    pass


def current_model():
    return os.environ.get("CATCHEDGE_LLM_MODEL") or DEFAULT_MODEL


def reset_usage():
    USAGE["prompt_tokens"] = 0
    USAGE["completion_tokens"] = 0


def estimate_cost(peak=False):
    pin, pout = PRICE_IN[1] if peak else PRICE_IN[0], PRICE_OUT[1] if peak else PRICE_OUT[0]
    return (USAGE["prompt_tokens"] * pin + USAGE["completion_tokens"] * pout) / 1e6


def _config():
    base = os.environ.get("CATCHEDGE_LLM_BASE_URL") or DEFAULT_BASE_URL
    model = os.environ.get("CATCHEDGE_LLM_MODEL") or DEFAULT_MODEL
    key = os.environ.get("CATCHEDGE_LLM_API_KEY")
    if not key:
        raise LLMError("没有配置 CATCHEDGE_LLM_API_KEY 环境变量")
    return base.rstrip("/"), key, model


def _post(system, user, max_tokens, timeout):
    base, key, model = _config()
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "response_format": {"type": "json_object"},
        # 默认是开启的，不关会把 max_tokens 全烧在推理上、content 返回空
        "thinking": {"type": "disabled"},
        "temperature": 0,
        "max_tokens": max_tokens,
    }
    try:
        response = requests.post(base + "/chat/completions",
                                 headers={"Authorization": "Bearer " + key},
                                 json=payload, timeout=timeout)
    except requests.RequestException as e:
        raise LLMError(f"请求失败：{e}") from e

    if response.status_code != 200:
        raise LLMError(f"HTTP {response.status_code}: {response.text[:200]}")

    body = response.json()
    usage = body.get("usage") or {}
    USAGE["prompt_tokens"] += usage.get("prompt_tokens", 0)
    USAGE["completion_tokens"] += usage.get("completion_tokens", 0)

    content = (body.get("choices") or [{}])[0].get("message", {}).get("content") or ""
    if not content.strip():
        raise LLMError("模型返回了空内容")
    return content, model


def chat_json(system, user, max_tokens=4000, timeout=180, retries=1):
    """发一次请求并解析 JSON。失败重试 retries 次，仍失败抛 LLMError。"""
    last_error = None
    for attempt in range(retries + 1):
        try:
            content, model = _post(system, user, max_tokens, timeout)
            return json.loads(content)
        except (LLMError, json.JSONDecodeError) as e:
            last_error = e
            if attempt < retries:
                time.sleep(2)
    raise LLMError(str(last_error))
