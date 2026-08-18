# -*- coding: utf-8 -*-
"""Construction des pages. Un seul endroit décide du texte de chaque page."""
from gabarit import e, page, url_absolue
from config import SITE, RESEAU_INDEX
import donnees_partis as dp
import donnees_scrutins as ds
import donnees_sondages as dso
import donnees_campagne as dca
import donnees_coalition as dco
import donnees_legislature as dle
import donnees_sources as dsrc
import donnees_glossaire as dglo
import donnees_actualites as dact
import donnees_reseau as dres
from moteur import dhondt, retro_test, tableau_dhondt

L = ["fr", "nl"]

# Chemins : (fr, nl) pour chaque page nommée.
CHEMINS = {
    "accueil": ("", "nl/"),
    "simulateur": ("simulateur/", "nl/simulator/"),
    "chambre": ("chambre/", "nl/kamer/"),
    "parlements": ("parlements/", "nl/parlementen/"),
    "regles": ("regles/", "nl/regels/"),
    "methode": ("methode/", "nl/methode/"),
    "coalitions": ("coalitions/", "nl/coalities/"),
    "actualites": ("actualites/", "nl/actualiteit/"),
    "sources": ("sources/", "nl/bronnen/"),
    "glossaire": ("glossaire/", "nl/woordenlijst/"),
    "reseau": ("reseau/", "nl/netwerk/"),
}


def chemin(nom, langue):
    return CHEMINS[nom][0 if langue == "fr" else 1]


def chemin_circ(code, langue):
    return ("chambre/" + code + "/") if langue == "fr" else ("nl/kamer/" + code + "/")


def chemin_parlement(code, langue):
    return ("parlements/" + code + "/") if langue == "fr" else ("nl/parlementen/" + code + "/")


def t(fr, nl, langue):
    return fr if langue == "fr" else nl


def nom_parti(code):
    p = dp.PARTIS.get(code)
    return p["nom"] if p else code


def couleur(code):
    p = dp.PARTIS.get(code)
    return p["couleur"] if p else "#9aa0a6"


def nombre(n, langue="fr"):
    s = f"{int(round(n)):,}".replace(",", " ")
    return s


def pct(x):
    return f"{x:.2f}".replace(".", ",") + " %"


def og_pour(nom):
    return "assets/og/" + nom + ".png"


# --------------------------------------------------------------------- outils
def table_resultat(circ, seuil, langue):
    total = circ["valables"]
    lignes = sorted(circ["voix"].items(), key=lambda kv: -kv[1])
    sieges = circ["officiel"]
    out = ['<div class="defile"><table>']
    out.append("<caption>" + t(
        f"Résultat officiel du 9 juin 2024 — {circ['nom_fr']}, {circ['sieges']} sièges, "
        f"{nombre(total)} votes valables. Le seuil de {int(seuil*100)} % écarte les listes en gris.",
        f"Officiële uitslag van 9 juni 2024 — {circ['nom_nl']}, {circ['sieges']} zetels, "
        f"{nombre(total)} geldige stemmen.", langue) + "</caption>")
    out.append("<thead><tr><th>" + t("Liste", "Lijst", langue) +
               '</th><th class="n">' + t("Voix", "Stemmen", langue) +
               '</th><th class="n">%</th><th class="n">' + t("Sièges", "Zetels", langue) +
               "</th></tr></thead><tbody>")
    for code, v in lignes:
        part = 100 * v / total
        sous = part < seuil * 100
        s = sieges.get(code, 0)
        style = ' style="color:var(--doux)"' if sous and not s else ""
        out.append(
            f'<tr{style}><td><span class="pastille" style="background:{couleur(code)}"></span>'
            f"{e(nom_parti(code))}</td>"
            f'<td class="n">{nombre(v)}</td><td class="n">{pct(part)}</td>'
            f'<td class="n">{s if s else "—"}</td></tr>')
    out.append("</tbody></table></div>")
    return "".join(out)


def hemicycle(sieges, langue):
    ordre = sorted(sieges.items(), key=lambda kv: -kv[1])
    pts = []
    for code, n in ordre:
        for _ in range(n):
            pts.append(f'<span class="siege" style="background:{couleur(code)}"></span>')
    total = sum(sieges.values())
    leg = " ".join(
        f'<span style="white-space:nowrap"><span class="pastille" style="background:{couleur(c)}"></span>'
        f"{e(nom_parti(c))} {n}</span>" for c, n in ordre if n)
    return ('<div class="hemicycle" role="img" aria-label="' +
            t(f"{total} sièges répartis : ", f"{total} zetels verdeeld: ", langue) +
            e(", ".join(f"{nom_parti(c)} {n}" for c, n in ordre if n)) + '">' +
            "".join(pts) + "</div><p style=\"font-size:.82rem;color:var(--doux)\">" + leg + "</p>")


# ------------------------------------------------------------------- accueil
def p_accueil(langue):
    chambre = ds.CHAMBRE
    ecart_w, _ = retro_test(ds.PARLEMENT_WALLON)
    corps = []
    corps.append("<h1>" + t(
        "Simuler une élection belge, du bulletin jusqu'au gouvernement",
        "Een Belgische verkiezing simuleren, van het stembiljet tot de regering", langue) + "</h1>")
    corps.append('<p class="chapeau">' + t(
        "Quatre actes : la campagne jusqu'en 2029, le scrutin fédéral et régional le même jour, "
        "la formation d'une coalition, puis la législature. Le calcul est le vrai calcul belge — "
        "clé D'Hondt, circonscription par circonscription, seuil de 5 %, groupes linguistiques — "
        "appliqué aux résultats officiels du 9 juin 2024. Aucun tirage au sort, aucun compte, "
        "aucun traceur.",
        "Vier bedrijven: de campagne tot 2029, de federale en regionale stembusgang op dezelfde dag, "
        "de coalitievorming, en dan de legislatuur. De berekening is de echte Belgische berekening — "
        "D'Hondt, kieskring per kieskring, 5 %-drempel, taalgroepen — toegepast op de officiële "
        "uitslag van 9 juni 2024.", langue) + "</p>")
    corps.append('<p><a class="bouton bouton--primaire" href="' +
                 e(chemin("simulateur", langue).replace("nl/", "")) + '">' +
                 t("Commencer la simulation", "De simulatie starten", langue) + "</a> " +
                 '<a class="bouton" href="' +
                 e(chemin("methode", langue).replace("nl/", "")) + '">' +
                 t("Lire la méthode d'abord", "Eerst de methode lezen", langue) + "</a></p>")

    corps.append('<div class="chiffres">')
    for val, lab in [
        ("150", t("sièges à la Chambre, en 11 circonscriptions", "Kamerzetels, in 11 kieskringen", langue)),
        ("313", t("sièges simulés au total, cinq assemblées", "gesimuleerde zetels in totaal, vijf assemblees", langue)),
        ("729", t("parcours de campagne possibles", "mogelijke campagnetrajecten", langue)),
        ("0", t("siège d'écart au rétro-test de la Chambre 2024", "zetels afwijking bij de terugtest van de Kamer 2024", langue)),
    ]:
        corps.append(f'<div class="chiffre"><b>{val}</b><span>{lab}</span></div>')
    corps.append("</div>")

    corps.append("<h2>" + t("Ce que fait ce site", "Wat deze site doet", langue) + "</h2>")
    corps.append('<div class="grille">')
    cartes = [
        (t("Il calcule, il ne prédit pas", "Hij rekent, hij voorspelt niet", langue),
         t("Le modèle applique un report de voix que <em>vous</em> choisissez, à partir d'un point "
           "de départ que <em>vous</em> choisissez — le vote de 2024 ou l'une des trois enquêtes "
           "publiées en 2026. Le site ne dit jamais ce qui va arriver.",
           "Het model past een stemverschuiving toe die <em>u</em> kiest, vanuit een startpunt dat "
           "<em>u</em> kiest — de stem van 2024 of een van de drie peilingen van 2026.", langue)),
        (t("Il ne dit jamais pour qui voter", "Hij zegt nooit op wie te stemmen", langue),
         t("Aucun parti n'est classé, noté ou recommandé. Les exclusions — cordon sanitaire compris — "
           "sont présentées comme des faits publics datés, et c'est vous qui décidez si vous les "
           "tenez pour encore valables en 2029.",
           "Geen enkele partij wordt gerangschikt of aanbevolen. Uitsluitingen — inclusief het cordon "
           "sanitaire — zijn gedateerde publieke feiten; u beslist of ze in 2029 nog gelden.", langue)),
        (t("Il publie ses erreurs", "Hij publiceert zijn fouten", langue),
         t(f"Le moteur reproduit la proclamation de 2024 <strong>siège pour siège</strong> à la "
           f"Chambre, au Parlement flamand et au Parlement germanophone. Au Parlement wallon, il "
           f"place {ecart_w} sièges ailleurs que la proclamation, parce qu'il n'implémente pas "
           f"l'apparentement provincial. C'est écrit sur la page Méthode.",
           f"De motor reproduceert de uitslag van 2024 <strong>zetel voor zetel</strong> in de Kamer, "
           f"het Vlaams Parlement en het Duitstalige Parlement. In het Waals Parlement plaatst hij "
           f"{ecart_w} zetels anders, omdat de provinciale lijstenverbinding niet is geïmplementeerd.", langue)),
        (t("Il tient dans une page", "Hij past in één pagina", langue),
         t("HTML, CSS et JavaScript, rien d'autre. Tout le contenu est lisible sans JavaScript ; "
           "seul le simulateur en a besoin. Rien ne quitte votre navigateur.",
           "HTML, CSS en JavaScript, meer niet. Alle inhoud is leesbaar zonder JavaScript.", langue)),
    ]
    for titre, texte in cartes:
        corps.append(f'<div class="carte"><h3>{titre}</h3><p>{texte}</p></div>')
    corps.append("</div>")

    corps.append("<h2>" + t("Par où entrer", "Waar te beginnen", langue) + "</h2>")
    corps.append('<div class="grille">')
    entrees = [
        (chemin("simulateur", langue), t("Le simulateur", "De simulator", langue),
         t("Les quatre actes, de septembre 2026 à 2034.", "De vier bedrijven, van september 2026 tot 2034.", langue)),
        (chemin("chambre", langue), t("La Chambre, circonscription par circonscription", "De Kamer, kieskring per kieskring", langue),
         t("Onze pages, une par circonscription : le résultat de 2024 et le calcul D'Hondt déroulé.",
           "Elf pagina's, één per kieskring: de uitslag van 2024 en de D'Hondt-berekening.", langue)),
        (chemin("parlements", langue), t("Les parlements de région et de communauté", "De gewest- en gemeenschapsparlementen", langue),
         t("Flandre, Wallonie, Bruxelles et la Communauté germanophone, élus le même jour.",
           "Vlaanderen, Wallonië, Brussel en de Duitstalige Gemeenschap, op dezelfde dag verkozen.", langue)),
        (chemin("regles", langue), t("Les règles du scrutin belge", "De regels van de Belgische stembusgang", langue),
         t("D'Hondt, seuil, apparentement, case de tête, groupes linguistiques, article 46.",
           "D'Hondt, drempel, lijstenverbinding, lijststem, taalgroepen, artikel 46.", langue)),
        (chemin("coalitions", langue), t("L'arithmétique des coalitions", "De rekenkunde van coalities", langue),
         t("76 sièges, deux tiers, majorité dans chaque groupe : ce que chaque chiffre autorise.",
           "76 zetels, twee derde, meerderheid in elke taalgroep.", langue)),
        (chemin("actualites", langue), t("L'actualité, datée et sourcée", "De actualiteit, gedateerd en gebronnnd", langue),
         t("De juin 2024 au conclave de septembre 2026, fait par fait.",
           "Van juni 2024 tot het conclaaf van september 2026, feit na feit.", langue)),
    ]
    for lien, titre, txt in entrees:
        lien2 = lien.replace("nl/", "")
        corps.append(f'<div class="carte carte--accent"><h3><a href="{e(lien2)}">{e(titre)}</a></h3><p>{txt}</p></div>')
    corps.append("</div>")

    jsonld = [
        {"@context": "https://schema.org", "@type": "WebSite",
         "name": SITE["nom"][langue], "url": url_absolue(chemin("accueil", langue)),
         "inLanguage": langue,
         "description": t("Simulateur d'élections belges fédérales et régionales, fondé sur les "
                          "résultats officiels du 9 juin 2024 et la clé D'Hondt.",
                          "Simulator van Belgische federale en regionale verkiezingen.", langue)},
        {"@context": "https://schema.org", "@type": "Game",
         "name": SITE["nom"][langue], "url": url_absolue(chemin("simulateur", langue)),
         "genre": t("simulation électorale", "verkiezingssimulatie", langue),
         "inLanguage": langue, "isAccessibleForFree": True,
         "numberOfPlayers": {"@type": "QuantitativeValue", "value": 1}},
    ]
    return {
        "titre": t("Le Scrutin — simulateur d'élections belges, fédérales et régionales",
                   "De Stembus — simulator van Belgische verkiezingen", langue),
        "description": t("Simulez les élections fédérales et régionales belges de 2029 : campagne, "
                         "scrutin à la clé D'Hondt circonscription par circonscription, formation de "
                         "coalition et législature. Données officielles du 9 juin 2024.",
                         "Simuleer de Belgische federale en regionale verkiezingen van 2029: campagne, "
                         "zetelverdeling volgens D'Hondt, coalitievorming en legislatuur.", langue),
        "corps": "\n".join(corps), "fil": None, "jsonld": jsonld, "og": og_pour("accueil"),
    }


