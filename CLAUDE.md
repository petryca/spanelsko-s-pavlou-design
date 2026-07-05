# Španělsko s Pavlou — Project Context

Personal brand website for Pavla, a Czech relocation consultant helping Czechs move to Spain.
Czech-only content. No frameworks, no build tools — pure HTML + CSS + vanilla JS.

## File structure

```
index.html          Homepage
sluzby.html         Services page (3 tiers)
o-pavle.html        About Pavla
kontakt.html        Contact form + WhatsApp
clanky.html         Blog listing
ebook.html          E-book landing page
articles/           This folder will contain articles and associated images
style.css           All styles (single shared stylesheet)
script.js           Mobile nav toggle + scroll fade-in animations
images/             All production images (see below)
```

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
`.post-row` — blog listing rows  
`.article`, `.article__hero`, `.article__body` — single article layout  

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

## Articles path note

The `articles/` subdirectory uses relative paths with `../` prefix:
- `../style.css`, `../script.js`
- `../images/logo.png`, `../images/logo-rev.png`
- All nav links prefixed with `../`
