#!/usr/bin/env bash
# Assemble the publishable tree and serve with live reload.
# Mirrors build.sh's assembly (content from the repo root, machinery under web/).
set -euo pipefail
cd "$(dirname "$0")/.."   # -> web/

rm -rf site_src
mkdir -p site_src
cp index.md site_src/
cp -R ../framework ../tickers site_src/
[ -d stylesheets ] && cp -R stylesheets site_src/
rm -f site_src/framework/report-template.md

mkdocs serve
