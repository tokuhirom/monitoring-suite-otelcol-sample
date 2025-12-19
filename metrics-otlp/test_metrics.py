#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pytest>=7.0.0",
#     "requests>=2.31.0",
# ]
# ///

import os
import time
import pytest
import requests


def test_cpu_metrics_with_labels():
    """メトリクスが取得できて、適切なラベルが付与されていることを確認"""
    prometheus_url = os.environ.get("PROMETHEUS_URL", "http://localhost:9090")

    # Prometheus が起動しているか確認
    response = requests.get(f"{prometheus_url}/-/ready", timeout=5)
    assert response.status_code == 200, "Prometheus is not ready"

    # CPU メトリクスを region=tokyo と sample_name=my-service でクエリ
    response = requests.get(
        f"{prometheus_url}/api/v1/query",
        params={"query": 'heartbeat_total{region="tokyo",service_name="metric-service"}'},
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    assert data.get("status") == "success", f"Query failed: {data}"
    results = data.get("data", {}).get("result", [])

    # メトリクスが取得できていることを確認
    assert len(results) > 0, "No OTLP metrics found with required labels"

    # 最初の結果を検証
    metric = results[0]
    labels = metric.get("metric", {})
    value_data = metric.get("value", [None, None])

    # ラベルの確認
    assert labels.get("__name__") == "heartbeat_total", "Metric name mismatch"
    assert labels.get("region") == "tokyo", "External label 'region=tokyo' not found"
    assert labels.get("service_name") == "metric-service", "Resource attribute 'service_name=metric-service' not found"

    # 値の確認
    value = float(value_data[1])
    assert value >= 0, f"Invalid metric value: {value}"

    print(f"✓ metrics found: {len(results)} time series")
    print(f"✓ Sample metric: {labels.get('__name__')}")
    print(f"✓ Labels: region={labels.get('region')}, service_name={labels.get('service_name')}")
    print(f"✓ Value: {value}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
