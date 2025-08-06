#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "opentelemetry-api>=1.36.0",
#     "opentelemetry-sdk>=1.36.0",
#     "opentelemetry-exporter-otlp-proto-grpc==1.36.0",
# ]
# ///

import time
import argparse
from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter


def parse_args():
    parser = argparse.ArgumentParser(
        description="Send OpenTelemetry metrics via OTLP gRPC"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="OTLP collector host (default: localhost)",
    )
    parser.add_argument(
        "--port", type=int, default=4317, help="OTLP gRPC port (default: 4317)"
    )
    parser.add_argument(
        "--insecure", action="store_true", help="Use insecure (no TLS) gRPC"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5000,
        help="Export interval millis (default: 5000)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    endpoint = f"http://{args.host}:{args.port}"
    exporter = OTLPMetricExporter(endpoint=endpoint, insecure=args.insecure)
    reader = PeriodicExportingMetricReader(
        exporter, export_interval_millis=args.interval
    )
    provider = MeterProvider(
        resource=Resource.create({"service.name": "metric-service"}),
        metric_readers=[reader],
    )
    metrics.set_meter_provider(provider)

    meter = metrics.get_meter(__name__)
    counter = meter.create_counter(
        name="heartbeat_total",
        description="Heartbeat events count",
        unit="1",
    )

    print(
        f"Sending metrics to {endpoint} every {args.interval} ms {'(insecure)' if args.insecure else ''}"
    )
    while True:
        counter.add(1, {"type": "heartbeat"})
        print("Sent one heartbeat")
        time.sleep(args.interval / 1000.0)


if __name__ == "__main__":
    main()