# ---------------------------------------------------------------- simulateur
def p_simulateur(langue):
    c = []
    c.append("<h1>" + t("Le simulateur", "De simulator", langue) + "</h1>")
    c.append('<p class="chapeau">' + t(
        "Quatre actes. Vous choisissez un point de départ, six issues d'échéances réelles, une "
        "coalition et un accord de gouvernement. Le reste est de l'arithmétique, et elle est "
        "affichée. Tout tient dans cette page ; rien n'est envoyé nulle part.",
        "Vier bedrijven. U kiest een startpunt, zes uitkomsten van reële ijkmomenten, een coalitie "
        "en een regeerakkoord. De rest is rekenkunde, en die staat op het scherm.", langue) + "</p>")
    c.append('<noscript><p class="sansjs">' + t(
        "Le simulateur a besoin de JavaScript pour calculer. Sans lui, cette page reste lisible : "
        "les six échéances, leurs issues et le report de voix que le modèle associe à chacune sont "
        "écrits ci-dessous, et la page Méthode publie le calcul complet.",
        "De simulator heeft JavaScript nodig om te rekenen. Zonder JavaScript blijft deze pagina "
        "leesbaar: de zes ijkmomenten, hun uitkomsten en de bijhorende stemverschuiving staan hieronder.",
        langue) + "</p></noscript>")

    # --- acte 0 : point de départ
    c.append('<section class="acte" id="depart"><span class="numero">' +
             t("Avant de commencer", "Vooraf", langue) + "</span>")
    c.append("<h2>" + t("Le point de départ", "Het startpunt", langue) + "</h2>")
    c.append("<p>" + t(
        "Un sondage n'est pas une prévision. Choisir celui de mars ou celui de juin 2026 change le "
        "résultat de plusieurs dizaines de sièges : c'est précisément ce que le simulateur veut "
        "rendre visible.",
        "Een peiling is geen voorspelling. De keuze tussen die van maart of juni 2026 verandert de "
        "uitslag met tientallen zetels.", langue) + "</p>")
    c.append('<fieldset><legend>' + t("Point de départ", "Startpunt", langue) + '</legend><div class="choix">')
    for s in dso.SONDAGES:
        coche = " checked" if s["code"] == dso.SONDAGE_DEFAUT else ""
        c.append(
            f'<label><input type="radio" name="depart" value="{e(s["code"])}"{coche}> '
            f'<span><strong>{e(t(s["nom_fr"], s["nom_nl"], langue))}</strong>'
            f'<small>{e(t(s["institut_fr"], s["institut_nl"], langue))} — '
            f'{e(t(s["note_fr"], s["note_nl"], langue))}</small></span></label>')
    c.append("</div></fieldset></section>")

    # --- acte I : la campagne
    c.append('<section class="acte" id="campagne"><span class="numero">' +
             t("Acte I", "Bedrijf I", langue) + "</span>")
    c.append("<h2>" + t("La campagne : six échéances, de septembre 2026 à 2029",
                        "De campagne: zes ijkmomenten, van september 2026 tot 2029", langue) + "</h2>")
    c.append("<p>" + t(
        "Chaque échéance est datée et documentée. Aucune issue n'est présentée comme souhaitable ni "
        "comme probable. À côté de chacune, le report de voix que le modèle lui associe, en points "
        "de pourcentage, avec sa bande d'incertitude et sa justification.",
        "Elk ijkmoment is gedateerd en gedocumenteerd. Geen enkele uitkomst wordt als wenselijk of "
        "waarschijnlijk voorgesteld.", langue) + "</p>")
    for i, ech in enumerate(dca.ECHEANCES, 1):
        c.append(f'<fieldset id="ech-{e(ech["code"])}"><legend>{i}. '
                 f'{e(t(ech["titre_fr"], ech["titre_nl"], langue))} — '
                 f'<time datetime="{e(ech["date"])}">{e(ech["date"])}</time></legend>')
        c.append("<p>" + e(t(ech["contexte_fr"], ech["contexte_nl"], langue)) + "</p>")
        c.append('<div class="choix">')
        for j, iss in enumerate(ech["issues"]):
            coche = " checked" if j == 0 else ""
            rep = []
            for reg in ("fl", "wa", "bxl"):
                if reg not in iss["report"]:
                    continue
                items = ", ".join(
                    f"{nom_parti(k)} {'+' if v > 0 else '−'}{abs(v):.1f}".replace(".", ",")
                    for k, v in sorted(iss["report"][reg].items(), key=lambda kv: -abs(kv[1])))
                nom_reg = {"fl": t("Flandre", "Vlaanderen", langue),
                           "wa": t("Wallonie", "Wallonië", langue),
                           "bxl": t("Bruxelles", "Brussel", langue)}[reg]
                rep.append(f"<strong>{nom_reg}</strong> : {e(items)}")
            c.append(
                f'<label><input type="radio" name="{e(ech["code"])}" value="{e(iss["code"])}"{coche}> '
                f'<span><strong>{e(t(iss["titre_fr"], iss["titre_nl"], langue))}</strong>'
                f'<small>{e(t(iss["resume_fr"], iss["resume_nl"], langue))}</small>'
                f'<small style="margin-top:.4rem">' + " · ".join(rep) +
                f' — {t("bande", "marge", langue)} ±{str(iss["bande"]).replace(".", ",")} '
                f'{t("point", "punt", langue)}. {e(t(iss["justification_fr"], iss["justification_nl"], langue))}'
                f"</small></span></label>")
        c.append("</div></fieldset>")
    c.append("</section>")

    # --- acte II : le scrutin
    c.append('<section class="acte" id="scrutin"><span class="numero">' +
             t("Acte II", "Bedrijf II", langue) + "</span>")
    c.append("<h2>" + t("Le scrutin", "De stembusgang", langue) + "</h2>")
    c.append("<p>" + t(
        "Le report est appliqué à chaque circonscription, proportionnellement à la part de 2024 de "
        "chaque liste dans sa région ; la circonscription est renormalisée, puis la clé D'Hondt est "
        "appliquée avec le seuil de 5 %. Cinq assemblées sont calculées le même jour.",
        "De verschuiving wordt op elke kieskring toegepast, evenredig met het aandeel van 2024 in "
        "het gewest; daarna wordt D'Hondt toegepast met de 5 %-drempel.", langue) + "</p>")
    c.append('<div id="resultat-scrutin" aria-live="polite"></div>')
    c.append("</section>")

    # --- acte III : la formation
    c.append('<section class="acte" id="formation"><span class="numero">' +
             t("Acte III", "Bedrijf III", langue) + "</span>")
    c.append("<h2>" + t("La formation", "De vorming", langue) + "</h2>")
    c.append("<p>" + t(
        "Le site n'écarte aucune coalition de lui-même. Il vous demande quelles exclusions vous "
        "tenez pour valables en 2029, puis il énumère toutes les combinaisons majoritaires et "
        "affiche, pour chacune, ce que son arithmétique autorise.",
        "De site sluit zelf geen enkele coalitie uit. Hij vraagt welke uitsluitingen u geldig acht, "
        "en somt dan alle meerderheidscombinaties op.", langue) + "</p>")
    c.append('<fieldset><legend>' + t("Exclusions déclarées", "Verklaarde uitsluitingen", langue) + '</legend><div class="choix">')
    for x in dco.EXCLUSIONS:
        coche = " checked" if x["defaut"] else ""
        c.append(
            f'<label><input type="checkbox" name="exclusion" value="{e(x["code"])}"{coche}> '
            f'<span><strong>{e(t(x["titre_fr"], x["titre_nl"], langue))}</strong>'
            f'<small>{e(t(x["fait_fr"], x["fait_nl"], langue))}</small></span></label>')
    c.append("</div></fieldset>")
    c.append('<div id="resultat-coalitions" aria-live="polite"></div>')
    c.append("</section>")

    # --- acte IV : la législature
    c.append('<section class="acte" id="legislature"><span class="numero">' +
             t("Acte IV", "Bedrijf IV", langue) + "</span>")
    c.append("<h2>" + t("La législature", "De legislatuur", langue) + "</h2>")
    c.append("<p>" + t(
        "Huit chantiers. Chacun porte la charge normative qu'il exige réellement : une loi ordinaire, "
        "une loi spéciale — majorité dans chaque groupe linguistique et deux tiers — ou une révision "
        "de la Constitution. Un chantier que votre coalition ne peut pas porter est refusé, et le "
        "procès-verbal le dit.",
        "Acht werven. Elk draagt de normatieve last die het werkelijk vereist: een gewone wet, een "
        "bijzondere wet, of een grondwetsherziening.", langue) + "</p>")
    c.append('<fieldset><legend>' + t("Les chantiers de l'accord", "De werven van het akkoord", langue) + '</legend><div class="choix" id="chantiers">')
    norme_nom = {"loi": t("loi ordinaire", "gewone wet", langue),
                 "loi-speciale": t("loi spéciale — art. 4", "bijzondere wet — art. 4", langue),
                 "revision": t("révision — art. 195", "herziening — art. 195", langue)}
    for ch in dco.CHANTIERS:
        c.append(
            f'<label><input type="checkbox" name="chantier" value="{e(ch["code"])}"> '
            f'<span><strong>{e(t(ch["titre_fr"], ch["titre_nl"], langue))}</strong>'
            f'<small><span class="etiquette">{e(norme_nom[ch["norme"]])}</span> '
            f'{e(t(ch["cout_fr"], ch["cout_nl"], langue))}</small></span></label>')
    c.append("</div></fieldset>")
    c.append('<div id="resultat-legislature" aria-live="polite"></div>')
    c.append("</section>")

    # --- procès-verbal
    c.append('<section class="acte" id="proces-verbal"><span class="numero">' +
             t("Le procès-verbal", "Het proces-verbaal", langue) + "</span>")
    c.append("<h2>" + t("Tout le calcul, ligne par ligne", "De volledige berekening, regel per regel", langue) + "</h2>")
    c.append('<p><button type="button" id="imprimer">' + t("Imprimer le procès-verbal", "Het proces-verbaal afdrukken", langue) +
             '</button> <button type="button" id="copier-lien">' +
             t("Copier le lien de cette partie", "De link van deze partij kopiëren", langue) + "</button></p>")
    c.append('<div id="pv" aria-live="polite"></div>')
    c.append("</section>")

    quiz = {"@context": "https://schema.org", "@type": "Game",
            "name": t("Le Scrutin — le simulateur", "De Stembus — de simulator", langue),
            "url": url_absolue(chemin("simulateur", langue)),
            "inLanguage": langue, "isAccessibleForFree": True,
            "gamePlatform": "Web", "applicationCategory": "GameApplication",
            "description": t("Quatre actes : campagne, scrutin, coalition, législature.",
                             "Vier bedrijven: campagne, stembusgang, coalitie, legislatuur.", langue)}
    return {
        "titre": t("Le simulateur : campagne, scrutin, coalition, législature — Le Scrutin",
                   "De simulator: campagne, stembusgang, coalitie, legislatuur — De Stembus", langue),
        "description": t("Simulez les élections belges de 2029 en quatre actes : six échéances "
                         "datées, la répartition des sièges à la clé D'Hondt, la formation d'une "
                         "coalition et la législature qui suit.",
                         "Simuleer de Belgische verkiezingen van 2029 in vier bedrijven: zes "
                         "gedateerde ijkmomenten, de zetelverdeling volgens D'Hondt, de "
                         "coalitievorming en de legislatuur.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (None, t("Le simulateur", "De simulator", langue))],
        "jsonld": [quiz], "og": og_pour("simulateur"),
        "scripts": ["assets/data/donnees.js", "assets/js/moteur.js", "assets/js/jeu.js"],
    }


# ------------------------------------------------------------------- Chambre
def p_chambre(langue):
    a = ds.CHAMBRE
    c = []
    c.append("<h1>" + t("La Chambre des représentants, circonscription par circonscription",
                        "De Kamer van volksvertegenwoordigers, kieskring per kieskring", langue) + "</h1>")
    c.append('<p class="chapeau">' + t(
        "150 sièges, onze circonscriptions provinciales, un seuil de 5 % par circonscription et la "
        "clé D'Hondt. Depuis 2003, il n'y a plus d'apparentement à la Chambre : chaque province "
        "compte pour elle-même, ce qui pénalise les petites listes dans les petites circonscriptions.",
        "150 zetels, elf provinciale kieskringen, een drempel van 5 % per kieskring en de D'Hondt-sleutel. "
        "Sinds 2003 is er geen lijstenverbinding meer in de Kamer.", langue) + "</p>")
    total = {}
    for circ in a["circonscriptions"]:
        for k, v in circ["officiel"].items():
            total[k] = total.get(k, 0) + v
    c.append("<h2>" + t("Le résultat du 9 juin 2024", "De uitslag van 9 juni 2024", langue) + "</h2>")
    c.append(hemicycle(total, langue))
    c.append('<div class="defile"><table><caption>' + t(
        "Sièges par liste et par circonscription. Les colonnes sont les circonscriptions, dans "
        "l'ordre alphabétique français.",
        "Zetels per lijst en per kieskring.", langue) + "</caption>")
    circs = a["circonscriptions"]
    c.append("<thead><tr><th>" + t("Liste", "Lijst", langue) + "</th>" +
             "".join(f'<th class="n" title="{e(x["nom_fr"])}">{e(x["nom_fr"][:4])}.</th>' for x in circs) +
             '<th class="n">' + t("Total", "Totaal", langue) + "</th></tr></thead><tbody>")
    for code, n in sorted(total.items(), key=lambda kv: -kv[1]):
        cells = "".join(f'<td class="n">{x["officiel"].get(code, 0) or "—"}</td>' for x in circs)
        c.append(f'<tr><td><span class="pastille" style="background:{couleur(code)}"></span>'
                 f'{e(nom_parti(code))}</td>{cells}<td class="n"><strong>{n}</strong></td></tr>')
    c.append("</tbody></table></div>")

    c.append("<h2>" + t("Les onze circonscriptions", "De elf kieskringen", langue) + "</h2>")
    c.append('<div class="grille">')
    for circ in circs:
        nom = circ["nom_fr"] if langue == "fr" else circ["nom_nl"]
        prem = max(circ["officiel"].items(), key=lambda kv: kv[1])
        lien = circ["code"] + "/"
        c.append(f'<div class="carte"><h3><a href="{e(lien)}">{e(nom)}</a></h3>'
                 f'<p>{circ["sieges"]} ' + t("sièges", "zetels", langue) + " · " +
                 nombre(circ["valables"]) + " " + t("votes valables", "geldige stemmen", langue) +
                 f'<br>{t("Première liste", "Grootste lijst", langue)} : '
                 f'<span class="pastille" style="background:{couleur(prem[0])}"></span>'
                 f'{e(nom_parti(prem[0]))} ({prem[1]})</p></div>')
    c.append("</div>")
    c.append('<p><a class="bouton" href="' + e("../" + chemin("regles", langue).replace("nl/", "")) + '">' +
             t("Comment les sièges sont attribués", "Hoe de zetels worden toegekend", langue) + "</a></p>")
    return {
        "titre": t("La Chambre des représentants : 150 sièges, 11 circonscriptions — Le Scrutin",
                   "De Kamer: 150 zetels, 11 kieskringen — De Stembus", langue),
        "description": t("Le résultat officiel du 9 juin 2024 à la Chambre, liste par liste et "
                         "circonscription par circonscription, avec le calcul D'Hondt et le seuil de 5 %.",
                         "De officiële uitslag van 9 juni 2024 in de Kamer, lijst per lijst en kieskring per "
                         "kieskring, met de D'Hondt-berekening en de drempel van 5 procent.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (None, t("La Chambre", "De Kamer", langue))],
        "jsonld": [{"@context": "https://schema.org", "@type": "Dataset",
                    "name": t("Chambre des représentants 2024 — résultats par circonscription",
                              "Kamer 2024 — uitslagen per kieskring", langue),
                    "inLanguage": langue,
                    "creator": {"@type": "GovernmentOrganization", "name": "SPF Intérieur — Direction des Élections"},
                    "temporalCoverage": "2024-06-09",
                    "license": "https://creativecommons.org/licenses/by-sa/4.0/",
                    "url": url_absolue(chemin("chambre", langue))}],
        "og": og_pour("chambre"),
    }


def p_circonscription(circ, langue):
    a = ds.CHAMBRE
    nom = circ["nom_fr"] if langue == "fr" else circ["nom_nl"]
    c = []
    c.append(f"<h1>{e(nom)} — " + t("circonscription de la Chambre", "kieskring van de Kamer", langue) + "</h1>")
    c.append('<p class="chapeau">' + t(
        f"{circ['sieges']} sièges sur 150. {nombre(circ['valables'])} votes valables le 9 juin 2024. "
        f"Le seuil d'éligibilité y vaut {nombre(circ['valables'] * 0.05)} voix.",
        f"{circ['sieges']} van de 150 zetels. {nombre(circ['valables'])} geldige stemmen op 9 juni 2024. "
        f"De kiesdrempel bedraagt er {nombre(circ['valables'] * 0.05)} stemmen.", langue) + "</p>")
    c.append(table_resultat(circ, a["seuil"], langue))

    c.append("<h2>" + t("Le calcul, déroulé", "De berekening, uitgerold", langue) + "</h2>")
    c.append("<p>" + t(
        "Chaque siège va au quotient le plus élevé. Voici la suite exacte des quotients qui ont "
        "attribué les sièges de cette circonscription, dans l'ordre.",
        "Elke zetel gaat naar het hoogste quotiënt. Hier is de exacte reeks quotiënten.", langue) + "</p>")
    suite = tableau_dhondt(circ["voix"], circ["sieges"], a["seuil"])
    c.append('<div class="defile"><table><thead><tr><th class="n">#</th><th>' +
             t("Liste", "Lijst", langue) + '</th><th class="n">' +
             t("Diviseur", "Deler", langue) + '</th><th class="n">' +
             t("Quotient", "Quotiënt", langue) + "</th></tr></thead><tbody>")
    for x in suite:
        c.append(f'<tr><td class="n">{x["rang"]}</td>'
                 f'<td><span class="pastille" style="background:{couleur(x["liste"])}"></span>'
                 f'{e(nom_parti(x["liste"]))}</td>'
                 f'<td class="n">÷{x["diviseur"]}</td>'
                 f'<td class="n">{nombre(x["quotient"])}</td></tr>')
    c.append("</tbody></table></div>")
    # le siège suivant : ce que le seuil et la taille coûtent
    suite_plus = tableau_dhondt(circ["voix"], circ["sieges"] + 1, a["seuil"])
    suivant = suite_plus[-1]
    c.append('<div class="encart"><p>' + t(
        f"S'il y avait eu un siège de plus dans cette circonscription, il serait allé à "
        f"{nom_parti(suivant['liste'])}, avec un quotient de {nombre(suivant['quotient'])}. "
        f"C'est la mesure la plus concrète de ce que la taille d'une circonscription décide.",
        f"Was er één zetel meer geweest, dan was die naar {nom_parti(suivant['liste'])} gegaan, "
        f"met een quotiënt van {nombre(suivant['quotient'])}.", langue) + "</p></div>")

    autres = [x for x in a["circonscriptions"] if x["code"] != circ["code"]]
    c.append("<h2>" + t("Les autres circonscriptions", "De andere kieskringen", langue) + "</h2>")
    c.append("<p>" + " · ".join(
        f'<a href="../{e(x["code"])}/">{e(x["nom_fr"] if langue == "fr" else x["nom_nl"])}</a>'
        for x in autres) + "</p>")

    return {
        "titre": t(f"{nom} : résultats 2024 et calcul D'Hondt — Le Scrutin",
                   f"{nom}: uitslag 2024 en D'Hondt-berekening — De Stembus", langue),
        "description": t(
            f"Circonscription de {nom}, {circ['sieges']} sièges à la Chambre : résultat officiel du "
            f"9 juin 2024, liste par liste, et la suite complète des quotients D'Hondt.",
            f"Kieskring {nom}, {circ['sieges']} Kamerzetels: officiële uitslag van 9 juni 2024 en de "
            f"volledige reeks D'Hondt-quotiënten.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (chemin("chambre", langue) if langue == "fr" else "nl/kamer/", t("La Chambre", "De Kamer", langue)),
                (None, nom)],
        "jsonld": [{"@context": "https://schema.org", "@type": "Article",
                    "headline": t(f"{nom} : résultats 2024 et calcul D'Hondt",
                                  f"{nom}: uitslag 2024 en D'Hondt-berekening", langue),
                    "inLanguage": langue, "datePublished": SITE["date_publication"],
                    "dateModified": SITE["date_maj"],
                    "author": {"@type": "Organization", "name": SITE["auteur"]},
                    "isPartOf": {"@type": "WebSite", "name": SITE["nom"][langue],
                                 "url": url_absolue(chemin("accueil", langue))},
                    "url": url_absolue(chemin_circ(circ["code"], langue))}],
        "og": og_pour("circ-" + circ["code"]),
    }


# --------------------------------------------------------------- parlements
def p_parlements(langue):
    c = []
    c.append("<h1>" + t("Les parlements élus le même jour",
                        "De parlementen die op dezelfde dag worden verkozen", langue) + "</h1>")
    c.append('<p class="chapeau">' + t(
        "Le même bulletin, le même jour, cinq assemblées : la Chambre, le Parlement flamand, le "
        "Parlement wallon, le Parlement bruxellois et le Parlement de la Communauté germanophone. "
        "Chacune a ses circonscriptions, son seuil et, pour la Wallonie, un apparentement "
        "provincial que ce simulateur n'implémente pas — et le dit.",
        "Dezelfde dag, vijf assemblees: de Kamer, het Vlaams Parlement, het Waals Parlement, het "
        "Brussels Parlement en het Parlement van de Duitstalige Gemeenschap.", langue) + "</p>")
    c.append("<h2>" + t("Les quatre assemblées", "De vier assemblees", langue) + "</h2>")
    c.append('<div class="grille">')
    for code in ("flamand", "wallon", "bruxellois", "germanophone"):
        a = ds.ASSEMBLEES[code]
        nom = ds.NOMS_ASSEMBLEES[code][langue]
        ecart, _ = retro_test(a)
        total = {}
        for circ in a["circonscriptions"]:
            for k, v in circ["officiel"].items():
                total[k] = total.get(k, 0) + v
        prem = max(total.items(), key=lambda kv: kv[1])
        c.append(f'<div class="carte"><h3><a href="{e(code)}/">{e(nom)}</a></h3>'
                 f'<p>{a["sieges"]} ' + t("sièges", "zetels", langue) + " · " +
                 f'{len(a["circonscriptions"])} ' +
                 t("circonscription(s)", "kieskring(en)", langue) + "<br>" +
                 t("Première liste en 2024", "Grootste lijst in 2024", langue) + " : " +
                 f'<span class="pastille" style="background:{couleur(prem[0])}"></span>'
                 f'{e(nom_parti(prem[0]))} ({prem[1]})<br>' +
                 t("Rétro-test", "Terugtest", langue) + f" : {ecart} " +
                 t("siège(s) d'écart", "zetel(s) afwijking", langue) + "</p></div>")
    c.append("</div>")
    return {
        "titre": t("Les parlements de région et de communauté — Le Scrutin",
                   "De gewest- en gemeenschapsparlementen — De Stembus", langue),
        "description": t("Parlement flamand, wallon, bruxellois et germanophone : effectifs, "
                         "circonscriptions, résultats officiels de 2024 et fiabilité du modèle.",
                         "Vlaams, Waals, Brussels en Duitstalig Parlement: zetelaantallen, kieskringen, officiële "
                         "uitslagen van 9 juni 2024 en de betrouwbaarheid van het model.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (None, t("Les parlements", "De parlementen", langue))],
        "jsonld": [{"@context": "https://schema.org", "@type": "CollectionPage",
                    "name": t("Les parlements élus le même jour",
                              "De parlementen verkozen op dezelfde dag", langue),
                    "inLanguage": langue, "url": url_absolue(chemin("parlements", langue))}],
        "og": og_pour("parlements"),
    }


def p_parlement(code, langue):
    a = ds.ASSEMBLEES[code]
    nom = ds.NOMS_ASSEMBLEES[code][langue]
    ecart, detail = retro_test(a)
    total = {}
    for circ in a["circonscriptions"]:
        for k, v in circ["officiel"].items():
            total[k] = total.get(k, 0) + v
    c = []
    c.append(f"<h1>{e(nom)}</h1>")
    c.append('<p class="chapeau">' + t(
        f"{a['sieges']} sièges, {len(a['circonscriptions'])} circonscription(s), "
        f"seuil de {int(a['seuil']*100)} %. Résultat officiel du 9 juin 2024.",
        f"{a['sieges']} zetels, {len(a['circonscriptions'])} kieskring(en), "
        f"drempel {int(a['seuil']*100)} %. Officiële uitslag van 9 juni 2024.", langue) + "</p>")
    c.append(hemicycle(total, langue))
    for circ in a["circonscriptions"]:
        c.append("<h2>" + e(circ["nom_fr"] if langue == "fr" else circ["nom_nl"]) + "</h2>")
        c.append(table_resultat(circ, a["seuil"], langue))
    if ecart:
        c.append('<div class="encart"><h2 style="margin-top:0">' +
                 t("Ce que le modèle ne reproduit pas", "Wat het model niet reproduceert", langue) + "</h2>")
        if code == "wallon":
            c.append("<p>" + t(
                "Le Parlement wallon applique, en plus de la clé D'Hondt et du seuil de 5 %, un "
                "apparentement provincial : dans le Hainaut, à Liège et à Namur, les listes d'un "
                "même parti sont groupées et une répartition complémentaire a lieu au niveau de la "
                "province. Ce simulateur ne l'implémente pas. Appliqué aux voix de 2024, il place "
                f"donc {ecart} sièges sur 75 ailleurs que la proclamation officielle. Le détail est ici, "
                "et la même mise en garde figure sur la page Méthode.",
                "Het Waals Parlement past bovenop D'Hondt en de 5 %-drempel een provinciale "
                "lijstenverbinding toe. Deze simulator implementeert die niet en plaatst daardoor "
                f"{ecart} van de 75 zetels anders dan de officiële uitslag.", langue) + "</p>")
        else:
            c.append("<p>" + t(
                "Appliquée aux chiffres publiés par le SPF Intérieur, la clé D'Hondt attribue le "
                f"dernier siège du groupe linguistique français autrement que la proclamation : "
                f"{ecart} siège sur 89. L'écart est publié plutôt que masqué.",
                "Toegepast op de gepubliceerde cijfers wijst D'Hondt de laatste zetel van de Franse "
                f"taalgroep anders toe dan de officiële uitslag: {ecart} van de 89.", langue) + "</p>")
        c.append('<div class="defile"><table><thead><tr><th>' +
                 t("Circonscription", "Kieskring", langue) + "</th><th>" +
                 t("Calcul du moteur", "Berekening van de motor", langue) + "</th><th>" +
                 t("Proclamation officielle", "Officiële uitslag", langue) + "</th></tr></thead><tbody>")
        for d in detail:
            fmt = lambda m: ", ".join(f"{nom_parti(k)} {v}" for k, v in sorted(m.items(), key=lambda kv: -kv[1]))
            c.append(f'<tr><td>{e(d["circonscription"])}</td><td>{e(fmt(d["calcule"]))}</td>'
                     f'<td>{e(fmt(d["officiel"]))}</td></tr>')
        c.append("</tbody></table></div></div>")
    else:
        c.append('<div class="encart"><p>' + t(
            f"Rétro-test : appliquée aux voix de 2024, la clé D'Hondt reproduit la proclamation "
            f"officielle <strong>siège pour siège</strong>, dans chacune des "
            f"{len(a['circonscriptions'])} circonscription(s).",
            f"Terugtest: toegepast op de stemmen van 2024 reproduceert D'Hondt de officiële uitslag "
            f"<strong>zetel voor zetel</strong>.", langue) + "</p></div>")
    return {
        "titre": t(f"{nom} : composition 2024 et méthode — Le Scrutin",
                   f"{nom}: samenstelling 2024 en methode — De Stembus", langue),
        "description": t(
            f"{nom} : {a['sieges']} sièges, résultats officiels du 9 juin 2024 par circonscription, "
            f"clé D'Hondt et seuil d'éligibilité.",
            f"{nom}: {a['sieges']} zetels, officiële uitslagen van 9 juni 2024 per kieskring.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (chemin("parlements", langue), t("Les parlements", "De parlementen", langue)),
                (None, nom)],
        "jsonld": [{"@context": "https://schema.org", "@type": "Dataset",
                    "name": nom + " — 2024", "inLanguage": langue,
                    "temporalCoverage": "2024-06-09",
                    "creator": {"@type": "GovernmentOrganization",
                                "name": "SPF Intérieur — Direction des Élections"},
                    "license": "https://creativecommons.org/licenses/by-sa/4.0/",
                    "url": url_absolue(chemin_parlement(code, langue))}],
        "og": og_pour("parlement-" + code),
    }


# ---------------------------------------------------------------- les règles
def p_regles(langue):
    c = []
    c.append("<h1>" + t("Les règles du scrutin belge", "De regels van de Belgische stembusgang", langue) + "</h1>")
    c.append('<p class="chapeau">' + t(
        "Tout ce que le simulateur applique, et pourquoi. Chaque règle est une règle de droit, avec "
        "sa référence. Aucune n'est une opinion.",
        "Alles wat de simulator toepast, en waarom. Elke regel is een rechtsregel, met verwijzing.", langue) + "</p>")

    c.append("<h2>" + t("La clé D'Hondt", "De D'Hondt-sleutel", langue) + "</h2>")
    c.append("<p>" + t(
        "On divise le nombre de voix de chaque liste par 1, 2, 3, 4… et l'on attribue les sièges aux "
        "quotients les plus élevés. La méthode favorise légèrement les grandes listes, et d'autant "
        "plus que la circonscription est petite : c'est pourquoi le Luxembourg, avec quatre sièges, "
        "n'a élu en 2024 que trois listes, quand Anvers, avec vingt-quatre, en a élu sept.",
        "Het stemmenaantal van elke lijst wordt gedeeld door 1, 2, 3, 4… en de zetels gaan naar de "
        "hoogste quotiënten. De methode bevoordeelt licht de grote lijsten, des te meer naarmate de "
        "kieskring kleiner is.", langue) + "</p>")
    # exemple vivant : Luxembourg
    lux = [x for x in ds.CHAMBRE["circonscriptions"] if x["code"] == "luxembourg"][0]
    suite = tableau_dhondt(lux["voix"], lux["sieges"] + 2, ds.CHAMBRE["seuil"])
    c.append('<div class="defile"><table><caption>' + t(
        "Luxembourg, 4 sièges : les six premiers quotients. Les deux derniers, en gris, n'ont pas "
        "été attribués — ils montrent qui aurait eu le cinquième et le sixième siège.",
        "Luxemburg, 4 zetels: de eerste zes quotiënten.", langue) +
        '</caption><thead><tr><th class="n">#</th><th>' + t("Liste", "Lijst", langue) +
        '</th><th class="n">' + t("Diviseur", "Deler", langue) + '</th><th class="n">' +
        t("Quotient", "Quotiënt", langue) + "</th></tr></thead><tbody>")
    for x in suite:
        gris = ' style="color:var(--doux)"' if x["rang"] > lux["sieges"] else ""
        c.append(f'<tr{gris}><td class="n">{x["rang"]}</td><td>'
                 f'<span class="pastille" style="background:{couleur(x["liste"])}"></span>'
                 f'{e(nom_parti(x["liste"]))}</td><td class="n">÷{x["diviseur"]}</td>'
                 f'<td class="n">{nombre(x["quotient"])}</td></tr>')
    c.append("</tbody></table></div>")

    c.append("<h2>" + t("Le seuil de 5 %", "De 5 %-drempel", langue) + "</h2>")
    c.append("<p>" + t(
        "Une liste qui n'atteint pas 5 % des votes valables d'une circonscription est écartée avant "
        "toute répartition, quelle que soit sa force ailleurs. En 2024, Ecolo a franchi le seuil à "
        "Bruxelles et à Liège, et l'a manqué dans le Brabant wallon, à Namur, dans le Hainaut et en "
        "Luxembourg. Le seuil, et non le nombre de voix, explique l'essentiel de son résultat.",
        "Een lijst die geen 5 % van de geldige stemmen van een kieskring haalt, wordt uitgesloten, "
        "hoe sterk ze elders ook staat.", langue) + "</p>")

    c.append("<h2>" + t("L'apparentement provincial", "De provinciale lijstenverbinding", langue) + "</h2>")
    c.append("<p>" + t(
        "Il a disparu de la Chambre en 2003, quand les circonscriptions sont devenues provinciales. "
        "Il subsiste au Parlement wallon, dans les trois provinces qui comptent plusieurs "
        "circonscriptions : le Hainaut, Liège et Namur. Les listes d'un même parti y sont groupées, "
        "une première répartition a lieu par circonscription et une répartition complémentaire au "
        "niveau du bureau central provincial. Ce simulateur ne l'implémente pas ; il publie l'écart "
        "que cela produit.",
        "Hij verdween in 2003 uit de Kamer. Hij bestaat nog in het Waals Parlement, in de drie "
        "provincies met meerdere kieskringen: Henegouwen, Luik en Namen.", langue) + "</p>")

    c.append("<h2>" + t("La case de tête et l'effet dévolutif", "De lijststem en het devolutief effect", langue) + "</h2>")
    c.append("<p>" + t(
        "La clé D'Hondt décide combien de sièges revient à chaque liste. L'effet dévolutif décide "
        "<em>qui</em>, dans la liste, les occupe : la moitié des voix de case de tête est "
        "redistribuée aux candidats dans l'ordre décidé par le parti. C'est la seule mécanique du "
        "système belge que ce simulateur ne modélise pas, parce qu'elle porte sur les personnes et "
        "non sur les sièges — mais elle décide, en pratique, l'essentiel de la composition d'une "
        "assemblée.",
        "D'Hondt bepaalt hoeveel zetels elke lijst krijgt. Het devolutief effect bepaalt <em>wie</em> "
        "ze bezet: de helft van de lijststemmen wordt verdeeld volgens de partijvolgorde.", langue) + "</p>")

    c.append("<h2>" + t("Les groupes linguistiques et les majorités",
                        "De taalgroepen en de meerderheden", langue) + "</h2>")
    for k in dco.CONTRAINTES:
        c.append(f'<h3>{e(t(k["titre_fr"], k["titre_nl"], langue))}</h3>'
                 f'<p>{e(t(k["texte_fr"], k["texte_nl"], langue))}</p>')

    c.append("<h2>" + t("Où voter change quoi", "Waar de stem wat verandert", langue) + "</h2>")
    c.append("<p>" + t(
        "Le tableau suivant donne, pour chaque circonscription de la Chambre, le nombre de voix "
        "qu'il fallait en 2024 pour obtenir un siège — le dernier quotient attribué. L'écart entre "
        "circonscriptions est le fait le plus concret de tout ce site.",
        "De volgende tabel geeft per Kamerkieskring het aantal stemmen dat in 2024 nodig was voor "
        "een zetel — het laatst toegekende quotiënt.", langue) + "</p>")
    c.append('<div class="defile"><table><thead><tr><th>' + t("Circonscription", "Kieskring", langue) +
             '</th><th class="n">' + t("Sièges", "Zetels", langue) + '</th><th class="n">' +
             t("Votes valables", "Geldige stemmen", langue) + '</th><th class="n">' +
             t("Dernier quotient", "Laatste quotiënt", langue) + '</th><th class="n">' +
             t("Seuil de 5 %", "5 %-drempel", langue) + "</th></tr></thead><tbody>")
    for circ in ds.CHAMBRE["circonscriptions"]:
        s = tableau_dhondt(circ["voix"], circ["sieges"], ds.CHAMBRE["seuil"])
        dernier = s[-1]["quotient"]
        nomc = circ["nom_fr"] if langue == "fr" else circ["nom_nl"]
        lien = ("../chambre/" if langue == "fr" else "../kamer/") + circ["code"] + "/"
        c.append(f'<tr><td><a href="{e(lien)}">{e(nomc)}</a></td>'
                 f'<td class="n">{circ["sieges"]}</td><td class="n">{nombre(circ["valables"])}</td>'
                 f'<td class="n">{nombre(dernier)}</td><td class="n">{nombre(circ["valables"]*0.05)}</td></tr>')
    c.append("</tbody></table></div>")

    return {
        "titre": t("Les règles du scrutin belge : D'Hondt, seuil, apparentement, majorités — Le Scrutin",
                   "De regels van de Belgische stembusgang — De Stembus", langue),
        "description": t("Comment les sièges sont attribués en Belgique : clé D'Hondt, seuil de 5 %, "
                         "apparentement provincial, effet dévolutif de la case de tête, groupes "
                         "linguistiques, majorité spéciale et article 46.",
                         "Hoe de zetels in België worden toegekend: de D'Hondt-sleutel, de drempel van 5 procent, "
                         "de provinciale lijstenverbinding, het devolutief effect van de lijststem, de "
                         "taalgroepen, de bijzondere meerderheid en artikel 46.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (None, t("Les règles", "De regels", langue))],
        "jsonld": [{"@context": "https://schema.org", "@type": "Article",
                    "headline": t("Les règles du scrutin belge", "De regels van de Belgische stembusgang", langue),
                    "inLanguage": langue, "datePublished": SITE["date_publication"],
                    "dateModified": SITE["date_maj"],
                    "author": {"@type": "Organization", "name": SITE["auteur"]},
                    "url": url_absolue(chemin("regles", langue))}],
        "og": og_pour("regles"),
    }


# --------------------------------------------------------------- la méthode
def p_methode(langue):
    c = []
    c.append("<h1>" + t("La méthode", "De methode", langue) + "</h1>")
    c.append('<p class="chapeau">' + t(
        "Ce simulateur ne prévoit rien. Il calcule les conséquences d'hypothèses que vous choisissez. "
        "Cette page publie le modèle en entier : ses données, son report de voix, ses seuils, ses "
        "limites et l'écart mesuré entre son calcul et la proclamation de 2024.",
        "Deze simulator voorspelt niets. Hij berekent de gevolgen van hypothesen die u kiest. Deze "
        "pagina publiceert het model volledig.", langue) + "</p>")

    c.append("<h2>" + t("1. Les données", "1. De gegevens", langue) + "</h2>")
    c.append("<p>" + t(
        "Les nombres de voix proviennent des pages « circonscription électorale » du SPF Intérieur, "
        "pour les cinq assemblées élues le 9 juin 2024. Ils sont recopiés tels quels ; les "
        "pourcentages et les sièges affichés sur ce site sont <em>recalculés</em>, jamais recopiés. "
        "La construction du site échoue si la somme des voix d'une circonscription ne correspond pas "
        "au total officiel de votes valables, ou si la somme des sièges d'une assemblée ne "
        "correspond pas à son effectif légal.",
        "De stemmenaantallen komen van de pagina's « kieskring » van de FOD Binnenlandse Zaken. Ze "
        "worden letterlijk overgenomen; de percentages en zetels worden <em>herberekend</em>.", langue) + "</p>")
    total_v = sum(x["valables"] for x in ds.CHAMBRE["circonscriptions"])
    c.append('<div class="chiffres">')
    for v, lab in [(nombre(total_v), t("votes valables recopiés pour la Chambre",
                                       "overgenomen geldige stemmen voor de Kamer", langue)),
                   ("31", t("circonscriptions, cinq assemblées", "kieskringen, vijf assemblees", langue)),
                   ("313", t("sièges au total", "zetels in totaal", langue))]:
        c.append(f'<div class="chiffre"><b>{v}</b><span>{lab}</span></div>')
    c.append("</div>")

    c.append("<h2>" + t("2. Le rétro-test", "2. De terugtest", langue) + "</h2>")
    c.append("<p>" + t(
        "Avant toute simulation, le moteur est appliqué aux voix réelles de 2024 et son résultat est "
        "comparé, circonscription par circonscription, à la proclamation officielle. Voici le résultat "
        "de ce contrôle, qui est rejoué à chaque construction du site.",
        "Vóór elke simulatie wordt de motor toegepast op de werkelijke stemmen van 2024 en vergeleken "
        "met de officiële uitslag.", langue) + "</p>")
    c.append('<div class="defile"><table><thead><tr><th>' + t("Assemblée", "Assemblee", langue) +
             '</th><th class="n">' + t("Sièges", "Zetels", langue) + '</th><th class="n">' +
             t("Circonscriptions", "Kieskringen", langue) + '</th><th class="n">' +
             t("Sièges mal placés", "Verkeerd geplaatste zetels", langue) + "</th><th>" +
             t("Cause", "Oorzaak", langue) + "</th></tr></thead><tbody>")
    causes = {
        "wallon": t("apparentement provincial en Hainaut, à Liège et à Namur, non implémenté",
                    "provinciale lijstenverbinding, niet geïmplementeerd", langue),
        "bruxellois": t("dernier siège du groupe français : la clé D'Hondt appliquée aux chiffres "
                        "publiés donne MR 19 et PTB 16, la proclamation donne MR 20 et PTB 15",
                        "laatste zetel van de Franse taalgroep: D'Hondt op de gepubliceerde cijfers "
                        "geeft MR 19 en PTB 16, de uitslag geeft MR 20 en PTB 15", langue),
    }
    for code, a in ds.ASSEMBLEES.items():
        ec, _ = retro_test(a)
        c.append(f'<tr><td>{e(ds.NOMS_ASSEMBLEES[code][langue])}</td>'
                 f'<td class="n">{a["sieges"]}</td><td class="n">{len(a["circonscriptions"])}</td>'
                 f'<td class="n">{ec}</td><td>{causes.get(code, "—")}</td></tr>')
    c.append("</tbody></table></div>")
    c.append('<div class="encart"><p>' + t(
        "La Chambre — c'est-à-dire le cœur du jeu — est reproduite exactement, siège pour siège, dans "
        "les onze circonscriptions. Le Parlement flamand et le Parlement germanophone aussi. Les deux "
        "écarts restants sont documentés ci-dessus plutôt que corrigés à la main : un modèle qui "
        "s'ajuste sur son propre résultat n'est plus un modèle.",
        "De Kamer — de kern van het spel — wordt exact gereproduceerd, zetel voor zetel. Ook het Vlaams "
        "en het Duitstalige Parlement. De twee resterende afwijkingen worden gedocumenteerd in plaats "
        "van met de hand gecorrigeerd.", langue) + "</p></div>")

    c.append("<h2>" + t("3. Le report de voix", "3. De stemverschuiving", langue) + "</h2>")
    c.append("<p>" + t(
        "Le modèle part d'une part par liste et par région — soit le vote de 2024, soit l'une des "
        "trois enquêtes de 2026 — puis il ajoute, en points de pourcentage, les reports associés aux "
        "issues que vous avez choisies. Les listes qu'une enquête ne cite pas conservent leur part de "
        "2024. L'ensemble est plancheré à 0,2 % puis renormalisé à 100 %.",
        "Het model vertrekt van een aandeel per lijst en per gewest, en telt daar de verschuivingen "
        "bij die horen bij de gekozen uitkomsten.", langue) + "</p>")
    c.append("<p>" + t(
        "Le report est ensuite appliqué <em>proportionnellement</em> : les voix de chaque liste dans "
        "chaque circonscription sont multipliées par le rapport entre sa part cible et sa part de "
        "2024 dans sa région, et la circonscription est renormalisée sur son nombre réel de votes "
        "valables. Une part ne peut donc jamais devenir négative, et la géographie interne de la "
        "région est conservée. C'est un modèle de report uniforme régional, standard et discutable — "
        "sa limite principale est qu'il ignore les mouvements propres à une seule province.",
        "De verschuiving wordt <em>evenredig</em> toegepast: de stemmen van elke lijst in elke "
        "kieskring worden vermenigvuldigd met de verhouding tussen doelaandeel en aandeel van 2024.", langue) + "</p>")

    c.append("<h3>" + t("La matrice complète des reports", "De volledige verschuivingsmatrix", langue) + "</h3>")
    c.append("<p>" + t(
        "Dix-huit issues, chacune avec son vecteur. Rien n'est caché ; tout est ici.",
        "Achttien uitkomsten, elk met haar vector.", langue) + "</p>")
    c.append('<div class="defile"><table><thead><tr><th>' + t("Échéance", "IJkmoment", langue) +
             "</th><th>" + t("Issue", "Uitkomst", langue) + "</th><th>" +
             t("Report, en points", "Verschuiving, in punten", langue) + '</th><th class="n">' +
             t("Bande", "Marge", langue) + "</th></tr></thead><tbody>")
    for ech in dca.ECHEANCES:
        for iss in ech["issues"]:
            morceaux = []
            for reg, nomreg in (("fl", t("FL", "VL", langue)), ("wa", "WA"), ("bxl", "BXL")):
                if reg in iss["report"]:
                    morceaux.append("<strong>" + nomreg + "</strong> " + e(", ".join(
                        f"{nom_parti(k)} {'+' if v > 0 else '−'}{abs(v):.1f}".replace(".", ",")
                        for k, v in sorted(iss["report"][reg].items(), key=lambda kv: -abs(kv[1])))))
            c.append(f'<tr><td>{e(t(ech["titre_fr"], ech["titre_nl"], langue))}</td>'
                     f'<td>{e(t(iss["titre_fr"], iss["titre_nl"], langue))}</td>'
                     f'<td>{" · ".join(morceaux)}</td>'
                     f'<td class="n">±{str(iss["bande"]).replace(".", ",")}</td></tr>')
    c.append("</tbody></table></div>")

    c.append("<h2>" + t("4. La cohésion et les issues", "4. De cohesie en de uitkomsten", langue) + "</h2>")
    b = dle.COHESION
    c.append("<p>" + t(
        f"La cohésion d'une coalition part de {b['base']} et se corrige ainsi : "
        f"{b['par_parti_au_dela_de_trois']} par parti au-delà du troisième ; "
        f"{b['sans_majorite_dans_un_groupe']} si la coalition n'a pas la majorité dans l'un des deux "
        f"groupes linguistiques ; {b['majorite_etroite_76_78']} si elle compte entre 76 et 78 sièges ; "
        f"+{b['majorite_confortable_90']} si elle en compte 90 ou plus. Chaque chantier adopté ajoute "
        f"ensuite son propre effet.",
        f"De cohesie van een coalitie start op {b['base']} en wordt zo gecorrigeerd.", langue) + "</p>")
    c.append("<p>" + t("L'arbre de décision, appliqué dans cet ordre :",
                       "De beslissingsboom, in deze volgorde toegepast:", langue) + "</p><ol>")
    for i, iss in enumerate(dle.ISSUES, 1):
        c.append(f'<li><strong>{e(t(iss["titre_fr"], iss["titre_nl"], langue))}</strong> — '
                 f'{e(t(iss["regle_fr"], iss["regle_nl"], langue))}</li>')
    c.append("</ol>")

    c.append("<h2>" + t("5. Ce que ce simulateur ne fait pas", "5. Wat deze simulator niet doet", langue) + "</h2>")
    c.append("<ul>")
    for x in [
        t("Il ne modélise pas l'effet dévolutif de la case de tête : il attribue des sièges à des "
          "listes, jamais à des personnes. Aucune personne vivante n'est nommée dans la partie jouable.",
          "Hij modelleert het devolutief effect niet: hij kent zetels toe aan lijsten, nooit aan personen.", langue),
        t("Il n'implémente pas l'apparentement provincial du Parlement wallon, et publie l'écart que "
          "cela produit.",
          "Hij implementeert de provinciale lijstenverbinding van het Waals Parlement niet.", langue),
        t("Il n'ajuste pas la participation ni les votes blancs et nuls : la structure de 2024 est "
          "conservée dans chaque circonscription.",
          "Hij past de opkomst en de blanco stemmen niet aan.", langue),
        t("Il ne pondère pas les enquêtes entre elles et n'en fabrique pas de moyenne : vous en "
          "choisissez une, ou vous partez du vote réel de 2024.",
          "Hij weegt de peilingen niet en maakt er geen gemiddelde van.", langue),
        t("Il ne classe aucun parti et ne recommande aucun vote. Les exclusions sont des faits "
          "publics que vous validez ou non.",
          "Hij rangschikt geen enkele partij en beveelt geen stem aan.", langue),
        t("Il n'a pas de version allemande, alors que la Communauté germanophone élit son parlement "
          "le même jour. C'est la limite la plus gênante de ce site.",
          "Hij heeft geen Duitse versie, terwijl de Duitstalige Gemeenschap op dezelfde dag haar "
          "parlement verkiest.", langue),
    ]:
        c.append(f"<li>{x}</li>")
    c.append("</ul>")
    return {
        "titre": t("La méthode : données, report de voix, rétro-test et limites — Le Scrutin",
                   "De methode: gegevens, stemverschuiving, terugtest en grenzen — De Stembus", langue),
        "description": t("Le modèle publié en entier : origine des données officielles, report de "
                         "voix proportionnel par région, matrice complète des dix-huit issues, "
                         "rétro-test sur 2024 et limites assumées.",
                         "Het model volledig gepubliceerd: herkomst van de officiële gegevens, evenredige "
                         "stemverschuiving per gewest, de volledige matrix van de achttien uitkomsten, "
                         "de terugtest op 2024 en de erkende grenzen.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (None, t("La méthode", "De methode", langue))],
        "jsonld": [{"@context": "https://schema.org", "@type": "TechArticle",
                    "headline": t("La méthode du simulateur", "De methode van de simulator", langue),
                    "inLanguage": langue, "datePublished": SITE["date_publication"],
                    "dateModified": SITE["date_maj"],
                    "author": {"@type": "Organization", "name": SITE["auteur"]},
                    "url": url_absolue(chemin("methode", langue))}],
        "og": og_pour("methode"),
    }


# ------------------------------------------------------------- coalitions
def p_coalitions(langue):
    a = ds.CHAMBRE
    total = {}
    for circ in a["circonscriptions"]:
        for k, v in circ["officiel"].items():
            total[k] = total.get(k, 0) + v
    gr = {"fr": 0, "nl": 0}
    for k, v in total.items():
        com = dp.PARTIS[k]["communaute"]
        if com == "fl":
            gr["nl"] += v
        elif com == "fr":
            gr["fr"] += v
    c = []
    c.append("<h1>" + t("L'arithmétique des coalitions", "De rekenkunde van coalities", langue) + "</h1>")
    c.append('<p class="chapeau">' + t(
        "Former un gouvernement belge, c'est franchir quatre seuils différents, et ils ne servent "
        "pas à la même chose. Cette page les met côte à côte, avec la Chambre de 2024 comme exemple.",
        "Een Belgische regering vormen betekent vier verschillende drempels halen, en ze dienen niet "
        "hetzelfde doel.", langue) + "</p>")
    c.append('<div class="chiffres">')
    for v, lab in [("76", t("sièges : la confiance de la Chambre", "zetels: het vertrouwen van de Kamer", langue)),
                   ("100", t("sièges : les deux tiers", "zetels: twee derde", langue)),
                   (str(gr["nl"] // 2 + 1), t("sièges du groupe néerlandais pour y être majoritaire",
                                              "zetels van de Nederlandse taalgroep voor een meerderheid", langue)),
                   (str(gr["fr"] // 2 + 1), t("sièges du groupe français pour y être majoritaire",
                                              "zetels van de Franse taalgroep voor een meerderheid", langue))]:
        c.append(f'<div class="chiffre"><b>{v}</b><span>{lab}</span></div>')
    c.append("</div>")
    c.append("<p>" + t(
        f"En 2024, la Chambre comptait {gr['nl']} sièges au groupe linguistique néerlandais et "
        f"{gr['fr']} au groupe français. Une loi spéciale — c'est-à-dire toute réforme de l'État — "
        f"exige donc simultanément 100 sièges, {gr['nl']//2+1} du côté néerlandophone et "
        f"{gr['fr']//2+1} du côté francophone. C'est cette double contrainte, et non l'absence de "
        f"majorité, qui explique la rareté des réformes institutionnelles.",
        f"In 2024 telde de Kamer {gr['nl']} zetels in de Nederlandse taalgroep en {gr['fr']} in de "
        f"Franse. Een bijzondere wet vereist dus tegelijk 100 zetels en een meerderheid in elke groep.",
        langue) + "</p>")

    c.append("<h2>" + t("Ce que chaque seuil autorise", "Wat elke drempel toelaat", langue) + "</h2>")
    c.append('<div class="defile"><table><thead><tr><th>' + t("Seuil", "Drempel", langue) +
             "</th><th>" + t("Ce qu'il permet", "Wat het toelaat", langue) + "</th><th>" +
             t("Référence", "Verwijzing", langue) + "</th></tr></thead><tbody>")
    for k in dco.CONTRAINTES:
        c.append(f'<tr><td>{e(t(k["titre_fr"], k["titre_nl"], langue))}</td>'
                 f'<td>{e(t(k["texte_fr"], k["texte_nl"], langue))}</td>'
                 f'<td>{e(dsrc.SOURCES[k["source"]]["auteur"])}</td></tr>')
    c.append("</tbody></table></div>")

    c.append("<h2>" + t("Les coalitions majoritaires de la Chambre de 2024",
                        "De meerderheidscoalities in de Kamer van 2024", langue) + "</h2>")
    c.append("<p>" + t(
        "Toutes les combinaisons minimales — celles dont on ne peut retirer aucun membre sans perdre "
        "les 76 sièges — parmi les listes ayant obtenu au moins un siège, en excluant la seule liste "
        "visée par une exclusion déclarée à laquelle tous les autres partis flamands se tiennent "
        "depuis 1989. Retirer cette exclusion sur la page du simulateur en fait apparaître d'autres.",
        "Alle minimale combinaties onder de lijsten met minstens één zetel, met uitzondering van de "
        "lijst waarop sinds 1989 een verklaarde uitsluiting rust.", langue) + "</p>")
    # énumération en Python (miroir du moteur JS)
    codes = [k for k, v in sorted(total.items(), key=lambda kv: -kv[1]) if v > 0 and k != "vb"]
    resultats = []
    n = len(codes)
    for masque in range(1, 1 << n):
        sous = [codes[i] for i in range(n) if masque & (1 << i)]
        s = sum(total[x] for x in sous)
        if s < 76:
            continue
        if any(s - total[x] >= 76 for x in sous):
            continue
        g = {"fr": 0, "nl": 0}
        for x in sous:
            com = dp.PARTIS[x]["communaute"]
            if com == "fl":
                g["nl"] += total[x]
            elif com == "fr":
                g["fr"] += total[x]
        resultats.append((len(sous), -s, sous, s, g))
    resultats.sort()
    c.append("<p>" + t(
        f"{len(resultats)} coalitions minimales majoritaires, dont "
        f"{sum(1 for r in resultats if r[0] <= 4)} de quatre partis ou moins.",
        f"{len(resultats)} minimale meerderheidscoalities.", langue) + "</p>")
    c.append('<div class="defile"><table><thead><tr><th>' + t("Coalition", "Coalitie", langue) +
             '</th><th class="n">' + t("Sièges", "Zetels", langue) + '</th><th class="n">NL</th>'
             '<th class="n">FR</th><th>' + t("Loi spéciale possible", "Bijzondere wet mogelijk", langue) +
             "</th></tr></thead><tbody>")
    for taille, _, sous, s, g in resultats[:24]:
        speciale = s >= 100 and g["nl"] * 2 > gr["nl"] and g["fr"] * 2 > gr["fr"]
        noms = " + ".join(
            f'<span class="pastille" style="background:{couleur(x)}"></span>{e(nom_parti(x))}'
            for x in sorted(sous, key=lambda k: -total[k]))
        c.append(f'<tr><td>{noms}</td><td class="n"><strong>{s}</strong></td>'
                 f'<td class="n">{g["nl"]}</td><td class="n">{g["fr"]}</td>'
                 f'<td>{t("oui", "ja", langue) if speciale else t("non", "nee", langue)}</td></tr>')
    c.append("</tbody></table></div>")
    if len(resultats) > 24:
        c.append("<p>" + t(f"Les {len(resultats)-24} autres combinaisons comptent cinq partis ou plus. "
                           "Le simulateur les énumère toutes.",
                           f"De {len(resultats)-24} andere combinaties tellen vijf partijen of meer.", langue) + "</p>")
    return {
        "titre": t("L'arithmétique des coalitions belges : 76, 100, et les deux groupes — Le Scrutin",
                   "De rekenkunde van Belgische coalities — De Stembus", langue),
        "description": t("76 sièges pour la confiance, 100 pour les deux tiers, et une majorité dans "
                         "chacun des deux groupes linguistiques pour une loi spéciale : toutes les "
                         "coalitions majoritaires de la Chambre de 2024.",
                         "76 zetels voor het vertrouwen, 100 voor twee derde, en een meerderheid in elke taalgroep "
                         "voor een bijzondere wet: alle meerderheidscoalities van de Kamer van 2024.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (None, t("Les coalitions", "De coalities", langue))],
        "jsonld": [{"@context": "https://schema.org", "@type": "Article",
                    "headline": t("L'arithmétique des coalitions belges",
                                  "De rekenkunde van Belgische coalities", langue),
                    "inLanguage": langue, "datePublished": SITE["date_publication"],
                    "dateModified": SITE["date_maj"],
                    "author": {"@type": "Organization", "name": SITE["auteur"]},
                    "url": url_absolue(chemin("coalitions", langue))}],
        "og": og_pour("coalitions"),
    }


# --------------------------------------------------------------- actualités
def p_actualites(langue):
    c = []
    c.append("<h1>" + t("L'actualité, datée et sourcée", "De actualiteit, gedateerd en gebrond", langue) + "</h1>")
    c.append('<p class="chapeau">' + t(
        "De l'élection de juin 2024 au conclave budgétaire de septembre 2026. Trois statuts, "
        "affichés : fait établi, échéance programmée, hypothèse. Rien n'est présenté comme certain "
        "s'il ne l'est pas.",
        "Van de verkiezing van juni 2024 tot het begrotingsconclaaf van september 2026. Drie statussen: "
        "vastgesteld feit, geprogrammeerd ijkmoment, hypothese.", langue) + "</p>")
    etiq = {"fait": t("fait", "feit", langue), "echeance": t("échéance", "ijkmoment", langue),
            "hypothese": t("hypothèse", "hypothese", langue)}
    c.append("<ol class='large' style='list-style:none;padding:0'>")
    for x in sorted(dact.CHRONOLOGIE, key=lambda y: y["date"], reverse=True):
        s = dsrc.SOURCES[x["source"]]
        c.append(
            f'<li class="carte" style="margin-bottom:.8rem"><p style="margin:0 0 .3rem">'
            f'<time datetime="{e(x["date"])}"><strong>{e(x["date"])}</strong></time> '
            f'<span class="etiquette etiquette--{e(x["statut"])}">{e(etiq[x["statut"]])}</span></p>'
            f'<p style="margin:0 0 .4rem">{e(t(x["fr"], x["nl"], langue))}</p>'
            f'<p style="margin:0;font-size:.8rem;color:var(--doux)">'
            f'<a href="{e(s["url"])}" rel="noopener">{e(s["auteur"])}</a></p></li>')
    c.append("</ol>")
    return {
        "titre": t("L'actualité politique belge, datée et sourcée — Le Scrutin",
                   "De Belgische politieke actualiteit, gedateerd en gebrond — De Stembus", langue),
        "description": t("Chronologie de la politique belge de juin 2024 au conclave budgétaire de "
                         "septembre 2026 : coalition Arizona, crise bruxelloise, Moody's, GRECO, "
                         "rapport état de droit, sondages 2026.",
                         "Chronologie van de Belgische politiek van juni 2024 tot het begrotingsconclaaf van "
                         "september 2026: Arizona-coalitie, Brusselse crisis, Moody's, GRECO, "
                         "rechtsstaatrapport en de peilingen van 2026.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (None, t("L'actualité", "Actualiteit", langue))],
        "jsonld": [{"@context": "https://schema.org", "@type": "ItemList",
                    "name": t("Chronologie politique belge 2024-2026",
                              "Belgische politieke chronologie 2024-2026", langue),
                    "inLanguage": langue,
                    "itemListElement": [
                        {"@type": "ListItem", "position": i + 1,
                         "item": {"@type": "Event", "name": t(x["fr"], x["nl"], langue)[:110],
                                  "startDate": x["date"],
                                  "eventStatus": "https://schema.org/EventScheduled",
                                  "location": {"@type": "Country", "name": "Belgique"}}}
                        for i, x in enumerate(sorted(dact.CHRONOLOGIE, key=lambda y: y["date"]))]}],
        "og": og_pour("actualites"),
    }


# ------------------------------------------------------- sources, glossaire
def p_sources(langue, citations):
    c = []
    c.append("<h1>" + t("Les sources", "De bronnen", langue) + "</h1>")
    c.append('<p class="chapeau">' + t(
        "Chaque chiffre de ce site vient d'ici. La construction du site échoue si une source citée "
        "manque à ce registre, ou si une source de ce registre n'est citée nulle part.",
        "Elk cijfer op deze site komt hiervandaan. De bouw faalt als een geciteerde bron ontbreekt, "
        "of als een bron nergens wordt geciteerd.", langue) + "</p>")
    etiq = {"fait": t("fait", "feit", langue), "echeance": t("échéance", "ijkmoment", langue),
            "hypothese": t("hypothèse", "hypothese", langue)}
    c.append('<div class="defile"><table><thead><tr><th>' + t("Source", "Bron", langue) +
             "</th><th>" + t("Auteur", "Auteur", langue) + "</th><th>" +
             t("Date", "Datum", langue) + "</th><th>" + t("Statut", "Status", langue) +
             "</th></tr></thead><tbody>")
    for code in sorted(dsrc.SOURCES, key=lambda k: dsrc.SOURCES[k]["date"], reverse=True):
        s = dsrc.SOURCES[code]
        c.append(f'<tr id="src-{e(code)}"><td><a href="{e(s["url"])}" rel="noopener">'
                 f'{e(t(s["titre_fr"], s["titre_nl"], langue))}</a></td>'
                 f'<td>{e(s["auteur"])}</td>'
                 f'<td><time datetime="{e(s["date"])}">{e(s["date"])}</time></td>'
                 f'<td><span class="etiquette etiquette--{e(s["statut"])}">{e(etiq[s["statut"]])}</span></td></tr>')
    c.append("</tbody></table></div>")
    c.append("<p>" + t(f"{len(dsrc.SOURCES)} sources au registre, toutes citées.",
                       f"{len(dsrc.SOURCES)} bronnen in het register, allemaal geciteerd.", langue) + "</p>")
    return {
        "titre": t("Les sources : registre complet — Le Scrutin",
                   "De bronnen: volledig register — De Stembus", langue),
        "description": t("Registre complet des sources du simulateur : résultats officiels du SPF "
                         "Intérieur, Constitution, CRISP, GRECO, Commission européenne, comité de "
                         "monitoring, enquêtes 2026.",
                         "Volledig bronnenregister van de simulator: officiële uitslagen van de FOD Binnenlandse "
                         "Zaken, de Grondwet, CRISP, GRECO, de Europese Commissie, het monitoringcomité "
                         "en de peilingen van 2026.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (None, t("Les sources", "De bronnen", langue))],
        "jsonld": [{"@context": "https://schema.org", "@type": "CollectionPage",
                    "name": t("Registre des sources", "Bronnenregister", langue),
                    "inLanguage": langue, "url": url_absolue(chemin("sources", langue))}],
        "og": og_pour("sources"),
    }


def p_glossaire(langue):
    c = []
    c.append("<h1>" + t("Le glossaire", "De woordenlijst", langue) + "</h1>")
    c.append('<p class="chapeau">' + t(
        "Douze termes suffisent à lire n'importe quelle page de ce site.",
        "Twaalf termen volstaan om elke pagina van deze site te lezen.", langue) + "</p>")
    c.append("<dl>")
    for g in dglo.GLOSSAIRE:
        s = dsrc.SOURCES[g["source"]]
        c.append(f'<dt id="{e(g["code"])}"><h2 style="margin:1.6rem 0 .3rem">'
                 f'{e(g["fr"] if langue == "fr" else g["nl"])}</h2></dt>'
                 f'<dd style="margin:0 0 .6rem"><p>{e(t(g["def_fr"], g["def_nl"], langue))}</p>'
                 f'<p style="font-size:.8rem;color:var(--doux)"><a href="{e(s["url"])}" rel="noopener">'
                 f'{e(s["auteur"])}</a></p></dd>')
    c.append("</dl>")
    return {
        "titre": t("Le glossaire : D'Hondt, seuil, apparentement, case de tête — Le Scrutin",
                   "De woordenlijst: D'Hondt, drempel, lijstenverbinding — De Stembus", langue),
        "description": t("Douze termes du droit électoral belge définis simplement : clé D'Hondt, "
                         "seuil d'éligibilité, apparentement, effet dévolutif, groupe linguistique, "
                         "loi spéciale, affaires courantes, Kern, dotation.",
                         "Twaalf termen van het Belgische kiesrecht eenvoudig gedefinieerd: D'Hondt-sleutel, "
                         "kiesdrempel, lijstenverbinding, devolutief effect, taalgroep, bijzondere wet, "
                         "lopende zaken, Kern en partijdotatie.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (None, t("Le glossaire", "De woordenlijst", langue))],
        "jsonld": [{"@context": "https://schema.org", "@type": "DefinedTermSet",
                    "name": t("Glossaire du scrutin belge", "Woordenlijst van de Belgische stembusgang", langue),
                    "inLanguage": langue, "url": url_absolue(chemin("glossaire", langue)),
                    "hasDefinedTerm": [
                        {"@type": "DefinedTerm", "name": g["fr"] if langue == "fr" else g["nl"],
                         "description": t(g["def_fr"], g["def_nl"], langue),
                         "url": url_absolue(chemin("glossaire", langue)) + "#" + g["code"]}
                        for g in dglo.GLOSSAIRE]}],
        "og": og_pour("glossaire"),
    }


def p_reseau(langue):
    c = []
    c.append("<h1>" + t("Le réseau", "Het netwerk", langue) + "</h1>")
    c.append('<p class="chapeau">' + t(
        "Ce simulateur est une entrée parmi d'autres dans un même ensemble de sites sur la situation "
        "politique et démocratique belge. Chacun est autonome et se lit seul ; ils partagent des "
        "faits, des sources et une règle éditoriale.",
        "Deze simulator is één ingang in een groter geheel van sites over de Belgische politieke en "
        "democratische situatie.", langue) + "</p>")
    c.append("<h2>" + t("Les six entrées", "De zes ingangen", langue) + "</h2>")
    c.append('<div class="grille">')
    for r in dres.RESEAU:
        etat = t("en ligne", "online", langue) if r["etat"] == "en-ligne" else t("à publier", "te publiceren", langue)
        cls = "etiquette--fait" if r["etat"] == "en-ligne" else "etiquette--echeance"
        titre = (f'<a href="{e(r["url"])}" rel="noopener">{e(r["nom"])}</a>'
                 if r["etat"] == "en-ligne" else e(r["nom"]))
        c.append(f'<div class="carte"><h3>{titre}</h3>'
                 f'<p>{e(t(r["role_fr"], r["role_nl"], langue))}</p>'
                 f'<p style="font-size:.8rem;color:var(--doux)">'
                 f'<span class="etiquette {cls}">{e(etat)}</span> '
                 f'<a href="https://github.com/{e(r["depot"])}" rel="noopener">{e(r["depot"])}</a></p></div>')
    c.append("</div>")
    c.append("<h2>" + t("La règle éditoriale commune", "De gemeenschappelijke redactionele regel", langue) + "</h2>")
    c.append("<ul>")
    for x in [
        t("Séparation en trois, affichée partout : fait établi, échéance programmée, hypothèse.",
          "Drievoudige scheiding, overal zichtbaar: vastgesteld feit, geprogrammeerd ijkmoment, hypothese.", langue),
        t("Aucun indice composite. Les jauges sont des variables de simulation, et c'est dit.",
          "Geen samengestelde index. De meters zijn simulatievariabelen, en dat wordt gezegd.", langue),
        t("Aucune personne vivante nommée dans les parties jouables : on décrit des instruments.",
          "Geen levende persoon genoemd in de speelbare delen: er worden instrumenten beschreven.", langue),
        t("Aucun parti n'est classé, noté ou recommandé.",
          "Geen enkele partij wordt gerangschikt, gescoord of aanbevolen.", langue),
        t("Aucun site n'est annoncé « en ligne » avant que son adresse ait été vérifiée.",
          "Geen enkele site wordt « online » genoemd voor het adres is geverifieerd.", langue),
        t("Aucun traceur, aucun cookie, aucune police distante, aucun appel réseau.",
          "Geen trackers, geen cookies, geen externe lettertypes, geen netwerkoproepen.", langue),
    ]:
        c.append(f"<li>{e(x)}</li>")
    c.append("</ul>")
    c.append(f'<p><a class="bouton" href="{e(RESEAU_INDEX)}" rel="noopener">' +
             t("L'index du réseau", "De index van het netwerk", langue) + "</a></p>")
    return {
        "titre": t("Le réseau : les autres sites — Le Scrutin", "Het netwerk: de andere sites — De Stembus", langue),
        "description": t("Les six sites de l'ensemble : l'enquête, l'action, le budget, les chiffres, "
                         "la satire, la décision — et ce simulateur.",
                         "De zes sites van het geheel: het onderzoek, de actie, de begroting, de cijfers, de satire "
                         "en de beslissing — en deze simulator van de Belgische verkiezingen.", langue),
        "corps": "\n".join(c),
        "fil": [("" if langue == "fr" else "nl/", t("Accueil", "Start", langue)),
                (None, t("Le réseau", "Het netwerk", langue))],
        "jsonld": [{"@context": "https://schema.org", "@type": "CollectionPage",
                    "name": t("Le réseau", "Het netwerk", langue), "inLanguage": langue,
                    "url": url_absolue(chemin("reseau", langue))}],
        "og": og_pour("reseau"),
    }
