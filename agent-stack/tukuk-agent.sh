#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$ROOT"
MODEL="${TUKUK_AGENT_MODEL:-llama3.2}"
case "${1:-kilo}" in
  agent)
    shift || true
    python cli.py agent "${1:-Build a student web app}" --model "$MODEL"
    ;;
  terminal|console|shell-session)
    python cli.py terminal
    ;;
  mcp)
    python cli.py mcp
    ;;
  pipeline)
    python cli.py pipeline
    ;;
  diagnostic|security)
    shift || true
    python cli.py diagnostic --url "${1:-https://example.com}"
    ;;
  web|website)
    python cli.py web --open
    ;;
  kilo|help|--help|-h|"")
    python cli.py kilo
    ;;
  docker)
    docker compose up --build
    ;;
  *)
    python cli.py "$@"
    ;;
esac
