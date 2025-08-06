.PHONY: all

all: otelcol-contrib
	dotenv -f .env run ./otelcol-contrib --config=otelcol-config.yaml

otelcol-contrib:
	curl -L https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.131.1/otelcol-contrib_0.131.1_darwin_arm64.tar.gz | tar xzf - otelcol-contrib

