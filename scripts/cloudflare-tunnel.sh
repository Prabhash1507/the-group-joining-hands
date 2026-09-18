#!/usr/bin/env bash

set -euo pipefail

PORT="${PORT:-8080}"
HOST="${HOST:-127.0.0.1}"

exec cloudflared tunnel --url "http://${HOST}:${PORT}"