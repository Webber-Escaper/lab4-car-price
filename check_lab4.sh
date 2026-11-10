#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
docker compose -f services/compose.yml ps
python3 - <<'PY'
import json
from urllib.request import build_opener, ProxyHandler

# These addresses belong to services running on this Ubuntu machine.
client = build_opener(ProxyHandler({}))
with client.open("http://127.0.0.1:8004/health", timeout=5) as response:
    health = json.load(response)
assert health["status"] == "ok" and health["service_version"] == 3
print("Prediction service is healthy.")

with client.open("http://127.0.0.1:9094/api/v1/targets", timeout=5) as response:
    targets = json.load(response)["data"]["activeTargets"]
assert any(target["labels"].get("job") == "ml_service" and target["health"] == "up" for target in targets)
print("Prometheus target is UP.")

with client.open("http://127.0.0.1:3004/api/health", timeout=5) as response:
    grafana = json.load(response)
assert grafana["database"] == "ok"
print("Grafana is healthy.")
PY
