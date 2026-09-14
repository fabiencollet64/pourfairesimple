# -*- coding: utf-8 -*-
"""
Générateur de pages statiques (outil de développement, non requis pour ouvrir le site).
Lit _dev/pages/*.html (fragment + bloc META JSON) et écrit les pages HTML complètes à la racine,
avec head SEO, header, footer, JSON-LD d'entité (NAP identique partout) et fil d'Ariane.
Usage : python3 _dev/gen.py
"""
import os, sys, json, re, html, datetime
sys.path.insert(0, os.path.dirname(__file__))
from data import SITE, NAV, CLIENTS, PROJECTS, FORMATS, SECTEURS
from faq_data import FAQ
from glossary_data import GLOSSARY
FAQ_ITEMS = [(q, a) for q, a, h in FAQ]

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAGES_DIR = os.path.join(os.path.dirname(__file__), "pages")
TODAY = "2026-09-14"
BASE = SITE["base"]

def esc(s):
    return html.escape(s, quote=True)

# ------------------------------------------------------------------ JSON-LD entité
ORG_ID = BASE + "#organization"
LB_ID = BASE + "#localbusiness"
SITE_ID = BASE + "#website"

def entity_graph():
    sameas = list(SITE["socials"].values())
    org = {
        "@type": "Organization", "@id": ORG_ID,
        "name": SITE["name"], "legalName": SITE["legal_name"], "url": BASE,
        "logo": {"@type": "ImageObject", "url": BASE + "assets/img/logo.svg", "width": 512, "height": 512},
        "foundingDate": SITE["founded"],
        "description": ("Pour Faire Simple. est une agence vidéo et société de production audiovisuelle à Paris, "
                        "créée en 2013. Périmètre : " + SITE["scope"] + "."),
        "email": SITE["email"], "telephone": SITE["phone_e164"],
        "address": {"@type": "PostalAddress", "streetAddress": SITE["street"], "postalCode": SITE["zip"],
                    "addressLocality": SITE["city"], "addressCountry": SITE["country"]},
        "sameAs": sameas,
        "contactPoint": [{"@type": "ContactPoint", "contactType": "sales", "telephone": SITE["phone_e164"],
                          "email": SITE["email"], "availableLanguage": ["fr", "en"], "areaServed": "FR"}],
        "knowsAbout": [s.strip() for s in SITE["scope"].split(",")],
    }
    lb = {
        "@type": "LocalBusiness", "@id": LB_ID, "parentOrganization": {"@id": ORG_ID},
        "name": SITE["name"], "image": BASE + "assets/img/og/index.png", "url": BASE,
        "telephone": SITE["phone_e164"], "email": SITE["email"], "priceRange": "€€",
        "address": {"@type": "PostalAddress", "streetAddress": SITE["street"], "postalCode": SITE["zip"],
                    "addressLocality": SITE["city"], "addressCountry": SITE["country"]},
        "geo": {"@type": "GeoCoordinates", "latitude": SITE["geo"]["lat"], "longitude": SITE["geo"]["lng"]},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "09:30", "closes": "18:30"}],
        "sameAs": sameas, "areaServed": [{"@type": "City", "name": "Paris"}, {"@type": "Country", "name": "France"}],
    }
    ws = {"@type": "WebSite", "@id": SITE_ID, "url": BASE, "name": SITE["name"], "publisher": {"@id": ORG_ID}, "inLanguage": "fr-FR"}
    return [org, lb, ws]

