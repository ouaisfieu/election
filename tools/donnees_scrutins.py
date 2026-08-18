# -*- coding: utf-8 -*-
"""Résultats officiels du 9 juin 2024, circonscription par circonscription.

Source unique et vérifiable : SPF Intérieur — Direction des Élections,
https://resultatselection.belgium.be/ (pages « circonscription électorale »
de chaque assemblée). Les nombres de voix sont recopiés tels quels ; les
pourcentages et les sièges sont RECALCULÉS par le build, jamais recopiés.

Le build échoue si :
  * la somme des voix d'une circonscription ne correspond pas au total déclaré ;
  * la répartition D'Hondt calculée ne reproduit pas les sièges officiels ;
  * la somme des sièges d'une assemblée ne correspond pas à son effectif légal.
"""

# ---------------------------------------------------------------------------
# CHAMBRE DES REPRÉSENTANTS — 150 sièges, 11 circonscriptions, seuil 5 %
# ---------------------------------------------------------------------------
CHAMBRE = {
    "code": "chambre",
    "sieges": 150,
    "seuil": 0.05,
    "circonscriptions": [
        {"code": "anvers", "nom_fr": "Anvers", "nom_nl": "Antwerpen", "region": "fl", "sieges": 24,
         "valables": 1191187,
         "voix": {"nva": 368877, "vb": 249826, "vooruit": 127973, "cdv": 125894, "pvda": 125257,
                  "groen": 90370, "openvld": 70890, "dieranimal": 10341, "voru": 8639,
                  "blanco": 7221, "volt": 4213, "bub": 1686},
         "officiel": {"nva": 8, "vb": 5, "vooruit": 3, "cdv": 3, "pvda": 2, "groen": 2, "openvld": 1}},

        {"code": "brabant-flamand", "nom_fr": "Brabant flamand", "nom_nl": "Vlaams-Brabant", "region": "fl", "sieges": 15,
         "valables": 716685,
         "voix": {"nva": 182883, "vb": 119345, "vooruit": 98092, "cdv": 93465, "openvld": 83744,
                  "pvda": 57600, "groen": 57395, "voru": 9961, "blanco": 6859, "bub": 4086, "unie": 3255},
         "officiel": {"nva": 4, "vb": 3, "vooruit": 2, "cdv": 2, "openvld": 2, "pvda": 1, "groen": 1}},

        {"code": "brabant-wallon", "nom_fr": "Brabant wallon", "nom_nl": "Waals-Brabant", "region": "wa", "sieges": 5,
         "valables": 256272,
         "voix": {"mr": 90486, "le": 58077, "ps": 31741, "ecolo": 23587, "ptb": 20221, "defi": 8750,
                  "nva": 5753, "blanco": 4830, "cc": 4781, "cheznous": 4659, "bub": 1003,
                  "unie": 918, "agora": 802, "rmc": 664},
         "officiel": {"mr": 3, "le": 1, "ps": 1}},

        {"code": "bruxelles", "nom_fr": "Bruxelles-Capitale", "nom_nl": "Brussel-Hoofdstad", "region": "bxl", "sieges": 16,
         "valables": 518926,
         "voix": {"mr": 120155, "ps": 96516, "ptb": 86927, "ecolo": 58645, "le": 49425, "defi": 34143,
                  "ahidar": 24826, "nva": 14472, "vb": 12754, "cc": 6579, "blanco": 3287, "volt": 3032,
                  "lo": 1872, "agora": 1688, "bub": 1604, "voru": 1534, "unie": 1467},
         "officiel": {"mr": 4, "ps": 4, "ptb": 3, "ecolo": 2, "le": 2, "defi": 1}},

        {"code": "flandre-occidentale", "nom_fr": "Flandre occidentale", "nom_nl": "West-Vlaanderen", "region": "fl", "sieges": 16,
         "valables": 827055,
         "voix": {"vb": 202800, "nva": 192037, "vooruit": 137422, "cdv": 121447, "openvld": 65840,
                  "groen": 45502, "pvda": 44129, "voru": 9700, "blanco": 8178},
         "officiel": {"vb": 4, "nva": 4, "vooruit": 3, "cdv": 2, "openvld": 1, "groen": 1, "pvda": 1}},

        {"code": "flandre-orientale", "nom_fr": "Flandre orientale", "nom_nl": "Oost-Vlaanderen", "region": "fl", "sieges": 20,
         "valables": 1038657,
         "voix": {"vb": 234888, "nva": 231470, "vooruit": 127758, "cdv": 125871, "openvld": 119200,
                  "groen": 103722, "pvda": 75942, "blanco": 8057, "voru": 8007, "gv": 2352, "bub": 1390},
         "officiel": {"vb": 5, "nva": 5, "vooruit": 3, "cdv": 2, "openvld": 2, "groen": 2, "pvda": 1}},

        {"code": "hainaut", "nom_fr": "Hainaut", "nom_nl": "Henegouwen", "region": "wa", "sieges": 17,
         "valables": 739851,
         "voix": {"ps": 213501, "mr": 192759, "le": 114559, "ptb": 103339, "ecolo": 36750,
                  "cheznous": 22039, "defi": 15189, "nva": 14184, "blanco": 13224, "cc": 7201,
                  "lo": 4680, "bub": 2426},
         "officiel": {"ps": 6, "mr": 5, "le": 3, "ptb": 3}},

        {"code": "liege", "nom_fr": "Liège", "nom_nl": "Luik", "region": "wa", "sieges": 14,
         "valables": 631915,
         "voix": {"mr": 179296, "ps": 137443, "le": 103711, "ptb": 91188, "ecolo": 49936,
                  "cheznous": 21877, "defi": 13816, "nva": 10840, "blanco": 10656, "cc": 8289,
                  "rmc": 3361, "bub": 1502},
         "officiel": {"mr": 5, "ps": 3, "le": 3, "ptb": 2, "ecolo": 1}},

        {"code": "limbourg", "nom_fr": "Limbourg", "nom_nl": "Limburg", "region": "fl", "sieges": 12,
         "valables": 576774,
         "voix": {"vb": 141988, "nva": 136606, "cdv": 90715, "vooruit": 75191, "pvda": 52303,
                  "openvld": 40985, "groen": 27619, "voru": 5505, "blanco": 4660, "bub": 1202},
         "officiel": {"vb": 3, "nva": 3, "cdv": 2, "vooruit": 2, "pvda": 1, "openvld": 1}},

        {"code": "luxembourg", "nom_fr": "Luxembourg", "nom_nl": "Luxemburg", "region": "wa", "sieges": 4,
         "valables": 175409,
         "voix": {"le": 56289, "mr": 54196, "ps": 29488, "ecolo": 13506, "cheznous": 5888,
                  "nva": 4413, "cc": 4300, "defi": 3975, "blanco": 3354},
         "officiel": {"le": 2, "mr": 1, "ps": 1}},

        {"code": "namur", "nom_fr": "Namur", "nom_nl": "Namen", "region": "wa", "sieges": 7,
         "valables": 312175,
         "voix": {"le": 90694, "mr": 80042, "ps": 52913, "ptb": 31463, "ecolo": 22014,
                  "cheznous": 9595, "defi": 8151, "nva": 5526, "blanco": 5357, "cc": 4556,
                  "agora": 983, "bub": 881},
         "officiel": {"le": 3, "mr": 2, "ps": 1, "ptb": 1}},
    ],
}

