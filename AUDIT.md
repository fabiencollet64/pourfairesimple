# AUDIT — Maquette de refonte pourfairesimple.fr

Support de présentation client. Ce document liste ce que la maquette corrige par rapport au site actuel,
les balises structurées implémentées, les mots-clés ciblés page par page, les leviers GEO activés,
et les vérifications effectuées avant livraison.

## 1. Ce que la maquette corrige par rapport au site actuel

| # | Faiblesse du site actuel | Réponse de la maquette |
|---|---|---|
| 1 | Aucune page de réalisation : le portfolio part vers Vimeo, zéro contenu indexable | Page `realisations.html` avec 12 réalisations filtrables par format (6) et par secteur (8), 3 études de cas détaillées (enjeu / dispositif / livrables / diffusion), balisage `ItemList` de 12 `VideoObject`, posters et vidéos hébergés sur le site, lecture à la demande |
| 2 | Métadonnées génériques, pas de données structurées, hiérarchie Hn absente | Title 55–60 caractères et meta description 150–160 caractères uniques sur les 17 pages (contrôlés par script), canonical, Open Graph et Twitter Card complets avec une image OG dédiée par page, JSON-LD sur chaque page, un seul H1 par page, H2 formulés en questions |
| 3 | Contact uniquement en `mailto:`, aucune qualification | Formulaire en 5 questions (profil, format, échéance, budget en fourchettes, cible de diffusion), validation JavaScript avec états d'erreur accessibles et état de succès avec récapitulatif, téléphone cliquable, email, adresse, horaires, bascule « vous êtes une agence » avec profil pré-sélectionné (`?profil=agence`) |
| 4 | Contenu trop mince, rien pour répondre aux questions d'un acheteur | 2 articles de 1 300 mots (prix 2026, formats selon l'objectif), FAQ de 18 questions, page méthode en 6 étapes, glossaire de 12 termes, 7 tableaux comparatifs, fourchettes de prix et délais sur chaque page de service |
| 5 | Blocs « No items found » et copyright 2023 | Aucun bloc vide, copyright 2026, dates de publication et `lastmod` renseignés |
| 6 | Aucune page mentions légales ni CGV | `mentions-legales.html` : éditeur, hébergement, propriété intellectuelle, données personnelles (RGPD), CGV en 9 articles, ancres utilisées depuis la FAQ et le formulaire |

Autres améliorations : hero vidéo plein écran, deux parcours PME / agences dès la navigation, CTA unique « Parlons de votre projet » sur tout le site, page 404 utile, `robots.txt`, `sitemap.xml`, `llms.txt`, polices self-hosted, aucune dépendance externe.

## 2. Balises structurées implémentées (JSON-LD, `@graph` par page)

| Type | Où | Détail |
|---|---|---|
| `Organization` | toutes les pages | nom, `legalName`, `foundingDate` 2013, adresse, téléphone E.164, email, logo, `sameAs` vers Vimeo, YouTube, Instagram, LinkedIn, `contactPoint`, `knowsAbout` = périmètre d'activité |
| `LocalBusiness` | toutes les pages | NAP strictement identique (généré depuis une source unique), `geo` (à valider), `openingHoursSpecification` (à valider), `areaServed`, `priceRange` |
| `WebSite` + `WebPage` | toutes les pages | `dateModified`, `primaryImageOfPage` = image OG, `inLanguage` fr-FR |
| `BreadcrumbList` | toutes les pages profondes (15) | fil d'Ariane visible et balisé |
| `Service` | agence-video, boite-de-prod, offre-pour-faire-court, offre-raconte | `provider` = Organization, `audience`, `OfferCatalog` des formats ; `Offer` avec prix sur les deux offres packagées (prix marqués à valider dans la page) |
| `ItemList` de `VideoObject` | index (6), realisations (12) | `thumbnailUrl`, `duration`, `uploadDate`, `genre`, `contentUrl` (placeholder à remplacer) |
| `CreativeWork` + `VideoObject` | 3 études de cas | étude de cas datée, `creator` = Organization |
| `HowTo` | methode | 6 `HowToStep` avec ancres, `totalTime` P8W |
| `FAQPage` | faq | 18 `Question` / `Answer`, texte identique à l'affichage |
| `Article` | 2 articles | `headline`, dates, `author` et `publisher` = Organization, `wordCount`, `articleSection`, `about` |
| `CollectionPage` + `DefinedTermSet` | ressources | 12 `DefinedTerm` (glossaire citable) |
| `ContactPage` | contact | avec LocalBusiness |

Non implémenté volontairement : `AggregateRating` et `Review` (aucun avis réel fourni), tout chiffre de résultat client.

## 3. Mots-clés ciblés page par page

