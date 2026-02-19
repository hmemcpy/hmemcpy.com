# hmemcpy.com

Source for my blog at [hmemcpy.com](https://hmemcpy.com) — a professional blog covering software engineering, functional programming, Scala, Haskell, and related topics.

## Stack

- **[Zola](https://www.getzola.org/)** (v0.19.2+) — static site generator
- **[linen](https://github.com/hmemcpy/zola-theme-linen)** — custom theme (see `themes/linen/`)
- **GitHub Pages** — hosting, deployed via GitHub Actions on every push to `main`

## Local development

Install Zola ([brew](https://brew.sh/) on macOS):

```bash
brew install zola
```

Serve locally with live reload:

```bash
zola serve
```

The site is available at `http://127.0.0.1:1111`.

## Theme — linen

A minimal, single-column reading theme in `themes/linen/`. Named for its warm off-white background (`#faf9f7`).

The theme is also published as a standalone Zola theme at **[hmemcpy/zola-theme-linen](https://github.com/hmemcpy/zola-theme-linen)**.

| Feature | Details |
|---|---|
| Layout | Sticky top nav bar + centered single column (860px max) |
| Fonts | [Gloria Hallelujah](https://fonts.google.com/specimen/Gloria+Hallelujah) (site title), [Lora](https://fonts.google.com/specimen/Lora) (body serif), [JetBrains Mono](https://www.jetbrains.com/lp/mono/) (code) |
| Icons | [Font Awesome 6](https://fontawesome.com/) |
| Palette | Warm off-white `#faf9f7` bg · near-black `#1a1a1a` text · orange `#fc6423` for links/accents |
| Syntax highlighting | Nord theme (built into Zola), with language label header |
| Post list | Clean date-prefixed list (no cards) |
| Mobile | Responsive with hamburger nav dropdown |

### Theme structure

```
themes/linen/
├── sass/
│   ├── linen.scss         # entry point (imports all partials)
│   ├── _variables.scss    # colours, fonts, spacing tokens
│   ├── _base.scss         # reset and global element styles
│   ├── _layout.scss       # single-column layout, headband
│   ├── _header.scss       # sticky top nav bar
│   ├── _menu.scss         # horizontal nav items
│   ├── _sidebar.scss      # (stub — sidebar removed in redesign)
│   ├── _post.scss         # post list, single post typography
│   ├── _pagination.scss   # page number links
│   ├── _highlight.scss    # code block chrome and language label
│   ├── _footer.scss       # footer with social icons
│   ├── _responsive.scss   # mobile + tablet breakpoints
│   └── _custom.scss       # site-specific overrides
└── templates/
    ├── base.html           # master layout (head, top nav, main, footer)
    ├── index.html          # paginated post list
    ├── page.html           # single post
    ├── section.html        # archive page
    ├── macros.html         # pagination, post_nav macros
    ├── 404.html
    ├── tags/               # tag list + single-tag pages
    └── categories/         # category list + single-category pages
```

### Content structure

Posts live in `content/posts/`. Posts with images use [page bundles](https://www.getzola.org/documentation/content/page/#asset-colocation):

```
content/posts/my-post/
├── index.md        # post content
├── screenshot.png  # colocated image
└── diagram.svg
```

Images are referenced in shortcodes as `{{ image(path="screenshot.png") }}` and resolve relative to the page permalink.

Custom shortcodes are in `templates/shortcodes/`:
- `image(path, alt, caption)` — figure with optional caption
- `asset_img(path, alt, caption)` — alias for image
- `blockquote(author, source)` — styled blockquote with attribution

Static pages (e.g. `content/talks-i-liked.md`) use `extra.skip_in_feed = true` in their frontmatter to be excluded from the post feed while still being routable.

## Content license

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
