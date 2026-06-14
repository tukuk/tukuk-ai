from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


def classify_request(text: str) -> dict[str, Any]:
    lower = text.lower()
    intents: list[str] = []
    if any(word in lower for word in ["study", "learn", "subject", "belajar", "kuiz"]):
        intents.append("study")
    if any(word in lower for word in ["code", "html", "css", "react", "node", "java", "npm", "app"]):
        intents.append("coding")
    if any(word in lower for word in ["music", "video", "image", "audio", "draw"]):
        intents.append("media")
    if any(word in lower for word in ["library", "tool", "python", "torch", "pandas"]):
        intents.append("library")
    if any(word in lower for word in ["security", "cyber", "diagnostic", "safety"]):
        intents.append("security_diagnostic")
    return {"intents": intents or ["general"], "language": "multilingual"}


def safe_slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "tukuk-agent-task"


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def memory_path(data_dir: Path, request: str) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / f"{safe_slug(request)}.json"


def save_memory(data_dir: Path, request: str, payload: dict[str, Any]) -> Path:
    path = memory_path(data_dir, request)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