# ---------------------------------------------------------------------------
# PARLEMENT FLAMAND — 124 sièges (118 en région flamande + 6 à Bruxelles)
# ---------------------------------------------------------------------------
PARLEMENT_FLAMAND = {
    "code": "flamand",
    "sieges": 124,
    "seuil": 0.05,
    "circonscriptions": [
        {"code": "anvers", "nom_fr": "Anvers", "nom_nl": "Antwerpen", "region": "fl", "sieges": 33,
         "valables": 1167826,
         "voix": {"nva": 327349, "vb": 269402, "vooruit": 141450, "pvda": 126899, "cdv": 119014,
                  "groen": 88424, "openvld": 69126, "voru": 9219, "dieranimal": 8485, "bbb": 4448, "volt": 4010},
         "officiel": {"nva": 10, "vb": 8, "vooruit": 4, "pvda": 4, "cdv": 3, "groen": 2, "openvld": 2}},

        {"code": "brabant-flamand", "nom_fr": "Brabant flamand", "nom_nl": "Vlaams-Brabant", "region": "fl", "sieges": 21,
         "valables": 725565,
         "voix": {"nva": 168814, "vb": 126749, "vooruit": 96154, "cdv": 90776, "openvld": 88439,
                  "groen": 59004, "pvda": 58670, "uf": 20452, "voru": 9068, "bomen": 3771, "volt": 3668},
         "officiel": {"nva": 5, "vb": 4, "vooruit": 3, "cdv": 3, "openvld": 3, "groen": 2, "pvda": 1}},

        {"code": "flandre-occidentale", "nom_fr": "Flandre occidentale", "nom_nl": "West-Vlaanderen", "region": "fl", "sieges": 21,
         "valables": 815178,
         "voix": {"vb": 207902, "nva": 177789, "cdv": 146291, "vooruit": 120690, "openvld": 61046,
                  "groen": 46179, "pvda": 43162, "voru": 9553, "l99": 2566},
         "officiel": {"vb": 6, "nva": 5, "cdv": 4, "vooruit": 3, "openvld": 1, "groen": 1, "pvda": 1}},

        {"code": "flandre-orientale", "nom_fr": "Flandre orientale", "nom_nl": "Oost-Vlaanderen", "region": "fl", "sieges": 27,
         "valables": 1022996,
         "voix": {"vb": 238108, "nva": 227043, "vooruit": 167488, "cdv": 117056, "openvld": 99395,
                  "groen": 81074, "pvda": 78788, "voru": 9078, "bbb": 4966},
         "officiel": {"vb": 7, "nva": 6, "vooruit": 5, "cdv": 3, "openvld": 2, "groen": 2, "pvda": 2}},

        {"code": "limbourg", "nom_fr": "Limbourg", "nom_nl": "Limburg", "region": "fl", "sieges": 16,
         "valables": 568913,
         "voix": {"vb": 141912, "nva": 135747, "cdv": 92984, "vooruit": 72166, "pvda": 50183,
                  "openvld": 38185, "groen": 26779, "voru": 7338, "bbb": 3619},
         "officiel": {"vb": 5, "nva": 4, "cdv": 3, "vooruit": 2, "pvda": 1, "openvld": 1}},

        {"code": "bruxelles", "nom_fr": "Bruxelles (élus bruxellois)", "nom_nl": "Brussel (Brusselse leden)", "region": "bxl", "sieges": 6,
         "valables": 78962,
         "voix": {"groen": 17936, "ahidar": 14187, "nva": 9208, "vooruitbxl": 8458, "vb": 8431,
                  "openvld": 8418, "pvda": 6368, "cdv": 5016, "voru": 940},
         "officiel": {"groen": 2, "ahidar": 1, "nva": 1, "vooruitbxl": 1, "vb": 1}},
    ],
}

