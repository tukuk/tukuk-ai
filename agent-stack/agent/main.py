from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx


@dataclass
class AgentConfig:
    model: str
    system_prompt: str
    mcp_url: str
    data_dir: Path


def load_config() -> AgentConfig:
    return AgentConfig(
        model=os.getenv("TUKUK_AGENT_MODEL", "llama3.2"),
        system_prompt=os.getenv("TUKUK_AGENT_SYSTEM", "Anda ialah AI agent pelajar Tukuk."),
        mcp_url=os.getenv("TUKUK_MCP_URL", "http://localhost:8080"),
        data_dir=Path(os.getenv("TUKUK_DATA_DIR", "data")),
    )


def build_prompt(request: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    config = load_config()
    return {
        "model": config.model,
        "system": config.system_prompt,
        "request": request,
        "context": context or {},
        "tools": ["study", "coding", "media", "library", "security_diagnostic", "mcp_lookup"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


async def ask_mcp(request: str) -> dict[str, Any]:
    config = load_config()
    config.data_dir.mkdir(parents=True, exist_ok=True)
    payload = build_prompt(request)
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(f"{config.mcp_url}/tools/invoke", json={"request": request, "payload": payload})
        response.raise_for_status()
        return response.json()


async def run_agent(request: str) -> dict[str, Any]:
    config = load_config()
    config.data_dir.mkdir(parents=True, exist_ok=True)
    payload = build_prompt(request)
    result = {
        "agent": "tukuk-llm-agent",
        "model": config.model,
        "mcp_url": config.mcp_url,
        "request": request,
        "pipeline": ["receive_request", "classify_intent", "select_engine", "call_mcp_if_needed", "return_answer"],
        "payload": payload,
    }
    (config.data_dir / "last-request.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Tukuk LLM Agent")
    parser.add_argument("--request", default="Bantu saya belajar dan buat app web pelajar")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        print("Tukuk LLM Agent self-test OK")
        return

    import asyncio

    print(json.dumps(asyncio.run(run_agent(args.request)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
