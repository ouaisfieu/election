# -*- coding: utf-8 -*-
"""Acte III — la formation. Le site ne dit jamais qui peut gouverner avec qui.

Il expose des CONTRAINTES DE DROIT, qui ne sont pas négociables, et des
EXCLUSIONS DÉCLARÉES, qui sont des faits publics datés — le joueur décide
lesquelles il tient pour encore valables en 2029. Toute la partie « qui avec
qui » est un choix du joueur, jamais une recommandation du site.
"""

# --- contraintes de droit ---------------------------------------------------
CONTRAINTES = [
    {"code": "majorite", "titre_fr": "La majorité absolue à la Chambre",
     "titre_nl": "De absolute meerderheid in de Kamer",
     "texte_fr": "76 sièges sur 150. C'est la seule condition pour obtenir la confiance "
                 "(art. 96 de la Constitution : le gouvernement doit obtenir la confiance de la Chambre).",
     "texte_nl": "76 van de 150 zetels. Dit is de enige voorwaarde voor het vertrouwen "
                 "(art. 96 van de Grondwet).",
     "source": "constitution-96"},
    {"code": "parite", "titre_fr": "La parité linguistique au Conseil des ministres",
     "titre_nl": "De taalpariteit in de Ministerraad",
     "texte_fr": "Article 99 de la Constitution : le Conseil des ministres compte au maximum "
                 "quinze membres et, le Premier ministre éventuellement excepté, autant de "
                 "ministres d'expression française que d'expression néerlandaise.",
     "texte_nl": "Artikel 99 van de Grondwet: de Ministerraad telt ten hoogste vijftien leden en, "
                 "de eerste minister eventueel uitgezonderd, evenveel Nederlandstalige als "
                 "Franstalige ministers.",
     "source": "constitution-99"},
    {"code": "loi-speciale", "titre_fr": "La majorité spéciale",
     "titre_nl": "De bijzondere meerderheid",
     "texte_fr": "Article 4 de la Constitution : une loi spéciale — toute modification de la "
                 "répartition des compétences — exige la majorité dans chaque groupe linguistique "
                 "de chaque chambre, la présence de la majorité des membres de chaque groupe, et "
                 "les deux tiers des suffrages exprimés au total.",
     "texte_nl": "Artikel 4 van de Grondwet: een bijzondere wet vereist een meerderheid in elke "
                 "taalgroep, het aanwezigheidsquorum per taalgroep, en twee derde van de uitgebrachte stemmen.",
     "source": "constitution-4"},
    {"code": "revision", "titre_fr": "La révision de la Constitution",
     "titre_nl": "De grondwetsherziening",
     "texte_fr": "Article 195 : les chambres déclarent les articles à réviser, sont dissoutes de "
                 "plein droit, et les nouvelles chambres statuent à la majorité des deux tiers, "
                 "avec un quorum de deux tiers des membres.",
     "texte_nl": "Artikel 195: de kamers wijzen de te herziene artikelen aan, worden van rechtswege "
                 "ontbonden, en de nieuwe kamers beslissen met twee derde meerderheid.",
     "source": "constitution-195"},
    {"code": "dissolution", "titre_fr": "La dissolution anticipée",
     "titre_nl": "De vervroegde ontbinding",
     "texte_fr": "Article 46 : trois cas seulement — rejet d'une motion de confiance sans "
                 "successeur proposé dans les trois jours ; adoption d'une motion de méfiance sans "
                 "successeur ; démission du gouvernement avec l'accord de la Chambre à la majorité "
                 "absolue. Les élections se tiennent dans les quarante jours.",
     "texte_nl": "Artikel 46: slechts drie gevallen. De verkiezingen vinden plaats binnen veertig dagen.",
     "source": "crisp-dissolution"},
]

