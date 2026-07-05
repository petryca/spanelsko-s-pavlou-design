# Španělsko s Pavlou — Project Context

Personal brand website for Pavla, a Czech relocation consultant helping Czechs move to Spain.
Czech-only content. No frameworks, no build tools — pure HTML + CSS + vanilla JS.

## File structure

```
index.html          Homepage
sluzby.html         Services page (3 tiers)
o-pavle.html        About Pavla
kontakt.html        Contact form + WhatsApp
clanky.html         Content hub: practical guides (post rows) + story grid with category filter + LGBT teaser
ebook.html          E-book landing page
lgbt-spanelsko.html Landing page listing the 6 LGBT travel guides
articles/           5 practical guides (conversion content) + their hero JPGs; CTA → e-book/consultation
blog/               55 story articles by Pavla (flat, generated from blog-md/); soft CTA → FB group/e-book
blog/images/        Compressed JPGs for blog articles (<slug>-N.jpg, max 1200px wide)
articles-md/        Markdown + PNG sources for articles/ (not published)
blog-md/            Markdown + image sources for blog/, one folder per category (not published)
style.css           All styles (single shared stylesheet)
script.js           Mobile nav toggle + scroll fade-in + story category filter
images/             All production images (see below)
```

## Content architecture (two content lines)

The site deliberately separates two kinds of content — keep them separate:

1. **Practical guides** (`articles/`, sourced from `articles-md/`) — bottom-of-funnel
   conversion content for people actively planning a move. Listed as large post rows at the
   top of clanky.html. Each ends with a **hard CTA** (`.article__cta`): e-book + consultation.
2. **Stories "Španělsko očima Pavly"** (`blog/`, sourced from `blog-md/`) — top-of-funnel
   personal essays on culture, festivals, food, history. Listed as a filterable card grid
   (`.story-grid` + `.filter-bar` chips) below the guides on clanky.html. Each ends with a
   **soft CTA**: Facebook group + e-book. Never put the hard sales CTA on stories.
   The 6 LGBT travel guides are a special series: they live in `blog/` too but are listed
   only on `lgbt-spanelsko.html` (linked from a teaser section on clanky.html), not in the grid.

Shared conventions: no publication dates anywhere — only "X min čtení" (~200 words/min);
category chip above the title; images compressed to JPG quality ~62, max 1200px wide.

## Publishing workflow — adding a new article

**New story (blog):**
1. Drop the markdown into `blog-md/<category>/<slug>.md` — H1 = title, first paragraph = excerpt/meta
   description. Images go in `blog-md/<category>/<slug>-media/` and are referenced inline with
   relative paths. Valid categories (folder → chip label): barcelona → Barcelona,
   spolecnost → Společnost, svatky-a-slavnosti → Svátky a slavnosti,
   dobroty-a-restaurace → Dobroty a restaurace, historie → Historie, mista → Místa,
   bydleni → Bydlení, spanelstina → Španělština, lgbt-spanelsko → LGBT průvodce.
   A new category = add it to `CATEGORIES` in `tools/gen_blog.py` + a new chip in clanky.html.
2. Run `python3 tools/gen_blog.py` (needs `pip install markdown`; uses macOS `sips` for images).
   It regenerates all `blog/*.html`, converts/compresses images to `blog/images/<slug>-N.jpg`,
   fixes docx artifacts (`--` → `–`, tiny inline images → 🙂), and writes `tools/manifest.json`
   (title/excerpt/read-time/thumbnail per article — useful for rebuilding the clanky.html grid).
