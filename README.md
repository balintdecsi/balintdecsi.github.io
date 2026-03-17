# Bálint Décsi Portfolio

Personal professional portfolio site built with Jekyll and hosted on GitHub Pages.

## Features
- **Experience-First Home Page:** Highlights actual work with ML and AI.
- **Dynamic PDF CV:** Interactive CV with automated PDF generation using `html2pdf.js`.
- **Responsive Design:** Modern, clean, and mobile-friendly aesthetics.
- **Jekyll Optimized:** Fully compatible with GitHub Pages and local development.

## Prerequisites

You'll need Ruby and Bundler installed on your system.

- **Ruby:** [Installation Guide](https://www.ruby-lang.org/en/documentation/installation/)
- **Bundler:** `gem install bundler`

## Local Development

1. **Install Dependencies:**
   ```bash
   bundle install
   ```

2. **Run Jekyll Server:**
   ```bash
   bundle exec jekyll serve
   ```

3. **View Site:**
   Open your browser at `http://localhost:4000`.

## Structure

- `index.html` — About page (landing)
- `cv.html` — CV / resume with automated PDF download
- `projects.html` — Project showcase
- `assets/pictures/` — Profile images and other visuals
- `assets/css/style.css` — Site styling
- `_layouts/` & `_includes/` — Jekyll templates
- `_config.yml` — Jekyll site configuration
