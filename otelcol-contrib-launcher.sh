#!/usr/bin/env bash
set -e

# otelcol-contrib-launcher.sh
# Universal launcher for otelcol-contrib (macOS/Linux, amd64/arm64)
# Usage: ./otelcol-contrib-launcher.sh
#
# - Downloads the correct otelcol-contrib binary for your OS/arch if not present
# - Loads environment variables from .env if present
# - Runs otelcol-contrib with otelcol-config.yaml

OTELCOL_VERSION="0.131.0"
BINARY_NAME="otelcol-contrib"
CONFIG_FILE="otelcol-config.yaml"

# Detect OS and ARCH
detect_platform() {
  OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
  ARCH="$(uname -m)"
  case "$ARCH" in
    x86_64|amd64) ARCH=amd64 ;;
    arm64|aarch64) ARCH=arm64 ;;
    *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
  esac
  echo "${OS}_${ARCH}"
}

PLATFORM=$(detect_platform)
TAR_NAME="${BINARY_NAME}_${OTELCOL_VERSION}_${PLATFORM}.tar.gz"
DOWNLOAD_URL="https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v${OTELCOL_VERSION}/${TAR_NAME}"

# Download otelcol-contrib if not present
if [ ! -x "./${BINARY_NAME}" ]; then
  echo "Downloading $TAR_NAME ..."
  curl -L "$DOWNLOAD_URL" | tar xzf - "$BINARY_NAME"
  chmod +x "$BINARY_NAME"
fi

# Load .env if present
if [ -f .env ]; then
  echo "Loading environment variables from .env ..."
  set -a
  . ./.env
  set +a
fi

# Run otelcol-contrib
exec ./$BINARY_NAME --config=$CONFIG_FILE "$@"
