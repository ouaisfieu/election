# -*- coding: utf-8 -*-
"""Contrôle du HTML produit. Ne construit rien : vérifie ce qui a été construit."""
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "tools"))
from config import SITE

echecs = []


def echec(fichier, message):
    echecs.append(f"{os.path.relpath(fichier, RACINE)} : {message}")


class Analyse(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.titres = []
        self.h1 = 0
        self.main = 0
        self.liens = []
        self.images = []
        self.ancres = set()
        self.balises = []
        self.dans_titre = None
        self.titre_texte = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.main += 1
        if tag == "h1":
            self.h1 += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.titres.append(int(tag[1]))
            self.dans_titre = tag
            self.titre_texte = ""
        if tag == "a" and "href" in a:
            self.liens.append(a["href"])
        if tag == "img":
            self.images.append(a)
        if "id" in a:
            self.ancres.add(a["id"])

    def handle_endtag(self, tag):
        if tag == self.dans_titre:
            self.dans_titre = None

    def handle_data(self, d):
        if self.dans_titre:
            self.titre_texte += d


def verifier():
    fichiers = sorted(glob.glob(os.path.join(RACINE, "**", "*.html"), recursive=True))
    fichiers = [f for f in fichiers if "/node_modules/" not in f]
    titres, descriptions, canoniques = {}, {}, {}
    for f in fichiers:
        with open(f, encoding="utf-8") as fh:
            html = fh.read()
        a = Analyse()
        a.feed(html)

        # titre et description
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        if not m:
            echec(f, "sans <title>")
        else:
            titre = m.group(1).strip()
            if titre in titres and "404" not in f and "404" not in titres[titre]:
                echec(f, f"titre en double avec {os.path.relpath(titres[titre], RACINE)}")
            titres[titre] = f
        m = re.search(r'<meta name="description" content="(.*?)">', html, re.S)
        if not m:
            echec(f, "sans méta-description")
        else:
            desc = m.group(1)
            if len(desc) < 60:
                echec(f, f"méta-description trop courte ({len(desc)})")
            if desc in descriptions and "404" not in f:
                echec(f, f"méta-description en double avec {os.path.relpath(descriptions[desc], RACINE)}")
            descriptions[desc] = f

        # canonique absolu et unique
        cans = re.findall(r'<link rel="canonical" href="(.*?)">', html)
        if len(cans) != 1:
            echec(f, f"{len(cans)} balise(s) canonique")
        elif not cans[0].startswith("https://"):
            echec(f, "canonique non absolu")
        elif cans[0] in canoniques and "404" not in f:
            echec(f, f"canonique en double avec {os.path.relpath(canoniques[cans[0]], RACINE)}")
        else:
            canoniques[cans[0]] = f

        # hreflang
        if len(re.findall(r'hreflang="', html)) < 3:
            echec(f, "moins de trois liens hreflang")

        # OpenGraph et existence de l'image
        og = re.search(r'<meta property="og:image" content="(.*?)">', html)
        if not og:
            echec(f, "sans og:image")
        else:
            rel = og.group(1).replace(SITE["url"].rstrip("/") + "/", "")
            if not os.path.exists(os.path.join(RACINE, rel)):
                echec(f, f"og:image déclarée mais absente du disque : {rel}")
        for prop in ("og:title", "og:description", "og:url", "twitter:card"):
            if prop not in html:
                echec(f, f"sans {prop}")

        # JSON-LD parsable
        for bloc in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            try:
                json.loads(bloc)
            except Exception as ex:
                echec(f, f"JSON-LD illisible : {ex}")

        # structure
        if a.main != 1:
            echec(f, f"{a.main} balise <main>")
        if a.h1 != 1:
            echec(f, f"{a.h1} balise <h1>")
        precedent = 0
        for n in a.titres:
            if precedent and n > precedent + 1:
                echec(f, f"saut de niveau de titre h{precedent} → h{n}")
                break
            precedent = n
        if 'class="saut"' not in html:
            echec(f, "sans lien d'évitement")
        if "lang=" not in html[:200]:
            echec(f, "sans attribut lang")

        # liens internes
        dossier = os.path.dirname(f)
        for lien in a.liens:
            if lien.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                continue
            base = lien.split("#")[0]
            if not base:
                continue
            cible = os.path.normpath(os.path.join(dossier, base))
            if os.path.isdir(cible):
                cible = os.path.join(cible, "index.html")
            if not os.path.exists(cible):
                echec(f, f"lien interne mort : {lien}")

    # sitemap cohérent
    sm = os.path.join(RACINE, "sitemap.xml")
    if not os.path.exists(sm):
        echecs.append("sitemap.xml absent")
    else:
        with open(sm, encoding="utf-8") as fh:
            contenu = fh.read()
        locs = re.findall(r"<loc>(.*?)</loc>", contenu)
        indexables = {k: v for k, v in canoniques.items() if not v.endswith("404.html")}
        if len(locs) != len(indexables):
            echecs.append(f"sitemap : {len(locs)} URL pour {len(indexables)} pages indexables")
        for loc in locs:
            if loc not in canoniques:
                echecs.append(f"sitemap : {loc} n'est la canonique d'aucune page")
    for oblige in ("robots.txt", "flux.xml", "manifeste.webmanifest", ".nojekyll"):
        if not os.path.exists(os.path.join(RACINE, oblige)):
            echecs.append(f"{oblige} absent")
    return fichiers


if __name__ == "__main__":
    fichiers = verifier()
    print(f"{len(fichiers)} pages analysées.")
    if echecs:
        for x in echecs:
            print("  ÉCHEC " + x)
        sys.exit(1)
    print("Aucun défaut.")