# ---------------------------------------------------------------------------
# PARLEMENT WALLON — 75 sièges, 11 circonscriptions
# ---------------------------------------------------------------------------
PARLEMENT_WALLON = {
    "code": "wallon",
    "sieges": 75,
    "seuil": 0.05,
    "circonscriptions": [
        {"code": "nivelles", "nom_fr": "Nivelles", "nom_nl": "Nijvel", "region": "wa", "sieges": 8,
         "valables": 248282,
         "voix": {"mr": 94100, "le": 58593, "ps": 32144, "ecolo": 23593, "ptb": 22037, "defi": 9593, "cc": 8222},
         "officiel": {"mr": 4, "le": 2, "ps": 1, "ecolo": 1}},

        {"code": "charleroi-thuin", "nom_fr": "Charleroi-Thuin", "nom_nl": "Charleroi-Thuin", "region": "wa", "sieges": 10,
         "valables": 257021,
         "voix": {"ps": 77432, "mr": 67877, "ptb": 40936, "le": 38480, "cheznous": 11843,
                  "ecolo": 9886, "defi": 6127, "cc": 4440},
         "officiel": {"ps": 3, "mr": 3, "ptb": 2, "le": 2}},

        {"code": "mons", "nom_fr": "Mons", "nom_nl": "Bergen", "region": "wa", "sieges": 5,
         "valables": 138745,
         "voix": {"ps": 46889, "mr": 37244, "ptb": 20170, "le": 19518, "ecolo": 6585,
                  "cheznous": 5191, "defi": 3148},
         "officiel": {"ps": 2, "mr": 2, "le": 1}},

        {"code": "tournai-ath-mouscron", "nom_fr": "Tournai-Ath-Mouscron", "nom_nl": "Doornik-Aat-Moeskroen", "region": "wa", "sieges": 7,
         "valables": 195935,
         "voix": {"mr": 55721, "ps": 48653, "le": 38742, "ptb": 25065, "ecolo": 14036,
                  "cheznous": 8932, "defi": 4786},
         "officiel": {"mr": 2, "ps": 2, "le": 1, "ptb": 1, "ecolo": 1}},

        {"code": "soignies-la-louviere", "nom_fr": "Soignies-La Louvière", "nom_nl": "Zinnik-La Louvière", "region": "wa", "sieges": 5,
         "valables": 136798,
         "voix": {"ps": 39630, "mr": 35409, "le": 23319, "ptb": 22356, "ecolo": 6846,
                  "cheznous": 5830, "defi": 3408},
         "officiel": {"ps": 2, "mr": 1, "le": 1, "ptb": 1}},

        {"code": "huy-waremme", "nom_fr": "Huy-Waremme", "nom_nl": "Hoei-Borgworm", "region": "wa", "sieges": 4,
         "valables": 125093,
         "voix": {"mr": 38986, "ps": 27812, "le": 24657, "ptb": 13178, "ecolo": 9194,
                  "cheznous": 4731, "defi": 3252, "cc": 2379, "rmc": 904},
         "officiel": {"le": 2, "mr": 1, "ps": 1}},

        {"code": "liege", "nom_fr": "Liège", "nom_nl": "Luik", "region": "wa", "sieges": 13,
         "valables": 336976,
         "voix": {"ps": 88446, "mr": 84621, "ptb": 56667, "le": 52239, "ecolo": 24192,
                  "cheznous": 14922, "defi": 8351, "cc": 5460, "rmc": 2078},
         "officiel": {"mr": 4, "ps": 3, "ptb": 3, "le": 2, "ecolo": 1}},

        {"code": "verviers", "nom_fr": "Verviers", "nom_nl": "Verviers", "region": "wa", "sieges": 6,
         "valables": 156811,
         "voix": {"mr": 53165, "le": 33669, "ps": 29862, "ptb": 15170, "ecolo": 13427,
                  "cheznous": 7116, "defi": 2684, "rmc": 1718},
         "officiel": {"mr": 2, "ps": 2, "le": 1, "ecolo": 1}},

        {"code": "luxembourg", "nom_fr": "Arlon-Marche-en-Famenne-Bastogne-Neufchâteau-Virton",
         "nom_nl": "Aarlen-Marche-en-Famenne-Bastenaken-Neufchâteau-Virton", "region": "wa", "sieges": 6,
         "valables": 167089,
         "voix": {"mr": 58034, "le": 52200, "ps": 31326, "ecolo": 13136, "cc": 7740, "defi": 4653},
         "officiel": {"mr": 3, "le": 2, "ps": 1}},

        {"code": "dinant-philippeville", "nom_fr": "Dinant-Philippeville", "nom_nl": "Dinant-Philippeville", "region": "wa", "sieges": 4,
         "valables": 110426,
         "voix": {"mr": 36503, "le": 28840, "ps": 21503, "ptb": 13026, "ecolo": 6941, "defi": 3613},
         "officiel": {"mr": 2, "le": 1, "ps": 1}},

        {"code": "namur", "nom_fr": "Namur", "nom_nl": "Namen", "region": "wa", "sieges": 7,
         "valables": 195590,
         "voix": {"le": 57222, "mr": 50830, "ps": 36721, "ptb": 21756, "ecolo": 16353,
                  "defi": 6179, "cc": 4959, "rmc": 1570},
         "officiel": {"le": 2, "mr": 2, "ps": 1, "ptb": 1, "ecolo": 1}},
    ],
}

