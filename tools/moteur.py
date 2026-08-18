# -*- coding: utf-8 -*-
"""Moteur de répartition des sièges. Référence Python du moteur JS.

Système D'Hondt : les sièges sont attribués un à un au quotient le plus élevé
voix / (sièges déjà obtenus + 1). Un seuil d'éligibilité de 5 % des votes
valables de la circonscription s'applique à la Chambre et aux parlements de
région (art. 165bis du Code électoral ; loi spéciale du 8 août 1980, art. 29).
En cas d'égalité parfaite de quotient, le siège va à la liste au chiffre
électoral le plus élevé, puis, à égalité, à la liste au numéro d'ordre le plus
bas — ici, à l'ordre alphabétique du code de liste, qui est déterministe.
"""
from fractions import Fraction


def dhondt(voix, sieges, seuil=0.0):
    """voix : dict {code: nombre de voix}. Retourne dict {code: sièges}."""
    total = sum(voix.values())
    if total <= 0 or sieges <= 0:
        return {c: 0 for c in voix}
    plancher = total * seuil
    eligibles = {c: v for c, v in voix.items() if v >= plancher and v > 0}
    resultat = {c: 0 for c in voix}
    if not eligibles:
        return resultat
    for _ in range(sieges):
        meilleur, quotient = None, None
        for c, v in eligibles.items():
            q = Fraction(v, resultat[c] + 1)
            if quotient is None or q > quotient or (
                q == quotient and (v > eligibles[meilleur] or (v == eligibles[meilleur] and c < meilleur))
            ):
                meilleur, quotient = c, q
        resultat[meilleur] += 1
    return resultat


def tableau_dhondt(voix, sieges, seuil=0.0, profondeur=None):
    """Retourne la suite des quotients attribués, pour affichage pédagogique."""
    total = sum(voix.values())
    plancher = total * seuil
    eligibles = {c: v for c, v in voix.items() if v >= plancher and v > 0}
    etat = {c: 0 for c in eligibles}
    suite = []
    n = profondeur or sieges
    for rang in range(1, min(n, sieges) + 1):
        meilleur, quotient = None, None
        for c, v in eligibles.items():
            q = Fraction(v, etat[c] + 1)
            if quotient is None or q > quotient or (
                q == quotient and (v > eligibles[meilleur] or (v == eligibles[meilleur] and c < meilleur))
            ):
                meilleur, quotient = c, q
        etat[meilleur] += 1
        suite.append({"rang": rang, "liste": meilleur, "diviseur": etat[meilleur],
                      "quotient": float(quotient)})
    return suite


# Assemblées dont la loi ajoute un apparentement provincial (groupement de listes)
# que ce moteur n'implémente pas : l'écart de rétro-test est publié tel quel.
# Source : SPF Intérieur, « Parlement wallon — Dépouillement, répartition des sièges ».
ECART_TOLERE = {"wallon": 8, "bruxellois": 1}


def retro_test(assemblee):
    """Nombre de sièges que D'Hondt place ailleurs que la proclamation de 2024."""
    ecart = 0
    detail = []
    for circ in assemblee["circonscriptions"]:
        calcule = {c: n for c, n in dhondt(circ["voix"], circ["sieges"], assemblee["seuil"]).items() if n}
        officiel = circ["officiel"]
        cles = set(calcule) | set(officiel)
        d = sum(abs(calcule.get(c, 0) - officiel.get(c, 0)) for c in cles) // 2
        ecart += d
        if d:
            detail.append({"circonscription": circ["code"], "ecart": d,
                           "calcule": calcule, "officiel": officiel})
    return ecart, detail


def verifier_assemblee(assemblee):
    """Vérifie la cohérence des données et le rétro-test. Lève AssertionError."""
    total_sieges = 0
    for circ in assemblee["circonscriptions"]:
        somme = sum(circ["voix"].values())
        assert somme == circ["valables"], (
            f"{assemblee['code']}/{circ['code']} : somme des voix {somme} "
            f"≠ votes valables déclarés {circ['valables']}")
        officiel = circ["officiel"]
        assert sum(officiel.values()) == circ["sieges"], (
            f"{assemblee['code']}/{circ['code']} : {sum(officiel.values())} sièges officiels "
            f"pour {circ['sieges']} à pourvoir")
        total_sieges += circ["sieges"]
    assert total_sieges == assemblee["sieges"], (
        f"{assemblee['code']} : {total_sieges} sièges répartis pour {assemblee['sieges']} légaux")
    ecart, _ = retro_test(assemblee)
    attendu = ECART_TOLERE.get(assemblee["code"], 0)
    assert ecart == attendu, (
        f"{assemblee['code']} : rétro-test 2024 = {ecart} siège(s) d'écart, "
        f"{attendu} attendu(s). Toute variation doit être documentée avant d'être admise.")
    return True


if __name__ == "__main__":
    import donnees_scrutins as ds
    for code, a in ds.ASSEMBLEES.items():
        try:
            verifier_assemblee(a)
            e, _ = retro_test(a)
            print(f"  OK   {code:14s} {a['sieges']:>4} sièges, "
                  f"{len(a['circonscriptions'])} circonscription(s), "
                  f"rétro-test 2024 : {e} siège(s) d'écart")
        except AssertionError as e:
            print(f"  ÉCHEC {code}: {e}")
