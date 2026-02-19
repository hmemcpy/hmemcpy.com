# hmemcpy.com

Source for my blog at [hmemcpy.com](https://hmemcpy.com) — a professional blog covering software engineering, functional programming, Scala, Haskell, and related topics.

## Stack

- **[Zola](https://www.getzola.org/)** (v0.22+) — static site generator
- **next-gemini** — custom theme (see `themes/next-gemini/`) inspired by the [NexT](https://theme-next.js.org/) Hexo theme's Gemini layout
- **GitHub Pages** — hosting, deployed via GitHub Actions on every push to `master`

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

## Theme — next-gemini

A custom Zola theme in `themes/next-gemini/` built from scratch to replicate the NexT Gemini layout:

| Feature | Details |
|---|---|
| Layout | Fixed dark sidebar (240px) + full-height scrollable content area |
| Fonts | [Gloria Hallelujah](https://fonts.google.com/specimen/Gloria+Hallelujah) (title), [Lato](https://fonts.google.com/specimen/Lato) (body), [JetBrains Mono](https://www.jetbrains.com/lp/mono/) (code) |
| Icons | [Font Awesome 6](https://fontawesome.com/) |
| Syntax highlighting | Nord theme (built into Zola) |
| Content width | Capped at 860px for comfortable line lengths |
| Prose width | 72ch max on single post pages |
| Mobile | Responsive with hamburger nav toggle |

### Theme structure

```
themes/next-gemini/
├── sass/
│   ├── next-gemini.scss   # entry point (imports all partials)
│   ├── _variables.scss    # colours, fonts, spacing tokens
│   ├── _base.scss         # reset and global element styles
│   ├── _layout.scss       # two-column flex layout
│   ├── _header.scss       # sidebar brand area
│   ├── _menu.scss         # nav items with orange active indicator
│   ├── _sidebar.scss      # author, avatar, social icon buttons
│   ├── _post.scss         # post cards, body typography, blockquote
│   ├── _pagination.scss   # prev/next and page links
│   ├── _highlight.scss    # code block chrome
│   ├── _footer.scss       # footer bar
│   ├── _responsive.scss   # mobile + tablet breakpoints
│   └── _custom.scss       # site-specific overrides
└── templates/
    ├── base.html           # master layout (head, sidebar, main, footer)
    ├── index.html          # paginated post list
    ├── page.html           # single post
    ├── section.html        # archive page
    ├── macros.html         # post_card, pagination, post_nav macros
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
