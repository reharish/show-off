import argparse
import base64
import json
import mimetypes
import os
import re
import sys
from pathlib import Path

# Base HTML Template for Reveal.js slideshows
HTML_TEMPLATE = """<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{title}</title>
    <style>
        {reset_css}
        {reveal_css}
        {theme_css}
        {highlight_css}
        {eye_catchy_css}
        {custom_css}
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
            <section data-markdown>
                <textarea data-template>
{markdown_content}
                </textarea>
            </section>
        </div>
    </div>
    <script>
        {reveal_js}
        {notes_js}
        {markdown_js}
        {highlight_js}
    </script>
    <script>
        const config = {config_json};
        config.plugins = [ RevealMarkdown, RevealHighlight, RevealNotes ];
        Reveal.initialize(config);
    </script>
</body>
</html>
"""

# show-off Premium Theme Enhancements (applied by default)
EYE_CATCHY_CSS = """
/* Font Imports */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

.reveal {
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
}

/* Radial Glow Background */
.reveal-viewport {
    background: radial-gradient(circle at center, #1e1b4b 0%, #0f172a 100%) !important;
}

/* Sleek Headings */
.reveal h1, .reveal h2, .reveal h3, .reveal h4, .reveal h5, .reveal h6 {
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
    font-weight: 800 !important;
    text-transform: none !important;
    letter-spacing: -0.03em !important;
    text-shadow: 0 10px 30px rgba(99, 102, 241, 0.15) !important;
}

.reveal h1 {
    font-size: 2.85em !important;
    background: linear-gradient(135deg, #c084fc 0%, #818cf8 50%, #60a5fa 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    padding-bottom: 0.15em !important;
}

.reveal h2 {
    font-size: 1.9em !important;
    color: #f1f5f9 !important;
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.reveal h3 {
    color: #cbd5e1 !important;
}

/* macOS Terminal Window Code Blocks styling */
.reveal pre {
    background: #0d1117 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.5) !important;
    padding: 16px 20px 20px 20px !important;
    margin: 24px auto !important;
    overflow: visible !important;
    position: relative !important;
    max-width: 90% !important;
}

.reveal pre::before {
    content: "";
    display: block;
    height: 12px;
    width: 48px;
    background-image: 
        radial-gradient(circle at 6px, #ff5f56 4px, transparent 5px),
        radial-gradient(circle at 18px, #ffbd2e 4px, transparent 5px),
        radial-gradient(circle at 30px, #27c93f 4px, transparent 5px);
    background-size: 36px 12px;
    background-repeat: no-repeat;
    margin-bottom: 12px;
    opacity: 0.85;
}

.reveal code {
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    font-size: 0.85em !important;
    line-height: 1.6 !important;
    background: transparent !important;
}

/* Bullet points customized with indigo symbol */
.reveal ul {
    list-style-type: none !important;
    padding-left: 0 !important;
}

.reveal ul li::before {
    content: "✦ " !important;
    color: #818cf8 !important;
    margin-right: 8px !important;
    display: inline-block !important;
}

.reveal p, .reveal li {
    font-size: 0.95em !important;
    line-height: 1.5 !important;
    color: #cbd5e1 !important;
}

/* Flexbox and Layout columns setup */
.reveal div[style*="display: flex"] {
    align-items: stretch !important;
}

/* Glassmorphism Cards styling */
.reveal div[style*="background"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.reveal div[style*="background"]:hover {
    background: rgba(255, 255, 255, 0.04) !important;
    border-color: rgba(129, 140, 248, 0.25) !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 20px 40px rgba(129, 140, 248, 0.08) !important;
}

/* Premium links */
.reveal a {
    color: #818cf8 !important;
    text-decoration: none !important;
    border-bottom: 1px dashed rgba(129, 140, 248, 0.3) !important;
    transition: all 0.2s ease !important;
}

.reveal a:hover {
    color: #a5b4fc !important;
    border-bottom: 1px solid #a5b4fc !important;
}
"""

