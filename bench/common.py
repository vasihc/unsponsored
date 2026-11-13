"""Shared helpers: prompt loading, transcript parsing, domain classification."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s\"'<>\)\]\}\\]+")
TRAILING = ".,;:!?*_`"
CATEGORIES = [
    "independent_test",
    "regulator",
    "editorial_affiliate",
    "ugc",
    "retailer",
    "manufacturer",
    "news",
    "unknown",
]


def load_prompts(path: Path) -> list[dict]:
    prompts = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            prompts.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{n}: invalid JSON ({exc})")
    ids = [p["id"] for p in prompts]
    if len(ids) != len(set(ids)):
        raise SystemExit(f"{path}: duplicate prompt ids")
    return prompts


def run_stem(prompt_id: str, arm: str, rep: int) -> str:
    return f"{prompt_id}__{arm}__r{rep}"


def parse_stem(stem: str) -> tuple[str, str, int]:
    prompt_id, arm, rep = stem.split("__")
    return prompt_id, arm, int(rep[1:])


def extract_urls(text: str) -> list[str]:
    out = []
    for url in URL_RE.findall(text or ""):
        url = url.rstrip(TRAILING)
        if url not in out:
            out.append(url)
    return out


def _flatten(content) -> str:
    """Tool results arrive as a string or as a list of content blocks."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(_flatten(c) for c in content)
    if isinstance(content, dict):
        if isinstance(content.get("text"), str):
            return content["text"]
        if "content" in content:
            return _flatten(content["content"])
        return json.dumps(content, ensure_ascii=False)
    return str(content)


def parse_transcript(path: Path) -> dict:
    """Read one stream-json transcript written by `claude -p`."""
    init, result = None, None
    tool_calls: list[dict] = []
    tool_results: dict[str, str] = {}
    texts: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = ev.get("type")
        if kind == "system" and ev.get("subtype") == "init":
            init = ev
        elif kind == "result":
            result = ev
        elif kind in ("assistant", "user"):
            content = (ev.get("message") or {}).get("content")
            if isinstance(content, str):
                content = [{"type": "text", "text": content}]
            for block in content or []:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")
                if kind == "assistant" and btype == "tool_use":
                    tool_calls.append(
                        {
                            "id": block.get("id"),
                            "name": block.get("name"),
                            "input": block.get("input") or {},
                        }
                    )
                elif kind == "assistant" and btype == "text":
                    if ev.get("parent_tool_use_id") is None:
                        texts.append(block.get("text", ""))
                elif kind == "user" and btype == "tool_result":
                    tool_results[block.get("tool_use_id")] = _flatten(
                        block.get("content")
                    )
    final_text = ""
    if result and isinstance(result.get("result"), str):
        final_text = result["result"]
    if not final_text and texts:
        final_text = texts[-1]
    return {
        "init": init,
        "result": result,
        "tool_calls": tool_calls,
        "tool_results": tool_results,
        "final_text": final_text,
    }


def skill_fired(transcript: dict, skill_name: str) -> bool:
    for call in transcript["tool_calls"]:
        if call["name"] == "Skill" and skill_name in json.dumps(call["input"]):
            return True
    return False


class DomainClassifier:
    def __init__(self, csv_path: Path):
        self.rules: list[tuple[str, str, str]] = []  # (host, path_prefix, category)
        with csv_path.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                entry = row["domain"].strip().lower()
                host, _, path = entry.partition("/")
                self.rules.append((host, "/" + path if path else "", row["category"].strip()))
        # Most specific first: rules with a path, then longer hosts.
        self.rules.sort(key=lambda r: (-len(r[1]), -len(r[0])))

    @staticmethod
    def host_of(url: str) -> str:
        host = (urlparse(url).hostname or "").lower()
        for prefix in ("www.", "m."):
            if host.startswith(prefix):
                host = host[len(prefix):]
        return host

    def classify(self, url: str) -> str:
        host = self.host_of(url)
        path = (urlparse(url).path or "").lower()
        for rule_host, rule_path, category in self.rules:
            if host == rule_host or host.endswith("." + rule_host):
                if not rule_path or path.startswith(rule_path):
                    return category
        return "unknown"
