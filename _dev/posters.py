# -*- coding: utf-8 -*-
"""Génère des posters SVG élégants (placeholders) pour chaque réalisation + visuels génériques."""
import os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from data import PROJECTS

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "posters")
os.makedirs(OUT, exist_ok=True)
FONT = "'Inter Variable', Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

def dims(ratio):
    return {"wide": (1600, 900), "std": (1600, 900), "tall": (900, 1600), "square": (1200, 1200)}[ratio]

def composition(i, w, h, c2, c3):
    """Une composition géométrique différente selon l'index, sans dégradé."""
    k = i % 6
    if k == 0:   # grand cercle décentré
        return f"<circle cx='{w*0.72:.0f}' cy='{h*0.38:.0f}' r='{min(w,h)*0.36:.0f}' fill='{c2}'/>"
    if k == 1:   # bande diagonale
        return f"<polygon points='{w*0.55:.0f},0 {w},0 {w},{h} {w*0.25:.0f},{h}' fill='{c2}'/>"
    if k == 2:   # trame de points
        pts = []
        step = min(w, h) / 9
        for y in range(1, 9):
            for x in range(1, int(w / step)):
                r = 6 + (x + y) % 4 * 4
                pts.append(f"<circle cx='{x*step:.0f}' cy='{y*step:.0f}' r='{r}' fill='{c2}' opacity='0.85'/>")
        return "".join(pts)
    if k == 3:   # rayures verticales
        return "".join(f"<rect x='{w*(0.5+j*0.12):.0f}' y='0' width='{w*0.05:.0f}' height='{h}' fill='{c2}'/>" for j in range(5))
    if k == 4:   # demi-disque en bas
        return f"<path d='M0 {h} A {w/2:.0f} {h*0.7:.0f} 0 0 1 {w} {h} Z' fill='{c2}'/>"
    # k == 5 : carré tourné
    s = min(w, h) * 0.55
    return f"<rect x='{w*0.62-s/2:.0f}' y='{h*0.4-s/2:.0f}' width='{s:.0f}' height='{s:.0f}' fill='{c2}' transform='rotate(18 {w*0.62:.0f} {h*0.4:.0f})'/>"

def poster(p, i):
    w, h = dims(p["ratio"])
    c1, c2, c3 = p["c1"], p["c2"], p["c3"]
    title = html.escape(p["title"])
    client = html.escape(p["client"].upper())
    fs = int(min(w, h) * 0.075)
    pad = int(min(w, h) * 0.07)
    # découpe du titre sur 2 lignes max
    words = p["title"].split()
    lines, cur = [], ""
    maxc = int(w / (fs * 0.55))
    for wd in words:
        if len(cur) + len(wd) + 1 > maxc and cur:
            lines.append(cur); cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur: lines.append(cur)
    lines = lines[:3]
    tspans = "".join(f"<tspan x='{pad}' dy='{'0' if j == 0 else '1.05em'}'>{html.escape(l)}</tspan>" for j, l in enumerate(lines))
    ty = h - pad - fs * 1.05 * (len(lines) - 1) - int(fs * 0.3)
    grain = ("<filter id='g'><feTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' stitchTiles='stitch'/>"
             "<feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.12 0'/></filter>")
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}' role='img' aria-label='{title} — {client}'>
<defs>{grain}</defs>
<rect width='{w}' height='{h}' fill='{c1}'/>
{composition(i, w, h, c2, c3)}
<rect width='{w}' height='{h}' filter='url(#g)' opacity='0.5'/>
<rect x='{pad}' y='{pad}' width='{w-2*pad}' height='{h-2*pad}' fill='none' stroke='{c3}' stroke-opacity='0.35' stroke-width='2'/>
<text x='{pad+int(fs*0.35)}' y='{pad+int(fs*0.75)}' font-family=\"{FONT}\" font-size='{int(fs*0.36)}' font-weight='600' letter-spacing='0.12em' fill='{c3}'>{client}</text>
<circle cx='{w-pad-int(fs*0.5)}' cy='{pad+int(fs*0.5)}' r='{int(fs*0.16)}' fill='#ff5a1f'/>
<text x='{pad}' y='{ty}' font-family=\"{FONT}\" font-size='{fs}' font-weight='800' letter-spacing='-0.03em' fill='{c3}' style='paint-order:stroke' stroke='{c1}' stroke-opacity='0.35' stroke-width='6'>{tspans}</text>
<text x='{w-pad-int(fs*0.35)}' y='{h-pad-int(fs*0.35)}' text-anchor='end' font-family=\"{FONT}\" font-size='{int(fs*0.32)}' font-weight='500' letter-spacing='0.1em' fill='{c3}' fill-opacity='0.8'>{html.escape(p['year'])} · {p['duration'][2:].replace('M', ':').replace('S','').replace('H','h')}</text>
</svg>"""

for i, p in enumerate(PROJECTS):
    with open(os.path.join(OUT, p["slug"] + ".svg"), "w", encoding="utf-8") as f:
        f.write(poster(p, i))
    # variante 16:9 pour les fiches (les cartes 9:16 / 1:1 ont aussi une version large)
    if p["ratio"] != "wide" and p["ratio"] != "std":
        q = dict(p, ratio="wide")
        with open(os.path.join(OUT, p["slug"] + "-16x9.svg"), "w", encoding="utf-8") as f:
            f.write(poster(q, i))

# Visuels génériques (offres, équipe, showreel, méthode)
GENERIC = [
    dict(slug="offre-pour-faire-court", client="Pour Faire Court.", title="🌭 3 à 15 secondes. À prix fixe.", ratio="tall", year="2026", duration="PT0M15S", c1="#ff5a1f", c2="#0c0c0d", c3="#f3efe6"),
    dict(slug="offre-raconte", client="Raconte...", title="🦫 Une capsule incarnée. Un teaser.", ratio="wide", year="2026", duration="PT2M00S", c1="#1c1c1f", c2="#ff5a1f", c3="#f3efe6"),
    dict(slug="showreel", client="Showreel 2026", title="", ratio="wide", year="2026", duration="PT1M20S", c1="#0c0c0d", c2="#ff5a1f", c3="#f3efe6"),
    dict(slug="equipe", client="L'équipe", title="Des gens qui répondent au téléphone.", ratio="wide", year="2026", duration="PT0M00S", c1="#141416", c2="#3a3a40", c3="#f3efe6"),
    dict(slug="methode", client="Méthode", title="Six étapes. Un interlocuteur.", ratio="wide", year="2026", duration="PT0M00S", c1="#0f3d3e", c2="#7fe0d2", c3="#f3efe6"),
    dict(slug="agence-video", client="Agence vidéo", title="Le film qui sert votre objectif.", ratio="wide", year="2026", duration="PT0M00S", c1="#1b2a6b", c2="#ff5a1f", c3="#f3efe6"),
    dict(slug="boite-de-prod", client="Boîte de prod", title="Votre production, notre plateau.", ratio="wide", year="2026", duration="PT0M00S", c1="#26262a", c2="#ff5a1f", c3="#f3efe6"),
]
for i, p in enumerate(GENERIC):
    with open(os.path.join(OUT, p["slug"] + ".svg"), "w", encoding="utf-8") as f:
        f.write(poster(p, i + 2))
print("posters:", len(os.listdir(OUT)))
