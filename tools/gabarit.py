# -*- coding: utf-8 -*-
"""Gabarit HTML unique. Nommé `gabarit` pour ne pas masquer le module `html`."""
import html as _html
import json
from config import SITE

ECHAPPER = _html.escape


def e(t):
    return ECHAPPER(str(t), quote=True)


NAV = {
    "fr": [
        ("", "Accueil"),
        ("simulateur/", "Le simulateur"),
        ("chambre/", "La Chambre"),
        ("parlements/", "Les parlements"),
        ("regles/", "Les règles"),
        ("methode/", "La méthode"),
        ("actualites/", "L'actualité"),
    ],
    "nl": [
        ("", "Start"),
        ("simulator/", "De simulator"),
        ("kamer/", "De Kamer"),
        ("parlementen/", "De parlementen"),
        ("regels/", "De regels"),
        ("methode/", "De methode"),
        ("actualiteit/", "Actualiteit"),
    ],
}

PIED = {
    "fr": {
        "licence": "Texte et code sous licence CC BY-SA 4.0. Aucun traceur, aucun cookie, "
                   "aucune police distante, aucun appel réseau.",
        "liens": [("sources/", "Les sources"), ("glossaire/", "Le glossaire"),
                  ("coalitions/", "Les coalitions"), ("reseau/", "Le réseau")],
        "maj": "Dernière mise à jour",
        "depot": "Code source",
    },
    "nl": {
        "licence": "Tekst en code onder CC BY-SA 4.0. Geen trackers, geen cookies, geen externe "
                   "lettertypes, geen netwerkoproepen.",
        "liens": [("bronnen/", "De bronnen"), ("woordenlijst/", "Woordenlijst"),
                  ("coalities/", "De coalities"), ("netwerk/", "Het netwerk")],
        "maj": "Laatst bijgewerkt",
        "depot": "Broncode",
    },
}

SAUT = {"fr": "Aller au contenu", "nl": "Naar de inhoud"}
LANGUE_AUTRE = {"fr": ("nl", "Nederlands"), "nl": ("fr", "Français")}


def prefixe(langue):
    return "" if langue == "fr" else "nl/"


def url_absolue(chemin):
    return SITE["url"].rstrip("/") + "/" + chemin.lstrip("/")


def relatif(depuis, vers):
    """Chemin relatif entre deux répertoires du site (tous deux se terminent par /)."""
    a = [x for x in depuis.split("/") if x]
    b = [x for x in vers.split("/") if x]
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    montee = "../" * (len(a) - i)
    descente = "/".join(b[i:])
    r = montee + (descente + "/" if descente else "")
    return r or "./"


def page(*, langue, chemin, chemin_autre, titre, description, corps, fil,
         jsonld=None, og_image=None, scripts=None, styles_sup=None, canonique=None,
         racine_absolue=False):
    """`chemin` : répertoire du site, ex. 'chambre/hainaut/'. Racine = ''."""
    racine = relatif(chemin, "")
    base = relatif(chemin, prefixe(langue))
    if racine_absolue:
        racine = SITE["url"].rstrip("/") + "/"
        base = racine + prefixe(langue)
    url = url_absolue(canonique if canonique is not None else chemin)
    autre = url_absolue(chemin_autre)
    og = og_image or "assets/og/accueil.png"
    nav = NAV[langue]
    pied = PIED[langue]
    lang_code, lang_nom = LANGUE_AUTRE[langue]

    fil_html = ""
    if fil:
        items = []
        for i, (lien, nom) in enumerate(fil):
            if lien is None:
                items.append(f'<li aria-current="page">{e(nom)}</li>')
            else:
                items.append(f'<li><a href="{e(racine + lien)}">{e(nom)}</a></li>')
        fil_html = ('<nav class="fil" aria-label="' +
                    ("Fil d'Ariane" if langue == "fr" else "Kruimelpad") + '"><ol>' +
                    "".join(items) + "</ol></nav>")

    blocs_jsonld = []
    if fil:
        elements = []
        pos = 1
        for lien, nom in fil:
            elements.append({"@type": "ListItem", "position": pos, "name": nom,
                             "item": url_absolue(lien if lien is not None else chemin)})
            pos += 1
        blocs_jsonld.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                             "itemListElement": elements})
    for b in (jsonld or []):
        blocs_jsonld.append(b)

    ld = "".join(
        '<script type="application/ld+json">' +
        json.dumps(b, ensure_ascii=False, separators=(",", ":")) + "</script>"
        for b in blocs_jsonld)

    courant = chemin[len(prefixe(langue)):] if chemin.startswith(prefixe(langue)) else chemin
    morceaux = []
    for l, n in nav:
        marque = ' aria-current="page"' if l == courant else ""
        morceaux.append('<li><a href="' + e(base + l) + '"' + marque + '>' + e(n) + "</a></li>")
    liens_nav = "".join(morceaux)
    liens_pied = " · ".join(
        f'<a href="{e(base + l)}">{e(n)}</a>' for l, n in pied["liens"])

    js = "".join(f'<script src="{e(racine + s)}" defer></script>' for s in (scripts or []))
    css_sup = "".join(f'<link rel="stylesheet" href="{e(racine + s)}">' for s in (styles_sup or []))

    return f"""<!DOCTYPE html>
<html lang="{langue}" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titre)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(url)}">
<link rel="alternate" hreflang="{langue}" href="{e(url)}">
<link rel="alternate" hreflang="{lang_code}" href="{e(autre)}">
<link rel="alternate" hreflang="x-default" href="{e(url_absolue(chemin if langue == 'fr' else chemin_autre))}">
<meta name="author" content="{e(SITE['auteur'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(SITE['nom'][langue])}">
<meta property="og:locale" content="{'fr_BE' if langue == 'fr' else 'nl_BE'}">
<meta property="og:title" content="{e(titre)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{e(url_absolue(og))}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(titre)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{e(url_absolue(og))}">
<meta name="theme-color" content="#12151c">
<link rel="icon" href="{e(racine)}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{e(racine)}assets/og/accueil.png">
<link rel="manifest" href="{e(racine)}manifeste.webmanifest">
<link rel="alternate" type="application/atom+xml" title="{e(SITE['nom'][langue])}" href="{e(racine)}flux.xml">
<link rel="stylesheet" href="{e(racine)}assets/css/style.css">{css_sup}
{ld}
</head>
<body>
<a class="saut" href="#contenu">{e(SAUT[langue])}</a>
<header class="entete">
  <div class="bandeau">
    <a class="marque" href="{e(base)}">{e(SITE['nom'][langue])}</a>
    <nav class="principale" aria-label="{'Navigation principale' if langue == 'fr' else 'Hoofdnavigatie'}">
      <ul>{liens_nav}</ul>
    </nav>
    <a class="langue" href="{e(autre)}" hreflang="{lang_code}" lang="{lang_code}">{e(lang_nom)}</a>
  </div>
  {fil_html}
</header>
<main id="contenu">
{corps}
</main>
<footer class="pied">
  <p class="pied-liens">{liens_pied}</p>
  <p>{e(pied['licence'])}</p>
  <p>{e(pied['maj'])} : <time datetime="{e(SITE['date_maj'])}">{e(SITE['date_maj'])}</time> ·
     <a href="{e(SITE['depot'])}" rel="noopener">{e(pied['depot'])}</a></p>
</footer>
{js}
</body>
</html>
"""
