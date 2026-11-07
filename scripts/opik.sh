#!/usr/bin/env bash
# Start a lightweight local Opik (Comet) for tracing, prompts and evaluation. Educational use only.
#
# Fetches only the official docker-compose files into .opik/ (git-ignored) and starts the
# core services: MySQL, Redis, ClickHouse, ZooKeeper, MinIO, the backend and the UI.
# It skips the python-backend (online scoring rules, needs a privileged container) and
# the optional guardrails, OTel and Jaeger services.
#
# Usage: scripts/opik.sh [up|down|status|logs|reset]
#   up      start Opik, UI at http://localhost:5173 (default)
#   down    stop it, keep the data
#   status  show running containers
#   logs    follow the logs
#   reset   stop it and DELETE all Opik data
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$ROOT/.opik"
COMPOSE_DIR="$DIR/deployment/docker-compose"
SERVICES=(mysql redis zookeeper clickhouse-init clickhouse minio-init minio mc backend frontend)

for cmd in docker git; do
  command -v "$cmd" >/dev/null || { echo "error: $cmd is required" >&2; exit 1; }
done
docker compose version >/dev/null 2>&1 || { echo "error: docker compose v2 is required" >&2; exit 1; }

compose() { docker compose --profile opik -f "$COMPOSE_DIR/docker-compose.yaml" "$@"; }

fetch() {
  [ -d "$COMPOSE_DIR" ] && return
  echo "Fetching Opik compose files into .opik/ ..."
  git clone --quiet --depth 1 --filter=blob:none --sparse https://github.com/comet-ml/opik.git "$DIR"
  git -C "$DIR" sparse-checkout set deployment/docker-compose
}

case "${1:-up}" in
  up)
    fetch
    compose up -d --wait "${SERVICES[@]}"
    echo
    echo "Opik is up: http://localhost:5173"
    echo "Set OPIK_URL_OVERRIDE=http://localhost:5173/api in .env and restart the API."
    ;;
  down)   fetch; compose down ;;
  status) fetch; compose ps ;;
  logs)   fetch; compose logs -f --tail 100 backend frontend ;;
  reset)  fetch; compose down -v ;;
  *) echo "usage: $0 [up|down|status|logs|reset]" >&2; exit 1 ;;
esac
