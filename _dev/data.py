# -*- coding: utf-8 -*-
"""Données partagées : entité (NAP), navigation, réalisations. Une seule source de vérité."""

SITE = {
    "name": "Pour Faire Simple.",
    "legal_name": "Pour Faire Simple",
    "base": "https://www.pourfairesimple.fr/",
    "street": "6 Passage Doisy",
    "zip": "75017",
    "city": "Paris",
    "country": "FR",
    "phone_display": "+33 (0)1 46 22 56 88",
    "phone_e164": "+33146225688",
    "email": "bonjour@pourfairesimple.fr",
    "founded": "2013",
    "geo": {"lat": 48.8797, "lng": 2.2941},   # approx. Passage Doisy — [À VALIDER]
    "hours": "Mo-Fr 09:30-18:30",              # [À VALIDER]
    "socials": {
        "vimeo": "https://vimeo.com/pourfairesimple",
        "youtube": "https://www.youtube.com/user/pourfairesimple",
        "instagram": "https://www.instagram.com/agencepourfairesimple/",
        "linkedin": "https://fr.linkedin.com/company/pour-faire-simple",
    },
    "scope": ("brand content, publicité TV, motion design 2D et 3D, social ads, films corporate et "
              "institutionnels, portraits RH, captation d'événements, contenus d'onboarding et de culture "
              "d'entreprise, case studies, témoignages, interviews, UGC, snack content, podcast audio et vidéo"),
    "cta": "Parlons de votre projet",
}

NAV = [
    ("agence-video.html", "Agence vidéo"),
    ("boite-de-prod.html", "Boîte de prod"),
    ("realisations.html", "Réalisations"),
    ("methode.html", "Méthode"),
    ("ressources.html", "Ressources"),
    ("faq.html", "FAQ"),
]

CLIENTS = ["SNCF", "Trade Republic", "Segafredo", "SeLoger", "Lectra", "Generix", "Nexira", "Ticketac",
           "Pharmalys", "Loiselet & Daigremont", "S2PWeb", "Thomann-Hanry"]

FORMATS = {
    "film-corporate": "Film corporate & institutionnel",
    "motion-design": "Motion design 2D / 3D",
    "social-ads": "Social ads & snack content",
    "portraits": "Portraits, témoignages & interviews",
    "captation": "Captation & podcast",
    "brand-content": "Brand content & publicité",
}
SECTEURS = {
    "transport": "Transport & mobilité",
    "finance": "Finance & assurance",
    "food": "Food & boissons",
    "immobilier": "Immobilier",
    "industrie": "Industrie & tech",
    "sante": "Santé",
    "culture": "Culture & loisirs",
    "batiment": "Bâtiment & patrimoine",
}

# Réalisations plausibles inspirées des logos affichés. Contenu à remplacer par le client.
PROJECTS = [
    dict(slug="sncf-serie-onboarding", client="SNCF", title="Bienvenue à bord : la série d'onboarding",
         format="film-corporate", secteur="transport", ratio="wide", duration="PT3M40S", year="2025",
         c1="#1b2a6b", c2="#ff5a1f", c3="#f3efe6", page=True, order=1,
         teaser="Six épisodes pour accueillir les nouveaux collaborateurs, tournés sur trois sites."),
    dict(slug="trade-republic-social-ads-motion", client="Trade Republic", title="Investir, expliqué en 15 secondes",
         format="social-ads", secteur="finance", ratio="tall", duration="PT0M15S", year="2025",
         c1="#0e0e10", c2="#a3ff5a", c3="#f3efe6", page=True, order=2,
         teaser="Une série de social ads en motion design, déclinée en 9:16, 1:1 et 16:9."),
    dict(slug="segafredo-brand-content", client="Segafredo", title="Le rituel du matin",
         format="brand-content", secteur="food", ratio="wide", duration="PT0M45S", year="2024",
         c1="#7a1f0f", c2="#ffb347", c3="#f3efe6", page=True, order=3,
         teaser="Film de marque 45 secondes et déclinaisons 20 et 6 secondes pour la TV et le digital."),
    dict(slug="seloger-motion-explicatif", client="SeLoger", title="Estimer son bien, sans jargon",
         format="motion-design", secteur="immobilier", ratio="std", duration="PT1M30S", year="2024",
         c1="#c8102e", c2="#ffd8cc", c3="#0c0c0d", page=False, order=4,
         teaser="Vidéo explicative en motion design 2D, voix off et sous-titres."),
    dict(slug="lectra-film-institutionnel", client="Lectra", title="L'industrie 4.0, vue de l'atelier",
         format="film-corporate", secteur="industrie", ratio="std", duration="PT2M20S", year="2024",
         c1="#0f3d3e", c2="#7fe0d2", c3="#f3efe6", page=False, order=5,
         teaser="Film institutionnel tourné sur un site de production, version FR et EN."),
    dict(slug="generix-case-study-client", client="Generix", title="Témoignage client : la supply chain en direct",
         format="portraits", secteur="industrie", ratio="square", duration="PT2M05S", year="2023",
         c1="#2b2d42", c2="#8d99ae", c3="#f3efe6", page=False, order=6,
         teaser="Case study vidéo avec interview croisée éditeur et client."),
    dict(slug="nexira-film-corporate", client="Nexira", title="Du végétal à l'ingrédient",
         format="film-corporate", secteur="industrie", ratio="std", duration="PT3M10S", year="2023",
         c1="#3a5a40", c2="#dad7cd", c3="#0c0c0d", page=False, order=7,
         teaser="Film corporate en prises de vues réelles avec inserts motion."),
    dict(slug="ticketac-snack-content", client="Ticketac", title="Pour Faire Court. : la saison en 6 secondes",
         format="social-ads", secteur="culture", ratio="tall", duration="PT0M06S", year="2025",
         c1="#5a189a", c2="#ffd60a", c3="#f3efe6", page=False, order=8,
         teaser="Abonnement snack content : 8 vidéos par mois pour Instagram et TikTok."),
    dict(slug="pharmalys-motion-3d", client="Pharmalys", title="Le produit, vu de l'intérieur",
         format="motion-design", secteur="sante", ratio="std", duration="PT1M10S", year="2024",
         c1="#0b3954", c2="#bfd7ea", c3="#f3efe6", page=False, order=9,
         teaser="Animation 3D de mécanisme produit pour les équipes commerciales."),
    dict(slug="loiselet-daigremont-portraits-rh", client="Loiselet & Daigremont", title="Portraits de gestionnaires",
         format="portraits", secteur="immobilier", ratio="square", duration="PT1M00S", year="2023",
         c1="#3d2b1f", c2="#d4a373", c3="#f3efe6", page=False, order=10,
         teaser="Série de portraits RH pour la marque employeur, format 1:1."),
    dict(slug="s2pweb-captation-podcast", client="S2PWeb", title="Le podcast des flux",
         format="captation", secteur="industrie", ratio="std", duration="PT24M00S", year="2025",
         c1="#14213d", c2="#fca311", c3="#f3efe6", page=False, order=11,
         teaser="Podcast vidéo enregistré en studio, 6 épisodes, capsules de 60 secondes."),
    dict(slug="thomann-hanry-film-patrimoine", client="Thomann-Hanry", title="Rendre aux façades leur lumière",
         format="film-corporate", secteur="batiment", ratio="std", duration="PT2M45S", year="2024",
         c1="#2f2f2f", c2="#e5c07b", c3="#f3efe6", page=False, order=12,
         teaser="Film institutionnel, tournage drone et macro sur chantier."),
]
