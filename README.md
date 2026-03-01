# balintdecsi.github.io

Personal professional portfolio site built with Jekyll and hosted on GitHub Pages.

## Structure

- `index.html` — About page (landing)
- `cv.html` — CV / resume with downloadable PDF
- `projects.html` — Project showcase with GitHub links
- `assets/documents/` — Downloadable documents (CV PDF)
- `assets/css/style.css` — All styling
- `_layouts/` / `_includes/` — Jekyll templates

## Editing Content

All page content lives in the HTML files at the root. Edit them directly — Jekyll
renders them via the layout templates. The CV PDF can be replaced by dropping a new
file into `assets/documents/`.

## Local Development

```bash
gem install bundler jekyll
bundle exec jekyll serve
```

Then visit `http://localhost:4000`.