# Default slides.md Template
DEFAULT_SLIDES_MD = """---
title: "show-off Presentation"
theme: dracula
transition: slide
revealConfig:
  hash: true
  controls: true
  progress: true
  slideNumber: true
---

# show-off 🚀
### HTML & CSS Presentations Made Easy

---

<!-- .slide: data-background-image="assets/sample.svg" -->

---

## Reveal.js Features

- **Auto-Animate**: Smooth transitions between elements
- **Fragments**: Reveal bullets step-by-step
- **Backgrounds**: Colors, Images, Videos, or Iframes
- **Custom CSS**: Style it exactly how you want

---

## Fragments in Action

- Step 1: Brainstorming <!-- .element: class="fragment" -->
- Step 2: Write Markdown <!-- .element: class="fragment" -->
- Step 3: Run `show-off make` <!-- .element: class="fragment" -->
- Step 4: Show off! 🎉 <!-- .element: class="fragment" -->

---

<!-- .slide: data-auto-animate -->
## Auto-Animate Demo

```javascript
const showOff = {
  easy: true,
  beautiful: true
};
```

---

<!-- .slide: data-auto-animate -->
## Auto-Animate Demo

```javascript
const showOff = {
  easy: true,
  beautiful: true,
  speed: "lightning fast",
  standalone: "yes, 100%!"
};
```

---

## Two Column Layout

<div style="display: flex; gap: 20px;">
  <div style="flex: 1; text-align: left; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px;">
    <h3>Left Column</h3>
    <p>Using standard HTML and inline styles, you can create any grid or column layout easily.</p>
  </div>
  <div style="flex: 1; text-align: left; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px;">
    <h3>Right Column</h3>
    <p>No complex markdown tricks required. Just write HTML when you need advanced structures.</p>
  </div>
</div>

---

## Speaker Notes

Press **`S`** on your keyboard to open the Speaker View.

<aside class="notes">
Here are some speaker notes. You can see them only in the speaker view window.
Perfect for keeping your thoughts organized!
</aside>

---

# Thank You! 💖
Go build something eye-catchy.
"""

# Default assets/sample.svg Illustration
DEFAULT_SAMPLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="100%" height="100%">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4f46e5;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ec4899;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="#0f172a" rx="20"/>
  <circle cx="400" cy="300" r="150" fill="url(#grad1)" opacity="0.8" />
  <text x="400" y="320" font-family="system-ui, sans-serif" font-size="48" font-weight="bold" fill="#ffffff" text-anchor="middle">show-off</text>
  <text x="400" y="370" font-family="system-ui, sans-serif" font-size="20" fill="#cbd5e1" text-anchor="middle">HTML &amp; CSS Presentations</text>
