# -*- coding: utf-8 -*-
"""Registre des sources. Le build refuse de construire si une source citée
n'existe pas ici, ou si une source du registre n'est citée nulle part.

`statut` : fait (établi et vérifiable) · echeance (date programmée) · hypothese.
"""

SOURCES = {
    "spf-resultats": {
        "titre_fr": "Résultats officiels des élections du 9 juin 2024, par circonscription",
        "titre_nl": "Officiële uitslagen van de verkiezingen van 9 juni 2024, per kieskring",
        "auteur": "SPF Intérieur — Direction des Élections",
        "url": "https://resultatselection.belgium.be/fr/search/chambre-des-repr%C3%A9sentants/2024/circonscription-%C3%A9lectorale",
        "date": "2024-06-09", "statut": "fait"},
    "spf-repartition-chambre": {
        "titre_fr": "Dépouillement, répartition des sièges et désignation des élus — Chambre",
        "titre_nl": "Telling, zetelverdeling en aanwijzing van de verkozenen — Kamer",
        "auteur": "SPF Intérieur — Direction des Élections",
        "url": "https://elections.fgov.be/informations-generales-depouillement-repartition-des-sieges-et-designation-des-elus/chambre-des",
        "date": "2024-06-09", "statut": "fait"},
    "spf-repartition-wallon": {
        "titre_fr": "Répartition des sièges au Parlement wallon : D'Hondt, seuil de 5 % et "
                    "apparentement provincial en Hainaut, à Liège et à Namur",
        "titre_nl": "Zetelverdeling in het Waals Parlement: D'Hondt, 5 %-drempel en provinciale "
                    "lijstenverbinding",
        "auteur": "SPF Intérieur — Direction des Élections",
        "url": "https://elections.fgov.be/informations-generales-depouillement-repartition-des-sieges-et-designation-des-elus/parlement-1",
        "date": "2024-06-09", "statut": "fait"},
    "spf-repartition-bruxellois": {
        "titre_fr": "Répartition des sièges au Parlement bruxellois : seuil de 5 % par groupe "
                    "linguistique, 72 sièges au groupe français et 17 au groupe néerlandais",
        "titre_nl": "Zetelverdeling in het Brussels Parlement: 5 %-drempel per taalgroep",
        "auteur": "SPF Intérieur — Direction des Élections",
        "url": "https://elections.fgov.be/informations-generales-depouillement-repartition-des-sieges-et-designation-des-elus/parlement-de-la",
        "date": "2024-06-09", "statut": "fait"},
    "lachambre-resultats-2024": {
        "titre_fr": "Résultats des élections fédérales du 9 juin 2024, fiche 09.02",
        "titre_nl": "Uitslagen van de federale verkiezingen van 9 juni 2024, fiche 09.02",
        "auteur": "Chambre des représentants",
        "url": "https://www.lachambre.be/pdf_sections/pri/fiche/fr_09_02.pdf",
        "date": "2024-06-09", "statut": "fait"},
    "crisp-dissolution": {
        "titre_fr": "Dissolution — Vocabulaire politique",
        "titre_nl": "Ontbinding — Politiek vocabularium",
        "auteur": "CRISP", "url": "https://www.vocabulairepolitique.be/dissolution/",
        "date": "2024-01-01", "statut": "fait"},
    "crisp-circonscription": {
        "titre_fr": "Circonscription électorale — Vocabulaire politique",
        "titre_nl": "Kieskring — Politiek vocabularium",
        "auteur": "CRISP", "url": "https://www.vocabulairepolitique.be/circonscription-electorale/",
        "date": "2024-01-01", "statut": "fait"},
    "crisp-proportionnel": {
        "titre_fr": "Scrutin proportionnel et clé D'Hondt",
        "titre_nl": "Evenredige vertegenwoordiging en D'Hondt-sleutel",
        "auteur": "CRISP", "url": "https://www.vocabulairepolitique.be/scrutin-proportionnel/",
        "date": "2024-01-01", "statut": "fait"},
    "crisp-apparentement": {
        "titre_fr": "Apparentement — Vocabulaire politique",
        "titre_nl": "Lijstenverbinding — Politiek vocabularium",
        "auteur": "CRISP", "url": "https://www.vocabulairepolitique.be/apparentement/",
        "date": "2024-01-01", "statut": "fait"},
    "crisp-devolutif": {
        "titre_fr": "Effet dévolutif de la case de tête",
        "titre_nl": "Devolutief effect van de lijststem",
        "auteur": "CRISP", "url": "https://www.vocabulairepolitique.be/scrutin-proportionnel/",
        "date": "2024-01-01", "statut": "fait"},
    "crisp-ptb": {
        "titre_fr": "Élections et gouvernements en Belgique depuis 1945",
        "titre_nl": "Verkiezingen en regeringen in België sinds 1945",
        "auteur": "Pascal Delwit, ULB",
        "url": "https://dipot.ulb.ac.be/dspace/bitstream/2013/336107/3/DelwitElectionsgouvernements.pdf",
        "date": "2019-01-01", "statut": "fait"},
    "constitution-4": {
        "titre_fr": "Constitution belge, article 4 — majorité spéciale",
        "titre_nl": "Belgische Grondwet, artikel 4 — bijzondere meerderheid",
        "auteur": "Constitution belge", "url": "https://www.senate.be/doc/const_fr.html",
        "date": "1994-02-17", "statut": "fait"},
    "constitution-96": {
        "titre_fr": "Constitution belge, article 96 — confiance de la Chambre",
        "titre_nl": "Belgische Grondwet, artikel 96 — vertrouwen van de Kamer",
        "auteur": "Constitution belge", "url": "https://www.senate.be/doc/const_fr.html",
        "date": "1994-02-17", "statut": "fait"},
    "constitution-99": {
        "titre_fr": "Constitution belge, article 99 — parité linguistique du Conseil des ministres",
        "titre_nl": "Belgische Grondwet, artikel 99 — taalpariteit van de Ministerraad",
        "auteur": "Constitution belge", "url": "https://www.senate.be/doc/const_fr.html",
        "date": "1994-02-17", "statut": "fait"},
    "constitution-195": {
        "titre_fr": "Constitution belge, article 195 — révision",
        "titre_nl": "Belgische Grondwet, artikel 195 — herziening",
        "auteur": "Constitution belge", "url": "https://www.senate.be/doc/const_fr.html",
        "date": "1994-02-17", "statut": "fait"},
    "cordon-vrt": {
        "titre_fr": "Ce qu'est le cordon sanitaire et pourquoi il tient depuis 1989",
        "titre_nl": "Wat het cordon sanitaire is en waarom het sinds 1989 standhoudt",
        "auteur": "VRT NWS",
        "url": "https://www.vrt.be/vrtnws/en/2024/03/06/cordon-sanitaire-elections-belgium-vlaams-nationa/",
        "date": "2024-03-06", "statut": "fait"},
    "monitoring-2026": {
        "titre_fr": "Comité de monitoring, juillet 2026 : écart de 7,7 milliards d'euros d'ici 2029, "
                    "9,8 milliards d'ici 2031",
        "titre_nl": "Monitoringcomité, juli 2026: tekort van 7,7 miljard euro tegen 2029",
        "auteur": "Comité de monitoring — repris par Le Vif et la Cour des comptes",
        "url": "https://www.levif.be/belgique/politique/la-cour-des-comptes-le-confirme-larizona-fait-encore-semblant-de-rien-le-budget-deraille-encore-plus-que-ce-que-bart-de-wever-craignait/",
        "date": "2026-07-01", "statut": "fait"},
    "objectif-10-milliards": {
        "titre_fr": "10 juillet 2026 : le gouvernement vise 10 milliards d'euros d'ici 2029, "
                    "dont « plus des deux tiers » structurels",
        "titre_nl": "10 juli 2026: de regering mikt op 10 miljard euro tegen 2029",
        "auteur": "Gouvernement fédéral — repris par la presse",
        "url": "https://fr.businessam.be/ce-qui-attend-encore-le-gouvernement-de-wever-en-2026",
        "date": "2026-07-10", "statut": "echeance"},
    "moodys-2026": {
        "titre_fr": "Moody's abaisse la Belgique de Aa3 à A1 le 17 avril 2026 ; Wallonie et "
                    "Communautés dégradées le 22 avril",
        "titre_nl": "Moody's verlaagt België van Aa3 naar A1 op 17 april 2026",
        "auteur": "Moody's — repris par la presse belge",
        "url": "https://fr.businessam.be/ce-qui-attend-encore-le-gouvernement-de-wever-en-2026",
        "date": "2026-04-17", "statut": "fait"},
    "bnb-croissance-2026": {
        "titre_fr": "Croissance nulle au deuxième trimestre 2026 : industrie −0,8 %, construction "
                    "−0,5 %, services +0,2 %",
        "titre_nl": "Nulgroei in het tweede kwartaal van 2026",
        "auteur": "Banque nationale de Belgique — repris par The Belgium Times",
        "url": "https://belgium-times.be/2026/08/economie-belge-la-croissance-tombe-a-0-la-belgique-face-au-risque-de-stagnation-en-2026/",
        "date": "2026-08-01", "statut": "fait"},
    "greco-2025": {
        "titre_fr": "Addendum GrecoRC5(2025) : 8 recommandations sur 22 traitées de manière "
                    "satisfaisante ; l'ultime étape de la règle 32 est une déclaration publique "
                    "de non-conformité",
        "titre_nl": "Addendum GrecoRC5(2025): 8 van de 22 aanbevelingen bevredigend opgevolgd",
        "auteur": "GRECO — Conseil de l'Europe",
        "url": "https://www.coe.int/en/web/greco/evaluations/belgium",
        "date": "2025-11-01", "statut": "fait"},
    "cue-etat-de-droit-2026": {
        "titre_fr": "Rapport état de droit 2026 : « le respect par le gouvernement des décisions "
                    "définitives des tribunaux et des astreintes reste problématique » ; aucune "
                    "avancée sur le lobbying ni le pantouflage",
        "titre_nl": "Rechtsstaatrapport 2026: de naleving van definitieve rechterlijke beslissingen "
                    "blijft problematisch",
        "auteur": "Commission européenne",
        "url": "https://commission.europa.eu/publications/2026-rule-law-report_en",
        "date": "2026-07-17", "statut": "fait"},
    "conseil-etat-2026": {
        "titre_fr": "27 mars 2026 : le Conseil d'État suspend des instructions ministérielles "
                    "contournant un arrêt de la Cour constitutionnelle en matière d'accueil",
        "titre_nl": "27 maart 2026: de Raad van State schorst ministeriële instructies",
        "auteur": "Conseil d'État — repris par la presse belge",
        "url": "https://www.lalibre.be/belgique/politique-belge/",
        "date": "2026-03-27", "statut": "fait"},
    "memorandum-juridictions": {
        "titre_fr": "La justice pèse environ 0,5 % du budget de l'État après quelque 14 % de coupes "
                    "cumulées ; mémorandum commun des trois hautes juridictions",
        "titre_nl": "Justitie weegt ongeveer 0,5 % van de staatsbegroting",
        "auteur": "Cour de cassation, Conseil d'État et Cour constitutionnelle",
        "url": "https://www.const-court.be/",
        "date": "2024-07-01", "statut": "fait"},
    "transaction-2011": {
        "titre_fr": "Loi du 14 avril 2011 sur la transaction pénale élargie, adoptée par amendement "
                    "sans débat ; arrêt 83/2016 de la Cour constitutionnelle",
        "titre_nl": "Wet van 14 april 2011 over de verruimde minnelijke schikking; arrest 83/2016",
        "auteur": "Moniteur belge — Cour constitutionnelle",
        "url": "https://www.const-court.be/public/f/2016/2016-083f.pdf",
        "date": "2011-04-14", "statut": "fait"},
    "ing-2026": {
        "titre_fr": "5 mai 2026 : ING paie 1,6 million d'euros dans le dossier Reynders, sans "
                    "reconnaissance de culpabilité",
        "titre_nl": "5 mei 2026: ING betaalt 1,6 miljoen euro in het dossier-Reynders",
        "auteur": "Presse belge",
        "url": "https://www.lalibre.be/belgique/politique-belge/",
        "date": "2026-05-05", "statut": "fait"},
    "dotations-2024": {
        "titre_fr": "104 millions d'euros de dotations aux groupes politiques et collaborateurs en "
                    "2024 ; 80 à 90 % des ressources des partis sont publiques ; loi du 4 juillet 1989",
        "titre_nl": "104 miljoen euro dotaties in 2024; 80 tot 90 % van de partijmiddelen is publiek",
        "auteur": "Chambre des représentants — commission de contrôle",
        "url": "https://www.lachambre.be/",
        "date": "2024-12-31", "statut": "fait"},
    "enquete-nationale-2026": {
        "titre_fr": "Enquête nationale 2026 (UAntwerpen et ULB), terrain mars-avril 2026, marge ±2,4",
        "titre_nl": "Nationaal verkiezingsonderzoek 2026 (UAntwerpen en ULB)",
        "auteur": "UAntwerpen et ULB — repris par la RTBF",
        "url": "https://www.rtbf.be/article/l-enquete-nationale-2026-le-mr-degringole-le-ps-et-le-ptb-en-profitent-pour-devenir-leaders-en-wallonie-et-a-bruxelles-11729854",
        "date": "2026-04-30", "statut": "fait"},
    "grande-enquete-mars-2026": {
        "titre_fr": "Grande Enquête HLN, VTM Nieuws, RTL et Le Soir, publiée le 14 mars 2026 : "
                    "N-VA 25,5 %, Vlaams Belang 25,4 % en Flandre",
        "titre_nl": "De Grote Peiling van 14 maart 2026",
        "auteur": "HLN, VTM Nieuws, RTL et Le Soir",
        "url": "https://www.21news.be/en-flandre-la-n-va-et-le-vlaams-belang-au-coude-a-coude-dans-un-nouveau-sondage-de-wever-plus-populaire-que-jamais/",
        "date": "2026-03-14", "statut": "fait"},
    "barometre-juin-2026": {
        "titre_fr": "Grand Baromètre RTL et Le Soir, publié le 12 juin 2026 : le Vlaams Belang "
                    "passe devant la N-VA en Flandre",
        "titre_nl": "Grote Barometer RTL en Le Soir van 12 juni 2026",
        "auteur": "RTL et Le Soir",
        "url": "https://www.21news.be/sondages-le-ps-reprend-la-main-en-wallonie-le-ptb-domine-bruxelles-le-vlaams-belang-loin-devant-en-flandre/",
        "date": "2026-06-12", "statut": "fait"},
    "dillies-2026": {
        "titre_fr": "Le gouvernement bruxellois Dilliès formé après 613 jours de crise ; confiance "
                    "accordée par le Parlement bruxellois le 27 février 2026",
        "titre_nl": "De Brusselse regering-Dilliès gevormd na 613 dagen crisis",
        "auteur": "BX1 et La Libre",
        "url": "https://bx1.be/categories/politique/suivez-en-direct-la-declaration-du-gouvernement-bruxellois-par-le-ministre-president-boris-dillies/",
        "date": "2026-02-27", "statut": "fait"},
    "arizona-2025": {
        "titre_fr": "Coalition Arizona : 81 sièges sur 150, quinze ministres sans secrétaires "
                    "d'État, prestation de serment le 3 février 2025",
        "titre_nl": "Arizona-coalitie: 81 van de 150 zetels, vijftien ministers",
        "auteur": "Gouvernement fédéral", "url": "https://www.belgium.be/fr/la_belgique/pouvoirs_publics/autorites_federales/gouvernement_federal",
        "date": "2025-02-03", "statut": "fait"},
    "kern-2026": {
        "titre_fr": "25 juillet 2026 : concentration croissante des décisions au Kern, le Conseil "
                    "des ministres devenant chambre d'enregistrement",
        "titre_nl": "25 juli 2026: toenemende concentratie van beslissingen in de Kern",
        "auteur": "Caroline Sägesser, CRISP — La Libre",
        "url": "https://www.lalibre.be/belgique/politique-belge/",
        "date": "2026-07-25", "statut": "fait"},
    "greves-2026": {
        "titre_fr": "12 mars 2026 : grève nationale du front commun syndical sur les pensions et "
                    "l'indexation ; grève du secteur public bruxellois le 23 juin 2026",
        "titre_nl": "12 maart 2026: nationale staking over de pensioenen en de indexering",
        "auteur": "Front commun syndical — presse belge",
        "url": "https://www.lalibre.be/belgique/politique-belge/",
        "date": "2026-03-12", "statut": "fait"},
    "bourgmestres-2024": {
        "titre_fr": "88,6 % des bourgmestres wallons désignés en 2024 étaient têtes de liste "
                    "(92,4 % en 2018)",
        "titre_nl": "88,6 % van de Waalse burgemeesters aangeduid in 2024 was lijsttrekker",
        "auteur": "CRISP", "url": "https://www.crisp.be/",
        "date": "2024-12-01", "statut": "fait"},
    "cpi-2025": {
        "titre_fr": "Indice de perception de la corruption : la Belgique passe de 77 à 69 entre "
                    "2016 et 2025",
        "titre_nl": "Corruptieperceptie-index: België gaat van 77 naar 69 tussen 2016 en 2025",
        "auteur": "Transparency International",
        "url": "https://www.transparency.org/en/cpi", "date": "2025-01-01", "statut": "fait"},
    "code-penal-2026": {
        "titre_fr": "Nouveau Code pénal en vigueur le 1er septembre 2026 (art. 634 à 639)",
        "titre_nl": "Nieuw Strafwetboek van kracht op 1 september 2026",
        "auteur": "Moniteur belge", "url": "https://www.ejustice.just.fgov.be/",
        "date": "2026-09-01", "statut": "echeance"},
}
