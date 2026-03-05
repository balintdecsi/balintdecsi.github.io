# AGENTS.md

## Cursor Cloud specific instructions

This is a Jekyll static site (portfolio + UniBridge tool) hosted on GitHub Pages.

### Running the dev server

```bash
jekyll serve --host 0.0.0.0 --port 4000
```

The site is then available at `http://localhost:4000`. Jekyll watches for file changes and auto-regenerates.

### Key caveats

- **No Gemfile in the repo.** Jekyll and Bundler are installed globally via `gem install bundler jekyll`. You can run `jekyll serve` directly (no `bundle exec` needed).
- **Pretty permalinks.** `_config.yml` sets `permalink: pretty`, so pages are served at `/cv/` and `/projects/` (not `/cv.html`).
- **No linter or test suite.** This is a pure static HTML/CSS/JS site with Jekyll templating. There are no automated tests or lint configurations.
- **UniBridge sub-app** lives under `tools/unibridge/` and uses its own layout (`_layouts/unibridge.html`). It uses vanilla JS with i18n and localStorage for state.
- **External CDN dependencies** (Google Fonts, `html2pdf.js`, QR code API) require internet access for full functionality.
