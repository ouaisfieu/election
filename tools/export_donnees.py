# -*- coding: utf-8 -*-
"""Export des données vers assets/data/. Source unique : les modules donnees_*.py."""
import json, os

import donnees_partis as dp
import donnees_scrutins as ds
import donnees_sondages as dso
import donnees_campagne as dca
import donnees_coalition as dco
import donnees_legislature as dle


def paquet():
    return {
        "partis": dp.PARTIS,
        "partisElus": dp.PARTIS_ELUS,
        "assemblees": ds.ASSEMBLEES,
        "nomsAssemblees": ds.NOMS_ASSEMBLEES,
        "sondages": dso.SONDAGES,
        "sondageDefaut": dso.SONDAGE_DEFAUT,
        "echeances": dca.ECHEANCES,
        "contraintes": dco.CONTRAINTES,
        "exclusions": dco.EXCLUSIONS,
        "portefeuilles": dco.PORTEFEUILLES,
        "chantiers": dco.CHANTIERS,
        "depart": dle.DEPART,
        "cohesion": dle.COHESION,
        "semestres": dle.SEMESTRES,
        "issues": dle.ISSUES,
    }


def ecrire(racine):
    chemin = os.path.join(racine, "assets", "data")
    os.makedirs(chemin, exist_ok=True)
    contenu = json.dumps(paquet(), ensure_ascii=False, separators=(",", ":"), sort_keys=False)
    with open(os.path.join(chemin, "donnees.js"), "w", encoding="utf-8") as f:
        f.write("/* Généré par tools/export_donnees.py — ne pas éditer à la main. */\n")
        f.write("(function(r){var d=" + contenu + ";")
        f.write("if(typeof module!=='undefined'&&module.exports)module.exports=d;else r.ScrutinDonnees=d;")
        f.write("})(typeof window!=='undefined'?window:globalThis);\n")
    return os.path.join(chemin, "donnees.js")


if __name__ == "__main__":
    import sys
    p = ecrire(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print("écrit :", p, os.path.getsize(p), "octets")
