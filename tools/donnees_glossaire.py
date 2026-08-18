# -*- coding: utf-8 -*-
"""Glossaire. Chaque terme porte une source du registre."""

GLOSSAIRE = [
    {"code": "dhondt", "fr": "Clé D'Hondt", "nl": "D'Hondt-sleutel", "source": "crisp-proportionnel",
     "def_fr": "Méthode d'attribution des sièges : on divise le nombre de voix de chaque liste par "
               "1, 2, 3, 4… et on attribue les sièges aux quotients les plus élevés. Elle favorise "
               "légèrement les grandes listes, d'autant plus que la circonscription est petite.",
     "def_nl": "Methode voor zetelverdeling: het aantal stemmen van elke lijst wordt gedeeld door "
               "1, 2, 3, 4… en de zetels gaan naar de hoogste quotiënten."},
    {"code": "seuil", "fr": "Seuil d'éligibilité", "nl": "Kiesdrempel", "source": "spf-repartition-chambre",
     "def_fr": "Une liste qui n'atteint pas 5 % des votes valables d'une circonscription ne "
               "participe pas à la répartition des sièges de cette circonscription.",
     "def_nl": "Een lijst die geen 5 % van de geldige stemmen van een kieskring haalt, neemt niet "
               "deel aan de zetelverdeling."},
    {"code": "apparentement", "fr": "Apparentement", "nl": "Lijstenverbinding", "source": "crisp-apparentement",
     "def_fr": "Groupement de listes d'un même parti dans plusieurs circonscriptions d'une même "
               "province, qui permet une répartition complémentaire au niveau provincial. Il "
               "s'applique au Parlement wallon en Hainaut, à Liège et à Namur — pas à la Chambre, "
               "où il a disparu en 2003 avec le passage aux circonscriptions provinciales.",
     "def_nl": "Groepering van lijsten van eenzelfde partij in verschillende kieskringen van een "
               "provincie, met een aanvullende verdeling op provinciaal niveau."},
    {"code": "case-de-tete", "fr": "Case de tête et effet dévolutif", "nl": "Lijststem en devolutief effect",
     "source": "crisp-devolutif",
     "def_fr": "Voter en case de tête, c'est approuver l'ordre de la liste. La moitié de ces voix "
               "est redistribuée aux candidats dans l'ordre décidé par le parti : c'est l'effet "
               "dévolutif. Il décide qui, parmi les élus d'une liste, occupe les sièges gagnés.",
     "def_nl": "Een lijststem is een goedkeuring van de lijstvolgorde. De helft van die stemmen "
               "wordt verdeeld volgens de door de partij bepaalde volgorde."},
    {"code": "groupe-linguistique", "fr": "Groupe linguistique", "nl": "Taalgroep", "source": "constitution-4",
     "def_fr": "Les membres de la Chambre sont répartis en un groupe linguistique français et un "
               "groupe néerlandais. Une loi spéciale exige la majorité dans chacun des deux, "
               "en plus des deux tiers de l'ensemble.",
     "def_nl": "De leden van de Kamer zijn verdeeld in een Franse en een Nederlandse taalgroep."},
    {"code": "loi-speciale", "fr": "Loi spéciale", "nl": "Bijzondere wet", "source": "constitution-4",
     "def_fr": "Loi modifiant la répartition des compétences entre l'État fédéral, les Communautés "
               "et les Régions. Elle est le seul véhicule d'une réforme de l'État.",
     "def_nl": "Wet die de bevoegdheidsverdeling wijzigt. Het enige voertuig van een staatshervorming."},
    {"code": "affaires-courantes", "fr": "Affaires courantes", "nl": "Lopende zaken", "source": "crisp-dissolution",
     "def_fr": "Situation d'un gouvernement démissionnaire qui reste en fonction : il ne peut plus "
               "prendre que les décisions urgentes ou de gestion quotidienne. La Belgique y a passé "
               "541 jours en 2010-2011 et Bruxelles 613 jours en 2024-2026.",
     "def_nl": "Toestand van een ontslagnemende regering die in functie blijft."},
    {"code": "kern", "fr": "Kern", "nl": "Kern", "source": "kern-2026",
     "def_fr": "Conseil des ministres restreint, réunissant le Premier ministre et les "
               "vice-Premiers. Il n'a aucune existence constitutionnelle et décide pourtant "
               "l'essentiel — grief relevé publiquement en juillet 2026.",
     "def_nl": "Kernkabinet met de eerste minister en de vicepremiers. Het heeft geen "
               "grondwettelijk bestaan en beslist toch het meeste."},
    {"code": "dotation", "fr": "Dotation publique", "nl": "Overheidsdotatie", "source": "dotations-2024",
     "def_fr": "Financement public des partis, institué par la loi du 4 juillet 1989. Il représente "
               "80 à 90 % de leurs ressources, et son contrôle est confié à une commission composée "
               "de parlementaires — grief central du GRECO.",
     "def_nl": "Overheidsfinanciering van partijen, ingevoerd bij de wet van 4 juli 1989."},
    {"code": "transaction", "fr": "Transaction pénale", "nl": "Minnelijke schikking", "source": "transaction-2011",
     "def_fr": "Extinction de l'action publique contre paiement d'une somme, sans reconnaissance "
               "de culpabilité. Élargie par la loi du 14 avril 2011, adoptée par amendement sans débat.",
     "def_nl": "Uitdoving van de strafvordering tegen betaling, zonder schuldbekentenis."},
    {"code": "report", "fr": "Report de voix", "nl": "Stemverschuiving", "source": "crisp-proportionnel",
     "def_fr": "Dans ce simulateur : différence, en points de pourcentage et par région, entre le "
               "vote de départ et le vote simulé. Le report est appliqué uniformément à chaque "
               "circonscription de la région, puis renormalisé à 100 %.",
     "def_nl": "In deze simulator: het verschil in procentpunten en per gewest tussen de "
               "startstem en de gesimuleerde stem."},
]
