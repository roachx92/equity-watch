#!/usr/bin/env bash
# Assemble the publishable tree and serve with live reload.
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf site_src
mkdir -p site_src
cp index.md site_src/
cp -R framework tickers reports site_src/
[ -d stylesheets ] && cp -R stylesheets site_src/
rm -f site_src/reports/_template.md

mkdocs serve
