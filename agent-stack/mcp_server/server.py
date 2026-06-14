from __future__ import annotations

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Tukuk Agent MCP")
DATA_DIR = Path(os.getenv("TUKUK_MCP_DATA_DIR", "data"))


@mcp.tool()
def classify_request(request: str) -> dict[str, object]:
    """Classify a user request into Tukuk AI engines."""
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


@mcp.tool()
def save_note(title: str, note: str) -> dict[str, str]:
    """Save a student note into the local MCP data directory."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    safe_title = "".join(ch if ch.isalnum() or ch in " -_" else "-" for ch in title).strip("-") or "note"
    path = DATA_DIR / f"{safe_title}.txt"
    path.write_text(note, encoding="utf-8")
    return {"status": "saved", "path": str(path)}


@mcp.tool()
def get_free_python_ai_libraries() -> dict[str, list[str]]:
    """Return a free/open-source Python AI library map."""
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
