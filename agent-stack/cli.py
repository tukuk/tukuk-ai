from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

from agent.main import run_agent
from security.diagnostic import check_url


async def agent_command(args: argparse.Namespace) -> None:
    print(json.dumps(await run_agent(args.request), indent=2, ensure_ascii=False))


def diagnostic_command(args: argparse.Namespace) -> None:
    print(json.dumps(check_url(args.url), indent=2, ensure_ascii=False))


def shell_command(args: argparse.Namespace) -> None:
    env = os.environ.copy()
    env["TUKUK_AGENT_MODEL"] = args.model
    subprocess.run(args.command, shell=True, env=env)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tukuk AI Agent CLI for terminal, console, shell, and automation.")
    parser.add_argument("--model", default=os.getenv("TUKUK_AGENT_MODEL", "llama3.2"))
    sub = parser.add_subparsers(dest="cmd", required=True)

    agent = sub.add_parser("agent", help="Run the LLM agent request pipeline")
    agent.add_argument("request")
    agent.set_defaults(func=agent_command)

    diag = sub.add_parser("diagnostic", help="Run defensive web security diagnostic")
    diag.add_argument("--url", required=True)
    diag.set_defaults(func=diagnostic_command)

    shell = sub.add_parser("shell", help="Run any shell command with Tukuk environment variables")
    shell.add_argument("command")
    shell.set_defaults(func=shell_command)

    args = parser.parse_args()
    if args.cmd == "agent":
        asyncio.run(args.func(args))
    else:
        args.func(args)


if __name__ == "__main__":
    main()
