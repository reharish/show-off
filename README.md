# show-off

Reveal.js is great, but managing presentations with it can be a hassle. You have to drag around a `dist/` directory, set up local HTTP servers just to preview your slides, deal with broken relative paths for images, and fight with CSS for custom layouts.

`show-off` is a simple Python CLI that takes a single Markdown file and compiles it into a completely standalone, beautiful HTML slideshow. 

No directories to manage, no CDNs to fetch, and everything—including your images and styles—is packed into a single offline-ready file that you can share anywhere.

---

## What it does

- **Zero-dependency output**: Your styles, scripts, plugins, and images (automatically converted to base64) are compiled inline. The output HTML file works 100% offline.
- **Polished styles by default**: Instead of reveal.js's basic styling, it automatically applies modern typography (Plus Jakarta Sans), radial dark backgrounds, glassmorphic cards, and macOS-style code blocks.
- **Layout flexibility**: Because it compiles to HTML, you can drop inline HTML elements (like flexbox/grid divs) directly into your Markdown for complex multi-column layouts.
- **YAML configuration**: Configure transitions, themes, core Reveal options, or write custom CSS directly in the Markdown's frontmatter.

---

## Installation

Install it directly via pip:
```bash
pip install show-off
```

Or clone the repository and install it locally:
```bash
git clone https://github.com/reharish/show-off.git
cd show-off
pip3 install -e . --break-system-packages
```

---

## Usage

### 1. Initialize a template
Generate a starting presentation template in your current directory:
```bash
show-off init
```
This creates `slides.md` (a template demonstrating fragments, layouts, and animations) and a sample image inside an `assets/` folder.

### 2. Compile your slides
To compile your Markdown file, pass it directly to the command:
```bash
show-off slides.md
```
This generates `slides.html` in the same directory. 

If you want to save it with a custom name, pass the output path as the second argument:
```bash
show-off slides.md output.html
```

*(You can also use `show-off make slides.md output.html` if you prefer the sub-command syntax).*

---

## Frontmatter Settings

You can customize the slideshow using the YAML block at the top of your Markdown file:

```yaml
---
title: "My Presentation"
theme: dracula               # reveal.js theme (dracula, moon, night, solarized, etc.)
transition: slide            # transition effect (slide, fade, zoom)
eyeCatchy: true              # set to false to fallback to plain reveal.js styling
revealConfig:
  controls: true             # show navigation arrows
  progress: true             # show bottom progress bar
  slideNumber: true          # show slide page numbers
css: |                       # write inline CSS styles to override anything
  .reveal h2 {
    color: #38bdf8 !important;
  }
---
```
