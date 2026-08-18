# -*- coding: utf-8 -*-
"""Registre des listes. Source unique : aucun autre fichier ne redéfinit un parti.

`communaute` : fl = liste déposée en région flamande, fr = en région wallonne,
bi = présente des deux côtés ou à Bruxelles dans les deux collèges, dg = germanophone.
`famille` regroupe les listes qui sont un même parti sous deux étiquettes
(PVDA/PTB) — utilisé uniquement pour les totaux nationaux, jamais pour la
répartition des sièges, qui se fait liste par liste.
"""

PARTIS = {
    # --- listes néerlandophones ---
    "nva":      {"nom": "N-VA",            "long_fr": "Nieuw-Vlaamse Alliantie",   "long_nl": "Nieuw-Vlaamse Alliantie",   "communaute": "fl", "couleur": "#f5a623", "famille": "nva"},
    "vb":       {"nom": "Vlaams Belang",   "long_fr": "Vlaams Belang",             "long_nl": "Vlaams Belang",             "communaute": "fl", "couleur": "#c8a415", "famille": "vb"},
    "vooruit":  {"nom": "Vooruit",         "long_fr": "Vooruit",                   "long_nl": "Vooruit",                   "communaute": "fl", "couleur": "#f2748a", "famille": "soc_fl"},
    "cdv":      {"nom": "cd&v",            "long_fr": "Christen-Democratisch en Vlaams", "long_nl": "Christen-Democratisch en Vlaams", "communaute": "fl", "couleur": "#f79a3d", "famille": "cdv"},
    "openvld":  {"nom": "Open Vld",        "long_fr": "Open Vlaamse Liberalen en Democraten", "long_nl": "Open Vlaamse Liberalen en Democraten", "communaute": "fl", "couleur": "#3fa7ea", "famille": "openvld"},
    "groen":    {"nom": "Groen",           "long_fr": "Groen",                     "long_nl": "Groen",                     "communaute": "fl", "couleur": "#5cb85c", "famille": "vert_fl"},
    "pvda":     {"nom": "PVDA",            "long_fr": "Partij van de Arbeid van België", "long_nl": "Partij van de Arbeid van België", "communaute": "fl", "couleur": "#9d1b26", "famille": "ptb_pvda"},
    "ahidar":   {"nom": "Team Fouad Ahidar", "long_fr": "Team Fouad Ahidar",       "long_nl": "Team Fouad Ahidar",         "communaute": "fl", "couleur": "#7c5cbf", "famille": "ahidar"},
    "vooruitbxl": {"nom": "Vooruit.brussels", "long_fr": "Vooruit.brussels",       "long_nl": "Vooruit.brussels",          "communaute": "fl", "couleur": "#f2748a", "famille": "soc_fl"},

    # --- listes francophones ---
    "mr":       {"nom": "MR",              "long_fr": "Mouvement réformateur",     "long_nl": "Mouvement réformateur",     "communaute": "fr", "couleur": "#3fa7ea", "famille": "mr"},
    "ps":       {"nom": "PS",              "long_fr": "Parti socialiste",          "long_nl": "Parti socialiste",          "communaute": "fr", "couleur": "#e0344b", "famille": "ps"},
    "le":       {"nom": "Les Engagés",     "long_fr": "Les Engagés",               "long_nl": "Les Engagés",               "communaute": "fr", "couleur": "#3ec6b6", "famille": "le"},
    "ptb":      {"nom": "PTB",             "long_fr": "Parti du Travail de Belgique", "long_nl": "Partij van de Arbeid van België", "communaute": "fr", "couleur": "#9d1b26", "famille": "ptb_pvda"},
    "ecolo":    {"nom": "Ecolo",           "long_fr": "Ecolo",                     "long_nl": "Ecolo",                     "communaute": "fr", "couleur": "#5cb85c", "famille": "vert_fr"},
    "defi":     {"nom": "DéFI",            "long_fr": "Démocrate Fédéraliste Indépendant", "long_nl": "Démocrate Fédéraliste Indépendant", "communaute": "fr", "couleur": "#c86fd1", "famille": "defi"},
    "cheznous": {"nom": "Chez Nous",       "long_fr": "Chez Nous",                 "long_nl": "Chez Nous",                 "communaute": "fr", "couleur": "#8a6a3a", "famille": "cheznous"},
    "cc":       {"nom": "Collectif Citoyen", "long_fr": "Collectif Citoyen",       "long_nl": "Collectif Citoyen",         "communaute": "fr", "couleur": "#9aa0a6", "famille": "autres"},

    # --- listes germanophones ---
    "prodg":    {"nom": "ProDG",           "long_fr": "Pro Deutschsprachige Gemeinschaft", "long_nl": "Pro Deutschsprachige Gemeinschaft", "communaute": "dg", "couleur": "#f5a623", "famille": "prodg"},
    "csp":      {"nom": "CSP",             "long_fr": "Christlich Soziale Partei", "long_nl": "Christlich Soziale Partei",  "communaute": "dg", "couleur": "#f79a3d", "famille": "csp"},
    "vivant":   {"nom": "Vivant",          "long_fr": "Vivant",                    "long_nl": "Vivant",                    "communaute": "dg", "couleur": "#9b59b6", "famille": "vivant"},
    "sp":       {"nom": "SP",              "long_fr": "Sozialistische Partei",     "long_nl": "Sozialistische Partei",     "communaute": "dg", "couleur": "#e0344b", "famille": "sp"},
    "pffmr":    {"nom": "PFF-MR",          "long_fr": "Partei für Freiheit und Fortschritt", "long_nl": "Partei für Freiheit und Fortschritt", "communaute": "dg", "couleur": "#3fa7ea", "famille": "mr"},
    "ecolodg":  {"nom": "Ecolo (DG)",      "long_fr": "Ecolo — Communauté germanophone", "long_nl": "Ecolo — Duitstalige Gemeenschap", "communaute": "dg", "couleur": "#5cb85c", "famille": "vert_fr"},

    # --- petites listes, sans siège en 2024 (conservées pour que les totaux soient exacts) ---
    "voru":     {"nom": "Voor U",          "long_fr": "Voor U",                    "long_nl": "Voor U",                    "communaute": "fl", "couleur": "#9aa0a6", "famille": "autres"},
    "blanco":   {"nom": "Blanco",          "long_fr": "Partij Blanco / Parti Blanco", "long_nl": "Partij Blanco",          "communaute": "bi", "couleur": "#9aa0a6", "famille": "autres"},
    "bub":      {"nom": "BUB",             "long_fr": "Belgische Unie — Union belge", "long_nl": "Belgische Unie",         "communaute": "bi", "couleur": "#9aa0a6", "famille": "autres"},
    "volt":     {"nom": "Volt",            "long_fr": "Volt Europa",               "long_nl": "Volt Europa",               "communaute": "bi", "couleur": "#9aa0a6", "famille": "autres"},
    "dieranimal": {"nom": "DierAnimal",    "long_fr": "DierAnimal",                "long_nl": "DierAnimal",                "communaute": "bi", "couleur": "#9aa0a6", "famille": "autres"},
    "bbb":      {"nom": "BBB",             "long_fr": "Boer Burger Beweging",      "long_nl": "Boer Burger Beweging",      "communaute": "fl", "couleur": "#9aa0a6", "famille": "autres"},
    "uf":       {"nom": "UF",              "long_fr": "Union des francophones",    "long_nl": "Union des Francophones",    "communaute": "fr", "couleur": "#9aa0a6", "famille": "autres"},
    "l99":      {"nom": "L99",             "long_fr": "L99",                       "long_nl": "L99",                       "communaute": "fl", "couleur": "#9aa0a6", "famille": "autres"},
    "lo":       {"nom": "Lutte ouvrière",  "long_fr": "Lutte ouvrière",            "long_nl": "Lutte ouvrière",            "communaute": "fr", "couleur": "#9aa0a6", "famille": "autres"},
    "agora":    {"nom": "Agora",           "long_fr": "Agora",                     "long_nl": "Agora",                     "communaute": "bi", "couleur": "#9aa0a6", "famille": "autres"},
    "rmc":      {"nom": "RMC",             "long_fr": "Rassemblement Modéré Citoyen", "long_nl": "Rassemblement Modéré Citoyen", "communaute": "fr", "couleur": "#9aa0a6", "famille": "autres"},
    "unie":     {"nom": "l'Unie",          "long_fr": "l'Unie",                    "long_nl": "l'Unie",                    "communaute": "bi", "couleur": "#9aa0a6", "famille": "autres"},
    "gv":       {"nom": "Gezond Verstand", "long_fr": "Gezond Verstand",           "long_nl": "Gezond Verstand",           "communaute": "fl", "couleur": "#9aa0a6", "famille": "autres"},
    "bomen":    {"nom": "Partij vr de Bomen", "long_fr": "Partij voor de Bomen",   "long_nl": "Partij voor de Bomen",      "communaute": "fl", "couleur": "#9aa0a6", "famille": "autres"},
    "transparence": {"nom": "Transparence", "long_fr": "Transparence",             "long_nl": "Transparence",              "communaute": "fr", "couleur": "#9aa0a6", "famille": "autres"},
    "planb":    {"nom": "Plan B",          "long_fr": "Plan B",                    "long_nl": "Plan B",                    "communaute": "fr", "couleur": "#9aa0a6", "famille": "autres"},
    "viva":     {"nom": "Viva Palestina!", "long_fr": "Viva Palestina !",          "long_nl": "Viva Palestina!",           "communaute": "fl", "couleur": "#9aa0a6", "famille": "autres"},
    "anticap":  {"nom": "Anticapitalistes", "long_fr": "Anticapitalistes",         "long_nl": "Anticapitalisten",          "communaute": "fr", "couleur": "#9aa0a6", "famille": "autres"},
    "huppertz": {"nom": "Huppertz+Co",     "long_fr": "Huppertz+Co",               "long_nl": "Huppertz+Co",               "communaute": "dg", "couleur": "#9aa0a6", "famille": "autres"},
    "liste24":  {"nom": "Liste24.dg",      "long_fr": "Liste24.dg",                "long_nl": "Liste24.dg",                "communaute": "dg", "couleur": "#9aa0a6", "famille": "autres"},
}

# Listes qui ont obtenu au moins un siège dans au moins une assemblée en 2024.
# C'est cette liste-là qui est jouable et documentée.
PARTIS_ELUS = [
    "nva", "vb", "vooruit", "cdv", "openvld", "groen", "pvda", "ahidar", "vooruitbxl",
    "mr", "ps", "le", "ptb", "ecolo", "defi",
    "prodg", "csp", "vivant", "sp", "pffmr", "ecolodg",
]
