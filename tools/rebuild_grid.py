#!/usr/bin/env python3
"""Rebuild the story card grid in clanky.html from tools/manifest.json."""
import json, os, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
manifest = json.load(open(os.path.join(ROOT, "tools", "manifest.json")))
stories = [a for a in manifest if a["cat"] != "lgbt-spanelsko"]

cards = []
for a in stories:
    t = html.escape(a["title"], quote=False)
    if a["thumb"]:
        media = f'<div class="story-card__media"><img src="{a["thumb"]}" alt="{html.escape(a["title"])}" loading="lazy"></div>'
    else:
        media = f'<div class="story-card__fallback" aria-hidden="true"><span>{a["title"][0].upper()}</span></div>'
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
