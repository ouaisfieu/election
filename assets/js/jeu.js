/* Le Scrutin — l'interface du simulateur. Le calcul est dans moteur.js ;
   ce fichier ne fait que lire les choix, appeler le moteur et écrire le résultat.
   Rien n'est envoyé nulle part : la progression tient dans l'adresse de la page. */
(function () {
  'use strict';
  var D = window.ScrutinDonnees, S = window.Scrutin;
  if (!D || !S) return;
  var LANG = document.documentElement.lang === 'nl' ? 'nl' : 'fr';
  function T(fr, nl) { return LANG === 'nl' ? nl : fr; }
  function q(s) { return document.querySelector(s); }
  function qa(s) { return Array.prototype.slice.call(document.querySelectorAll(s)); }
  function nom(c) { return (D.partis[c] && D.partis[c].nom) || c; }
  function coul(c) { return (D.partis[c] && D.partis[c].couleur) || '#9aa0a6'; }
  function ech(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function nb(n) { return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }
  function virgule(x, d) { return x.toFixed(d === undefined ? 1 : d).replace('.', ','); }

  var etat = { coalition: null, appuis: [] };

  /* ------------------------------------------------------------- lecture */
  function lireChoix() {
    var c = {};
    D.echeances.forEach(function (e) {
      var r = q('input[name="' + e.code + '"]:checked');
      if (r) c[e.code] = r.value;
    });
    return c;
  }
  function lireDepart() {
    var r = q('input[name="depart"]:checked');
    return r ? r.value : D.sondageDefaut;
  }
  function lireExclusions() {
    var codes = [];
    qa('input[name="exclusion"]:checked').forEach(function (i) {
      D.exclusions.forEach(function (x) { if (x.code === i.value) codes = codes.concat(x.cible); });
    });
    return codes.filter(function (v, i, a) { return a.indexOf(v) === i; });
  }
  function lireChantiers() {
    return qa('input[name="chantier"]:checked').map(function (i) { return i.value; });
  }

  /* --------------------------------------------------------------- rendus */
  function hemicycle(sieges) {
    var ordre = Object.keys(sieges).filter(function (k) { return sieges[k] > 0; })
      .sort(function (a, b) { return sieges[b] - sieges[a]; });
    var pts = '', leg = '';
    ordre.forEach(function (c) {
      for (var i = 0; i < sieges[c]; i++) pts += '<span class="siege" style="background:' + coul(c) + '"></span>';
      leg += '<span style="white-space:nowrap"><span class="pastille" style="background:' + coul(c) + '"></span>' +
             ech(nom(c)) + ' ' + sieges[c] + '</span> ';
    });
    var total = ordre.reduce(function (a, c) { return a + sieges[c]; }, 0);
    return '<div class="hemicycle" role="img" aria-label="' +
      ech(ordre.map(function (c) { return nom(c) + ' ' + sieges[c]; }).join(', ')) + '">' + pts +
      '</div><p style="font-size:.82rem;color:var(--doux)">' + leg + ' — ' + total + ' ' +
      T('sièges', 'zetels') + '</p>';
  }

  function officiel2024(codeAssemblee) {
    var a = D.assemblees[codeAssemblee], out = {};
    a.circonscriptions.forEach(function (c) {
      Object.keys(c.officiel).forEach(function (k) { out[k] = (out[k] || 0) + c.officiel[k]; });
    });
    return out;
  }

  function tableauAssemblee(res) {
    var off = officiel2024(res.code);
    var codes = Object.keys(res.sieges).filter(function (k) { return res.sieges[k] > 0 || off[k]; })
      .sort(function (a, b) { return (res.sieges[b] || 0) - (res.sieges[a] || 0); });
    var h = '<div class="defile"><table><thead><tr><th>' + T('Liste', 'Lijst') +
      '</th><th class="n">' + T('Sièges simulés', 'Gesimuleerde zetels') +
      '</th><th class="n">' + T('En 2024', 'In 2024') + '</th><th class="n">' +
      T('Écart', 'Verschil') + '</th><th class="n">%</th></tr></thead><tbody>';
    codes.forEach(function (c) {
      var s = res.sieges[c] || 0, o = off[c] || 0, d = s - o;
      var pct = 100 * (res.voix[c] || 0) / res.valables;
      h += '<tr><td><span class="pastille" style="background:' + coul(c) + '"></span>' + ech(nom(c)) +
        '</td><td class="n"><strong>' + s + '</strong></td><td class="n">' + o + '</td><td class="n">' +
        (d === 0 ? '—' : (d > 0 ? '+' + d : d)) + '</td><td class="n">' + virgule(pct, 2) + ' %</td></tr>';
    });
    return h + '</tbody></table></div>';
  }

  function rendreScrutin(sim) {
    var h = '';
    var ordre = ['chambre', 'flamand', 'wallon', 'bruxellois', 'germanophone'];
    ordre.forEach(function (code) {
      var res = sim.assemblees[code];
      h += '<h3>' + ech(D.nomsAssemblees[code][LANG]) + '</h3>';
      h += hemicycle(res.sieges);
      h += tableauAssemblee(res);
    });
    /* la Chambre, circonscription par circonscription */
    var ch = sim.assemblees.chambre;
    h += '<h3>' + T('La Chambre, circonscription par circonscription',
                    'De Kamer, kieskring per kieskring') + '</h3>';
    h += '<div class="defile"><table><thead><tr><th>' + T('Circonscription', 'Kieskring') + '</th>';
    var listes = Object.keys(ch.sieges).filter(function (k) { return ch.sieges[k] > 0; })
      .sort(function (a, b) { return ch.sieges[b] - ch.sieges[a]; });
    listes.forEach(function (c) {
      h += '<th class="n" title="' + ech(nom(c)) + '"><span class="pastille" style="background:' +
        coul(c) + '"></span></th>';
    });
    h += '<th class="n">' + T('Total', 'Totaal') + '</th></tr></thead><tbody>';
    ch.circonscriptions.forEach(function (c, i) {
      var meta = D.assemblees.chambre.circonscriptions[i];
      h += '<tr><td>' + ech(LANG === 'nl' ? meta.nom_nl : meta.nom_fr) + '</td>';
      listes.forEach(function (k) { h += '<td class="n">' + (c.resultat[k] || '') + '</td>'; });
      h += '<td class="n">' + c.sieges + '</td></tr>';
    });
    h += '</tbody></table><p style="font-size:.8rem;color:var(--doux)">' +
      listes.map(function (c) {
        return '<span class="pastille" style="background:' + coul(c) + '"></span>' + ech(nom(c));
      }).join(' · ') + '</p></div>';
    q('#resultat-scrutin').innerHTML = h;
  }

  /* ---------------------------------------------------------- coalitions */
  function rendreCoalitions(sim) {
    var ch = sim.assemblees.chambre.sieges;
    var exclus = lireExclusions();
    var gr = S.groupes(ch, D.partis);
    var toutes = S.coalitionsPossibles(ch, D.partis, exclus, 6);
    var minimales = toutes.filter(function (c) { return c.minimale; });
    if (etat.coalition) {
      var encore = minimales.concat(toutes).some(function (c) {
        return c.membres.join('+') === etat.coalition.membres.join('+');
      });
      if (!encore) etat.coalition = null;
    }
    var h = '<div class="chiffres">' +
      '<div class="chiffre"><b>76</b><span>' + T('sièges pour la confiance', 'zetels voor het vertrouwen') + '</span></div>' +
      '<div class="chiffre"><b>' + gr.nl + '</b><span>' + T('sièges au groupe néerlandais', 'zetels in de Nederlandse taalgroep') + '</span></div>' +
      '<div class="chiffre"><b>' + gr.fr + '</b><span>' + T('sièges au groupe français', 'zetels in de Franse taalgroep') + '</span></div>' +
      '<div class="chiffre"><b>' + minimales.length + '</b><span>' + T('coalitions minimales possibles', 'mogelijke minimale coalities') + '</span></div>' +
      '</div>';
    if (!minimales.length) {
      h += '<div class="encart"><p>' + T(
        'Aucune coalition majoritaire ne subsiste avec les exclusions que vous avez retenues. ' +
        'C\'est une issue possible : le pays reste alors en affaires courantes, comme il l\'a fait ' +
        '541 jours en 2010-2011 et Bruxelles 613 jours en 2024-2026.',
        'Geen enkele meerderheidscoalitie blijft over met de gekozen uitsluitingen.') + '</p></div>';
      q('#resultat-coalitions').innerHTML = h;
      etat.coalition = null;
      return;
    }
    h += '<div class="defile"><table><thead><tr><th></th><th>' + T('Coalition', 'Coalitie') +
      '</th><th class="n">' + T('Sièges', 'Zetels') + '</th><th class="n">NL</th><th class="n">FR</th><th>' +
      T('Loi spéciale', 'Bijzondere wet') + '</th></tr></thead><tbody>';
    minimales.slice(0, 30).forEach(function (c, i) {
      var cle = c.membres.join('+');
      var coche = (etat.coalition && etat.coalition.membres.join('+') === cle) || (!etat.coalition && i === 0);
      if (coche && !etat.coalition) etat.coalition = c;
      h += '<tr><td><input type="radio" name="coalition" value="' + ech(cle) + '"' +
        (coche ? ' checked' : '') + ' aria-label="' + ech(c.membres.map(nom).join(' + ')) + '"></td><td>' +
        c.membres.map(function (m) {
          return '<span class="pastille" style="background:' + coul(m) + '"></span>' + ech(nom(m));
        }).join(' + ') + '</td><td class="n"><strong>' + c.sieges + '</strong></td><td class="n">' +
        c.groupeNl + '</td><td class="n">' + c.groupeFr + '</td><td>' +
        (c.loiSpeciale ? T('oui', 'ja') : T('non', 'nee')) + '</td></tr>';
    });
    h += '</tbody></table></div>';
    if (minimales.length > 30) {
      h += '<p style="font-size:.85rem;color:var(--doux)">' +
        T('Les ' + (minimales.length - 30) + ' autres combinaisons minimales sont plus larges encore.',
          'De ' + (minimales.length - 30) + ' andere minimale combinaties zijn nog breder.') + '</p>';
    }
    /* appuis extérieurs */
    h += '<h3>' + T('Appuis extérieurs pour une charge spéciale',
                    'Externe steun voor een bijzondere last') + '</h3>';
    h += '<p>' + T(
      'Une loi spéciale ou une révision de la Constitution peut être portée avec l\'accord de partis ' +
      'restés hors du gouvernement. Ces appuis comptent pour l\'arithmétique, jamais pour la cohésion.',
      'Een bijzondere wet kan worden gedragen met de steun van partijen buiten de regering.') + '</p>';
    h += '<div class="choix" style="grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));display:grid">';
    Object.keys(ch).filter(function (k) { return ch[k] > 0; })
      .sort(function (a, b) { return ch[b] - ch[a]; }).forEach(function (k) {
        var dedans = etat.coalition && etat.coalition.membres.indexOf(k) !== -1;
        if (dedans) return;
        h += '<label style="padding:.4rem .6rem"><input type="checkbox" name="appui" value="' + ech(k) + '"' +
          (etat.appuis.indexOf(k) !== -1 ? ' checked' : '') + '> <span><span class="pastille" style="background:' +
          coul(k) + '"></span>' + ech(nom(k)) + ' (' + ch[k] + ')</span></label>';
      });
    h += '</div>';
    /* ministères */
    if (etat.coalition) {
      var min = S.ministeres(etat.coalition, ch, D.partis, D.portefeuilles);
      h += '<h3>' + T('Le Conseil des ministres', 'De Ministerraad') + '</h3>';
      h += '<p>' + T(
        'Quinze portefeuilles, répartis à la proportionnelle des sièges de la coalition, sous la ' +
        'contrainte de l\'article 99 : autant de ministres d\'expression française que néerlandaise, ' +
        'le Premier ministre éventuellement excepté.',
        'Vijftien portefeuilles, evenredig verdeeld, onder de beperking van artikel 99.') + '</p>';
      h += '<div class="defile"><table><thead><tr><th>' + T('Portefeuille', 'Portefeuille') + '</th><th>' +
        T('Groupe', 'Groep') + '</th><th>' + T('Liste', 'Lijst') + '</th></tr></thead><tbody>';
      min.postes.forEach(function (p, i) {
        var pf = D.portefeuilles[i];
        h += '<tr><td>' + ech(LANG === 'nl' ? pf.nl : pf.fr) + '</td><td>' +
          (pf.groupe === 'libre' ? '—' : pf.groupe.toUpperCase()) + '</td><td>' +
          (p.liste ? '<span class="pastille" style="background:' + coul(p.liste) + '"></span>' + ech(nom(p.liste)) : '—') +
          '</td></tr>';
      });
      h += '</tbody></table></div>';
    }
    q('#resultat-coalitions').innerHTML = h;
  }

  /* --------------------------------------------------------- législature */
  function rendreLegislature(sim) {
    if (!etat.coalition) { q('#resultat-legislature').innerHTML = ''; return; }
    var ch = sim.assemblees.chambre.sieges;
    var elargie = S.elargir(etat.coalition, etat.appuis, ch, D.partis);
    var choisis = lireChantiers();
    var l = S.legislature(etat.coalition, choisis, D.chantiers, D.cohesion, D.depart, elargie);
    var issue = null;
    D.issues.forEach(function (i) { if (i.code === l.issue) issue = i; });
    var h = '<div class="chiffres">' +
      '<div class="chiffre"><b>' + virgule(l.budget) + ' ' + T('Md€', 'mld €') + '</b><span>' +
      T('effort structurel acquis, sur 10 visés', 'structurele inspanning, op 10 beoogd') + '</span></div>' +
      '<div class="chiffre"><b>' + l.cohesion + '</b><span>' + T('cohésion de la coalition, sur 100', 'cohesie van de coalitie, op 100') + '</span></div>' +
      '<div class="chiffre"><b>' + (l.droit >= 0 ? '+' : '') + l.droit + '</b><span>' +
      T('points d\'état de droit', 'punten rechtsstaat') + '</span></div>' +
      '<div class="chiffre"><b>' + elargie.sieges + '</b><span>' +
      T('sièges avec les appuis', 'zetels met de steun') + '</span></div></div>';
    if (l.refuses.length) {
      h += '<div class="encart"><p><strong>' + T('Chantiers refusés par l\'arithmétique',
        'Werven geweigerd door de rekenkunde') + '</strong> : ' +
        l.refuses.map(function (code) {
          var t = null; D.chantiers.forEach(function (c) { if (c.code === code) t = c; });
          var norme = t.norme === 'loi' ? T('majorité absolue', 'absolute meerderheid')
            : t.norme === 'loi-speciale' ? T('deux tiers et majorité dans chaque groupe linguistique',
                                            'twee derde en meerderheid in elke taalgroep')
            : T('deux tiers', 'twee derde');
          return ech(LANG === 'nl' ? t.titre_nl : t.titre_fr) + ' (' + norme + ')';
        }).join(' · ') + '</p></div>';
    }
    h += '<h3>' + ech(LANG === 'nl' ? issue.titre_nl : issue.titre_fr) + '</h3>';
    h += '<p style="font-size:.82rem;color:var(--doux)">' + ech(LANG === 'nl' ? issue.regle_nl : issue.regle_fr) + '</p>';
    h += '<p>' + ech(LANG === 'nl' ? issue.texte_nl : issue.texte_fr) + '</p>';
    q('#resultat-legislature').innerHTML = h;
    return l;
  }

  /* ------------------------------------------------------ procès-verbal */
  function rendrePV(sim, l) {
    var choix = lireChoix(), depart = lireDepart();
    var son = null;
    D.sondages.forEach(function (s) { if (s.code === depart) son = s; });
    var h = '<h3>' + T('1. Le point de départ', '1. Het startpunt') + '</h3><p>' +
      ech(LANG === 'nl' ? son.nom_nl : son.nom_fr) + ' — ' + ech(LANG === 'nl' ? son.institut_nl : son.institut_fr) + '</p>';
    h += '<h3>' + T('2. Les six échéances', '2. De zes ijkmomenten') + '</h3><ol>';
    D.echeances.forEach(function (e) {
      var iss = null;
      e.issues.forEach(function (i) { if (i.code === choix[e.code]) iss = i; });
      if (!iss) return;
      h += '<li><strong>' + ech(LANG === 'nl' ? e.titre_nl : e.titre_fr) + '</strong> (' + e.date + ') → ' +
        ech(LANG === 'nl' ? iss.titre_nl : iss.titre_fr) + '</li>';
    });
    h += '</ol>';
    h += '<h3>' + T('3. Le report cumulé, en points', '3. De gecumuleerde verschuiving, in punten') + '</h3>';
    h += '<div class="defile"><table><thead><tr><th>' + T('Région', 'Gewest') + '</th><th>' +
      T('Report appliqué', 'Toegepaste verschuiving') + '</th></tr></thead><tbody>';
    ['fl', 'wa', 'bxl'].forEach(function (r) {
      if (!sim.reports[r]) return;
      var m = Object.keys(sim.reports[r]).sort(function (a, b) {
        return Math.abs(sim.reports[r][b]) - Math.abs(sim.reports[r][a]);
      }).map(function (k) {
        var v = sim.reports[r][k];
        return nom(k) + ' ' + (v > 0 ? '+' : '−') + virgule(Math.abs(v));
      }).join(', ');
      var nomr = { fl: T('Flandre', 'Vlaanderen'), wa: T('Wallonie', 'Wallonië'), bxl: T('Bruxelles', 'Brussel') }[r];
      h += '<tr><td>' + nomr + '</td><td>' + ech(m) + '</td></tr>';
    });
    h += '</tbody></table></div>';
    h += '<h3>' + T('4. Les cinq assemblées', '4. De vijf assemblees') + '</h3>';
    h += '<div class="defile"><table><thead><tr><th>' + T('Assemblée', 'Assemblee') + '</th><th>' +
      T('Composition simulée', 'Gesimuleerde samenstelling') + '</th></tr></thead><tbody>';
    Object.keys(sim.assemblees).forEach(function (code) {
      var s = sim.assemblees[code].sieges;
      var m = Object.keys(s).filter(function (k) { return s[k] > 0; })
        .sort(function (a, b) { return s[b] - s[a]; })
        .map(function (k) { return nom(k) + ' ' + s[k]; }).join(', ');
      h += '<tr><td>' + ech(D.nomsAssemblees[code][LANG]) + '</td><td>' + ech(m) + '</td></tr>';
    });
    h += '</tbody></table></div>';
    if (etat.coalition && l) {
      h += '<h3>' + T('5. La coalition et la législature', '5. De coalitie en de legislatuur') + '</h3><ul>';
      h += '<li>' + T('Coalition', 'Coalitie') + ' : ' + ech(etat.coalition.membres.map(nom).join(' + ')) +
        ' — ' + etat.coalition.sieges + ' ' + T('sièges', 'zetels') + '</li>';
      h += '<li>' + T('Appuis extérieurs', 'Externe steun') + ' : ' +
        (etat.appuis.length ? ech(etat.appuis.map(nom).join(', ')) : T('aucun', 'geen')) + '</li>';
      h += '<li>' + T('Chantiers adoptés', 'Aangenomen werven') + ' : ' +
        (l.adoptes.length ? ech(l.adoptes.join(', ')) : T('aucun', 'geen')) + '</li>';
      h += '<li>' + T('Chantiers refusés', 'Geweigerde werven') + ' : ' +
        (l.refuses.length ? ech(l.refuses.join(', ')) : T('aucun', 'geen')) + '</li>';
      h += '<li>' + T('Budget', 'Begroting') + ' : ' + virgule(l.budget) + ' / ' + D.depart.objectif +
        ' ' + T('Md€', 'mld €') + ' — ' + T('écart restant', 'resterend tekort') + ' : ' + virgule(l.ecartRestant) + '</li>';
      h += '<li>' + T('Cohésion', 'Cohesie') + ' : ' + l.cohesion + ' / 100</li>';
      h += '<li>' + T('État de droit', 'Rechtsstaat') + ' : ' + (l.droit >= 0 ? '+' : '') + l.droit + '</li>';
      h += '<li><strong>' + T('Issue', 'Uitkomst') + ' : ' + ech(l.issue) + '</strong></li></ul>';
    }
    h += '<p style="font-size:.8rem;color:var(--doux)">' + T(
      'Ce procès-verbal est calculé dans votre navigateur, à partir des chiffres officiels du ' +
      '9 juin 2024 et des hypothèses de report publiées sur la page Méthode. Il n\'est envoyé nulle part.',
      'Dit proces-verbaal wordt in uw browser berekend en wordt nergens verstuurd.') + '</p>';
    q('#pv').innerHTML = h;
  }

  /* -------------------------------------------------------------- carnet */
  function codeEtat() {
    var c = lireChoix(), p = [lireDepart()];
    D.echeances.forEach(function (e) {
      var i = 0;
      e.issues.forEach(function (x, j) { if (x.code === c[e.code]) i = j; });
      p.push(i);
    });
    p.push(lireExclusions().join('.'));
    p.push(lireChantiers().join('.'));
    if (etat.coalition) p.push(etat.coalition.membres.join('.'));
    return p.join('_');   /* « _ » n'apparaît dans aucun code de liste ni d'issue */
  }
  function appliquerCode(code) {
    if (!code) return;
    var p = code.split('_');
    if (p.length < 9) return;   /* code d'une version antérieure : on ignore */
    var d = q('input[name="depart"][value="' + p[0] + '"]');
    if (d) d.checked = true;
    D.echeances.forEach(function (e, i) {
      var j = parseInt(p[i + 1], 10);
      if (isNaN(j) || !e.issues[j]) return;
      var r = q('input[name="' + e.code + '"][value="' + e.issues[j].code + '"]');
      if (r) r.checked = true;
    });
    var ex = (p[7] || '').split('.').filter(Boolean);
    qa('input[name="exclusion"]').forEach(function (i) {
      var cible = null;
      D.exclusions.forEach(function (x) { if (x.code === i.value) cible = x.cible; });
      i.checked = cible.some(function (k) { return ex.indexOf(k) !== -1; });
    });
    var chs = (p[8] || '').split('.').filter(Boolean);
    qa('input[name="chantier"]').forEach(function (i) { i.checked = chs.indexOf(i.value) !== -1; });
    if (p[9]) etat.coalition = { membres: p[9].split('.') };
  }

  /* ---------------------------------------------------------------- boucle */
  function tout() {
    var sim = S.simuler(D, lireDepart(), lireChoix());
    rendreScrutin(sim);
    rendreCoalitions(sim);
    var l = rendreLegislature(sim);
    rendrePV(sim, l);
    try {
      var c = codeEtat();
      history.replaceState(null, '', '#c=' + c);
      localStorage.setItem('scrutin', c);
    } catch (err) { /* mode privé : on continue sans mémoire */ }
  }

  document.addEventListener('change', function (ev) {
    var n = ev.target.name;
    if (n === 'coalition') {
      var membres = ev.target.value.split('+');
      var sim = S.simuler(D, lireDepart(), lireChoix());
      etat.coalition = S.evaluerCoalition(membres, sim.assemblees.chambre.sieges, D.partis);
      etat.appuis = etat.appuis.filter(function (a) { return membres.indexOf(a) === -1; });
      tout();
      return;
    }
    if (n === 'appui') {
      etat.appuis = qa('input[name="appui"]:checked').map(function (i) { return i.value; });
      var sim2 = S.simuler(D, lireDepart(), lireChoix());
      rendreLegislature(sim2);
      rendrePV(sim2, rendreLegislature(sim2));
      return;
    }
    if (n === 'depart' || n === 'exclusion' || n === 'chantier' ||
        D.echeances.some(function (e) { return e.code === n; })) {
      if (n === 'depart' || D.echeances.some(function (e) { return e.code === n; })) etat.coalition = null;
      tout();
    }
  });

  var hash = location.hash.match(/c=([^&]+)/);
  var memoire = null;
  try { memoire = localStorage.getItem('scrutin'); } catch (err) { memoire = null; }
  appliquerCode(hash ? decodeURIComponent(hash[1]) : memoire);
  tout();

  var imp = q('#imprimer');
  if (imp) imp.addEventListener('click', function () { window.print(); });
  var cop = q('#copier-lien');
  if (cop) cop.addEventListener('click', function () {
    var url = location.origin + location.pathname + '#c=' + codeEtat();
    if (navigator.clipboard) navigator.clipboard.writeText(url);
    cop.textContent = T('Lien copié', 'Link gekopieerd');
    setTimeout(function () { cop.textContent = T('Copier le lien de cette partie', 'De link van deze partij kopiëren'); }, 2000);
  });
})();
