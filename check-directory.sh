#!/usr/bin/env bash

ROOT=${1:-.}

echo "Directory structure summary"
echo

echo "Total directories:"
find "$ROOT" -type d | wc -l

echo
echo "Total files:"
find "$ROOT" -type f | wc -l

echo
echo "File types:"
find "$ROOT" -type f \
| sed 's/.*\.//' \
| sort \
| uniq -c \
| sort -nr
