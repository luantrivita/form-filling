"""Small OpenAI-compatible chat client for self-hosted vLLM/SGLang endpoints.

No OpenAI SDK dependency is required. This module is intended for controlled
benchmarking against local/self-hosted endpoints and records latency + usage.
"""
from __future__ import annotations
import json
import os
import time
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Any


@dataclass
class ChatResult:
    text: str
    latency_seconds: float
    usage: dict[str, Any]
    raw: dict[str, Any]


class OpenAICompatClient:
    def __init__(self, base_url: str, api_key: str | None = None, timeout: int = 300):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.getenv("ESF_LLM_API_KEY", "EMPTY")
        self.timeout = timeout

    def chat(self, *, model: str, messages: list[dict[str, str]], temperature: float = 0.0,
             max_tokens: int = 4096, extra_body: dict[str, Any] | None = None) -> ChatResult:
        url = self.base_url + "/v1/chat/completions"
        body: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        if extra_body:
            body.update(extra_body)
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.api_key}")
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code} from model endpoint: {detail[:1000]}") from exc
        latency = time.perf_counter() - t0
        text = raw["choices"][0]["message"].get("content") or ""
        return ChatResult(text=text, latency_seconds=latency, usage=raw.get("usage") or {}, raw=raw)