# ---------------------------------------------------------------------------
# PARLEMENT BRUXELLOIS — 89 sièges : 72 au groupe linguistique français,
# 17 au groupe linguistique néerlandais. Deux collèges séparés, un seul territoire.
# ---------------------------------------------------------------------------
PARLEMENT_BRUXELLOIS = {
    "code": "bruxellois",
    "sieges": 89,
    "seuil": 0.05,
    "circonscriptions": [
        {"code": "college-francais", "nom_fr": "Collège français", "nom_nl": "Franse taalgroep",
         "region": "bxl", "sieges": 72, "valables": 389761,
         "voix": {"mr": 101157, "ps": 85929, "ptb": 81542, "le": 41640, "ecolo": 38386,
                  "defi": 31614, "cc": 5642, "volt": 1531, "transparence": 1282, "planb": 1038},
         "officiel": {"mr": 20, "ps": 16, "ptb": 15, "le": 8, "ecolo": 7, "defi": 6}},

        {"code": "college-neerlandais", "nom_fr": "Collège néerlandais", "nom_nl": "Nederlandse taalgroep",
         "region": "bxl", "sieges": 17, "valables": 80379,
         "voix": {"groen": 18345, "ahidar": 13242, "nva": 9571, "openvld": 8537, "vb": 8475,
                  "vooruitbxl": 8045, "pvda": 5619, "cdv": 5102, "viva": 1944, "voru": 930, "volt": 569},
         "officiel": {"groen": 4, "ahidar": 3, "nva": 2, "openvld": 2, "vb": 2, "vooruitbxl": 2,
                      "pvda": 1, "cdv": 1}},
    ],
}

