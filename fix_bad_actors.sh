#!/usr/bin/env bash
set -euo pipefail

python3 - "$@" <<'PY'
import argparse
import difflib
from pathlib import Path
import re
import shutil

parser = argparse.ArgumentParser(description="Correct the Bad Actors TXT and VTT transcripts.")
parser.add_argument("--dry-run", action="store_true", help="show changes without writing")
parser.add_argument("directory", nargs="?", type=Path, default=Path.cwd())
args = parser.parse_args()

corrections = {
    r"\bVaughn\b": "Vaughan",
    r"\bChristy\b": "Christie",
    r"\bStrathairn\b": "Strathern",
    r"\bDanello Meadows\b": "Donella Meadows",
    r"\bEleanor Ostrom\b": "Elinor Ostrom",
    r"\bexplanational\b": "explanation",
    r"\bReinforce\b": "REINFORCE",
    r"\bsafe space, they discard\b": "save space, they discard",
    r"\bthe research, Flyxion cited,": "the research Flyxion cited",
    r"\bO-rings and the solid rocket boosters\b": "O-rings in the solid rocket boosters",
}
criterion = re.compile(
    r"Criterion four\.(?=\r?\n(?:\r?\n[0-9:.]+ --> [^\r\n]+\r?\n)?"
    r"Preservation of provenance and alternatives\.)"
)
stem = "Why_Systems_Keep_Manufacturing_Bad_Actors"
changes = []
for extension in ("txt", "vtt"):
    path = args.directory / f"{stem}.{extension}"
    original = path.read_bytes().decode("utf-8")
    corrected = original
    for pattern, replacement in corrections.items():
        corrected = re.sub(pattern, replacement, corrected)
    corrected = criterion.sub("Criterion five.", corrected)
    if extension == "vtt":
        timing = lambda text: [line for line in text.splitlines() if " --> " in line]
        if timing(original) != timing(corrected):
            raise SystemExit("WebVTT cue timings changed. No files were written.")
    changes.append((path, original, corrected))

for path, original, corrected in changes:
    if original == corrected:
        print(f"{path.name}: no changes")
    elif args.dry_run:
        for line in difflib.unified_diff(
            original.splitlines(), corrected.splitlines(),
            fromfile=path.name, tofile=f"{path.name} (corrected)", lineterm="",
        ):
            print(line)
    else:
        backup = path.with_name(path.name + ".bak")
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_bytes(corrected.encode("utf-8"))
        print(f"Corrected {path.name} (backup: {backup.name})")
PY
