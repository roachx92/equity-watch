# Site-directory consolidation — design

**Date:** 2026-07-17
**Branch:** `work/2026-07-17-site-dir-cleanup`

## Problem
The MkDocs site's build machinery was scattered across the repo root — `mkdocs.yml`,
`index.md`, `requirements.txt`, `overrides/`, `stylesheets/`, `hooks/`, and two build
scripts mixed into a `scripts/` folder that also held the Discord notifiers. Hard to see
at a glance what belongs to the website versus the research tooling.

## Decision
Consolidate **all site build machinery** into a single `web/` directory. Leave the
research master (`framework/`, `tickers/`, `summaries/`, `daily-watch.md`) at the repo
root — it is the substance the site publishes, referenced throughout CLAUDE.md, the
skills, and the workflows, and is not itself "the site." Keep the Discord notifiers in
`scripts/`, which becomes cleanly notification-only once the build scripts leave.

`web/` (not `site/`) because `site/` and `site_src/` are the gitignored MkDocs build
artifacts.

## Final layout
```
web/
  mkdocs.yml            # unchanged — its paths are relative to itself
  index.md
  requirements.txt
  overrides/            # theme templates
  stylesheets/home.css
  hooks/coverage.py     # build-time coverage-grid generator
  scripts/build.sh      # was scripts/build-site.sh
  scripts/serve.sh      # was scripts/serve-site.sh
  site_src/  site/      # gitignored build artifacts

scripts/                # notification tooling only (discord_common, notify_*, tests/)
framework/  tickers/  summaries/   # research master, untouched at root
```

## Why `mkdocs.yml` needs no edits
`custom_dir: overrides`, `hooks: hooks/coverage.py`, and `docs_dir: site_src` resolve
relative to the config file; the whole set moved into `web/` together, so they still
point at the right siblings. `extra_css: stylesheets/home.css` resolves under `docs_dir`
and the build copies stylesheets in as before.

## Build flow
`web/scripts/build.sh` / `serve.sh` `cd` into `web/`, assemble `site_src` from
`../framework ../tickers` (root content) plus the local `index.md`/`stylesheets`, and run
mkdocs — artifacts land at `web/site_src` and `web/site`. `serve.sh` also drops its
pre-existing bug (it copied a nonexistent top-level `reports/` dir, which fails under
`set -e`).

## Reference updates
`.gitignore` (`web/site*`), `.github/workflows/pages.yml` (trigger paths + run steps +
upload path), `web/hooks/coverage.py` docstring, `web/overrides/home.html` comment,
`CLAUDE.md` (coverage-hook path + a `web/` file-map entry), `.claude/skills/deep-dive/SKILL.md`,
`docs/part-2-scripts-plan.md`. Archival specs under `docs/superpowers/specs/` are left
as-is (historical).

## Verification
`./web/scripts/build.sh` builds `--strict` with all five coverage cards and their report
links intact; `web/site*` artifacts stay untracked.