# ------------------------------------------------------------------ partials
def header(root, current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a class="nav__link" href="{root}{href}"{cur}>{label}</a></li>')
    CUR = ' aria-current="page"'
    menu_items = "".join(f'<li><a href="{root}{h}"{CUR if h == current else ""}>{l}</a></li>' for h, l in NAV)
    return f"""<a class="skip-link" href="#contenu">Aller au contenu</a>
<header class="site-header">
  <div class="container site-header__inner">
    <a class="logo" href="{root}index.html" aria-label="Pour Faire Simple, retour à l'accueil">Pour Faire Simple<span class="logo__dot" aria-hidden="true"></span></a>
    <nav class="nav" aria-label="Navigation principale"><ul class="nav__list">{"".join(items)}</ul></nav>
    <div class="cluster">
      <a class="btn btn--primary header-cta" href="{root}contact.html">{SITE["cta"]}</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="menu" id="menu" aria-label="Menu mobile">
  <nav aria-label="Navigation mobile"><ul class="menu__list">
    <li><a href="{root}index.html">Accueil</a></li>{menu_items}
    <li><a href="{root}offre-pour-faire-court.html">Pour Faire Court. 🌭</a></li>
    <li><a href="{root}offre-raconte.html">Raconte... 🦫</a></li>
  </ul></nav>
  <div class="menu__foot">
    <a class="btn btn--primary" href="{root}contact.html">{SITE["cta"]}</a>
    <a href="tel:{SITE["phone_e164"]}">{SITE["phone_display"]}</a>
    <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>
  </div>
</div>"""

def end_card(root, title=None, voice=None):
    title = title or "Parlons de votre projet"
    voice = voice or "Un appel de 20 minutes suffit souvent à cadrer l'essentiel."
    return f"""<section class="end-card" aria-labelledby="end-title">
  <div class="container">
    <h2 class="end-card__title reveal" id="end-title">{title}<span class="dot">.</span><br><span class="voice">{voice}</span></h2>
    <div class="end-card__row reveal">
      <div class="end-card__contacts">
        <a href="tel:{SITE["phone_e164"]}">{SITE["phone_display"]}</a>
        <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>
        <span>{SITE["street"]}, {SITE["zip"]} {SITE["city"]}</span>
      </div>
      <a class="btn btn--primary btn--lg" href="{root}contact.html">{SITE["cta"]} <span class="arrow" aria-hidden="true">→</span></a>
    </div>
  </div>
</section>"""

def footer(root):
    s = SITE["socials"]
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div>
        <a class="logo" href="{root}index.html">Pour Faire Simple<span class="logo__dot" aria-hidden="true"></span></a>
        <p class="mt-6">Agence vidéo et société de production audiovisuelle à Paris, depuis 2013. Le bon message, aux bonnes personnes, de la bonne manière.</p>
        <address>{SITE["street"]}<br>{SITE["zip"]} {SITE["city"]}<br><a href="tel:{SITE["phone_e164"]}">{SITE["phone_display"]}</a><br><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></address>
      </div>
      <div>
        <h2>Pour qui</h2>
        <ul>
          <li><a href="{root}agence-video.html">Agence vidéo pour les PME</a></li>
          <li><a href="{root}boite-de-prod.html">Boîte de prod pour les agences</a></li>
          <li><a href="{root}offre-pour-faire-court.html">Offre Pour Faire Court.</a></li>
          <li><a href="{root}offre-raconte.html">Offre Raconte...</a></li>
        </ul>
      </div>
      <div>
        <h2>Découvrir</h2>
        <ul>
          <li><a href="{root}realisations.html">Réalisations</a></li>
          <li><a href="{root}methode.html">Notre méthode de production</a></li>
          <li><a href="{root}ressources.html">Ressources et glossaire</a></li>
          <li><a href="{root}faq.html">Questions fréquentes</a></li>
          <li><a href="{root}contact.html">Contact et devis</a></li>
        </ul>
      </div>
      <div>
        <h2>Suivre</h2>
        <ul>
          <li><a href="{s["vimeo"]}" rel="noopener" target="_blank">Vimeo</a></li>
          <li><a href="{s["youtube"]}" rel="noopener" target="_blank">YouTube</a></li>
          <li><a href="{s["instagram"]}" rel="noopener" target="_blank">Instagram @agencepourfairesimple</a></li>
          <li><a href="{s["linkedin"]}" rel="noopener" target="_blank">LinkedIn</a></li>
        </ul>
      </div>
    </div>
    <div class="site-footer__bottom">
      <span>© 2026 Pour Faire Simple. Tous droits réservés.</span>
      <ul><li><a href="{root}mentions-legales.html">Mentions légales et CGV</a></li><li><a href="{root}sitemap.xml">Plan du site (XML)</a></li><li><a href="{root}llms.txt">llms.txt</a></li></ul>
    </div>
  </div>
</footer>"""

def breadcrumb_html(root, crumbs):
    if not crumbs: return ""
    lis = [f'<li><a href="{root}index.html">Accueil</a></li>']
    for i, (label, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            lis.append(f'<li><span aria-current="page">{esc(label)}</span></li>')
        else:
            lis.append(f'<li><a href="{root}{href}">{esc(label)}</a></li>')
    return f'<nav class="breadcrumb" aria-label="Fil d\'Ariane"><ol>{"".join(lis)}</ol></nav>'

def breadcrumb_ld(crumbs, path):
    items = [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "index.html"}]
    for i, (label, href) in enumerate(crumbs):
        items.append({"@type": "ListItem", "position": i + 2, "name": label, "item": BASE + (href if href else path)})
    return {"@type": "BreadcrumbList", "itemListElement": items}

# ------------------------------------------------------------------ helpers réutilisés par les fragments
def project_card(p, root, extra_class=""):
    ratio_cls = {"wide": "work-card--wide", "tall": "work-card--tall", "square": "work-card--square", "std": ""}[p["ratio"]]
    poster = f'{root}assets/img/posters/{p["slug"]}.svg'
    w, h = {"wide": (1600, 900), "std": (1600, 900), "tall": (900, 1600), "square": (1200, 1200)}[p["ratio"]]
    alt = f'Image de la vidéo « {p["title"]} » réalisée pour {p["client"]}, {FORMATS[p["format"]].lower()}'
    inner = f"""<div class="work-card__media"><img src="{poster}" alt="{esc(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"><span class="work-card__play" aria-hidden="true">▶</span><span class="work-card__progress" aria-hidden="true"></span></div>
      <div class="work-card__meta"><span class="work-card__title">{esc(p["title"])}</span><span class="work-card__sub">{esc(p["client"])} · {FORMATS[p["format"]]} · {SECTEURS[p["secteur"]]}</span></div>"""
    attrs = f'class="work-card {ratio_cls} {extra_class}" data-format="{p["format"]}" data-secteur="{p["secteur"]}"'
    if p["page"]:
        return f'<a {attrs} href="{root}realisations/{p["slug"]}.html" data-cursor="Voir l\'étude de cas">{inner}</a>'
    poster_wide = f'{root}assets/img/posters/{p["slug"]}{"-16x9" if p["ratio"] in ("tall", "square") else ""}.svg'
    return f'<button type="button" {attrs} data-cursor="Aperçu" data-title="{esc(p["title"])}" data-sub="{esc(p["client"])} · {FORMATS[p["format"]]} · {esc(p["teaser"])}" data-poster="{poster_wide}">{inner}</button>'

def marquee(root):
    items = "".join(f'<span class="marquee__item">{esc(c)}</span>' for c in CLIENTS)
    return f'<div class="marquee" aria-label="Ils nous font confiance"><div class="marquee__track">{items}{items}</div></div>'

def related_projects(root, slugs):
    cards = [project_card(p, root) for p in PROJECTS if p["slug"] in slugs]
    return '<div class="work-grid work-grid--related reveal--stagger">' + "".join(cards) + "</div>"

def video_ld(p, root_url=BASE):
    poster = f'{root_url}assets/img/posters/{p["slug"]}{"-16x9" if p["ratio"] in ("tall", "square") else ""}.svg'
    return {"@type": "VideoObject", "name": p["title"], "description": p["teaser"],
            "thumbnailUrl": [poster, f'{root_url}assets/img/posters/{p["slug"]}.svg'],
            "uploadDate": f'{p["year"]}-06-01', "duration": p["duration"],
            "contentUrl": f'{root_url}assets/video/showreel-placeholder.webm',
            "url": f'{root_url}realisations/{p["slug"]}.html' if p["page"] else f'{root_url}realisations.html',
            "publisher": {"@id": ORG_ID}, "inLanguage": "fr-FR", "genre": FORMATS[p["format"]]}

CONTEXT = {"SITE": SITE, "NAV": NAV, "CLIENTS": CLIENTS, "PROJECTS": PROJECTS, "FORMATS": FORMATS, "SECTEURS": SECTEURS,
           "project_card": project_card, "marquee": marquee, "related_projects": related_projects, "video_ld": video_ld,
           "esc": esc, "json": json, "FAQ_ITEMS": FAQ_ITEMS, "GLOSSARY": GLOSSARY, "BASE": BASE, "ORG_ID": ORG_ID, "LB_ID": LB_ID, "SITE_ID": SITE_ID, "TODAY": TODAY}

# ------------------------------------------------------------------ build
META_RE = re.compile(r"<!--META\s*(\{.*?\})\s*-->", re.S)
PY_RE = re.compile(r"\{\{py:(.*?)\}\}", re.S)

def render_fragment(src, root):
    """Remplace {{root}} et évalue les blocs {{py: ...}} (expressions Python avec CONTEXT)."""
    ctx = dict(CONTEXT, root=root, FAQ_HTML=[(q, a, h.replace("{root}", root)) for q, a, h in FAQ])
    def sub(m):
        return str(eval(m.group(1).strip(), dict(ctx)))
    out = PY_RE.sub(sub, src)
    return out.replace("{{root}}", root)

def build_page(fname):
    with open(os.path.join(PAGES_DIR, fname), encoding="utf-8") as f:
        src = f.read()
    m = META_RE.search(src)
    meta = json.loads(m.group(1))
    body = src[m.end():].strip()
    path = meta["path"]
    depth = path.count("/")
    root = "../" * depth
    current = meta.get("nav", "")
    url = BASE + path
    og_img = BASE + f"assets/img/og/{meta['og']}.png"
    graph = entity_graph()
    page_type = meta.get("type", "WebPage")
    webpage = {"@type": page_type, "@id": url + "#webpage", "url": url, "name": meta["title"],
               "description": meta["description"], "isPartOf": {"@id": SITE_ID}, "about": {"@id": ORG_ID},
               "inLanguage": "fr-FR", "dateModified": meta.get("lastmod", TODAY),
               "primaryImageOfPage": {"@type": "ImageObject", "url": og_img, "width": 1200, "height": 630}}
    crumbs = meta.get("breadcrumb")
    if crumbs:
        bl = breadcrumb_ld(crumbs, path); bl["@id"] = url + "#breadcrumb"
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append(bl)
    graph.append(webpage)
    # JSON-LD spécifique de la page, évalué (peut référencer CONTEXT)
    extra = meta.get("jsonld_py")
    if extra:
        graph.extend(eval(extra, dict(CONTEXT, root=root, url=url, og_img=og_img)))
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    ld = ld.replace("</", "<\\/")
    seo_note = meta["seo_note"].strip()
    body = render_fragment(body, root)
    bc = breadcrumb_html(root, crumbs) if crumbs else ""
    body = body.replace("{{breadcrumb}}", bc)
    end = "" if meta.get("no_endcard") else end_card(root, meta.get("end_title"), meta.get("end_voice"))
    robots = meta.get("robots", "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1")
    ogtype = "article" if page_type == "Article" else "website"
    article_meta = ""
    if page_type == "Article":
        article_meta = f'\n  <meta property="article:published_time" content="{meta.get("published", TODAY)}">\n  <meta property="article:modified_time" content="{meta.get("lastmod", TODAY)}">\n  <meta property="article:author" content="{BASE}">'
    doc = f"""<!DOCTYPE html>
<html lang="fr">
<!--
  CHOIX SEO DE CETTE PAGE
  {seo_note}
-->
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(meta["title"])}</title>
  <meta name="description" content="{esc(meta["description"])}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="{robots}">
  <meta name="author" content="Pour Faire Simple.">
  <meta name="theme-color" content="#0c0c0d">
  <link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{root}assets/img/favicon.svg">
  <meta property="og:type" content="{ogtype}">
  <meta property="og:site_name" content="Pour Faire Simple.">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{esc(meta.get("og_title", meta["title"]))}">
  <meta property="og:description" content="{esc(meta["description"])}">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{esc(meta.get("og_alt", meta.get("og_title", meta["title"])))}">{article_meta}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(meta.get("og_title", meta["title"]))}">
  <meta name="twitter:description" content="{esc(meta["description"])}">
  <meta name="twitter:image" content="{og_img}">
  <meta name="twitter:image:alt" content="{esc(meta.get("og_alt", meta.get("og_title", meta["title"])))}">
  <link rel="stylesheet" href="{root}assets/css/fonts.css">
  <link rel="stylesheet" href="{root}assets/css/styles.css">
  <script type="application/ld+json">
{ld}
  </script>
