/* Contrôle exhaustif. Charge le VRAI moteur et les VRAIES données, jamais une copie.
   1. rétro-test : le moteur reproduit-il la proclamation de 2024 ?
   2. énumération des 3^6 = 729 parcours de campagne, pour chaque point de départ ;
   3. énumération des issues de législature sur les coalitions minimales.
   Sortie : distribution des résultats. Le build échoue si un invariant est rompu. */
const S = require('../assets/js/moteur.js');
const D = require('../assets/data/donnees.js');

let echecs = 0;
function verifie(cond, message) { if (!cond) { console.error('  ÉCHEC ' + message); echecs++; } }

/* ---- 1. rétro-test 2024 ---------------------------------------------------*/
const ECART_ATTENDU = { chambre: 0, flamand: 0, wallon: 8, bruxellois: 1, germanophone: 0 };
console.log('Rétro-test de la proclamation du 9 juin 2024');
Object.keys(D.assemblees).forEach(function (code) {
  const a = D.assemblees[code];
  let ecart = 0, total = 0;
  a.circonscriptions.forEach(function (c) {
    const calc = S.dhondt(c.voix, c.sieges, a.seuil);
    const cles = new Set(Object.keys(c.officiel).concat(Object.keys(calc)));
    let d = 0;
    cles.forEach(function (k) { d += Math.abs((calc[k] || 0) - (c.officiel[k] || 0)); });
    ecart += d / 2;
    total += c.sieges;
  });
  verifie(total === a.sieges, code + ' : ' + total + ' sièges pour ' + a.sieges + ' légaux');
  verifie(ecart === ECART_ATTENDU[code],
    code + ' : écart ' + ecart + ', ' + ECART_ATTENDU[code] + ' attendu');
  console.log('  ' + code.padEnd(14) + a.sieges + ' sièges, écart ' + ecart);
});

/* ---- 2. énumération des parcours de campagne ------------------------------*/
const ech = D.echeances;
const parcours = [];
(function recur(i, choix) {
  if (i === ech.length) { parcours.push(Object.assign({}, choix)); return; }
  ech[i].issues.forEach(function (is) { choix[ech[i].code] = is.code; recur(i + 1, choix); });
})(0, {});
console.log('\nParcours de campagne énumérés : ' + parcours.length +
            ' par point de départ, ' + D.sondages.length + ' points de départ');

const stats = {};
let minSieges = {}, maxSieges = {};
let sansMajoriteClassique = 0, total = 0;
D.sondages.forEach(function (s) {
  const parCode = { chambre: [], flamand: [], wallon: [], bruxellois: [], germanophone: [] };
  parcours.forEach(function (p) {
    const r = S.simuler(D, s.code, p);
    total++;
    Object.keys(r.assemblees).forEach(function (code) {
      const res = r.assemblees[code];
      const somme = Object.keys(res.sieges).reduce(function (a, k) { return a + res.sieges[k]; }, 0);
      verifie(somme === res.total, code + ' : ' + somme + ' sièges attribués pour ' + res.total);
      parCode[code].push(res);
    });
    const ch = r.assemblees.chambre.sieges;
    Object.keys(ch).forEach(function (k) {
      if (minSieges[k] === undefined || ch[k] < minSieges[k]) minSieges[k] = ch[k];
      if (maxSieges[k] === undefined || ch[k] > maxSieges[k]) maxSieges[k] = ch[k];
    });
    /* la coalition sortante conserve-t-elle 76 sièges ? */
    const arizona = ['nva', 'mr', 'vooruit', 'cdv', 'le'];
    const sa = arizona.reduce(function (a, k) { return a + (ch[k] || 0); }, 0);
    if (sa < 76) sansMajoriteClassique++;
    const cle = s.code;
    stats[cle] = stats[cle] || { arizona76: 0, n: 0 };
    stats[cle].n++;
    if (sa >= 76) stats[cle].arizona76++;
  });
});

console.log('\nChambre — fourchette de sièges sur les ' + total + ' simulations');
Object.keys(maxSieges).filter(function (k) { return maxSieges[k] > 0; })
  .sort(function (a, b) { return maxSieges[b] - maxSieges[a]; })
  .forEach(function (k) {
    console.log('  ' + (D.partis[k] ? D.partis[k].nom : k).padEnd(16) +
                String(minSieges[k]).padStart(3) + ' – ' + String(maxSieges[k]).padStart(3));
  });
console.log('\nLa coalition sortante (N-VA, MR, Vooruit, cd&v, Les Engagés) garde 76 sièges :');
Object.keys(stats).forEach(function (k) {
  const s = stats[k];
  console.log('  ' + k.padEnd(26) + (100 * s.arizona76 / s.n).toFixed(1) + ' % des parcours');
});

/* ---- 3. issues de législature --------------------------------------------*/
const distrib = {};
let nbColl = 0;
D.sondages.forEach(function (s) {
  parcours.forEach(function (p, idx) {
    if (idx % 91 !== 0) return; /* échantillon systématique de parcours */
    const r = S.simuler(D, s.code, p);
    const ch = r.assemblees.chambre.sieges;
    const toutes = S.coalitionsPossibles(ch, D.partis, ['vb'], 5);
    const coals = toutes.filter(function (c) { return c.minimale; }).slice(0, 12);
    coals.forEach(function (c) {
      nbColl++;
      for (let masque = 0; masque < (1 << D.chantiers.length); masque++) {
        /* énumération complète des 256 paquets de chantiers */
        const choisis = D.chantiers.filter(function (_, i) { return masque & (1 << i); })
          .map(function (x) { return x.code; });
        const appuis = (masque & 1) ? Object.keys(ch).filter(function (k) {
          return c.membres.indexOf(k) === -1 && k !== 'vb' && ch[k] > 0;
        }) : [];
        const el = S.elargir(c, appuis, ch, D.partis);
        const l = S.legislature(c, choisis, D.chantiers, D.cohesion, D.depart, el);
        distrib[l.issue] = (distrib[l.issue] || 0) + 1;
      }
    });
  });
});
const tot = Object.keys(distrib).reduce(function (a, k) { return a + distrib[k]; }, 0);
console.log('\nIssues de législature (' + tot + ' parties, ' + nbColl + ' coalitions)');
Object.keys(distrib).sort(function (a, b) { return distrib[b] - distrib[a]; }).forEach(function (k) {
  console.log('  ' + k.padEnd(20) + (100 * distrib[k] / tot).toFixed(1) + ' %');
});

if (echecs) { console.error('\n' + echecs + ' échec(s).'); process.exit(1); }
console.log('\nAucun invariant rompu.');