| Page | Requête principale | Requêtes secondaires |
|---|---|---|
| index.html | agence vidéo Paris | société de production audiovisuelle Paris, boîte de prod Paris |
| agence-video.html | agence vidéo PME | film d'entreprise Paris, film corporate entreprise, vidéo institutionnelle prix |
| boite-de-prod.html | boîte de prod pour agence | production vidéo marque blanche, société de production audiovisuelle Paris |
| offre-pour-faire-court.html | snack content vidéo | vidéos courtes réseaux sociaux, vidéo TikTok Instagram entreprise, social ads |
| offre-raconte.html | vidéo de présentation entreprise | portrait vidéo dirigeant, vidéo témoignage entreprise prix |
| realisations.html | réalisations agence vidéo | exemples film corporate, portfolio motion design |
| realisations/sncf-serie-onboarding.html | vidéo onboarding entreprise | film d'intégration collaborateurs, film corporate RH |
| realisations/trade-republic-social-ads-motion.html | social ads motion design | vidéo publicitaire fintech, motion design finance |
| realisations/segafredo-brand-content.html | film de marque | brand content vidéo, publicité TV PME |
| methode.html | comment se passe une production vidéo | étapes production film d'entreprise, délai vidéo corporate |
| ressources.html | prix vidéo corporate, quel format vidéo choisir | glossaire vidéo, définition snack content |
| ressources/combien-coute-une-video-corporate-2026.html | combien coûte une vidéo corporate | prix vidéo entreprise, vidéo institutionnelle prix, tarif film d'entreprise 2026 |
| ressources/quel-format-video-choisir-selon-votre-objectif.html | quel format vidéo choisir | motion design ou tournage, motion design 2D 3D, format vidéo réseaux sociaux |
| faq.html | combien coûte une vidéo d'entreprise | combien de temps pour une vidéo, droits vidéo entreprise |
| contact.html | devis vidéo entreprise Paris | contact agence vidéo Paris |
| mentions-legales.html | — (conformité, priorité 0.3) | — |

## 4. Leviers GEO activés (visibilité dans ChatGPT, Claude, Gemini, Perplexity, AI Overviews)

1. **Réponse directe en ouverture** : chaque page commence par un bloc de 2 ou 3 phrases autoportantes (`.answer-box`) qui répond à la question implicite de la page, compréhensible hors contexte.
2. **Intertitres en questions réelles** : « Combien coûte… ? », « Comment se déroule… ? », « Motion design ou prises de vues réelles ? », etc.
3. **Faits chiffrés et datés** : fourchettes de prix 2026, délais par format, nombre de livrables, durées, mis en évidence typographique (`.figure`, `.stat__num`).
4. **7 tableaux comparatifs** : formats selon l'objectif, motion design contre prises de vues réelles, agence contre freelance contre interne, délais par étape, formules d'offre, capacités de production, déclinaisons par plateforme.
5. **Glossaire** de 12 termes avec définitions courtes, balisé `DefinedTermSet`.
6. **FAQ** de 18 questions formulées telles qu'on les pose, réponses de 52 à 73 mots, balisée `FAQPage`.
7. **`llms.txt`** à la racine : entreprise, périmètre, cibles, offres, repères chiffrés, arborescence, en markdown.
8. **`robots.txt`** autorisant explicitement GPTBot, OAI-SearchBot, ClaudeBot, Claude-User, anthropic-ai, PerplexityBot, Google-Extended, Applebot-Extended, avec référence au sitemap.
9. **Cohérence d'entité** : nom, adresse, téléphone, année de création et périmètre d'activité générés depuis une source unique (`_dev/data.py`) et identiques dans le texte, le footer, le JSON-LD et `llms.txt`.
10. **Signaux E-E-A-T** : page méthode avec rôles et engagements écrits, ancienneté depuis 2013, marque blanche depuis 2015, secteurs (santé, banque, assurance, industrie), articles signés par l'équipe et datés.
11. **Maillage contextuel** : chaque page de service pointe vers 2 ou 3 réalisations, chaque réalisation renvoie vers l'offre correspondante, ancres descriptives (jamais « cliquez ici »), filtres pré-appliqués via `?format=`.

## 5. Vérifications effectuées

Script `_dev/check.py` (17 pages) : aucun lien mort, aucune ressource manquante, aucune ancre cassée, aucune page orpheline (hors 404), toutes les pages dans le sitemap avec `lastmod`, 17 titles uniques, 1 H1 par page, toutes les images avec `alt`, `width` et `height`, JSON-LD valide sur chaque page, robots.txt conforme.

Tests navigateur (Chromium headless, Playwright) :
- Aucune erreur console, aucune requête en échec, aucun débordement horizontal à 375 px sur les 12 gabarits.
- Navigation clavier : skip-link en premier Tab, menu mobile avec piège de focus et fermeture par Échap, accordéon FAQ ouvrable au clavier, focus visible partout.
- Filtres de réalisations (format × secteur, état vide, pré-filtrage par URL), modale des fiches à venir, curseur personnalisé, lecteur vidéo à la demande, formulaire (5 erreurs détectées, email invalide, succès avec récapitulatif, profil agence via URL).
- `prefers-reduced-motion` : révélations désactivées, vidéo hero en pause, curseur désactivé.

## 6. À valider avec le client avant mise en ligne

Tous les éléments concernés sont marqués `[À VALIDER AVEC LE CLIENT]` dans les pages :
nombre de films livrés, grilles tarifaires des deux offres, seuils de dégressivité, noms et photos de l'équipe, contenu réel des 3 études de cas et des 9 fiches à venir, showreel et vidéos, coordonnées GPS et horaires, SIREN / forme juridique / hébergeur, relecture juridique des CGV.