</svg>
"""


def parse_yaml(yaml_text):
    import yaml
    try:
        return yaml.safe_load(yaml_text) or {}
    except Exception as e:
        print(f"Warning: Failed to parse YAML frontmatter: {e}", file=sys.stderr)
        return {}


def file_to_base64_data_url(file_path):
    try:
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if not mime_type:
            ext = file_path.suffix.lower()
            if ext == '.svg':
                mime_type = 'image/svg+xml'
            elif ext == '.mp4':
                mime_type = 'video/mp4'
            elif ext == '.webp':
                mime_type = 'image/webp'
            else:
                mime_type = 'application/octet-stream'
                
        with open(file_path, 'rb') as f:
            data = f.read()
            encoded = base64.b64encode(data).decode('utf-8')
            return f"data:{mime_type};base64,{encoded}"
    except Exception as e:
        print(f"Warning: Could not base64 encode file {file_path}: {e}", file=sys.stderr)
        return None


def inline_assets(markdown_content, base_dir):
    base_dir = Path(base_dir)
    
    # 1. Replace Markdown images: ![alt](path "optional title")
    def replace_markdown_image(match):
        alt = match.group(1)
        url_part = match.group(2).strip()
        parts = re.split(r'\s+', url_part, maxsplit=1)
        url = parts[0].strip('"\'')
        title_part = f" {parts[1]}" if len(parts) > 1 else ""
        
        if url.startswith(('http://', 'https://', 'data:')):
            return match.group(0)
            
        file_path = (base_dir / url).resolve()
        if file_path.exists() and file_path.is_file():
            base64_url = file_to_base64_data_url(file_path)
            if base64_url:
                return f"![{alt}]({base64_url}{title_part})"
        return match.group(0)

    # 2. Replace HTML images: <img src="path" ...>
    def replace_html_img(match):
        full_tag = match.group(0)
        url = match.group(1)
        
        if url.startswith(('http://', 'https://', 'data:')):
            return full_tag
            
        file_path = (base_dir / url).resolve()
        if file_path.exists() and file_path.is_file():
            base64_url = file_to_base64_data_url(file_path)
            if base64_url:
                return full_tag.replace(url, base64_url)
        return full_tag

    # 3. Replace Reveal.js slide backgrounds: data-background-image="path"
    def replace_bg(match):
        full_attr = match.group(0)
        bg_type = match.group(1)  # image or video
        url = match.group(2)
        
        if url.startswith(('http://', 'https://', 'data:')):
            return full_attr
            
        file_path = (base_dir / url).resolve()
        if file_path.exists() and file_path.is_file():
            if bg_type == 'video' and file_path.stat().st_size > 10 * 1024 * 1024:
                print(f"Warning: Large background video '{url}' ({file_path.stat().st_size / (1024*1024):.1f} MB) will be inlined. This could slow down browser rendering.", file=sys.stderr)
            base64_url = file_to_base64_data_url(file_path)
            if base64_url:
                return f'data-background-{bg_type}="{base64_url}"'
        return full_attr

    # Run replacements
    markdown_image_pattern = re.compile(r'!\[(.*?)\]\(([^)]+)\)')
    content = markdown_image_pattern.sub(replace_markdown_image, markdown_content)
    
    html_img_pattern = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>')
    content = html_img_pattern.sub(replace_html_img, content)
    
    bg_pattern = re.compile(r'data-background-(image|video)=["\']([^"\']+)["\']')
    content = bg_pattern.sub(replace_bg, content)
    
    return content


def process_css(css_content):
    # Remove relative @import statement referencing fonts to avoid 404 console errors when offline
    css_content = re.sub(r'@import\s+url\([\'"]?.*?fonts/.*?[\'"]?\);', '', css_content)
    return css_content


def run_init(directory):
    target_dir = Path(directory).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    
    slides_file = target_dir / 'slides.md'
    assets_dir = target_dir / 'assets'
    sample_svg = assets_dir / 'sample.svg'
    
    # Create templates if they do not exist
    if not slides_file.exists():
        slides_file.write_text(DEFAULT_SLIDES_MD, encoding='utf-8')
        print(f"Created template: {slides_file.relative_to(Path.cwd()) if slides_file.is_relative_to(Path.cwd()) else slides_file}")
    else:
        print(f"Slides file already exists: {slides_file}")
        
    assets_dir.mkdir(exist_ok=True)
    if not sample_svg.exists():
        sample_svg.write_text(DEFAULT_SAMPLE_SVG, encoding='utf-8')
        print(f"Created template asset: {sample_svg.relative_to(Path.cwd()) if sample_svg.is_relative_to(Path.cwd()) else sample_svg}")
        
    print("\nInitialization complete! To compile your presentation, run:\n  show-off make")


def run_make(input_path, output_path):
    input_file = Path(input_path).resolve()
    output_file = Path(output_path).resolve()
    
    if not input_file.exists():
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
        
    # Find package directory where Reveal.js assets are stored
    pkg_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    dist_dir = pkg_dir / 'dist'
    plugin_dir = pkg_dir / 'plugin'
    
    if not dist_dir.exists() or not plugin_dir.exists():
        print(f"Error: Reveal.js resources not found inside the show-off installation package.", file=sys.stderr)
        sys.exit(1)
        
    # Read Markdown and parse Frontmatter
    content = input_file.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    
    if match:
        frontmatter_text = match.group(1)
        markdown_content = match.group(2)
        metadata = parse_yaml(frontmatter_text)
    else:
        metadata = {}
        markdown_content = content
        
    # Inline local images and videos referenced in Markdown
    base_dir = input_file.parent
    markdown_content = inline_assets(markdown_content, base_dir)
    
    # Escape closing textarea tags
    markdown_content = markdown_content.replace('</textarea>', '&lt;/textarea&gt;')
    
    # Load Reveal.js Core Styles
    try:
        reset_css = (dist_dir / 'reset.css').read_text(encoding='utf-8')
        reveal_css = (dist_dir / 'reveal.css').read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading reveal core styles: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Load Theme Style
    theme = metadata.get('theme', 'black')
    theme_file = dist_dir / 'theme' / f"{theme}.css"
    if not theme_file.exists():
        print(f"Warning: Theme '{theme}' not found. Falling back to 'black' theme.", file=sys.stderr)
        theme_file = dist_dir / 'theme' / "black.css"
        
    try:
        theme_css = theme_file.read_text(encoding='utf-8')
        theme_css = process_css(theme_css)
    except Exception as e:
        print(f"Error reading theme styles: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Load Highlight Style
    hl_theme = metadata.get('highlightTheme', 'monokai')
    hl_theme_file = plugin_dir / 'highlight' / f"{hl_theme}.css"
    if not hl_theme_file.exists():
        hl_theme_file = plugin_dir / 'highlight' / "monokai.css"
        
    try:
        highlight_css = hl_theme_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading highlighting styles: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Load Javascript Assets
    try:
        reveal_js = (dist_dir / 'reveal.js').read_text(encoding='utf-8')
        notes_js = (plugin_dir / 'notes' / 'notes.js').read_text(encoding='utf-8')
        markdown_js = (plugin_dir / 'markdown' / 'markdown.js').read_text(encoding='utf-8')
        highlight_js = (plugin_dir / 'highlight' / 'highlight.js').read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading javascript resources: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Build configuration object
    reveal_config = {
        'hash': True
    }
    
    # Inject transition if defined in frontmatter
    if 'transition' in metadata:
        reveal_config['transition'] = metadata['transition']
        
    # Merge custom revealConfig
    user_config = metadata.get('revealConfig', {})
    if isinstance(user_config, dict):
        user_config.pop('plugins', None)  # Ensure plugins cannot be overridden as strings
        reveal_config.update(user_config)
        
    config_json = json.dumps(reveal_config, indent=2)
    custom_css = metadata.get('css', '')
    title = metadata.get('title', 'show-off Presentation')
    
    # Load Eye Catchy Theme Override (enabled by default)
    eye_catchy_enabled = metadata.get('eyeCatchy', True)
    eye_catchy_css = EYE_CATCHY_CSS if eye_catchy_enabled else ""

    # Generate standalone HTML content
    html_content = HTML_TEMPLATE.format(
        title=title,
        reset_css=reset_css,
        reveal_css=reveal_css,
        theme_css=theme_css,
        highlight_css=highlight_css,
        eye_catchy_css=eye_catchy_css,
        custom_css=custom_css,
        markdown_content=markdown_content,
        reveal_js=reveal_js,
        notes_js=notes_js,
        markdown_js=markdown_js,
        highlight_js=highlight_js,
        config_json=config_json
    )
    
    # Save the output file
    try:
        output_file.write_text(html_content, encoding='utf-8')
        print(f"Compiled successfully: {output_file.relative_to(Path.cwd()) if output_file.is_relative_to(Path.cwd()) else output_file}")
    except Exception as e:
        print(f"Error writing output HTML file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    # Direct Markdown compilation support:
    # If the first argument is not init or make, and looks like a markdown file or an existing file path, compile it directly.
    if len(sys.argv) > 1 and sys.argv[1] not in ["init", "make", "-h", "--help"]:
        arg1 = sys.argv[1]
        arg1_path = Path(arg1)
        if arg1_path.suffix.lower() == '.md' or arg1_path.exists():
            input_file = arg1
            if len(sys.argv) > 2:
                output_file = sys.argv[2]
            else:
                output_file = str(arg1_path.with_suffix('.html'))
            run_make(input_file, output_file)
            return

    parser = argparse.ArgumentParser(description="show-off: Presentation tool using Markdown, HTML, and CSS")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")
    
    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a presentation template in the target directory")
    init_parser.add_argument("directory", nargs="?", default=".", help="Directory to initialize (default: current directory)")
    
    # make command
    make_parser = subparsers.add_parser("make", help="Compile slides.md into a standalone slides.html")
    make_parser.add_argument("input", nargs="?", default="slides.md", help="Input Markdown file (default: slides.md)")
    make_parser.add_argument("output", nargs="?", default="slides.html", help="Output HTML file (default: slides.html)")
    
    args = parser.parse_args()
    
    if args.command == "init":
        run_init(args.directory)
    elif args.command == "make":
        run_make(args.input, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
