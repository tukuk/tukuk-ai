from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
import webbrowser
from pathlib import Path

from agent.main import run_agent
from security.diagnostic import check_url


ROOT = Path(__file__).resolve().parent
WEBSITE_INDEX = ROOT.parent / "index.html"


async def agent_command(args: argparse.Namespace) -> None:
    print(json.dumps(await run_agent(args.request), indent=2, ensure_ascii=False))


def diagnostic_command(args: argparse.Namespace) -> None:
    print(json.dumps(check_url(args.url), indent=2, ensure_ascii=False))


def shell_command(args: argparse.Namespace) -> None:
    env = os.environ.copy()
    env["TUKUK_AGENT_MODEL"] = args.model
    subprocess.run(args.command, shell=True, env=env, cwd=args.cwd)


def terminal_command(args: argparse.Namespace) -> None:
    env = os.environ.copy()
    env["TUKUK_AGENT_MODEL"] = args.model
    shell = args.shell or os.environ.get("SHELL") or "sh"
    subprocess.run([shell], env=env, cwd=args.cwd)


def pipeline_command(args: argparse.Namespace) -> None:
    subprocess.run([sys.executable, "-m", "compileall", "agent", "mcp_server", "security", "cli.py"], cwd=ROOT, check=args.strict)
    subprocess.run([sys.executable, "agent/main.py", "--self-test"], cwd=ROOT, check=args.strict)
    subprocess.run([sys.executable, "security/diagnostic.py", "--url", args.url, "--output", "diagnostic-report.json"], cwd=ROOT, check=args.strict)


def mcp_command(args: argparse.Namespace) -> None:
    subprocess.run([sys.executable, "-m", "uvicorn", "mcp_server.server:app", "--host", args.host, "--port", str(args.port)], cwd=ROOT)


def web_command(args: argparse.Namespace) -> None:
    url = args.url or WEBSITE_INDEX.as_uri()
    if args.open:
        webbrowser.open(url)
    print(url)


def kilo_command(args: argparse.Namespace) -> None:
    print("Tukuk Kilo-Free Agent")
    print("Commands:")
    print("  python cli.py agent \"Build a student web app\"")
    print("  python cli.py terminal")
    print("  python cli.py mcp")
    print("  python cli.py pipeline")
    print("  python cli.py diagnostic --url https://example.com")
    print("  python cli.py web --open")
    print("  python cli.py shell \"echo hello\"")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tukuk AI Kilo-Free CLI for terminal, console, shell, web, and automation.")
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
    shell.add_argument("--cwd", default=str(ROOT))
    shell.set_defaults(func=shell_command)

    terminal = sub.add_parser("terminal", help="Open a Tukuk terminal/console/shell session")
    terminal.add_argument("--shell")
    terminal.add_argument("--cwd", default=str(ROOT))
    terminal.set_defaults(func=terminal_command)

    pipeline = sub.add_parser("pipeline", help="Run Tukuk agent stack pipeline checks")
    pipeline.add_argument("--url", default="https://example.com")
    pipeline.add_argument("--strict", action="store_true")
    pipeline.set_defaults(func=pipeline_command)

    mcp = sub.add_parser("mcp", help="Start MCP-compatible tool server")
    mcp.add_argument("--host", default="0.0.0.0")
    mcp.add_argument("--port", type=int, default=8080)
    mcp.set_defaults(func=mcp_command)

    web = sub.add_parser("web", help="Open or print the Tukuk AI website")
    web.add_argument("--url")
    web.add_argument("--open", action="store_true")
    web.set_defaults(func=web_command)

    kilo = sub.add_parser("kilo", help="Show Kilo-Free command guide")
    kilo.set_defaults(func=kilo_command)

    args = parser.parse_args()
    if args.cmd == "agent":
        asyncio.run(args.func(args))
    else:
        args.func(args)


if __name__ == "__main__":
    main()
