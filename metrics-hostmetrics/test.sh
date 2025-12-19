#!/usr/bin/env bash
#
# 環境変数を設定してテスト環境を起動
SAKURA_MONITORINGSUITE_METRICS_ENDPOINT=http://prometheus:9090/api/v1/write \
    SAKURA_MONITORINGSUITE_METRICS_INSECURE=true \
    SAKURA_MONITORINGSUITE_METRICS_CREDENTIALS=dummy \
    docker-compose --profile test up -d

uv run --script test_metrics.py

