# -*- coding: utf-8 -*-
"""Vignettes sociales 1200×630, une par page, générées depuis les mêmes données."""
import os
from PIL import Image, ImageDraw, ImageFont

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RACINE, "assets", "og")

FOND = (14, 17, 22)
CARTE = (22, 27, 35)
TEXTE = (232, 236, 242)
DOUX = (168, 179, 194)
ACCENT = (224, 179, 65)
TRAIT = (43, 51, 63)

PISTES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def police(taille, gras=False):
    chemin = PISTES[0] if gras else PISTES[1]
    if not os.path.exists(chemin):
        return ImageFont.load_default()
    return ImageFont.truetype(chemin, taille)


def couper(dessin, texte, fonte, largeur):
    mots, lignes, courant = texte.split(), [], ""
    for m in mots:
        essai = (courant + " " + m).strip()
        if dessin.textlength(essai, font=fonte) <= largeur:
            courant = essai
        else:
            if courant:
                lignes.append(courant)
            courant = m
    if courant:
        lignes.append(courant)
    return lignes


def vignette(nom, surtitre, titre, sous, barres=None):
    img = Image.new("RGB", (1200, 630), FOND)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1200, 8], fill=ACCENT)
    d.text((70, 62), surtitre.upper(), font=police(24, True), fill=ACCENT)
    f = police(58, True)
    y = 118
    for ligne in couper(d, titre, f, 1060)[:3]:
        d.text((70, y), ligne, font=f, fill=TEXTE)
        y += 70
    fs = police(28)
    y += 14
    for ligne in couper(d, sous, fs, 1060)[:3]:
        d.text((70, y), ligne, font=fs, fill=DOUX)
        y += 40
    if barres:
        total = sum(v for _, v in barres) or 1
        x = 70
        largeur = 1060
        yb = 470
        for coul, v in barres:
            w = max(3, int(largeur * v / total))
            c = tuple(int(coul.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
            d.rectangle([x, yb, x + w - 2, yb + 34], fill=c)
            x += w
    d.line([(70, 556), (1130, 556)], fill=TRAIT, width=1)
    d.text((70, 574), "Le Scrutin · De Stembus — ouaisfieu.github.io/election", font=police(24), fill=DOUX)
    os.makedirs(DEST, exist_ok=True)
    img.save(os.path.join(DEST, nom + ".png"), optimize=True)
    return nom


def toutes():
    import sys
    sys.path.insert(0, os.path.join(RACINE, "tools"))
    import donnees_scrutins as ds
    import donnees_partis as dp

    def barres_de(circ):
        return [(dp.PARTIS.get(k, {}).get("couleur", "#9aa0a6"), v)
                for k, v in sorted(circ["voix"].items(), key=lambda kv: -kv[1])[:9]]

    faites = []
    total_ch = {}
    for c in ds.CHAMBRE["circonscriptions"]:
        for k, v in c["officiel"].items():
            total_ch[k] = total_ch.get(k, 0) + v
    b_ch = [(dp.PARTIS[k]["couleur"], v) for k, v in sorted(total_ch.items(), key=lambda kv: -kv[1])]

    faites.append(vignette("accueil", "Simulateur d'élections belges",
                           "Du bulletin jusqu'au gouvernement",
                           "Campagne, scrutin, coalition, législature. Clé D'Hondt, circonscription "
                           "par circonscription, sur les résultats officiels du 9 juin 2024.", b_ch))
    faites.append(vignette("simulateur", "Le simulateur", "Quatre actes, aucun tirage au sort",
                           "Six échéances datées, 729 parcours, cinq assemblées calculées le même jour.", b_ch))
    faites.append(vignette("chambre", "La Chambre des représentants",
                           "150 sièges, 11 circonscriptions",
                           "Le résultat officiel du 9 juin 2024, liste par liste et circonscription "
                           "par circonscription.", b_ch))
    faites.append(vignette("parlements", "Les parlements", "Cinq assemblées, un seul jour",
                           "Flandre 124, Wallonie 75, Bruxelles 89, Communauté germanophone 25."))
    faites.append(vignette("regles", "Les règles", "D'Hondt, seuil, apparentement, majorités",
                           "Ce que le droit électoral belge décide avant que le premier bulletin soit compté."))
    faites.append(vignette("methode", "La méthode", "Le modèle publié en entier",
                           "Données, report de voix, matrice des dix-huit issues, rétro-test sur 2024, limites."))
    faites.append(vignette("coalitions", "Les coalitions", "76, 100, et les deux groupes",
                           "Ce que chaque seuil autorise, et pourquoi une réforme de l'État est rare."))
    faites.append(vignette("actualites", "L'actualité", "Datée, sourcée, séparée en trois",
                           "Fait établi, échéance programmée, hypothèse. De juin 2024 au conclave de septembre 2026."))
    faites.append(vignette("sources", "Les sources", "Le registre complet",
                           "Chaque chiffre du site vient d'ici. Le build échoue si une source manque."))
    faites.append(vignette("glossaire", "Le glossaire", "Douze termes suffisent",
                           "Clé D'Hondt, seuil, apparentement, case de tête, groupe linguistique, loi spéciale."))
    faites.append(vignette("reseau", "Le réseau", "Six entrées, un même ensemble",
                           "L'enquête, l'action, le budget, les chiffres, la satire, la décision."))
    for c in ds.CHAMBRE["circonscriptions"]:
        faites.append(vignette("circ-" + c["code"], "Circonscription de la Chambre",
                               c["nom_fr"] + " — " + str(c["sieges"]) + " sièges",
                               f"{c['valables']:,}".replace(",", " ") + " votes valables le 9 juin 2024. "
                               "Le calcul D'Hondt déroulé, quotient par quotient.", barres_de(c)))
    for code in ("flamand", "wallon", "bruxellois", "germanophone"):
        a = ds.ASSEMBLEES[code]
        tot = {}
        for c in a["circonscriptions"]:
            for k, v in c["officiel"].items():
                tot[k] = tot.get(k, 0) + v
        b = [(dp.PARTIS[k]["couleur"], v) for k, v in sorted(tot.items(), key=lambda kv: -kv[1])]
        faites.append(vignette("parlement-" + code, "Parlement",
                               ds.NOMS_ASSEMBLEES[code]["fr"] + " — " + str(a["sieges"]) + " sièges",
                               "Composition officielle du 9 juin 2024, circonscription par "
                               "circonscription, et fiabilité du modèle.", b))
    return faites


if __name__ == "__main__":
    f = toutes()
    print(f"{len(f)} vignettes écrites dans assets/og/")
