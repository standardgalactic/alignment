#!/usr/bin/env bash

set -e

OUT="tree.json"

echo "Scanning directory structure..."

python3 << 'PY' > "$OUT"
import os, json

IGNORE = {".git", "__pycache__", "node_modules", ".venv"}

def build(path):
    name = os.path.basename(path) or "root"

    node = {
        "name": name,
        "type": "dir",
        "children": []
    }

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return node

    for e in entries:
        if e in IGNORE:
            continue

        full = os.path.join(path, e)

        if os.path.isdir(full):
            node["children"].append(build(full))
        else:
            try:
                size = os.path.getsize(full)
            except:
                size = 0

            node["children"].append({
                "name": e,
                "type": "file",
                "size": size
            })

    return node

print(json.dumps(build("."), indent=2))
PY

echo "Directory tree written to $OUT"
echo "Open local-map.html in a browser"
