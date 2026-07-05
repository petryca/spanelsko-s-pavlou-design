#!/usr/bin/env python3
"""Generate blog article pages from blog-md/ markdown sources."""
import re, os, glob, html, json, math, subprocess, unicodedata

ROOT = "/Users/david/Code/spanelsko-s-pavlou-design"
OUT_HTML = os.path.join(ROOT, "blog")
OUT_IMG = os.path.join(ROOT, "blog", "images")
SCRATCH = os.path.dirname(os.path.abspath(__file__))

import markdown as md_lib

CATEGORIES = {  # folder -> (label, order)
    "barcelona": ("Barcelona", 1),
    "spolecnost": ("Společnost", 2),
    "svatky-a-slavnosti": ("Svátky a slavnosti", 3),
    "dobroty-a-restaurace": ("Dobroty a restaurace", 4),
    "historie": ("Historie", 5),
    "mista": ("Místa", 6),
    "bydleni": ("Bydlení", 7),
    "spanelstina": ("Španělština", 8),
    "lgbt-spanelsko": ("LGBT průvodce", 9),
}

PAGE_TMPL = """<!DOCTYPE html>
<html lang="cs">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>@TITLE@ — Španělsko s Pavlou</title>
  <meta name="description" content="@DESC@">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
</head>
<body>

  <!-- Header -->
  <header class="header">
    <div class="container header__inner">
      <a href="../index.html" class="brand">
        <span class="brand__mark" aria-hidden="true">
          <img src="../images/logo.png" alt="" width="44" height="44">
        </span>
        Španělsko s Pavlou
      </a>
      <nav class="nav" id="nav">
        <button class="nav__toggle" aria-label="Otevřít menu" aria-expanded="false">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <div class="nav__links">
          <a href="../index.html" class="nav__link">Domů</a>
          <a href="../sluzby.html" class="nav__link">Služby</a>
          <a href="../o-pavle.html" class="nav__link">O Pavle</a>
          <a href="../clanky.html" class="nav__link is-active">Články</a>
          <a href="../kontakt.html" class="nav__link">Kontakt</a>
        </div>
        <a href="../kontakt.html" class="btn btn--primary">Nezávazná konzultace</a>
      </nav>
    </div>
  </header>

  <main>

    <article class="article">
      <div class="container container--narrow">
        <a href="@BACKURL@" class="article__back">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          @BACKLABEL@
        </a>
        <div class="article__meta">
          <span class="post-row__cat">@CAT@</span>
          @READ@ min čtení
        </div>
        <h1 class="article__title">@H1@</h1>
      </div>

      <div class="container container--narrow">
        <div class="article__body">
@BODY@
        </div>

        <!-- CTA -->
        <div class="article__cta">
          <h2>Chcete Španělsko nejen číst, ale zažít?</h2>
          <p>Přidejte se do facebookové komunity Čechů, kteří Španělsko milují, žijí v něm nebo se do něj chystají. A pokud přesun plánujete, e-book vás provede vším podstatným.</p>
          <a href="https://www.facebook.com/groups/1294335829405014" target="_blank" rel="noopener noreferrer" class="btn btn--light">Přidat se do FB skupiny</a>
          <a href="../ebook.html" class="btn btn--ghost-light">Prohlédnout e-book</a>
        </div>
      </div>
    </article>

  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer__top">
        <div class="footer__col footer__col--brand">
          <a href="../index.html" class="brand">
            <span class="brand__mark" aria-hidden="true">
          <img src="../images/logo-rev.png" alt="" width="44" height="44">
        </span>
            Španělsko s Pavlou
          </a>
          <p class="footer__about">Profesionální relokační služby pro Čechy, kteří se stěhují do Španělska. Osobní přístup, zkušenost a klid na duši.</p>
        </div>
        <div class="footer__col">
          <h4>Navigace</h4>
          <ul>
            <li><a href="../index.html">Domů</a></li>
            <li><a href="../sluzby.html">Služby</a></li>
            <li><a href="../o-pavle.html">O Pavle</a></li>
            <li><a href="../clanky.html">Články</a></li>
            <li><a href="../ebook.html">E-book</a></li>
          </ul>
        </div>
        <div class="footer__col">
          <h4>Právní</h4>
          <ul>
            <li><a href="../kontakt.html">Kontakt</a></li>
            <li><a href="#">Ochrana údajů</a></li>
            <li><a href="#">Obchodní podmínky</a></li>
          </ul>
        </div>
        <div class="footer__col">
          <h4>Kontakt</h4>
          <div class="footer__detail"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg><a href="mailto:info@spanelskospavlou.cz">info@spanelskospavlou.cz</a></div>
          <div class="footer__detail"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg><a href="tel:+420776544156">+420 776 544 156</a></div>
          <div class="footer__social">
            <a href="https://www.facebook.com/groups/1294335829405014" aria-label="Facebook" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
            <a href="https://www.linkedin.com/in/pavla-vovsov%C3%A1-kulh%C3%A1nkov%C3%A1-76503a37" aria-label="LinkedIn" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg></a>
          </div>
        </div>
      </div>
      <div class="footer__bottom">
        <span>&copy; 2026 Španělsko s Pavlou. Všechna práva vyhrazena.</span>
        <span>Pavla je relokační konzultantka pro Španělsko.</span>
      </div>
    </div>
  </footer>

  <script src="../script.js"></script>
</body>
</html>
"""

