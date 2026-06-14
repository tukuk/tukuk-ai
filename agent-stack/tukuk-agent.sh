#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$ROOT"
MODEL="${TUKUK_AGENT_MODEL:-llama3.2}"
case "${1:-agent}" in
  agent)
    shift || true
    python cli.py agent "${1:-Bantu saya belajar dan buat app web pelajar}" --model "$MODEL"
    ;;
  diagnostic)
    shift || true
    python cli.py diagnostic --url "${1:-https://example.com}"
    ;;
  docker)
    docker compose up --build
    ;;
  pipeline)
    python -m compileall agent mcp_server security
    python security/diagnostic.py --url https://example.com --output diagnostic-report.json || true
    ;;
  *)
    python cli.py "$@"
    ;;
esac
