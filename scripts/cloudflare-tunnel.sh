#!/usr/bin/env bash

set -euo pipefail

PORT="${PORT:-8080}"
HOST="${HOST:-127.0.0.1}"
PROTOCOL="${CLOUDFLARED_PROTOCOL:-http2}"

exec cloudflared tunnel --protocol "$PROTOCOL" --url "http://${HOST}:${PORT}"