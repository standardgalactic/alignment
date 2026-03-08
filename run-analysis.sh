#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CORPUS="$SCRIPT_DIR"
OUTPUT="$SCRIPT_DIR/semantic_index"

mkdir -p "$OUTPUT"

python3 "$SCRIPT_DIR/analyze.py" "$CORPUS" "$OUTPUT"
