#!/usr/bin/env bash
set -euo pipefail

VERSION="v0.2.1"
URL="https://github.com/andrewyng/openworker/releases/download/${VERSION}/OpenWorker-macos-arm64.app.tar.gz"
EXPECTED_SHA256="7d9dbb9af9da61029f98260bf46efd7432e2ef1dc8727a5c24deb5f4568c9067"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

curl -fL "$URL" -o "$TMP/openworker.tar.gz"
ACTUAL="$(shasum -a 256 "$TMP/openworker.tar.gz" | awk '{print $1}')"
if [[ "$ACTUAL" != "$EXPECTED_SHA256" ]]; then
  echo "BLOCKED: OpenWorker archive checksum mismatch" >&2
  echo "expected=$EXPECTED_SHA256 actual=$ACTUAL" >&2
  exit 1
fi

mkdir -p "$HOME/Applications"
tar -xzf "$TMP/openworker.tar.gz" -C "$HOME/Applications"
echo "REAL: OpenWorker ${VERSION} archive verified and extracted to $HOME/Applications"