# --- exclusions déclarées : des faits publics, pas des jugements -------------
EXCLUSIONS = [
    {"code": "cordon", "titre_fr": "Le cordon sanitaire",
     "titre_nl": "Het cordon sanitaire",
     "cible": ["vb"],
     "par": ["nva", "cdv", "openvld", "vooruit", "groen", "pvda"],
     "fait_fr": "Depuis 1989, les autres partis flamands refusent publiquement toute coalition "
                "avec le Vlaams Blok puis le Vlaams Belang. L'engagement est renouvelé à chaque "
                "scrutin ; il n'a aucune valeur juridique et n'engage que ceux qui le prennent.",
     "fait_nl": "Sinds 1989 weigeren de andere Vlaamse partijen publiek elke coalitie met het "
                "Vlaams Blok en later Vlaams Belang. De afspraak heeft geen juridische waarde.",
     "defaut": True, "source": "cordon-vrt"},
    {"code": "ptb-federal", "titre_fr": "Le refus du PTB d'entrer au fédéral",
     "titre_nl": "De weigering van PVDA om federaal toe te treden",
     "cible": ["ptb", "pvda"],
     "par": [],
     "fait_fr": "Le PTB-PVDA n'a jamais participé à un gouvernement fédéral et pose des conditions "
                "programmatiques que les autres formations ont jusqu'ici refusées. C'est un fait "
                "observé, pas une règle : il peut cesser d'être vrai.",
     "fait_nl": "PVDA-PTB nam nooit deel aan een federale regering. Dat is een vaststelling, geen regel.",
     "defaut": True, "source": "crisp-ptb"},
]

# --- postes ministériels ----------------------------------------------------
# Le gouvernement De Wever compte quinze ministres, sans secrétaires d'État
# (prestation de serment le 3 février 2025) — c'est le format retenu ici.
PORTEFEUILLES = [
    {"code": "pm", "fr": "Premier ministre", "nl": "Eerste minister", "poids": 5, "groupe": "libre"},
    {"code": "budget", "fr": "Budget et Finances", "nl": "Begroting en Financiën", "poids": 4, "groupe": "nl"},
    {"code": "emploi", "fr": "Emploi et Pensions", "nl": "Werk en Pensioenen", "poids": 4, "groupe": "fr"},
    {"code": "justice", "fr": "Justice", "nl": "Justitie", "poids": 4, "groupe": "nl"},
    {"code": "interieur", "fr": "Intérieur et Asile", "nl": "Binnenlandse Zaken en Asiel", "poids": 4, "groupe": "nl"},
    {"code": "social", "fr": "Affaires sociales et Santé", "nl": "Sociale Zaken en Volksgezondheid", "poids": 4, "groupe": "fr"},
    {"code": "economie", "fr": "Économie et Énergie", "nl": "Economie en Energie", "poids": 3, "groupe": "fr"},
    {"code": "defense", "fr": "Défense", "nl": "Defensie", "poids": 3, "groupe": "nl"},
    {"code": "etrangeres", "fr": "Affaires étrangères", "nl": "Buitenlandse Zaken", "poids": 3, "groupe": "fr"},
    {"code": "mobilite", "fr": "Mobilité et Entreprises publiques", "nl": "Mobiliteit en Overheidsbedrijven", "poids": 2, "groupe": "nl"},
    {"code": "fonction", "fr": "Fonction publique et Numérique", "nl": "Ambtenarenzaken en Digitalisering", "poids": 2, "groupe": "fr"},
    {"code": "climat", "fr": "Climat et Environnement", "nl": "Klimaat en Leefmilieu", "poids": 2, "groupe": "nl"},
    {"code": "cooperation", "fr": "Coopération au développement", "nl": "Ontwikkelingssamenwerking", "poids": 1, "groupe": "fr"},
    {"code": "independants", "fr": "Classes moyennes et Indépendants", "nl": "Middenstand en Zelfstandigen", "poids": 1, "groupe": "nl"},
    {"code": "egalite", "fr": "Égalité des chances et Institutions", "nl": "Gelijke Kansen en Instellingen", "poids": 1, "groupe": "fr"},
]

