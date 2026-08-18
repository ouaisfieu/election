# Le Scrutin · De Stembus

Simulateur d'élections belges — fédérales et régionales, 2029 et après.
HTML, CSS et JavaScript purs, sans dépendance, sans traceur, sans appel réseau.

**https://ouaisfieu.github.io/election/**

## Ce que c'est

Quatre actes : la campagne de septembre 2026 à 2029, le scrutin fédéral et régional
le même jour, la formation d'une coalition, puis la législature. Le calcul est le
calcul belge réel — clé D'Hondt circonscription par circonscription, seuil de 5 %,
groupes linguistiques, article 99, article 4 — appliqué aux résultats officiels du
9 juin 2024.

Le site ne dit jamais pour qui voter, ne classe aucun parti et ne prévoit rien : il
calcule les conséquences d'hypothèses que l'utilisateur choisit, et publie
intégralement le modèle qui les traduit en sièges.

## Les cinq assemblées

| Assemblée | Sièges | Circonscriptions | Rétro-test 2024 |
|---|---:|---:|---:|
| Chambre des représentants | 150 | 11 | **0 siège d'écart** |
| Parlement flamand | 124 | 6 | **0 siège d'écart** |
| Parlement wallon | 75 | 11 | 8 sièges (apparentement provincial non implémenté) |
| Parlement bruxellois | 89 | 2 collèges | 1 siège |
| Parlement de la Communauté germanophone | 25 | 1 | **0 siège d'écart** |

Le rétro-test applique le moteur aux voix réelles de 2024 et compare, circonscription
par circonscription, à la proclamation officielle. Il est rejoué à chaque construction ;
le build échoue si l'écart change sans être documenté.

## Où éditer quoi

| Contenu | Fichier |
|---|---|
| Résultats officiels 2024, cinq assemblées | `tools/donnees_scrutins.py` |
| Registre des listes, couleurs, communauté | `tools/donnees_partis.py` |
| Points de départ (vote 2024 et enquêtes 2026) | `tools/donnees_sondages.py` |
| Les six échéances, leurs issues et leurs reports | `tools/donnees_campagne.py` |
| Contraintes de droit, exclusions, portefeuilles, chantiers | `tools/donnees_coalition.py` |
| Cohésion, semestres, arbre des issues | `tools/donnees_legislature.py` |
| Registre des sources | `tools/donnees_sources.py` |
| Chronologie | `tools/donnees_actualites.py` |
| Glossaire | `tools/donnees_glossaire.py` |
| Réseau des sites | `tools/donnees_reseau.py` |
| Textes des pages | `tools/pages.py` |
| Gabarit HTML et SEO | `tools/gabarit.py` |
| Configuration du site | `tools/config.py` |
| Moteur de calcul (source unique) | `assets/js/moteur.js` — miroir Python : `tools/moteur.py` |

Après toute modification : `python3 tools/build.py`.

## Le build refuse de construire si

* la somme des voix d'une circonscription ne correspond pas au total officiel
  de votes valables ;
* la somme des sièges d'une assemblée ne correspond pas à son effectif légal ;
* le rétro-test de 2024 change sans que l'écart attendu soit mis à jour ;
* une source citée manque au registre, ou une source du registre n'est citée nulle part ;
* une échéance a moins de deux issues, ou une issue n'a ni report ni justification ;
* deux pages partagent un titre ou une méta-description ;
* une méta-description sort de la fourchette 70-320 caractères.

## Contrôles

```
python3 tools/build.py          # construit le site
python3 tools/verifier.py       # titres, canoniques, hreflang, OG, JSON-LD, liens, sitemap
node    tools/equilibrage.js    # rétro-test + 2916 simulations + distribution des issues
node    tools/test_navigateur.js # 22 assertions Playwright, dont la lisibilité sans JavaScript
python3 tools/og.py             # régénère les 26 vignettes sociales
```

Les quatre tournent en intégration continue, qui refuse en outre un HTML divergent
des sources.

## Licence

CC BY-SA 4.0. Les données électorales proviennent du SPF Intérieur — Direction des
Élections ; elles sont recopiées telles quelles et les pourcentages sont recalculés.
