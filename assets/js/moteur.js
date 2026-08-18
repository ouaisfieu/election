/* Le Scrutin — moteur de simulation.
   Aucune dépendance. Aucun tirage aléatoire. Toute la fonction est déterministe :
   les mêmes choix donnent toujours le même parlement.
   Ce fichier est la source unique du calcul : les pages, le procès-verbal et le
   contrôle d'équilibrage exhaustif chargent celui-ci, jamais une copie. */
(function (racine) {
  'use strict';

  /* ---------------------------------------------------------------- D'Hondt */
  /* Les sièges sont attribués un à un au quotient voix/(sièges+1) le plus élevé.
     Les listes sous le seuil de la circonscription sont écartées d'abord.
     Comparaison en entiers croisés : aucune erreur de virgule flottante. */
  function dhondt(voix, sieges, seuil) {
    var codes = Object.keys(voix);
    var total = 0, i, c;
    for (i = 0; i < codes.length; i++) total += voix[codes[i]];
    var res = {};
    for (i = 0; i < codes.length; i++) res[codes[i]] = 0;
    if (total <= 0 || sieges <= 0) return res;
    var plancher = total * (seuil || 0);
    var elig = [];
    for (i = 0; i < codes.length; i++) {
      c = codes[i];
      if (voix[c] > 0 && voix[c] >= plancher) elig.push(c);
    }
    if (!elig.length) return res;
    for (var s = 0; s < sieges; s++) {
      var meilleur = null;
      for (i = 0; i < elig.length; i++) {
        c = elig[i];
        if (meilleur === null) { meilleur = c; continue; }
        /* voix[c]/(res[c]+1) > voix[m]/(res[m]+1)  <=>  produit croisé */
        var g = voix[c] * (res[meilleur] + 1);
        var d = voix[meilleur] * (res[c] + 1);
        if (g > d) meilleur = c;
        else if (g === d) {
          if (voix[c] > voix[meilleur]) meilleur = c;
          else if (voix[c] === voix[meilleur] && c < meilleur) meilleur = c;
        }
      }
      res[meilleur] += 1;
    }
    return res;
  }

  /* Suite des quotients attribués, pour montrer le calcul plutôt que l'asséner. */
  function tableauDhondt(voix, sieges, seuil, profondeur) {
    var res = {}, elig = [], codes = Object.keys(voix), total = 0, i, c;
    for (i = 0; i < codes.length; i++) total += voix[codes[i]];
    var plancher = total * (seuil || 0);
    for (i = 0; i < codes.length; i++) {
      c = codes[i];
      res[c] = 0;
      if (voix[c] > 0 && voix[c] >= plancher) elig.push(c);
    }
    var suite = [], n = Math.min(profondeur || sieges, sieges);
    for (var s = 0; s < n; s++) {
      var m = null;
      for (i = 0; i < elig.length; i++) {
        c = elig[i];
        if (m === null) { m = c; continue; }
        var g = voix[c] * (res[m] + 1), d = voix[m] * (res[c] + 1);
        if (g > d || (g === d && (voix[c] > voix[m] || (voix[c] === voix[m] && c < m)))) m = c;
      }
      res[m] += 1;
      suite.push({ rang: s + 1, liste: m, diviseur: res[m], quotient: voix[m] / res[m] });
    }
    return suite;
  }

  /* ------------------------------------------------- parts régionales 2024 */
  /* Référence du report : la part de chaque liste dans sa région, à la Chambre. */
  function partsRegion(chambre) {
    var acc = {};
    chambre.circonscriptions.forEach(function (circ) {
      var r = circ.region;
      if (!acc[r]) acc[r] = { total: 0, voix: {} };
      acc[r].total += circ.valables;
      Object.keys(circ.voix).forEach(function (c) {
        acc[r].voix[c] = (acc[r].voix[c] || 0) + circ.voix[c];
      });
    });
    var parts = {};
    Object.keys(acc).forEach(function (r) {
      parts[r] = {};
      Object.keys(acc[r].voix).forEach(function (c) {
        parts[r][c] = 100 * acc[r].voix[c] / acc[r].total;
      });
    });
    return parts;
  }

  /* --------------------------------------------------------------- la cible */
  /* Point de départ (sondage ou vote de 2024) + reports de campagne, en points.
     Toute part est plancherée à 0,2 % puis l'ensemble est renormalisé à 100 %. */
  function construireCible(base2024, sondage, reports) {
    var cible = {};
    Object.keys(base2024).forEach(function (r) {
      cible[r] = {};
      var depart = (sondage && sondage.parts && sondage.parts[r]) || null;
      Object.keys(base2024[r]).forEach(function (c) {
        var v = (depart && typeof depart[c] === 'number') ? depart[c] : base2024[r][c];
        var d = (reports && reports[r] && reports[r][c]) || 0;
        cible[r][c] = Math.max(0.2, v + d);
      });
      var somme = 0;
      Object.keys(cible[r]).forEach(function (c) { somme += cible[r][c]; });
      Object.keys(cible[r]).forEach(function (c) { cible[r][c] = 100 * cible[r][c] / somme; });
    });
    return cible;
  }

  /* Somme des reports choisis par le joueur, échéance par échéance. */
  function cumulerReports(echeances, choix) {
    var total = {};
    echeances.forEach(function (e) {
      var code = choix[e.code];
      if (!code) return;
      var issue = null;
      e.issues.forEach(function (i) { if (i.code === code) issue = i; });
      if (!issue) return;
      Object.keys(issue.report).forEach(function (r) {
        if (!total[r]) total[r] = {};
        Object.keys(issue.report[r]).forEach(function (c) {
          total[r][c] = (total[r][c] || 0) + issue.report[r][c];
        });
      });
    });
    return total;
  }

  /* ------------------------------------------------------ la simulation */
  /* Report proportionnel : chaque liste voit ses voix multipliées par le rapport
     entre sa part cible et sa part de 2024 DANS SA RÉGION, puis la circonscription
     est renormalisée. Une part ne peut donc jamais devenir négative, et la
     géographie interne de la région est conservée. */
  function facteurs(base2024, cible) {
    var f = {};
    Object.keys(cible).forEach(function (r) {
      f[r] = {};
      Object.keys(cible[r]).forEach(function (c) {
        var b = base2024[r][c];
        f[r][c] = (b && b > 0) ? cible[r][c] / b : 1;
      });
    });
    return f;
  }

  function simulerAssemblee(assemblee, f) {
    var parCirc = [], totaux = {}, voixTotales = {}, valables = 0;
    assemblee.circonscriptions.forEach(function (circ) {
      var fr = f[circ.region] || {};
      var brut = {}, somme = 0;
      Object.keys(circ.voix).forEach(function (c) {
        var v = circ.voix[c] * (typeof fr[c] === 'number' ? fr[c] : 1);
        brut[c] = v; somme += v;
      });
      var voix = {};
      Object.keys(brut).forEach(function (c) {
        voix[c] = Math.round(brut[c] * circ.valables / somme);
      });
      var sieges = dhondt(voix, circ.sieges, assemblee.seuil);
      parCirc.push({ code: circ.code, sieges: circ.sieges, voix: voix, resultat: sieges });
      Object.keys(sieges).forEach(function (c) {
        if (sieges[c]) totaux[c] = (totaux[c] || 0) + sieges[c];
      });
      Object.keys(voix).forEach(function (c) {
        voixTotales[c] = (voixTotales[c] || 0) + voix[c];
      });
      valables += circ.valables;
    });
    return { code: assemblee.code, total: assemblee.sieges, sieges: totaux,
             voix: voixTotales, valables: valables, circonscriptions: parCirc };
  }

  function simuler(donnees, sondageCode, choix) {
    var chambre = donnees.assemblees.chambre;
    var base = partsRegion(chambre);
    var sondage = null;
    (donnees.sondages || []).forEach(function (s) { if (s.code === sondageCode) sondage = s; });
    var reports = cumulerReports(donnees.echeances, choix || {});
    var cible = construireCible(base, sondage, reports);
    var f = facteurs(base, cible);
    var out = { base: base, cible: cible, reports: reports, sondage: sondageCode, assemblees: {} };
    Object.keys(donnees.assemblees).forEach(function (code) {
      out.assemblees[code] = simulerAssemblee(donnees.assemblees[code], f);
    });
    return out;
  }

  /* -------------------------------------------------- groupes linguistiques */
  /* À la Chambre, chaque élu appartient au groupe linguistique français ou
     néerlandais. Le modèle rattache l'élu à la communauté de sa liste. */
  function groupes(siegesChambre, partis) {
    var g = { fr: 0, nl: 0 };
    Object.keys(siegesChambre).forEach(function (c) {
      var p = partis[c];
      if (!p) return;
      if (p.communaute === 'fl') g.nl += siegesChambre[c];
      else if (p.communaute === 'fr') g.fr += siegesChambre[c];
    });
    return g;
  }

  /* ------------------------------------------------------------ coalitions */
  function combinaisons(liste) {
    var out = [];
    var n = liste.length;
    for (var masque = 1; masque < (1 << n); masque++) {
      var sous = [];
      for (var i = 0; i < n; i++) if (masque & (1 << i)) sous.push(liste[i]);
      out.push(sous);
    }
    return out;
  }

  function evaluerCoalition(membres, siegesChambre, partis) {
    var total = 0, gr = { fr: 0, nl: 0 };
    membres.forEach(function (c) {
      var s = siegesChambre[c] || 0;
      total += s;
      var p = partis[c];
      if (p && p.communaute === 'fl') gr.nl += s;
      else if (p && p.communaute === 'fr') gr.fr += s;
    });
    var grTotal = groupes(siegesChambre, partis);
    return {
      membres: membres.slice(),
      sieges: total,
      majorite: total >= 76,
      deuxTiers: total >= 100,
      groupeFr: gr.fr, groupeNl: gr.nl,
      majoriteGroupeFr: grTotal.fr > 0 && gr.fr * 2 > grTotal.fr,
      majoriteGroupeNl: grTotal.nl > 0 && gr.nl * 2 > grTotal.nl,
      loiSpeciale: total >= 100 && grTotal.fr > 0 && grTotal.nl > 0 &&
                   gr.fr * 2 > grTotal.fr && gr.nl * 2 > grTotal.nl,
      partis: membres.length,
      bilingue: gr.fr > 0 && gr.nl > 0
    };
  }

  /* Toutes les coalitions majoritaires, moins celles que le joueur exclut.
     Le site n'exclut rien de lui-même : `exclus` vient des cases cochées. */
  function coalitionsPossibles(siegesChambre, partis, exclus, maxPartis) {
    var codes = Object.keys(siegesChambre).filter(function (c) {
      return siegesChambre[c] > 0 && exclus.indexOf(c) === -1;
    }).sort(function (a, b) { return siegesChambre[b] - siegesChambre[a]; });
    var out = [];
    combinaisons(codes).forEach(function (sous) {
      if (maxPartis && sous.length > maxPartis) return;
      var e = evaluerCoalition(sous, siegesChambre, partis);
      if (!e.majorite) return;
      /* minimalité : retirer n'importe quel membre ferait perdre la majorité */
      var minimale = true;
      for (var i = 0; i < sous.length; i++) {
        if (e.sieges - siegesChambre[sous[i]] >= 76) { minimale = false; break; }
      }
      e.minimale = minimale;
      out.push(e);
    });
    out.sort(function (a, b) {
      if (a.partis !== b.partis) return a.partis - b.partis;
      return b.sieges - a.sieges;
    });
    return out;
  }

  /* ------------------------------------------------------------ cohésion */
  function cohesion(coalition, bareme) {
    var v = bareme.base;
    if (coalition.partis > 3) v += bareme.par_parti_au_dela_de_trois * (coalition.partis - 3);
    if (!coalition.majoriteGroupeFr || !coalition.majoriteGroupeNl) v += bareme.sans_majorite_dans_un_groupe;
    if (coalition.sieges >= 76 && coalition.sieges <= 78) v += bareme.majorite_etroite_76_78;
    if (coalition.sieges >= 90) v += bareme.majorite_confortable_90;
    return Math.max(0, Math.min(100, v));
  }

  /* ---------------------------------------------------------- législature */
  /* Un chantier n'est adopté que si la coalition a l'arithmétique de sa charge
     normative. Le reste est une addition, publiée dans le procès-verbal. */
  /* Une charge spéciale peut être atteinte avec l'appui de partis extérieurs à la
     coalition : c'est ainsi que passent les réformes de l'État en Belgique. Les
     appuis comptent pour l'arithmétique, jamais pour la cohésion du gouvernement. */
  function elargir(coalition, appuis, siegesChambre, partis) {
    if (!appuis || !appuis.length) return coalition;
    var membres = coalition.membres.concat(appuis.filter(function (a) {
      return coalition.membres.indexOf(a) === -1;
    }));
    var e = evaluerCoalition(membres, siegesChambre, partis);
    e.appuis = appuis.slice();
    return e;
  }

  function chargeDisponible(coalition, norme) {
    if (norme === 'loi') return coalition.majorite;
    if (norme === 'loi-speciale') return coalition.loiSpeciale;
    if (norme === 'revision') return coalition.deuxTiers;
    return false;
  }

  function legislature(coalition, chantiersChoisis, chantiers, bareme, depart, elargie) {
    var budget = 0, droit = 0, coh = cohesion(coalition, bareme);
    var adoptes = [], refuses = [];
    chantiers.forEach(function (ch) {
      if (chantiersChoisis.indexOf(ch.code) === -1) return;
      var portee = (ch.norme === 'loi') ? coalition : (elargie || coalition);
      if (!chargeDisponible(portee, ch.norme)) { refuses.push(ch.code); return; }
      adoptes.push(ch.code);
      budget += ch.effet.budget;
      droit += ch.effet.droit;
      coh += ch.effet.cohesion;
    });
    coh = Math.max(0, Math.min(100, coh));
    var constituant = adoptes.some(function (code) {
      var t = null; chantiers.forEach(function (c) { if (c.code === code) t = c; });
      return t && (t.norme === 'loi-speciale' || t.norme === 'revision');
    });
    var issue;
    if (!coalition.membres.length) issue = 'sans-gouvernement';
    else if (coh < 25) issue = 'chute';
    else if (constituant) issue = 'constituant';
    else if (droit >= 5) issue = 'reformateur';
    else if (budget >= depart.objectif) issue = 'comptable';
    else issue = 'reconduit';
    return { budget: Math.round(budget * 10) / 10, droit: droit, cohesion: Math.round(coh),
             adoptes: adoptes, refuses: refuses, issue: issue,
             ecartRestant: Math.round((depart.objectif - budget) * 10) / 10 };
  }

  /* ------------------------------------------------------------- ministères */
  /* Répartition proportionnelle des portefeuilles (méthode D'Hondt appliquée aux
     poids), sous la contrainte de parité de l'article 99. */
  function ministeres(coalition, siegesChambre, partis, portefeuilles) {
    /* Article 99 : quinze membres au plus et, le Premier ministre éventuellement excepté,
       autant de ministres d'expression française que d'expression néerlandaise. La parité
       est donc une contrainte de droit, appliquée AVANT la proportionnelle interne. */
    var groupes = { fr: [], nl: [] };
    coalition.membres.forEach(function (c) {
      var com = partis[c] ? partis[c].communaute : null;
      if (com === 'fl') groupes.nl.push(c);
      else if (com === 'fr') groupes.fr.push(c);
    });
    var postesNl = portefeuilles.filter(function (p) { return p.groupe === 'nl'; }).length;
    var postesFr = portefeuilles.filter(function (p) { return p.groupe === 'fr'; }).length;
    function repartir(liste, n) {
      var voix = {};
      liste.forEach(function (c) { voix[c] = siegesChambre[c] || 0; });
      return liste.length ? dhondt(voix, n, 0) : {};
    }
    /* Si la coalition n'a aucun parti d'un des deux groupes, la parité ne peut pas être
       tenue : le fait est signalé plutôt que corrigé en silence. */
    var pariteImpossible = !groupes.fr.length || !groupes.nl.length;
    var quotaNl = repartir(groupes.nl, pariteImpossible && !groupes.fr.length ? postesNl + postesFr : postesNl);
    var quotaFr = repartir(groupes.fr, pariteImpossible && !groupes.nl.length ? postesNl + postesFr : postesFr);
    var restants = {};
    coalition.membres.forEach(function (c) { restants[c] = (quotaNl[c] || 0) + (quotaFr[c] || 0); });

    /* Le Premier ministre revient à la liste la plus forte de la coalition ; son poste
       s'ajoute au compte, il ne s'en retranche pas (art. 99). */
    var pm = coalition.membres.slice().sort(function (a, b) {
      return (siegesChambre[b] || 0) - (siegesChambre[a] || 0);
    })[0];
    var attrib = [];
    portefeuilles.forEach(function (p) {
      if (p.groupe === 'libre') { attrib.push({ poste: p.code, liste: pm || null }); return; }
      var pool = (p.groupe === 'nl') ? groupes.nl : groupes.fr;
      var cands = pool.filter(function (c) { return restants[c] > 0; });
      if (!cands.length) cands = coalition.membres.filter(function (c) { return restants[c] > 0; });
      if (!cands.length) { attrib.push({ poste: p.code, liste: null }); return; }
      cands.sort(function (a, b) { return (siegesChambre[b] || 0) - (siegesChambre[a] || 0); });
      restants[cands[0]] -= 1;
      attrib.push({ poste: p.code, liste: cands[0] });
    });
    return { quotaNl: quotaNl, quotaFr: quotaFr, premier: pm,
             pariteImpossible: pariteImpossible, postes: attrib };
  }

  var api = {
    dhondt: dhondt, tableauDhondt: tableauDhondt, partsRegion: partsRegion,
    construireCible: construireCible, cumulerReports: cumulerReports, facteurs: facteurs,
    simulerAssemblee: simulerAssemblee, simuler: simuler, groupes: groupes,
    evaluerCoalition: evaluerCoalition, coalitionsPossibles: coalitionsPossibles,
    cohesion: cohesion, legislature: legislature, ministeres: ministeres, elargir: elargir
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else racine.Scrutin = api;
})(typeof window !== 'undefined' ? window : globalThis);
