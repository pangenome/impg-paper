#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

pdflatex -interaction=nonstopmode main.tex
bibtex main
bibtex Meth
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

echo "Done: main.pdf"
