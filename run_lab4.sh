#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")/services"
# Build the project images and start the four services.
docker compose up -d --build
printf '\nPrediction: http://127.0.0.1:8004/docs\n'
printf 'Prometheus: http://127.0.0.1:9094/targets\n'
printf 'Grafana: http://127.0.0.1:3004/d/lab4-car-price-monitoring\n'