# ---------------------------------------------------------------------------
# PARLEMENT DE LA COMMUNAUTÉ GERMANOPHONE — 25 sièges, circonscription unique
# ---------------------------------------------------------------------------
PARLEMENT_GERMANOPHONE = {
    "code": "germanophone",
    "sieges": 25,
    "seuil": 0.0,
    "circonscriptions": [
        {"code": "germanophone", "nom_fr": "Communauté germanophone", "nom_nl": "Duitstalige Gemeenschap",
         "region": "dg", "sieges": 25, "valables": 40047,
         "voix": {"prodg": 11654, "csp": 7920, "vivant": 5700, "sp": 5473, "pffmr": 4817,
                  "ecolodg": 3644, "huppertz": 666, "liste24": 173},
         "officiel": {"prodg": 8, "csp": 5, "vivant": 4, "sp": 3, "pffmr": 3, "ecolodg": 2}},
    ],
}

ASSEMBLEES = {
    "chambre": CHAMBRE,
    "flamand": PARLEMENT_FLAMAND,
    "wallon": PARLEMENT_WALLON,
    "bruxellois": PARLEMENT_BRUXELLOIS,
    "germanophone": PARLEMENT_GERMANOPHONE,
}

NOMS_ASSEMBLEES = {
    "chambre":      {"fr": "Chambre des représentants", "nl": "Kamer van volksvertegenwoordigers"},
    "flamand":      {"fr": "Parlement flamand",         "nl": "Vlaams Parlement"},
    "wallon":       {"fr": "Parlement wallon",          "nl": "Waals Parlement"},
    "bruxellois":   {"fr": "Parlement bruxellois",      "nl": "Brussels Parlement"},
    "germanophone": {"fr": "Parlement de la Communauté germanophone", "nl": "Parlement van de Duitstalige Gemeenschap"},
}
