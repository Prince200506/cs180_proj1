# Web Branch Workflow

This document defines a simple branch architecture for development and GitHub Pages publishing.

## Branch Roles

- main: code development branch for notebook, utilities, and experiments.
- web: publish branch for GitHub Pages and static visualization content.

## Recommended Repository Layout on web

- index.html: GitHub Pages entry point.
- web/styles.css: page styling.
- code/results/: final result images shown on the page.
- code/test_results/: test result images shown on the page.

## Daily Workflow

1. Work on algorithm and notebook changes in main.
2. Generate images into code/results and code/test_results.
3. Switch to web and sync latest result files.
4. Commit only static-site and result updates on web.
5. Push web and let GitHub Pages deploy.

## Commands

Use these commands from repository root.

```powershell
# 1) develop in main
git checkout main

# 2) after generating new images, switch to publish branch
git checkout web

# 3) pull latest remote web (optional but recommended)
git pull origin web

# 4) commit page/results updates
git add index.html web/styles.css web/app.js code/results code/test_results
git commit -m "Update gallery and latest project outputs"

# 5) push for GitHub Pages deployment
git push origin web
```

## GitHub Pages Settings

In repository settings:

- Source branch: web
- Folder: /(root)

Then the page serves from index.html at the root of web.

## Keep web Clean

- Do not put training data or large raw assets not needed for showcase in web branch.
- Keep notebook iterations and debug files in main.
- Only publish final artifacts and minimal static site files in web.