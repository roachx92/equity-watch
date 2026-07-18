#!/usr/bin/env bash
# Assemble the publishable tree and build the site. Extra args pass through to mkdocs.
# Content (framework/, tickers/) lives at the repo root; the site machinery lives here
# under web/. We run from web/ so mkdocs picks up web/mkdocs.yml and writes web/site.
set -euo pipefail
cd "$(dirname "$0")/.."   # -> web/

rm -rf site_src
mkdir -p site_src
cp index.md site_src/
cp -R ../framework ../tickers site_src/
[ -d stylesheets ] && cp -R stylesheets site_src/
rm -f site_src/framework/report-template.md   # skeleton is not published

mkdocs build --strict "$@"
