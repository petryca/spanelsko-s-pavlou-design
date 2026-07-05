#!/usr/bin/env python3
"""Rebuild the story card grid in clanky.html from tools/manifest.json."""
import json, os, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
manifest = json.load(open(os.path.join(ROOT, "tools", "manifest.json")))
stories = [a for a in manifest if a["cat"] != "lgbt-spanelsko"]

# Fallback icons for cards without a thumbnail — inline SVG from Lucide (lucide.dev, ISC).
CATEGORY_ICONS = {
    "barcelona": '<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>',
    "spolecnost": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "svatky-a-slavnosti": '<path d="M5.8 11.3 2 22l10.7-3.79"/><path d="M4 3h.01"/><path d="M22 8h.01"/><path d="M15 2h.01"/><path d="M22 20h.01"/><path d="m22 2-2.24.75a2.9 2.9 0 0 0-1.96 3.12v0c.1.86-.57 1.63-1.45 1.63h-.38c-.86 0-1.6.6-1.76 1.44L14 10"/><path d="m22 13-.82-.33c-.86-.34-1.82.2-1.98 1.11v0c-.11.7-.72 1.22-1.43 1.22H17"/><path d="m11 2 .33.82c.34.86-.2 1.82-1.11 1.98v0C9.52 4.9 9 5.52 9 6.23V7"/><path d="M11 13c1.93 1.93 2.83 4.17 2 5-.83.83-3.07-.07-5-2-1.93-1.93-2.83-4.17-2-5 .83-.83 3.07.07 5 2Z"/>',
    "dobroty-a-restaurace": '<path d="M8 22h8"/><path d="M7 10h10"/><path d="M12 15v7"/><path d="M12 15a5 5 0 0 0 5-5c0-2-.5-4-2-8H9c-1.5 4-2 6-2 8a5 5 0 0 0 5 5Z"/>',
    "historie": '<path d="M19 17V5a2 2 0 0 0-2-2H4"/><path d="M8 21h12a2 2 0 0 0 2-2v-1a1 1 0 0 0-1-1H11a1 1 0 0 0-1 1v1a2 2 0 1 1-4 0V5a2 2 0 1 0-4 0v2a1 1 0 0 0 1 1h3"/>',
    "mista": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "bydleni": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "spanelstina": '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
}
DEFAULT_ICON = '<path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M18 14h-8"/><path d="M15 18h-5"/><path d="M10 6h8v4h-8V6Z"/>'

def icon_svg(cat):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
            f'{CATEGORY_ICONS.get(cat, DEFAULT_ICON)}</svg>')

cards = []
for a in stories:
    t = html.escape(a["title"], quote=False)
    if a["thumb"]:
        media = f'<div class="story-card__media"><img src="{a["thumb"]}" alt="{html.escape(a["title"])}" loading="lazy"></div>'
    else:
        media = f'<div class="story-card__fallback" aria-hidden="true">{icon_svg(a["cat"])}</div>'
    cards.append(f'''<a class="story-card" href="blog/{a["slug"]}.html" data-cat="{a["cat"]}">
            {media}
            <div class="story-card__body">
              <span class="post-row__cat">{a["label"]}</span>
              <h3 class="story-card__title">{t}</h3>
              <p class="story-card__meta">{a["read"]} min čtení</p>
            </div>
          </a>''')

path = os.path.join(ROOT, "clanky.html")
doc = open(path).read()
new_grid = '<div class="story-grid">\n          ' + "\n          ".join(cards) + "\n        </div>"
doc, count = re.subn(r'<div class="story-grid">.*?\n        </div>', new_grid, doc, count=1, flags=re.S)
assert count == 1, "story-grid block not found"
open(path, "w").write(doc)
print(f"story grid rebuilt: {len(cards)} cards")