# --- chantiers de l'accord de gouvernement ----------------------------------
# Chacun porte la charge normative qu'il exige réellement : c'est cette charge
# qui décide si la coalition peut ou non l'adopter, et l'arithmétique tranche.
CHANTIERS = [
    {"code": "trajectoire", "titre_fr": "La trajectoire budgétaire 2029-2034",
     "titre_nl": "Het begrotingstraject 2029-2034", "norme": "loi",
     "cout_fr": "Rendement visé : 10 milliards d'euros structurels sur la législature.",
     "cout_nl": "Beoogde opbrengst: 10 miljard euro structureel over de legislatuur.",
     "effet": {"budget": +10, "cohesion": -2, "droit": 0}, "source": "monitoring-2026"},
    {"code": "financement-partis", "titre_fr": "Le financement des partis et le contrôle externe",
     "titre_nl": "De partijfinanciering en de externe controle", "norme": "loi",
     "cout_fr": "104 millions d'euros de dotations aux groupes et collaborateurs en 2024 ; "
                "80 à 90 % des ressources des partis sont publiques.",
     "cout_nl": "104 miljoen euro dotaties in 2024; 80 tot 90 % van de partijmiddelen is publiek.",
     "effet": {"budget": +0.1, "cohesion": -3, "droit": +3}, "source": "greco-2025"},
    {"code": "lobbying", "titre_fr": "Un registre de lobbying contraignant et le pantouflage",
     "titre_nl": "Een bindend lobbyregister en draaideurpolitiek", "norme": "loi",
     "cout_fr": "Grief constant de la Commission européenne et du GRECO : aucune avancée "
                "constatée au 17 juillet 2026.",
     "cout_nl": "Vaste grief van de Europese Commissie en GRECO: geen vooruitgang op 17 juli 2026.",
     "effet": {"budget": 0, "cohesion": -1, "droit": +3}, "source": "cue-etat-de-droit-2026"},
    {"code": "justice", "titre_fr": "Le refinancement de la justice",
     "titre_nl": "De herfinanciering van justitie", "norme": "loi",
     "cout_fr": "La justice pèse environ 0,5 % du budget de l'État après quelque 14 % de coupes cumulées.",
     "cout_nl": "Justitie weegt ongeveer 0,5 % van de staatsbegroting na circa 14 % cumulatieve besparingen.",
     "effet": {"budget": -1.5, "cohesion": +1, "droit": +3}, "source": "memorandum-juridictions"},
    {"code": "case-de-tete", "titre_fr": "La suppression de l'effet dévolutif de la case de tête",
     "titre_nl": "De afschaffing van het devolutief effect van de lijststem", "norme": "loi",
     "cout_fr": "L'effet dévolutif transfère la moitié du pot des votes de liste aux candidats "
                "dans l'ordre décidé par le parti. 88,6 % des bourgmestres wallons désignés en "
                "2024 étaient têtes de liste.",
     "cout_nl": "Het devolutief effect draagt de helft van de lijststemmen over volgens de "
                "partijvolgorde.",
     "effet": {"budget": 0, "cohesion": -4, "droit": +2}, "source": "crisp-devolutif"},
    {"code": "reforme-etat", "titre_fr": "Une réforme de l'État",
     "titre_nl": "Een staatshervorming", "norme": "loi-speciale",
     "cout_fr": "Toute modification de la répartition des compétences exige la majorité dans "
                "chaque groupe linguistique et les deux tiers au total (art. 4 de la Constitution).",
     "cout_nl": "Elke wijziging van de bevoegdheidsverdeling vereist een meerderheid in elke "
                "taalgroep en twee derde in totaal (art. 4 van de Grondwet).",
     "effet": {"budget": 0, "cohesion": -5, "droit": 0}, "source": "constitution-4"},
    {"code": "transaction", "titre_fr": "La transaction pénale élargie",
     "titre_nl": "De verruimde minnelijke schikking", "norme": "loi",
     "cout_fr": "Loi du 14 avril 2011, adoptée par amendement sans débat ; arrêt 83/2016 de la "
                "Cour constitutionnelle ; 1,6 million d'euros payés par ING le 5 mai 2026 sans "
                "reconnaissance de culpabilité.",
     "cout_nl": "Wet van 14 april 2011, aangenomen bij amendement zonder debat; arrest 83/2016.",
     "effet": {"budget": +0.3, "cohesion": -2, "droit": -2}, "source": "transaction-2011"},
    {"code": "circonscription", "titre_fr": "La circonscription fédérale",
     "titre_nl": "De federale kieskring", "norme": "revision",
     "cout_fr": "Une part des sièges de la Chambre élue dans une circonscription unique : "
                "cela suppose une révision de la Constitution, donc une dissolution préalable.",
     "cout_nl": "Een deel van de Kamerzetels verkozen in één kieskring: dit vereist een "
                "grondwetsherziening en dus een voorafgaande ontbinding.",
     "effet": {"budget": 0, "cohesion": -4, "droit": +2}, "source": "crisp-circonscription"},
]
