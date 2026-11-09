#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for step in "pdflatex -interaction=nonstopmode -halt-on-error main.tex" "bibtex main" "pdflatex -interaction=nonstopmode -halt-on-error main.tex" "pdflatex -interaction=nonstopmode -halt-on-error main.tex"; do
  echo "[build] $step"
  $step > /dev/null || { echo "[build] failed: $step"; tail -40 main.log; exit 1; }
done
echo "[build] warnings:"; grep -E "Warning|undefined" main.log | sort | uniq -c | sort -rn | head -20 || true
echo "[build] done: $(pwd)/main.pdf"