</head>
<body>
{header(root, current)}
<main id="contenu" tabindex="-1">
{body}
</main>
{end}
{footer(root)}
<script src="{root}assets/js/main.js" defer></script>
</body>
</html>
"""
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    # contrôles longueur title / description
    tl, dl = len(meta["title"]), len(meta["description"])
    flag = ""
    if not (55 <= tl <= 60): flag += f"  !! title {tl} car."
    if not (150 <= dl <= 160): flag += f"  !! description {dl} car."
    print(f"{path:55s} title={tl:2d} desc={dl:3d}{flag}")
    return meta

if __name__ == "__main__":
    metas = []
    for fname in sorted(os.listdir(PAGES_DIR)):
        if fname.endswith(".html"):
            metas.append(build_page(fname))
    # sitemap.xml
    urls = []
    for m in metas:
        if m.get("nositemap"): continue
        urls.append(f"  <url>\n    <loc>{BASE}{m['path']}</loc>\n    <lastmod>{m.get('lastmod', TODAY)}</lastmod>\n    <changefreq>{m.get('changefreq', 'monthly')}</changefreq>\n    <priority>{m.get('priority', '0.6')}</priority>\n  </url>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "_dev", "pages.json"), "w", encoding="utf-8") as f:
        json.dump([{"path": m["path"], "title": m["title"], "og": m["og"], "og_title": m.get("og_title", m["title"]), "kicker": m.get("kicker", "")} for m in metas], f, ensure_ascii=False, indent=1)
    print(f"{len(metas)} pages générées, sitemap : {len(urls)} URL.")
