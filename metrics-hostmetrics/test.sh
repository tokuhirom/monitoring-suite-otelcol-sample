#!/bin/bash
set -e

echo "Starting test environment..."

docker compose --profile test down --remove-orphans

# 環境変数を設定
export SAKURA_MONITORINGSUITE_METRICS_ENDPOINT=http://prometheus:9090/api/v1/write
export SAKURA_MONITORINGSUITE_METRICS_INSECURE=true
export SAKURA_MONITORINGSUITE_METRICS_CREDENTIALS=dummy

# テスト環境を起動
docker compose --profile test up -d

echo "Waiting 70 seconds for metrics collection..."
sleep 70

echo "Running tests..."
uv run test_metrics.py -v

# クリーンアップ
echo "Cleaning up..."
docker compose --profile test down

echo "Test completed!"
