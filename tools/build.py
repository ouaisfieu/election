# -*- coding: utf-8 -*-
"""Construction du site. Aucun HTML n'existe hors de ce processus."""
import json
import os
import shutil
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "tools"))

from config import SITE
from gabarit import page, url_absolue, e
import pages as P
import donnees_scrutins as ds
import donnees_sources as dsrc
import donnees_actualites as dact
import donnees_glossaire as dglo
import donnees_campagne as dca
import donnees_coalition as dco
import moteur
import export_donnees

SORTIE = RACINE


def ecrire(chemin_rel, contenu):
    dest = os.path.join(SORTIE, chemin_rel, "index.html") if chemin_rel.endswith("/") or chemin_rel == "" \
        else os.path.join(SORTIE, chemin_rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(contenu)
    return dest


def controles_prealables():
    """Le build refuse de construire si un invariant est rompu."""
    # 1. cohérence des données et rétro-test
    for code, a in ds.ASSEMBLEES.items():
        moteur.verifier_assemblee(a)
    # 2. toute source citée existe, toute source du registre est citée
    citees = set()
    for x in dact.CHRONOLOGIE:
        citees.add(x["source"])
    for g in dglo.GLOSSAIRE:
        citees.add(g["source"])
    for k in dco.CONTRAINTES:
        citees.add(k["source"])
    for x in dco.EXCLUSIONS:
        citees.add(x["source"])
    for c in dco.CHANTIERS:
        citees.add(c["source"])
    import donnees_sondages as dso
    for s in dso.SONDAGES:
        citees.add(s["source"])
    inconnues = citees - set(dsrc.SOURCES)
    assert not inconnues, f"sources citées hors registre : {sorted(inconnues)}"
    # sources du registre jamais citées : autorisées seulement si citées par le texte des pages
    return citees


def controles_finaux(citees, pages_faites):
    # toute source du registre doit apparaître au moins une fois dans le HTML produit
    corpus = ""
    for chemin in pages_faites:
        with open(chemin, encoding="utf-8") as f:
            corpus += f.read()
    orphelines = []
    for code, s in dsrc.SOURCES.items():
        if code in citees:
            continue
        if s["url"] not in corpus:
            orphelines.append(code)
    assert not orphelines, ("sources au registre jamais citées : " + ", ".join(sorted(orphelines)))
    # une échéance sans issue, une issue sans report : refus
    for ech in dca.ECHEANCES:
        assert len(ech["issues"]) >= 2, f"{ech['code']} : moins de deux issues"
        for iss in ech["issues"]:
            assert iss["report"], f"{ech['code']}/{iss['code']} : report vide"
            assert iss.get("justification_fr"), f"{ech['code']}/{iss['code']} : sans justification"


def toutes_les_pages():
    """Retourne une liste de (chemin_fr, chemin_nl, fabrique)."""
    routes = []
    routes.append(("", "nl/", P.p_accueil))
    routes.append((P.CHEMINS["simulateur"][0], P.CHEMINS["simulateur"][1], P.p_simulateur))
    routes.append((P.CHEMINS["chambre"][0], P.CHEMINS["chambre"][1], P.p_chambre))
    for circ in ds.CHAMBRE["circonscriptions"]:
        routes.append((P.chemin_circ(circ["code"], "fr"), P.chemin_circ(circ["code"], "nl"),
                       (lambda c: (lambda langue: P.p_circonscription(c, langue)))(circ)))
    routes.append((P.CHEMINS["parlements"][0], P.CHEMINS["parlements"][1], P.p_parlements))
    for code in ("flamand", "wallon", "bruxellois", "germanophone"):
        routes.append((P.chemin_parlement(code, "fr"), P.chemin_parlement(code, "nl"),
                       (lambda k: (lambda langue: P.p_parlement(k, langue)))(code)))
    routes.append((P.CHEMINS["regles"][0], P.CHEMINS["regles"][1], P.p_regles))
    routes.append((P.CHEMINS["methode"][0], P.CHEMINS["methode"][1], P.p_methode))
    routes.append((P.CHEMINS["coalitions"][0], P.CHEMINS["coalitions"][1], P.p_coalitions))
    routes.append((P.CHEMINS["actualites"][0], P.CHEMINS["actualites"][1], P.p_actualites))
    routes.append((P.CHEMINS["sources"][0], P.CHEMINS["sources"][1],
                   lambda langue: P.p_sources(langue, None)))
    routes.append((P.CHEMINS["glossaire"][0], P.CHEMINS["glossaire"][1], P.p_glossaire))
    routes.append((P.CHEMINS["reseau"][0], P.CHEMINS["reseau"][1], P.p_reseau))
    return routes


def page_404(langue):
    c = ["<h1>" + P.t("Cette page n'existe pas", "Deze pagina bestaat niet", langue) + "</h1>",
         '<p class="chapeau">' + P.t(
             "L'adresse demandée n'existe pas sur ce site. Chaque page d'ici est autonome : "
             "vous pouvez repartir de n'importe laquelle.",
             "Het gevraagde adres bestaat niet op deze site.", langue) + "</p>",
         '<p><a class="bouton bouton--primaire" href="' + SITE["url"] + ("" if langue == "fr" else "nl/") + '">' +
         P.t("Retour à l'accueil", "Terug naar de start", langue) + "</a></p>"]
    return {"titre": P.t("Page introuvable — Le Scrutin", "Pagina niet gevonden — De Stembus", langue),
            "description": P.t(
                "La page demandée n'existe pas sur Le Scrutin, simulateur d'élections belges. "
                "Chaque page du site est autonome : repartez de l'accueil, du simulateur ou de "
                "n'importe quelle circonscription.",
                "De gevraagde pagina bestaat niet op De Stembus, simulator van Belgische "
                "verkiezingen. Elke pagina van de site staat op zichzelf: begin opnieuw bij de "
                "start, de simulator of eender welke kieskring.", langue),
            "corps": "\n".join(c), "fil": None, "jsonld": [], "og": "assets/og/accueil.png"}


def construire():
    citees = controles_prealables()
    export_donnees.ecrire(RACINE)
    faites = []
    entrees_sitemap = []
    titres, descriptions = {}, {}
    for chemin_fr, chemin_nl, fabrique in toutes_les_pages():
        for langue, chemin, autre in (("fr", chemin_fr, chemin_nl), ("nl", chemin_nl, chemin_fr)):
            d = fabrique(langue)
            html = page(langue=langue, chemin=chemin, chemin_autre=autre,
                        titre=d["titre"], description=d["description"], corps=d["corps"],
                        fil=d.get("fil"), jsonld=d.get("jsonld"), og_image=d.get("og"),
                        scripts=d.get("scripts"))
            faites.append(ecrire(chemin, html))
            entrees_sitemap.append((chemin, chemin_fr if langue == "nl" else chemin_nl, langue))
            assert d["titre"] not in titres, f"titre en double : {d['titre']} ({chemin} et {titres[d['titre']]})"
            titres[d["titre"]] = chemin
            assert d["description"] not in descriptions, \
                f"méta-description en double : {chemin} et {descriptions[d['description']]}"
            descriptions[d["description"]] = chemin
            assert 70 <= len(d["description"]) <= 320, \
                f"{chemin} : méta-description de {len(d['description'])} caractères"
            assert len(d["titre"]) <= 90, f"{chemin} : titre de {len(d['titre'])} caractères"

    # 404 (une par langue ; GitHub Pages sert /404.html)
    for langue, chemin in (("fr", "404.html"), ("nl", "nl/404.html")):
        d = page_404(langue)
        html = page(langue=langue, chemin="" if langue == "fr" else "nl/",
                    chemin_autre="nl/404.html" if langue == "fr" else "404.html",
                    titre=d["titre"], description=d["description"], corps=d["corps"],
                    fil=None, jsonld=[], og_image=d["og"], canonique=chemin,
                    racine_absolue=True)
        faites.append(ecrire(chemin, html))

    # sitemap
    lignes = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
              'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for chemin, autre, langue in entrees_sitemap:
        lignes.append("<url><loc>" + e(url_absolue(chemin)) + "</loc>")
        lignes.append('<xhtml:link rel="alternate" hreflang="' + langue + '" href="' +
                      e(url_absolue(chemin)) + '"/>')
        lignes.append('<xhtml:link rel="alternate" hreflang="' + ("nl" if langue == "fr" else "fr") +
                      '" href="' + e(url_absolue(autre)) + '"/>')
        lignes.append("<lastmod>" + SITE["date_maj"] + "</lastmod>")
        lignes.append("<changefreq>monthly</changefreq>")
        lignes.append("<priority>" + ("1.0" if chemin in ("", "nl/") else "0.7") + "</priority></url>")
    lignes.append("</urlset>")
    ecrire("sitemap.xml", "\n".join(lignes))

    ecrire("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: " +
           url_absolue("sitemap.xml") + "\n")

    # flux Atom : la chronologie
    entrees = sorted(dact.CHRONOLOGIE, key=lambda x: x["date"], reverse=True)[:20]
    atom = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="fr">',
            "<title>" + e(SITE["nom"]["fr"]) + "</title>",
            '<link href="' + e(url_absolue("")) + '"/>',
            '<link rel="self" href="' + e(url_absolue("flux.xml")) + '"/>',
            "<id>" + e(url_absolue("")) + "</id>",
            "<updated>" + SITE["date_maj"] + "T00:00:00Z</updated>",
            "<author><name>" + e(SITE["auteur"]) + "</name></author>"]
    for x in entrees:
        atom.append("<entry><title>" + e(x["fr"][:90]) + "</title>")
        atom.append('<link href="' + e(url_absolue(P.CHEMINS["actualites"][0])) + '"/>')
        atom.append("<id>" + e(url_absolue(P.CHEMINS["actualites"][0]) + "#" + x["date"]) + "</id>")
        atom.append("<updated>" + x["date"] + "T00:00:00Z</updated>")
        atom.append("<summary>" + e(x["fr"]) + "</summary></entry>")
    atom.append("</feed>")
    ecrire("flux.xml", "\n".join(atom))

    manifeste = {
        "name": SITE["nom"]["fr"], "short_name": SITE["nom"]["fr"],
        "start_url": "./", "display": "standalone",
        "background_color": "#0e1116", "theme_color": "#12151c",
        "lang": "fr", "description": SITE["accroche"]["fr"],
        "icons": [{"src": "assets/og/accueil.png", "sizes": "1200x630", "type": "image/png"}],
    }
    ecrire("manifeste.webmanifest", json.dumps(manifeste, ensure_ascii=False, indent=1))
    ecrire(".nojekyll", "")

    controles_finaux(citees, faites)
    return faites


if __name__ == "__main__":
    faites = construire()
    print(f"{len(faites)} fichiers HTML construits.")
