# -*- coding: utf-8 -*-
"""Points de départ du modèle : le scrutin de 2024 et les enquêtes publiées depuis.

Un sondage n'est pas une prévision. Il est ici un *point de départ* que le
joueur choisit explicitement, et dont l'écart avec le vote réel de 2024 fournit
le vecteur de report initial. Les parts non renseignées par une enquête sont
complétées par le résultat 2024 de la liste concernée, puis l'ensemble est
renormalisé à 100 % : le procédé est décrit sur la page Méthode.
"""

SONDAGES = [
    {
        "code": "resultat2024",
        "nom_fr": "Le vote de 2024",
        "nom_nl": "De stembusgang van 2024",
        "date": "2024-06-09",
        "institut_fr": "SPF Intérieur — résultat officiel",
        "institut_nl": "FOD Binnenlandse Zaken — officieel resultaat",
        "marge": None,
        "source": "spf-resultats",
        "note_fr": "Aucun report : le modèle part du dernier vote réellement exprimé. "
                   "C'est le seul point de départ qui ne repose sur aucune enquête.",
        "note_nl": "Geen verschuiving: het model vertrekt van de laatste werkelijk "
                   "uitgebrachte stem. Dit is het enige startpunt zonder enquête.",
        "parts": None,
    },
    {
        "code": "enquete2026",
        "nom_fr": "Enquête nationale 2026",
        "nom_nl": "Nationaal verkiezingsonderzoek 2026",
        "date": "2026-04-30",
        "institut_fr": "UAntwerpen et ULB — terrain mars-avril 2026, marge ±2,4 points",
        "institut_nl": "UAntwerpen en ULB — veldwerk maart-april 2026, marge ±2,4 punten",
        "marge": 2.4,
        "source": "enquete-nationale-2026",
        "note_fr": "Enquête académique. La N-VA reste devant en Flandre ; le PS "
                   "redevient premier en Wallonie ; le PTB est premier à Bruxelles.",
        "note_nl": "Academisch onderzoek. N-VA blijft eerste in Vlaanderen; PS is opnieuw "
                   "eerste in Wallonië; PVDA is eerste in Brussel.",
        "parts": {
            "fl": {"nva": 27.7, "vb": 20.8, "vooruit": 12.9, "cdv": 12.2, "pvda": 8.2, "groen": 7.3},
            "wa": {"ps": 24.9, "mr": 20.0, "le": 19.3, "ptb": 18.6, "ecolo": 6.8},
            "bxl": {"ptb": 24.4, "ps": 15.9, "mr": 14.2, "le": 11.4, "defi": 7.3, "ecolo": 6.5},
        },
    },
    {
        "code": "grande-enquete-mars2026",
        "nom_fr": "Grande Enquête, mars 2026",
        "nom_nl": "De Grote Peiling, maart 2026",
        "date": "2026-03-14",
        "institut_fr": "HLN, VTM Nieuws, RTL et Le Soir — publiée le 14 mars 2026",
        "institut_nl": "HLN, VTM Nieuws, RTL en Le Soir — gepubliceerd op 14 maart 2026",
        "marge": None,
        "source": "grande-enquete-mars-2026",
        "note_fr": "N-VA et Vlaams Belang à 0,1 point l'un de l'autre en Flandre. "
                   "Les parts wallonnes et bruxelloises sont celles de mars 2026.",
        "note_nl": "N-VA en Vlaams Belang op 0,1 punt van elkaar in Vlaanderen. "
                   "De Waalse en Brusselse cijfers zijn die van maart 2026.",
        "parts": {
            "fl": {"nva": 25.5, "vb": 25.4, "vooruit": 12.8, "cdv": 12.6, "pvda": 9.8, "groen": 7.7},
            "wa": {"ps": 26.0, "mr": 21.5, "le": 19.8, "ptb": 17.2, "ecolo": 7.4},
            "bxl": {"ptb": 24.0, "ps": 17.0, "mr": 14.5, "le": 10.0, "ecolo": 8.5, "defi": 6.5},
        },
    },
    {
        "code": "barometre-juin2026",
        "nom_fr": "Grand Baromètre, juin 2026",
        "nom_nl": "Grote Barometer, juni 2026",
        "date": "2026-06-12",
        "institut_fr": "RTL et Le Soir — publié le 12 juin 2026",
        "institut_nl": "RTL en Le Soir — gepubliceerd op 12 juni 2026",
        "marge": None,
        "source": "barometre-juin-2026",
        "note_fr": "Première enquête où le Vlaams Belang passe nettement devant la N-VA "
                   "en Flandre. Publiée à trois ans du scrutin : à prendre comme tel.",
        "note_nl": "Eerste peiling waarin Vlaams Belang duidelijk voorbij N-VA gaat in "
                   "Vlaanderen. Gepubliceerd op drie jaar van de verkiezing.",
        "parts": {
            "fl": {"vb": 26.6, "nva": 22.3, "vooruit": 12.9, "cdv": 12.6, "pvda": 10.1, "groen": 6.8},
            "wa": {"ps": 29.0, "le": 20.2, "mr": 20.1, "ptb": 16.8, "ecolo": 8.1},
            "bxl": {"ptb": 24.9, "ps": 18.4, "mr": 14.0, "le": 9.4, "ecolo": 8.9, "defi": 6.0},
        },
    },
]

SONDAGE_DEFAUT = "barometre-juin2026"
