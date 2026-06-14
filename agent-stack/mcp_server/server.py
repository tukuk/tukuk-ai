from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Tukuk MCP-compatible Tool Server")
DATA_DIR = Path(os.getenv("TUKUK_MCP_DATA_DIR", "data"))


class ToolCall(BaseModel):
    request: str
    payload: dict[str, Any] | None = None


def classify_request(request: str) -> dict[str, object]:
    lower = request.lower()
    engines = []
    if any(word in lower for word in ["study", "learn", "subject", "belajar", "kuiz"]):
        engines.append("study")
    if any(word in lower for word in ["code", "html", "css", "react", "node", "java", "npm", "app"]):
        engines.append("coding")
    if any(word in lower for word in ["music", "video", "image", "audio", "draw"]):
        engines.append("media")
    if any(word in lower for word in ["library", "tool", "python", "torch", "pandas"]):
        engines.append("library")
    if any(word in lower for word in ["security", "cyber", "diagnostic", "safety"]):
        engines.append("security_diagnostic")
    return {"request": request, "engines": engines or ["general"]}


def save_note(title: str, note: str) -> dict[str, str]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    safe_title = "".join(ch if ch.isalnum() or ch in " -_" else "-" for ch in title).strip("-") or "note"
    path = DATA_DIR / f"{safe_title}.txt"
    path.write_text(note, encoding="utf-8")
    return {"status": "saved", "path": str(path)}


def get_free_python_ai_libraries() -> dict[str, list[str]]:
    return {
        "ai_llm": ["torch", "transformers", "diffusers", "sentence-transformers", "llama-cpp-python"],
        "data": ["numpy", "pandas", "polars", "pyarrow"],
        "ml": ["scikit-learn", "xgboost", "lightgbm"],
        "nlp": ["spacy", "nltk", "gensim"],
        "vision": ["opencv-python", "pillow", "ultralytics"],
        "audio": ["librosa", "soundfile", "pydub", "faster-whisper"],
        "web": ["fastapi", "flask", "httpx", "playwright"],
        "dashboard": ["streamlit", "gradio", "plotly"],
    }


TOOLS: dict[str, Callable[..., dict[str, Any]]] = {
    "classify_request": classify_request,
    "save_note": save_note,
    "get_free_python_ai_libraries": get_free_python_ai_libraries,
}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "tukuk-mcp-compatible-server"}


@app.get("/tools/list")
def tools_list() -> dict[str, list[dict[str, str]]]:
    return {"tools": [{"name": name, "description": tool.__doc__ or name} for name, tool in TOOLS.items()]}


@app.post("/tools/invoke")
def tools_invoke(call: ToolCall) -> dict[str, Any]:
    name = call.payload.get("tool") if call.payload else None
    if name not in TOOLS:
        return {"ok": False, "error": f"Unknown tool: {name}"}
    result = TOOLS[name](**call.payload.get("arguments", {}))
    return {"ok": True, "tool": name, "result": result}
