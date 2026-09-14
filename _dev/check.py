# -*- coding: utf-8 -*-
"""Vérifications avant livraison : liens morts, pages orphelines, sitemap, titles uniques, alt, JSON-LD, Hn."""
import os, re, json, sys, html
from html.parser import HTMLParser
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
pages = []
for dp, dn, fn in os.walk(ROOT):
    if "/_dev" in dp or "/.git" in dp: continue
    for f in fn:
        if f.endswith(".html"): pages.append(os.path.relpath(os.path.join(dp, f), ROOT))
pages.sort()
errors, warnings = [], []
titles, inbound = {}, {p: set() for p in pages}

class P(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.imgs=[]; self.ids=set(); self.h=[]; self.title=None; self._t=False; self.ld=[]; self._ld=False; self.desc=None; self.canonical=None; self.buttons=[]; self._h=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag=="a" and "href" in a: self.links.append(a["href"])
        if tag in ("img","source","video") and a.get("src"): self.imgs.append((tag, a.get("src"), a.get("alt"), a.get("width"), a.get("height"), a.get("loading")))
        if tag=="img" and a.get("alt") is None: errors.append(f"{self.cur}: <img> sans alt : {a.get('src')}")
        if tag=="link" and a.get("rel") in ("stylesheet","icon","apple-touch-icon","preload","canonical") and a.get("href"):
            if a.get("rel")=="canonical": self.canonical=a["href"]
            else: self.imgs.append((tag, a["href"], "x", 1, 1, None))
        if tag=="script" and a.get("src"): self.imgs.append((tag, a["src"], "x", 1, 1, None))
        if tag=="script" and a.get("type")=="application/ld+json": self._ld=True
        if tag=="title": self._t=True
        if tag=="meta" and a.get("name")=="description": self.desc=a.get("content")
        if tag in ("h1","h2","h3","h4"): self._h=tag; self.h.append([tag,""])
        if tag in ("button","a") and not a.get("aria-label") and tag=="button": self.buttons.append(a)
    def handle_endtag(self, tag):
        if tag=="title": self._t=False
        if tag=="script": self._ld=False
        if tag in ("h1","h2","h3","h4"): self._h=None
    def handle_data(self, d):
        if self._t: self.title=(self.title or "")+d
        if self._ld: self.ld.append(d)
        if self._h: self.h[-1][1]+=d

for p in pages:
    src=open(os.path.join(ROOT,p),encoding="utf-8").read()
    ps=P(); ps.cur=p; ps.feed(src)
    base=os.path.dirname(p)
    # title unique
    t=(ps.title or "").strip()
    if t in titles: errors.append(f"{p}: title dupliqué avec {titles[t]}")
    titles[t]=p
    if not ps.desc: errors.append(f"{p}: pas de meta description")
    if not ps.canonical: errors.append(f"{p}: pas de canonical")
    # H1 unique + hiérarchie
    h1=[h for h in ps.h if h[0]=="h1"]
    if len(h1)!=1: errors.append(f"{p}: {len(h1)} H1")
    prev=1
    for tag,txt in ps.h:
        lvl=int(tag[1])
        if lvl>prev+1: warnings.append(f"{p}: saut de niveau {prev}->{lvl} ({txt.strip()[:40]})")
        prev=lvl
    # JSON-LD valide
    for ld in ps.ld:
        try: json.loads(html.unescape(ld).replace("<\\/","</"))
        except Exception as e: errors.append(f"{p}: JSON-LD invalide : {e}")
    # liens
    for href in ps.links:
        if href.startswith(("http","mailto:","tel:")): continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in ps.ids: errors.append(f"{p}: ancre #{href[1:]} introuvable")
            continue
        path,_,frag=href.partition("#"); path=path.split("?")[0]
        target=os.path.normpath(os.path.join(base,path))
        if not os.path.exists(os.path.join(ROOT,target)): errors.append(f"{p}: lien mort {href}")
        elif target in inbound: inbound[target].add(p)
        if frag:
            tsrc=open(os.path.join(ROOT,target),encoding="utf-8").read() if os.path.exists(os.path.join(ROOT,target)) else ""
            if f'id="{frag}"' not in tsrc: errors.append(f"{p}: ancre {href} introuvable dans la cible")
    for tag,srcp,alt,w,h,lazy in ps.imgs:
        if srcp.startswith(("http","data:")): continue
        target=os.path.normpath(os.path.join(base,srcp.split("?")[0]))
        if not os.path.exists(os.path.join(ROOT,target)): errors.append(f"{p}: ressource manquante {srcp}")
        if tag=="img" and (not w or not h): errors.append(f"{p}: <img> sans width/height : {srcp}")
        if tag=="img" and alt is not None and alt.strip()=="" and "modal-img" not in srcp: pass
# orphelines
for p,ins in inbound.items():
    if p in ("index.html", "404.html"): continue  # 404 servie automatiquement par l'hébergeur
    others={i for i in ins if i!=p}
    if not others: errors.append(f"{p}: page orpheline (aucun lien entrant)")
# sitemap
sm=open(os.path.join(ROOT,"sitemap.xml"),encoding="utf-8").read()
locs=re.findall(r"<loc>https://www.pourfairesimple.fr/(.*?)</loc>",sm)
for p in pages:
    if p=="404.html": continue
    if p not in locs: errors.append(f"{p}: absente du sitemap")
for l in locs:
    if not os.path.exists(os.path.join(ROOT,l)): errors.append(f"sitemap: {l} n'existe pas")
    if "<lastmod>" not in sm: errors.append("sitemap sans lastmod")
# robots / llms
rb=open(os.path.join(ROOT,"robots.txt"),encoding="utf-8").read()
for bot in ["GPTBot","ClaudeBot","PerplexityBot","Google-Extended"]:
    if bot not in rb: errors.append(f"robots.txt: {bot} manquant")
if "Sitemap:" not in rb: errors.append("robots.txt: pas de Sitemap")
print(f"{len(pages)} pages, {len(locs)} URL dans le sitemap")
for w in warnings: print("WARN", w)
for e in errors: print("ERR ", e)
print("OK, aucune erreur" if not errors else f"{len(errors)} erreurs")
sys.exit(1 if errors else 0)
