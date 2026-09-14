# Maquette de refonte — pourfairesimple.fr

Site statique : HTML5, CSS (une feuille `assets/css/styles.css` pilotée par variables) et JavaScript vanilla (`assets/js/main.js`).
Aucun framework, aucune dépendance CDN, aucun build nécessaire.

## Ouvrir la maquette

Double-cliquer sur `index.html`. Tout fonctionne en local (polices embarquées, vidéo placeholder, formulaire validé côté client).

## Déployer

Glisser le dossier sur Netlify Drop, ou connecter le dépôt à Netlify / Vercel sans aucune configuration.
`404.html` est servie automatiquement sur les URL inconnues. `robots.txt`, `sitemap.xml` et `llms.txt` sont à la racine.

## Structure

```
index.html                      Accueil
agence-video.html               Parcours PME
boite-de-prod.html              Parcours agences (marque blanche)
offre-pour-faire-court.html     Offre snack content
offre-raconte.html              Offre capsules incarnées
realisations.html               Grille filtrable
realisations/*.html             3 études de cas
methode.html                    Déroulé d'une production
ressources.html                 Hub : guides + glossaire
ressources/*.html               2 articles complets
faq.html                        18 questions (FAQPage)
contact.html                    Formulaire de qualification
mentions-legales.html           Mentions légales + CGV
404.html
assets/css/styles.css           Variables : couleurs, typo, espacements, rayons
assets/css/fonts.css            Inter Variable + Instrument Serif (self-hosted, data-URI)
assets/js/main.js               Menu, révélations, filtres, curseur, lecteur, formulaire
assets/img/posters/*.svg        Posters placeholders (à remplacer par les vraies vignettes)
assets/img/og/*.png             Images Open Graph 1200×630, une par page
assets/video/showreel-placeholder.webm   Showreel placeholder (à remplacer)
```

## Remplacer les médias

- Showreel : déposer le vrai fichier en `assets/video/showreel.mp4` (+ `.webm`) et changer la source dans `index.html`.
- Vignettes : remplacer chaque `assets/img/posters/<slug>.svg` par un JPG/WebP du même ratio, mettre à jour l'attribut `src`.
- Vidéos des réalisations : renseigner `data-src` sur chaque bloc `.player` et `contentUrl` dans le JSON-LD.

## Dossier `_dev/` (optionnel)

Outil de génération utilisé pour garantir un header, un footer et un balisage d'entité (NAP) identiques sur toutes les pages.
Il n'est pas nécessaire pour ouvrir ou déployer le site. Pour régénérer après modification d'un fragment :
`python3 _dev/gen.py` puis `python3 _dev/check.py` (liens, orphelines, sitemap, titles, alt, JSON-LD).

Les blocs marqués **[À VALIDER AVEC LE CLIENT]** (chiffres, prix, équipe, mentions juridiques) sont à confirmer avant mise en ligne.
