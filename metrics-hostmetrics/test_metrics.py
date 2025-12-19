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
from typing import List, Dict, Any
import pytest
import requests


class TestHostMetrics:
    """Test suite for hostmetrics forwarding via Prometheus Remote Write"""

    @pytest.fixture(scope="module")
    def prometheus_url(self):
        """Get Prometheus URL from environment or use default"""
        return os.environ.get("PROMETHEUS_URL", "http://localhost:9090")

    @pytest.fixture(scope="module", autouse=True)
    def wait_for_metrics(self, prometheus_url):
        """Wait for metrics to be collected (collection_interval is 1m)"""
        print("\n[INFO] Waiting for Prometheus to start...")
        # Wait for Prometheus to be ready
        for i in range(30):
            try:
                response = requests.get(f"{prometheus_url}/-/ready", timeout=2)
                if response.status_code == 200:
                    print("[INFO] Prometheus is ready")
                    break
            except:
                pass
            time.sleep(1)
        else:
            pytest.fail("Prometheus did not become ready in time")

        print("[INFO] Waiting for OTel Collector to collect and send metrics (70 seconds)...")
        time.sleep(70)
        print("[INFO] Wait complete, running tests...")

    @pytest.fixture(autouse=True)
    def wait_between_tests(self):
        """Small delay between tests to avoid rate limiting"""
        yield
        time.sleep(0.1)

    def _query_prometheus(self, prometheus_url: str, query: str) -> List[Dict[str, Any]]:
        """Execute PromQL query and return results

        Args:
            prometheus_url: Base URL of Prometheus
            query: PromQL query string

        Returns:
            List of result items from the query
        """
        response = requests.get(
            f"{prometheus_url}/api/v1/query",
            params={"query": query},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        assert data.get("status") == "success", f"Query failed: {data}"
        return data.get("data", {}).get("result", [])

    def _get_all_metric_names(self, prometheus_url: str) -> List[str]:
        """Get all metric names from Prometheus"""
        response = requests.get(
            f"{prometheus_url}/api/v1/label/__name__/values",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        assert data.get("status") == "success", f"Failed to get metric names: {data}"
        return data.get("data", [])

    def test_prometheus_is_running(self, prometheus_url):
        """Verify Prometheus is accessible"""
        response = requests.get(f"{prometheus_url}/-/ready", timeout=5)
        assert response.status_code == 200
        print("[OK] Prometheus is running")

    def test_metrics_received(self, prometheus_url):
        """Verify metrics are received"""
        metric_names = self._get_all_metric_names(prometheus_url)
        # Filter out Prometheus's own metrics
        otel_metrics = [m for m in metric_names if not m.startswith('prometheus_')
                       and not m.startswith('go_') and not m.startswith('process_')]

        assert len(otel_metrics) > 0, f"No metrics received from OTel Collector. Available metrics: {metric_names}"
        print(f"[OK] Received {len(otel_metrics)} metrics from OTel Collector")
        print(f"     Sample metrics: {otel_metrics[:10]}")

    def test_external_labels_present(self, prometheus_url):
        """Verify external_labels (region: tokyo) is attached"""
        # Query for any metric with region=tokyo label
        results = self._query_prometheus(prometheus_url, '{region="tokyo"}')

        assert len(results) > 0, "External label 'region=tokyo' not found in any metrics"
        print(f"[OK] Found {len(results)} time series with region=tokyo")

    def test_resource_attributes_present(self, prometheus_url):
        """Verify resource attributes (sample.name) are converted to labels"""
        # Note: Prometheus converts '.' to '_' in label names
        # So 'sample.name' becomes 'sample_name'
        results = self._query_prometheus(prometheus_url, '{sample_name="my-service"}')

        assert len(results) > 0, "Resource attribute 'sample_name=my-service' not found"
        print(f"[OK] Found {len(results)} time series with sample_name=my-service")

    def test_cpu_metrics_present(self, prometheus_url):
        """Verify CPU metrics are collected"""
        metric_names = self._get_all_metric_names(prometheus_url)
        cpu_metrics = [m for m in metric_names if 'cpu' in m.lower()]

        assert len(cpu_metrics) > 0, f"No CPU metrics found. Available metrics: {metric_names}"
        print(f"[OK] Found {len(cpu_metrics)} CPU metric types")
        print(f"     CPU metrics: {cpu_metrics}")

    def test_memory_metrics_present(self, prometheus_url):
        """Verify memory metrics are collected"""
        metric_names = self._get_all_metric_names(prometheus_url)
        memory_metrics = [m for m in metric_names if 'memory' in m.lower()]

        assert len(memory_metrics) > 0, f"No memory metrics found"
        print(f"[OK] Found {len(memory_metrics)} memory metric types")
        print(f"     Memory metrics: {memory_metrics}")

    def test_disk_metrics_present(self, prometheus_url):
        """Verify disk/filesystem metrics are collected"""
        metric_names = self._get_all_metric_names(prometheus_url)
        disk_metrics = [m for m in metric_names
                       if 'disk' in m.lower() or 'filesystem' in m.lower()]

        assert len(disk_metrics) > 0, f"No disk/filesystem metrics found"
        print(f"[OK] Found {len(disk_metrics)} disk/filesystem metric types")

    def test_metric_values_are_numeric(self, prometheus_url):
        """Verify metric values are valid numbers"""
        # Query for all OTel metrics
        results = self._query_prometheus(prometheus_url, '{sample_name="my-service"}')
        assert len(results) > 0, "No metrics to check"

        invalid_values = []
        for result in results:
            metric_name = result.get("metric", {}).get("__name__", "unknown")
            value = result.get("value", [None, None])[1]  # [timestamp, value]

            try:
                float_value = float(value)
                if float_value != float_value:  # NaN check
                    invalid_values.append(f"{metric_name}: NaN")
            except (ValueError, TypeError):
                invalid_values.append(f"{metric_name}: {type(value)}")

        assert len(invalid_values) == 0, f"Found invalid metric values: {invalid_values[:5]}"
        print(f"[OK] All metric values are valid numeric values")

    def test_multiple_metric_types(self, prometheus_url):
        """Verify we have multiple types of host metrics"""
        metric_names = self._get_all_metric_names(prometheus_url)

        # Filter to OTel metrics only
        otel_metrics = [m for m in metric_names if not m.startswith('prometheus_')
                       and not m.startswith('go_') and not m.startswith('process_')]

        # We expect metrics from multiple scrapers
        expected_keywords = ["cpu", "memory", "disk", "filesystem", "network", "process"]
        found_keywords = []

        for keyword in expected_keywords:
            if any(keyword in name.lower() for name in otel_metrics):
                found_keywords.append(keyword)

        assert len(found_keywords) >= 3, \
            f"Expected metrics from at least 3 scrapers, found: {found_keywords}"
        print(f"[OK] Found metrics from {len(found_keywords)} scrapers: {found_keywords}")
        print(f"     Total unique OTel metrics: {len(otel_metrics)}")

    def test_labels_include_region_and_sample_name(self, prometheus_url):
        """Verify both region and sample_name labels are present on metrics"""
        # Query for metrics with both labels
        results = self._query_prometheus(
            prometheus_url,
            '{region="tokyo",sample_name="my-service"}'
        )

        assert len(results) > 0, \
            "No metrics found with both region=tokyo and sample_name=my-service labels"
        print(f"[OK] Found {len(results)} time series with both required labels")

        # Show a sample metric with all its labels
        if results:
            sample = results[0]
            print(f"     Sample metric: {sample['metric']['__name__']}")
            print(f"     Sample labels: {sample['metric']}")


if __name__ == "__main__":
    # Run pytest with verbose output
    pytest.main([__file__, "-v", "-s"])
