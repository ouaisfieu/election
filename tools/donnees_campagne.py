# -*- coding: utf-8 -*-
"""Acte I — les six échéances de la législature 2025-2029.

Chaque échéance est datée et documentée. Chaque issue est plausible : aucune
n'est présentée comme bonne ou mauvaise, et aucune n'est présentée comme
probable. Le joueur choisit ce qu'il tient pour l'issue la plus vraisemblable ;
le modèle applique le report de voix associé, en points de pourcentage, par
région. Ce report est une HYPOTHÈSE DE MODÈLE, écrite ici et republiée
intégralement sur la page Méthode et dans le procès-verbal.

`report` : {region: {liste: points}}. Les listes non citées ne bougent pas ;
l'ensemble est renormalisé à 100 % après application (voir moteur).
`bande` : incertitude en points que le modèle attache à ce report.
"""

ECHEANCES = [
    {
        "code": "conclave",
        "date": "2026-09-30",
        "titre_fr": "Le conclave budgétaire de l'automne 2026",
        "titre_nl": "Het begrotingsconclaaf van najaar 2026",
        "contexte_fr":
            "Le comité de monitoring de juillet 2026 chiffre l'écart à 7,7 milliards d'euros "
            "d'ici 2029 et 9,8 milliards d'ici 2031, contre 4,9 milliards estimés en mars. "
            "Le 10 juillet 2026, le gouvernement s'est fixé 10 milliards d'ici 2029, dont "
            "« plus des deux tiers » structurels. Le conclave s'ouvre fin septembre ; la "
            "déclaration de politique fédérale est attendue le deuxième mardi d'octobre.",
        "contexte_nl":
            "Het monitoringcomité becijferde in juli 2026 het tekort op 7,7 miljard euro tegen "
            "2029 en 9,8 miljard tegen 2031, tegenover 4,9 miljard in maart. Op 10 juli 2026 "
            "legde de regering 10 miljard tegen 2029 vast, waarvan « meer dan twee derde » "
            "structureel. Het conclaaf begint eind september.",
        "issues": [
            {"code": "accord-structurel", "titre_fr": "Un accord majoritairement structurel",
             "titre_nl": "Een overwegend structureel akkoord",
             "resume_fr": "Les 10 milliards sont bouclés, aux deux tiers par des mesures "
                          "permanentes : marché du travail, soins de santé, fiscalité du capital. "
                          "La coalition tient, le coût politique est réparti.",
             "resume_nl": "De 10 miljard wordt gehaald, voor twee derde met permanente "
                          "maatregelen. De coalitie houdt stand, de politieke kost wordt gedeeld.",
             "report": {"fl": {"nva": +1.2, "cdv": +0.4, "vooruit": -0.6, "vb": -0.8, "pvda": +0.4},
                        "wa": {"mr": +0.9, "le": +0.5, "ps": -0.7, "ptb": +0.6},
                        "bxl": {"mr": +0.7, "le": +0.3, "ps": -0.5, "ptb": +0.5}},
             "bande": 1.5,
             "justification_fr": "Un accord tenu profite d'abord aux partis qui le revendiquent "
                                 "et pénalise les partenaires qui en portent le coût social ; "
                                 "l'opposition de gauche capitalise sur les mesures permanentes.",
             "justification_nl": "Een gehaald akkoord komt eerst de partijen ten goede die het "
                                 "opeisen; de linkse oppositie kapitaliseert op de besparingen."},
            {"code": "accord-facade", "titre_fr": "Un accord de façade",
             "titre_nl": "Een akkoord in schijn",
             "resume_fr": "Le chiffre est annoncé mais reposant sur des recettes une fois, des "
                          "reports et des « efforts à préciser ». La Cour des comptes le relève "
                          "en décembre, comme elle l'a fait pour le budget 2026.",
             "resume_nl": "Het cijfer wordt aangekondigd maar steunt op eenmalige ontvangsten en "
                          "uitgestelde inspanningen. Het Rekenhof stelt dit in december vast.",
             "report": {"fl": {"vb": +1.4, "nva": -0.9, "pvda": +0.7, "cdv": -0.3, "vooruit": -0.4},
                        "wa": {"ptb": +1.3, "ps": +0.3, "mr": -1.0, "le": -0.4},
                        "bxl": {"ptb": +1.2, "ps": +0.2, "mr": -0.9, "le": -0.3}},
             "bande": 1.5,
             "justification_fr": "L'écart entre l'annonce et le contrôle nourrit les oppositions "
                                 "aux deux extrémités et coûte aux partis qui ont porté le chiffre.",
             "justification_nl": "De kloof tussen aankondiging en controle voedt de oppositie "
                                 "aan beide uiteinden."},
            {"code": "echec", "titre_fr": "L'échec et la crise",
             "titre_nl": "Mislukking en crisis",
             "resume_fr": "Le conclave n'aboutit pas dans les délais. Le gouvernement fonctionne "
                          "en douzièmes provisoires ; l'hypothèse d'une démission est ouverte. "
                          "L'article 46 de la Constitution encadre alors la dissolution.",
             "resume_nl": "Het conclaaf haalt de deadline niet. De regering werkt met voorlopige "
                          "twaalfden; artikel 46 van de Grondwet regelt de ontbinding.",
             "report": {"fl": {"vb": +2.6, "nva": -1.6, "pvda": +0.9, "cdv": -0.5, "vooruit": -0.8, "groen": +0.2},
                        "wa": {"ptb": +2.2, "ps": +0.6, "mr": -1.8, "le": -1.0, "ecolo": +0.3},
                        "bxl": {"ptb": +2.0, "ps": +0.5, "mr": -1.6, "le": -0.8, "ecolo": +0.3}},
             "bande": 2.5,
             "justification_fr": "Une crise budgétaire ouverte a historiquement profité aux partis "
                                 "hors coalition ; l'ampleur du report est la plus incertaine du modèle.",
             "justification_nl": "Een open begrotingscrisis kwam historisch de partijen buiten de "
                                 "coalitie ten goede; dit is de meest onzekere verschuiving."},
        ],
    },
    {
        "code": "pensions",
        "date": "2027-03-01",
        "titre_fr": "Les pensions et la concertation sociale",
        "titre_nl": "De pensioenen en het sociaal overleg",
        "contexte_fr":
            "Le front commun syndical a mené des grèves nationales en 2025 et 2026, dont celle "
            "du 12 mars 2026 sur les pensions et l'indexation. Les magistrats eux-mêmes se sont "
            "mis en grève sur la question des pensions. La trajectoire budgétaire suppose un "
            "rendement des mesures pensions que la Cour des comptes juge incertain.",
        "contexte_nl":
            "Het gemeenschappelijk vakbondsfront voerde nationale stakingen in 2025 en 2026, "
            "waaronder die van 12 maart 2026 over pensioenen en indexering.",
        "issues": [
            {"code": "impose", "titre_fr": "La réforme passe en force",
             "titre_nl": "De hervorming wordt doorgeduwd",
             "resume_fr": "Le texte est adopté sans accord des interlocuteurs sociaux. "
                          "Le rendement budgétaire est acquis ; le conflit social s'installe.",
             "resume_nl": "De tekst wordt aangenomen zonder akkoord van de sociale partners.",
             "report": {"fl": {"pvda": +1.3, "vb": +0.7, "vooruit": -1.0, "nva": +0.3, "cdv": -0.4},
                        "wa": {"ptb": +1.6, "ps": +0.5, "mr": -0.9, "le": -0.6},
                        "bxl": {"ptb": +1.5, "ps": +0.4, "mr": -0.8, "le": -0.5}},
             "bande": 1.5,
             "justification_fr": "Le conflit social bénéficie d'abord aux formations qui l'organisent "
                                 "ou le portent, et coûte au partenaire social-démocrate de la coalition.",
             "justification_nl": "Sociaal conflict komt eerst de organiserende formaties ten goede."},
            {"code": "negocie", "titre_fr": "Un compromis négocié",
             "titre_nl": "Een onderhandeld compromis",
             "resume_fr": "Accord partiel avec les interlocuteurs sociaux : calendrier étalé, "
                          "rendement réduit. L'écart budgétaire se creuse d'autant.",
             "resume_nl": "Gedeeltelijk akkoord met de sociale partners: gespreide kalender, "
                          "lagere opbrengst. Het begrotingstekort groeit navenant.",
             "report": {"fl": {"vooruit": +1.0, "cdv": +0.5, "nva": -0.6, "vb": -0.3, "pvda": -0.3},
                        "wa": {"ps": +0.6, "le": +0.5, "mr": -0.5, "ptb": -0.6},
                        "bxl": {"ps": +0.6, "le": +0.4, "mr": -0.4, "ptb": -0.6}},
             "bande": 1.2,
             "justification_fr": "Un compromis visible valorise les partis qui l'ont négocié et "
                                 "démobilise partiellement les oppositions de rupture.",
             "justification_nl": "Een zichtbaar compromis komt de onderhandelende partijen ten goede."},
            {"code": "recul", "titre_fr": "Le recul",
             "titre_nl": "De terugtrekking",
             "resume_fr": "La réforme est retirée ou vidée. Le coût social disparaît, le trou "
                          "budgétaire demeure et la crédibilité de la trajectoire s'érode.",
             "resume_nl": "De hervorming wordt ingetrokken of uitgehold. De begrotingskloof blijft.",
             "report": {"fl": {"vb": +1.1, "nva": -1.0, "vooruit": +0.4, "pvda": +0.3},
                        "wa": {"ptb": +0.8, "mr": -1.1, "ps": +0.5, "le": -0.2},
                        "bxl": {"ptb": +0.8, "mr": -1.0, "ps": +0.4}},
             "bande": 1.5,
             "justification_fr": "Un recul coûte au parti qui portait la réforme sans profiter "
                                 "durablement à ceux qui s'y opposaient.",
             "justification_nl": "Een terugtrekking kost de dragende partij zonder blijvend "
                                 "voordeel voor de tegenstanders."},
        ],
    },
    {
        "code": "etat-de-droit",
        "date": "2027-07-01",
        "titre_fr": "L'état de droit : GRECO, Commission, justice",
        "titre_nl": "De rechtsstaat: GRECO, Commissie, justitie",
        "contexte_fr":
            "L'addendum GrecoRC5(2025) de novembre 2025 ne considère que 8 recommandations sur 22 "
            "comme traitées de manière satisfaisante ; l'ultime étape de la procédure est une "
            "déclaration publique de non-conformité. Le rapport état de droit de la Commission "
            "européenne du 17 juillet 2026 relève que « le respect par le gouvernement des "
            "décisions définitives des tribunaux et des astreintes reste problématique », et "
            "aucune avancée sur le lobbying ni sur le pantouflage. La justice pèse environ "
            "0,5 % du budget de l'État après quelque 14 % de coupes cumulées.",
        "contexte_nl":
            "Het GRECO-addendum van november 2025 beschouwt slechts 8 van de 22 aanbevelingen als "
            "bevredigend opgevolgd. Het rechtsstaatrapport van 17 juli 2026 stelt vast dat de "
            "naleving van definitieve rechterlijke beslissingen problematisch blijft.",
        "issues": [
            {"code": "mise-en-conformite", "titre_fr": "Une mise en conformité",
             "titre_nl": "Een aanpassing aan de aanbevelingen",
             "resume_fr": "Registre de lobbying contraignant, contrôle externe du financement des "
                          "partis, refinancement partiel de la justice. Le dossier GRECO se referme.",
             "resume_nl": "Bindend lobbyregister, externe controle op partijfinanciering, "
                          "gedeeltelijke herfinanciering van justitie.",
             "report": {"fl": {"groen": +0.5, "cdv": +0.4, "vb": -0.9, "nva": +0.2, "pvda": -0.3},
                        "wa": {"ecolo": +0.6, "le": +0.5, "ptb": -0.5, "mr": +0.3},
                        "bxl": {"ecolo": +0.7, "le": +0.4, "ptb": -0.6, "mr": +0.3}},
             "bande": 1.2,
             "justification_fr": "Le grief d'entre-soi institutionnel alimente le vote protestataire ; "
                                 "le traiter le désamorce en partie.",
             "justification_nl": "De grief van institutionele geslotenheid voedt de proteststem."},
            {"code": "statu-quo", "titre_fr": "Le statu quo",
             "titre_nl": "Het status quo",
             "resume_fr": "Rien ne bouge : le financement des partis reste contrôlé par une "
                          "commission parlementaire, le lobbying reste non régulé.",
             "resume_nl": "Er verandert niets: partijfinanciering blijft gecontroleerd door een "
                          "parlementaire commissie, lobbying blijft ongereguleerd.",
             "report": {"fl": {"vb": +0.9, "pvda": +0.5, "nva": -0.4, "cdv": -0.3, "openvld": -0.3},
                        "wa": {"ptb": +0.9, "mr": -0.4, "ps": -0.4, "le": -0.2},
                        "bxl": {"ptb": +1.0, "mr": -0.4, "ps": -0.4}},
             "bande": 1.0,
             "justification_fr": "L'indice de perception de la corruption est passé de 77 à 69 entre "
                                 "2016 et 2025 ; l'inaction entretient cette pente.",
             "justification_nl": "De corruptieperceptie-index daalde van 77 naar 69 tussen 2016 en 2025."},
            {"code": "non-conformite", "titre_fr": "La déclaration de non-conformité",
             "titre_nl": "De verklaring van niet-naleving",
             "resume_fr": "Le GRECO va au bout de la règle 32. Le cadre financier européen "
                          "2028-2034 lie état de droit et financement : le dossier devient budgétaire.",
             "resume_nl": "GRECO gaat tot het einde van regel 32. Het Europese financiële kader "
                          "2028-2034 koppelt rechtsstaat aan financiering.",
             "report": {"fl": {"vb": +1.5, "pvda": +0.7, "nva": -0.7, "cdv": -0.5, "openvld": -0.4, "groen": +0.3},
                        "wa": {"ptb": +1.4, "ecolo": +0.4, "mr": -0.8, "ps": -0.6, "le": -0.4},
                        "bxl": {"ptb": +1.5, "ecolo": +0.5, "mr": -0.8, "ps": -0.6}},
             "bande": 1.8,
             "justification_fr": "Une sanction internationale explicite est un fait public daté, "
                                 "utilisable par toutes les oppositions.",
             "justification_nl": "Een expliciete internationale sanctie is een gedateerd publiek feit."},
        ],
    },
    {
        "code": "notation",
        "date": "2028-01-15",
        "titre_fr": "La note souveraine et la charge de la dette",
        "titre_nl": "De rating en de schuldenlast",
        "contexte_fr":
            "Le 17 avril 2026, Moody's a abaissé la Belgique de Aa3 à A1 : le pays perd son double A. "
            "La Wallonie et les Communautés ont été dégradées le 22 avril. Les charges d'intérêts "
            "fédérales dépassent 10 milliards d'euros depuis juillet 2026. Le déficit est projeté "
            "à 5,2 % du PIB en 2029 et la dette à 117,1 % du PIB.",
        "contexte_nl":
            "Op 17 april 2026 verlaagde Moody's België van Aa3 naar A1. De federale rentelasten "
            "overschrijden sinds juli 2026 de 10 miljard euro.",
        "issues": [
            {"code": "stabilisation", "titre_fr": "La stabilisation",
             "titre_nl": "Stabilisering",
             "resume_fr": "Perspective ramenée à stable, écart de taux contenu. Le coût de la dette "
                          "cesse de progresser plus vite que le PIB nominal.",
             "resume_nl": "Vooruitzicht terug op stabiel, renteverschil beheerst.",
             "report": {"fl": {"nva": +0.8, "openvld": +0.3, "vb": -0.5, "pvda": -0.3},
                        "wa": {"mr": +0.8, "le": +0.3, "ptb": -0.4, "ps": -0.3},
                        "bxl": {"mr": +0.7, "le": +0.2, "ptb": -0.4}},
             "bande": 1.0,
             "justification_fr": "Le crédit accordé à la gestion budgétaire profite aux partis qui "
                                 "en ont fait leur ligne principale.",
             "justification_nl": "Krediet voor het begrotingsbeleid komt de dragende partijen ten goede."},
            {"code": "nouvelle-degradation", "titre_fr": "Une nouvelle dégradation",
             "titre_nl": "Een nieuwe verlaging",
             "resume_fr": "Une deuxième dégradation en moins de deux ans. Le débat se déplace sur "
                          "la soutenabilité, et sur qui paie.",
             "resume_nl": "Een tweede verlaging in minder dan twee jaar. Het debat verschuift naar "
                          "houdbaarheid, en naar wie betaalt.",
             "report": {"fl": {"vb": +1.3, "nva": -0.8, "pvda": +0.6, "cdv": -0.3, "vooruit": -0.4},
                        "wa": {"ptb": +1.2, "mr": -1.1, "ps": +0.3, "le": -0.3},
                        "bxl": {"ptb": +1.2, "mr": -1.0, "ps": +0.3}},
             "bande": 1.5,
             "justification_fr": "L'échec sur le terrain choisi par la coalition coûte davantage "
                                 "que sur un terrain qu'elle n'a pas choisi.",
             "justification_nl": "Falen op het eigen gekozen terrein kost meer."},
            {"code": "choc-de-taux", "titre_fr": "Un choc de taux",
             "titre_nl": "Een renteschok",
             "resume_fr": "Un choc externe fait monter l'écart de taux. Les 21 milliards de charges "
                          "d'intérêts projetés pour 2030 par le Bureau du Plan deviennent une contrainte immédiate.",
             "resume_nl": "Een externe schok doet het renteverschil stijgen. De geprojecteerde "
                          "rentelasten worden een onmiddellijke beperking.",
             "report": {"fl": {"vb": +1.8, "nva": -0.5, "pvda": +0.9, "vooruit": -0.6, "cdv": -0.5, "openvld": -0.5},
                        "wa": {"ptb": +1.7, "mr": -1.0, "ps": -0.3, "le": -0.5, "ecolo": +0.3},
                        "bxl": {"ptb": +1.7, "mr": -1.0, "ps": -0.3, "ecolo": +0.3}},
             "bande": 2.2,
             "justification_fr": "Un choc exogène est le report le moins prévisible du modèle : "
                                 "il déplace le vote sans que le gouvernement en soit l'auteur.",
             "justification_nl": "Een exogene schok is de minst voorspelbare verschuiving."},
        ],
    },
    {
        "code": "migration",
        "date": "2028-06-01",
        "titre_fr": "Migration, sécurité et exécution des décisions de justice",
        "titre_nl": "Migratie, veiligheid en uitvoering van rechterlijke beslissingen",
        "contexte_fr":
            "Le 27 mars 2026, le Conseil d'État a suspendu des instructions ministérielles qui "
            "contournaient un arrêt de la Cour constitutionnelle en matière d'accueil ; la ministre "
            "a maintenu une politique au cas par cas. Le rapport européen du 17 juillet 2026 relève "
            "que l'exécution des astreintes reste problématique. Le nouveau Code pénal est entré "
            "en vigueur le 1er septembre 2026.",
        "contexte_nl":
            "Op 27 maart 2026 schorste de Raad van State ministeriële instructies die een arrest van "
            "het Grondwettelijk Hof omzeilden. Het nieuwe Strafwetboek trad in werking op 1 september 2026.",
        "issues": [
            {"code": "durcissement", "titre_fr": "Le durcissement assumé",
             "titre_nl": "De bewuste verstrakking",
             "resume_fr": "Le cadre légal est modifié pour aligner le droit sur la pratique. "
                          "Le contentieux se déplace vers les juridictions européennes.",
             "resume_nl": "Het wettelijk kader wordt aangepast aan de praktijk. Het geschil "
                          "verschuift naar de Europese rechtscolleges.",
             "report": {"fl": {"nva": +1.1, "vb": +0.6, "groen": -0.4, "cdv": -0.3, "vooruit": -0.3},
                        "wa": {"mr": +0.7, "le": +0.2, "ecolo": -0.4, "ps": -0.3},
                        "bxl": {"mr": +0.4, "ecolo": -0.5, "ptb": +0.4, "ps": -0.3}},
             "bande": 1.5,
             "justification_fr": "Le thème est plus saillant en Flandre : les médias néerlandophones "
                                 "lui donnent une place plus grande, ce que la recherche documente.",
             "justification_nl": "Het thema is salienter in Vlaanderen."},
            {"code": "arbitrage-judiciaire", "titre_fr": "L'arbitrage judiciaire contraignant",
             "titre_nl": "De bindende rechterlijke uitspraak",
             "resume_fr": "Les juridictions imposent l'exécution ; l'État paie les astreintes et "
                          "adapte sa politique. La contrainte judiciaire devient effective.",
             "resume_nl": "De rechtscolleges leggen uitvoering op; de staat betaalt de dwangsommen.",
             "report": {"fl": {"groen": +0.5, "vb": +0.9, "nva": -0.6, "cdv": +0.2},
                        "wa": {"ecolo": +0.6, "ptb": +0.3, "mr": -0.6, "le": +0.2},
                        "bxl": {"ecolo": +0.8, "ptb": +0.4, "mr": -0.7}},
             "bande": 1.3,
             "justification_fr": "Une contrainte judiciaire nourrit à la fois le camp qui la réclamait "
                                 "et le discours anti-institutionnel : le report est bilatéral.",
             "justification_nl": "Een rechterlijke beperking voedt beide kampen tegelijk."},
            {"code": "crise-execution", "titre_fr": "La crise d'exécution",
             "titre_nl": "De uitvoeringscrisis",
             "resume_fr": "Les décisions ne sont ni exécutées ni contestées : les astreintes "
                          "s'accumulent, l'autorité de la chose jugée s'effrite.",
             "resume_nl": "Beslissingen worden niet uitgevoerd noch aangevochten: de dwangsommen "
                          "stapelen zich op.",
             "report": {"fl": {"vb": +1.6, "pvda": +0.5, "nva": -0.5, "cdv": -0.4, "openvld": -0.3, "groen": +0.3},
                        "wa": {"ptb": +1.2, "ecolo": +0.4, "mr": -0.7, "ps": -0.5, "le": -0.3},
                        "bxl": {"ptb": +1.3, "ecolo": +0.5, "mr": -0.7, "ps": -0.5}},
             "bande": 1.8,
             "justification_fr": "L'inexécution durable des décisions de justice est le grief que "
                                 "la Commission européenne relève depuis plusieurs rapports.",
             "justification_nl": "De aanhoudende niet-uitvoering is de grief die de Commissie "
                                 "sinds meerdere rapporten vaststelt."},
        ],
    },
    {
        "code": "fin-de-legislature",
        "date": "2029-03-01",
        "titre_fr": "La fin de législature",
        "titre_nl": "Het einde van de legislatuur",
        "contexte_fr":
            "Les élections fédérales et régionales sont fixées au même jour, en principe en mai ou "
            "juin 2029. Une dissolution anticipée est encadrée par l'article 46 de la Constitution "
            "— trois cas seulement — et l'article 195 permet une dissolution automatique par la "
            "publication d'une déclaration de révision. Le scrutin doit alors se tenir dans les 40 jours.",
        "contexte_nl":
            "De federale en regionale verkiezingen vallen op dezelfde dag, in principe in mei of "
            "juni 2029. Artikel 46 van de Grondwet regelt de vervroegde ontbinding.",
        "issues": [
            {"code": "terme", "titre_fr": "La législature va à son terme",
             "titre_nl": "De legislatuur gaat tot het einde",
             "resume_fr": "Le gouvernement dépose un budget 2029 et se présente devant les électeurs "
                          "sur son bilan. La campagne dure ce qu'elle doit durer.",
             "resume_nl": "De regering dient een begroting 2029 in en verschijnt voor de kiezer.",
             "report": {"fl": {"nva": +0.6, "cdv": +0.3, "vb": -0.4},
                        "wa": {"mr": +0.5, "le": +0.3, "ptb": -0.3},
                        "bxl": {"mr": +0.4, "le": +0.2, "ptb": -0.3}},
             "bande": 1.0,
             "justification_fr": "Aller au terme est en soi un résultat dans un pays où la durée "
                                 "de formation d'un gouvernement est un enjeu public.",
             "justification_nl": "Het einde halen is op zich een resultaat."},
            {"code": "rupture", "titre_fr": "La rupture et les élections anticipées",
             "titre_nl": "De breuk en vervroegde verkiezingen",
             "resume_fr": "Un partenaire quitte la coalition. Le scrutin est avancé ; la campagne "
                          "se joue sur la responsabilité de la rupture.",
             "resume_nl": "Een partner verlaat de coalitie. De verkiezing wordt vervroegd.",
             "report": {"fl": {"vb": +1.7, "pvda": +0.6, "nva": -0.6, "cdv": -0.6, "vooruit": -0.6, "openvld": -0.4},
                        "wa": {"ptb": +1.5, "ecolo": +0.3, "mr": -0.9, "ps": -0.4, "le": -0.5},
                        "bxl": {"ptb": +1.6, "ecolo": +0.4, "mr": -0.9, "ps": -0.4, "le": -0.4}},
             "bande": 2.0,
             "justification_fr": "Les ruptures de coalition ont historiquement bénéficié aux "
                                 "formations extérieures plutôt qu'à celle qui rompt.",
             "justification_nl": "Coalitiebreuken kwamen historisch de buitenstaanders ten goede."},
            {"code": "affaires-courantes", "titre_fr": "Les affaires courantes",
             "titre_nl": "De lopende zaken",
             "resume_fr": "Le gouvernement démissionne mais reste en place. La Belgique a connu "
                          "541 jours sans gouvernement fédéral de plein exercice en 2010-2011, "
                          "236 jours en 2024-2025, et Bruxelles 613 jours en 2024-2026.",
             "resume_nl": "De regering treedt af maar blijft aan. België kende 541 dagen zonder "
                          "volwaardige federale regering in 2010-2011, 236 in 2024-2025, en "
                          "Brussel 613 dagen in 2024-2026.",
             "report": {"fl": {"vb": +2.0, "pvda": +0.7, "nva": -0.8, "cdv": -0.6, "vooruit": -0.7, "openvld": -0.5},
                        "wa": {"ptb": +1.8, "ecolo": +0.4, "mr": -1.0, "ps": -0.6, "le": -0.6},
                        "bxl": {"ptb": +1.9, "ecolo": +0.5, "mr": -1.0, "ps": -0.6, "le": -0.5}},
             "bande": 2.2,
             "justification_fr": "La durée d'incapacité à gouverner est le grief le plus directement "
                                 "mesurable de la particratie belge.",
             "justification_nl": "De duur van het onvermogen om te regeren is de meest meetbare grief."},
        ],
    },
]