_dim_cache = {}
def img_dims(path):
    if path not in _dim_cache:
        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                             capture_output=True, text=True).stdout
        w = int(re.search(r"pixelWidth: (\d+)", out).group(1))
        h = int(re.search(r"pixelHeight: (\d+)", out).group(1))
        _dim_cache[path] = (w, h)
    return _dim_cache[path]

def convert_img(src, dest):
    w, _ = img_dims(src)
    args = ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "62"]
    if w > 1200:
        args += ["--resampleWidth", "1200"]
    args += [src, "--out", dest]
    subprocess.run(args, capture_output=True, check=True)

def strip_md(text):
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text.strip()

def truncate(text, limit):
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(",.;:–- ") + "…"

os.makedirs(OUT_IMG, exist_ok=True)
manifest = []

for f in sorted(glob.glob(os.path.join(ROOT, "blog-md", "*", "*.md"))):
    cat_key = os.path.basename(os.path.dirname(f))
    slug = os.path.basename(f)[:-3]
    label, order = CATEGORIES[cat_key]
    text = open(f).read()

    # title = first H1
    m = re.search(r"^# (.+)$", text, re.M)
    title = strip_md(m.group(1))
    text = text[:m.start()] + text[m.end():]

    # images: convert + rewrite refs
    n = 0
    thumb = None
    def repl_img(match):
        global n, thumb
        alt, path = match.group(1), match.group(2).strip()
        src = os.path.join(os.path.dirname(f), path)
        w, _ = img_dims(src)
        if w < 100:
            return "🙂"
        n += 1
        name = f"{slug}-{n}.jpg"
        dest = os.path.join(OUT_IMG, name)
        if not os.path.exists(dest):
            convert_img(src, dest)
        if thumb is None:
            thumb = f"blog/images/{name}"
        return f"![{alt}](images/{name})"
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl_img, text)

    # docx export artifact: "--" should be a dash (skip table separator lines)
    text = "\n".join(
        line if line.lstrip().startswith("|") or re.fullmatch(r"-{3,}", line.strip())
        else re.sub(r"(?<!-)--(?!-)", "–", line)
        for line in text.split("\n")
    )

    # excerpt: first real paragraph
    excerpt = ""
    for para in text.split("\n\n"):
        p = para.strip()
        if not p or p.startswith("#") or p.startswith("![") or p.startswith("|"):
            continue
        if re.fullmatch(r"\*[^*]+\*", p):  # italic-only subtitle
            continue
        excerpt = strip_md(p.replace("\n", " "))
        break

    words = len(strip_md(text).split())
    read = max(1, math.ceil(words / 200))

    # internal cross-links written as ../<category>/<slug>.html -> flat blog/
    text = re.sub(r"\]\(\.\./[a-z0-9-]+/([a-z0-9-]+\.html)\)", r"](\1)", text)

    body = md_lib.markdown(text, extensions=["tables"])
    body = body.replace("<img ", '<img loading="lazy" ')
    body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener noreferrer"', body)

    if cat_key == "lgbt-spanelsko":
        backurl, backlabel = "../lgbt-spanelsko.html", "Zpět na LGBT průvodce"
    else:
        backurl, backlabel = "../clanky.html", "Zpět na články"

    page = (PAGE_TMPL
        .replace("@TITLE@", html.escape(title))
        .replace("@DESC@", html.escape(truncate(excerpt, 155)))
        .replace("@CAT@", label)
        .replace("@READ@", str(read))
        .replace("@H1@", html.escape(title, quote=False))
        .replace("@BODY@", body)
        .replace("@BACKURL@", backurl)
        .replace("@BACKLABEL@", backlabel))
    open(os.path.join(OUT_HTML, slug + ".html"), "w").write(page)

    manifest.append({
        "slug": slug, "cat": cat_key, "label": label, "order": order,
        "title": title, "excerpt": excerpt, "read": read, "thumb": thumb,
    })

manifest.sort(key=lambda a: (a["order"], a["title"]))
json.dump(manifest, open(os.path.join(SCRATCH, "manifest.json"), "w"), ensure_ascii=False, indent=1)
print(f"Generated {len(manifest)} pages, {len(glob.glob(OUT_IMG + '/*.jpg'))} images")
