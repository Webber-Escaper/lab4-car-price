#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")/services"
docker compose down
