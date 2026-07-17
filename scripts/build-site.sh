#!/usr/bin/env bash
# Assemble the publishable tree and build the site. Extra args pass through to mkdocs.
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf site_src
mkdir -p site_src
cp index.md site_src/
cp -R framework tickers site_src/
[ -d stylesheets ] && cp -R stylesheets site_src/
rm -f site_src/framework/report-template.md   # skeleton is not published

mkdocs build --strict "$@"