3. Add the story card to the grid in clanky.html by hand (copy an existing `.story-card`,
   set `data-cat`, href `blog/<slug>.html`, thumbnail = first image `blog/images/<slug>-1.jpg`,
   or `.story-card__fallback` with the title's first letter if the article has no images).
   For an LGBT guide, add a `.post-row--simple` row to lgbt-spanelsko.html instead.
4. Verify: no dead links/images, then commit.

**New practical guide (articles):**
1. Markdown + feature image (PNG) into `articles-md/` (flat, ASCII slug).
2. Convert image: `sips --resampleWidth 1200 -s format jpeg -s formatOptions 62` → `articles/<slug>.jpg`.
3. Create `articles/<slug>.html` by copying an existing guide page (keep the `.article__cta` block,
   tailor its headline to the topic; link the closing e-book mention to `../ebook.html`).
4. Add a `.post-row` to the practical section of clanky.html (excerpt + "X min čtení", no date).

The generator is idempotent — re-running it is safe (images are cached by filename, pages are
overwritten). Hand edits to `blog/*.html` will be lost on regeneration; edit the markdown source.

## Images

| File | Usage |
|------|-------|
| `header.jpg` | Hero background on index.html and o-pavle.html (horizontally flipped from original) |
| `cortado.jpg` | Real estate section on index.html and sluzby.html |
| `pavla.jpg` | Pavla bio section on index.html and o-pavle.html |
| `tapas.jpg` | Mission section on o-pavle.html |
| `beach.jpg` | Vision section on o-pavle.html |
| `ebook.jpg` | E-book cover on index.html and ebook.html |
| `logo.png` | Header logo (44×44) on all pages |
| `logo-rev.png` | Footer logo (44×44) on all pages |

## Design tokens (style.css :root)

```css
--ink:        #33271b   /* headings */
--ink-deep:   #271d13   /* footer background */
--terra:      #c0532f   /* terracotta — primary accent, CTAs */
--terra-dark: #a03f1f   /* hover state */
--terra-soft: #f7e9e0   /* pale terracotta tint */
--gold:       #d9a441   /* ochre — stars, small accents */
--text:       #5b5245   /* body copy */
--muted:      #8a8071
--line:       #eae2d6
--bg:         #ffffff
--bg-alt:     #f9f5ee   /* warm sand — alternate sections */
```

Fonts: **Inter** (sans-serif) + **Lora** (serif headings) via Google Fonts.

## Layout conventions

- `.container` — max-width 1180px, `padding-inline: 24px`
- `.container--narrow` — max-width 780px (article pages)
- `.cta-band__inner` uses `padding-block: 60px` (not shorthand `padding`, which would zero the horizontal padding inherited from `.container`)
- Hamburger nav breakpoint: `@media (max-width: 1080px)`
- Scroll animations: IntersectionObserver adds `.visible` to `.fade-in` elements
- Section backgrounds alternate between `--bg` (white) and `--bg-alt` (warm sand) — maintain this pattern when inserting new sections

## BEM-style class naming

`.tier`, `.tier--featured` — service pricing cards  
`.pain-grid` — 6-card pain points grid  
`.feature`, `.feature--reverse` — alternating image+text sections  
`.post-row`, `.post-row--simple` — blog listing rows (simple = no media column)  
`.article`, `.article__hero`, `.article__body`, `.article__cta` — single article layout  
`.story-card`, `.story-grid`, `.filter-bar`, `.chip` — story card grid with category filter  
`.bio`, `.bio__aside`, `.bio__photo` — circular portrait + caption (o-pavle.html, index.html)  

## Services structure (sluzby.html)

Three tiers only — do not add a 4th:
1. **Základní konzultace** — od 2 500 Kč (fixed price)
2. **Kompletní podpora** — na míru (featured/highlighted tier)
3. **Osobní concierge** — na míru (premium)

Real estate is woven into tiers 2 and 3 as bullets, plus a standalone feature section below the tiers. A "router" sentence directs property-only clients to tier 1.

## Contact & integrations

- **Formspree** form action: `https://formspree.io/f/mpqnkqro`
- **WhatsApp**: `https://wa.me/420776544156`
- **Facebook group**: `https://www.facebook.com/groups/1294335829405014`
- **LinkedIn**: `https://www.linkedin.com/in/pavla-vovsova-kulhankova-76503a37`
- **E-book** (Stripe buy link): on ebook.html
- Contact email `info@spanelskospavlou.cz` — verify this is the live address before going live

## Pages not yet built

- Ochrana údajů (GDPR) — footer link points to `#`
- Obchodní podmínky — footer link points to `#`

## Subdirectory path note

The `articles/` and `blog/` subdirectories use relative paths with `../` prefix:
- `../style.css`, `../script.js`
- `../images/logo.png`, `../images/logo-rev.png`
- All nav links prefixed with `../`
- Blog article images are referenced as `images/<slug>-N.jpg` (i.e. `blog/images/` relative to the page)
- Back link: blog stories → `../clanky.html`, LGBT guides → `../lgbt-spanelsko.html`
