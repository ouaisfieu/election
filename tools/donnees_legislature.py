# -*- coding: utf-8 -*-
"""Acte IV — la législature 2029-2034, et les six issues.

Aucun tirage aléatoire. Trois variables seulement, toutes affichées :
  * `budget`     — milliards d'euros d'effort structurel acquis sur la législature ;
  * `cohesion`   — capacité de la coalition à tenir, 0 à 100 ;
  * `droit`      — points d'état de droit gagnés ou perdus, échelle -10 à +10.
Elles sont des variables de simulation, pas des indices composites publiés.
"""

# Point de départ chiffré, tiré des faits documentés (voir /sources/).
DEPART = {
    "ecart_2029": 7.7,          # milliards d'euros, comité de monitoring, juillet 2026
    "objectif": 10.0,           # milliards d'euros visés d'ici 2029 (10 juillet 2026)
    "deficit_2029": 5.2,        # % du PIB
    "dette_2029": 117.1,        # % du PIB
    "charges_interets": 10.0,   # milliards d'euros, juillet 2026
    "greco_traitees": 8,        # sur 22 recommandations (addendum GrecoRC5(2025))
    "cpi_2025": 69,             # indice de perception de la corruption (77 en 2016)
}

# Coût de cohésion : plus la coalition est large et plus elle est écartelée
# entre les deux groupes linguistiques, plus elle s'use vite.
COHESION = {
    "base": 64,
    "par_parti_au_dela_de_trois": -7,
    "sans_majorite_dans_un_groupe": -12,
    "majorite_etroite_76_78": -7,
    "majorite_confortable_90": +6,
}

SEMESTRES = [
    {"code": "s1", "titre_fr": "Premier semestre : la déclaration de politique",
     "titre_nl": "Eerste semester: de beleidsverklaring"},
    {"code": "s2", "titre_fr": "Deuxième année : le premier conclave",
     "titre_nl": "Tweede jaar: het eerste conclaaf"},
    {"code": "s3", "titre_fr": "Mi-législature : le contrôle européen",
     "titre_nl": "Halverwege: de Europese controle"},
    {"code": "s4", "titre_fr": "Dernière année : le bilan",
     "titre_nl": "Laatste jaar: de balans"},
]

# Arbre de décision, appliqué DANS CET ORDRE, et reproduit tel quel dans le
# procès-verbal. Aucun seuil n'est caché.
ISSUES = [
    {"code": "sans-gouvernement", "titre_fr": "Sans gouvernement",
     "titre_nl": "Zonder regering",
     "regle_fr": "Aucune coalition n'a été formée : la Belgique reste en affaires courantes.",
     "regle_nl": "Er is geen coalitie gevormd: België blijft in lopende zaken.",
     "texte_fr": "Le pays a déjà tenu 541 jours ainsi en 2010-2011 et Bruxelles 613 jours en "
                 "2024-2026. L'administration continue, le budget roule en douzièmes provisoires, "
                 "et aucune des huit lignes de l'accord n'existe.",
     "texte_nl": "Het land hield dit al 541 dagen vol in 2010-2011 en Brussel 613 dagen in 2024-2026."},
    {"code": "chute", "titre_fr": "La chute",
     "titre_nl": "De val",
     "regle_fr": "Cohésion inférieure à 25 en fin de législature.",
     "regle_nl": "Cohesie onder 25 op het einde van de legislatuur.",
     "texte_fr": "La coalition s'est défaite avant le terme. Le budget non bouclé et la charge "
                 "d'intérêts poursuivent leur trajectoire ; le prochain gouvernement héritera "
                 "d'un écart plus large que celui de 2026.",
     "texte_nl": "De coalitie viel uiteen voor het einde van de rit."},
    {"code": "constituant", "titre_fr": "Le constituant",
     "titre_nl": "De grondwetgever",
     "regle_fr": "Un chantier de charge « révision » ou « loi spéciale » a été adopté avec "
                 "l'arithmétique requise.",
     "regle_nl": "Een hervorming met bijzondere-wet- of herzieningslast werd aangenomen.",
     "texte_fr": "La législature a modifié la règle du jeu elle-même, pas seulement ses résultats. "
                 "C'est la seule issue qui laisse une trace après le mandat.",
     "texte_nl": "De legislatuur wijzigde de spelregel zelf, niet enkel de uitkomst."},
    {"code": "reformateur", "titre_fr": "Le réformateur",
     "titre_nl": "De hervormer",
     "regle_fr": "Gain d'état de droit d'au moins 5 points.",
     "regle_nl": "Rechtsstaatwinst van minstens 5 punten.",
     "texte_fr": "Le lobbying, le financement des partis ou la justice ont bougé pour de bon. "
                 "L'écart budgétaire, lui, se reporte sur la législature suivante.",
     "texte_nl": "Lobbying, partijfinanciering of justitie zijn echt bewogen. De begrotingskloof "
                 "schuift door naar de volgende legislatuur."},
    {"code": "comptable", "titre_fr": "Le comptable",
     "titre_nl": "De boekhouder",
     "regle_fr": "Objectif budgétaire atteint : au moins 10 milliards d'euros structurels.",
     "regle_nl": "Begrotingsdoel gehaald: minstens 10 miljard euro structureel.",
     "texte_fr": "Les chiffres sont tenus. Les griefs du GRECO et de la Commission européenne, eux, "
                 "sont restés au même endroit — huit recommandations sur vingt-deux.",
     "texte_nl": "De cijfers kloppen. De grieven van GRECO en de Commissie bleven waar ze waren."},
    {"code": "reconduit", "titre_fr": "Reconduit",
     "titre_nl": "Verlengd",
     "regle_fr": "Aucune des conditions précédentes : la législature va à son terme sans "
                 "changer ni les comptes ni les règles.",
     "regle_nl": "Geen van de vorige voorwaarden: de legislatuur eindigt zonder de rekeningen "
                 "of de regels te veranderen.",
     "texte_fr": "Quatre ans, quinze ministres, un accord de gouvernement et un pays dans le même "
                 "état qu'au départ. C'est l'issue la plus fréquente du modèle, et ce n'est pas un hasard.",
     "texte_nl": "Vier jaar, vijftien ministers, en een land in dezelfde staat als bij de start."},
]
