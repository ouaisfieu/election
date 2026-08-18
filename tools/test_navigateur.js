/* Tests de navigateur. Aucun élément n'est simulé : c'est le vrai site qui est chargé. */
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const RACINE = path.join(__dirname, '..');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript',
  '.png': 'image/png', '.xml': 'application/xml', '.webmanifest': 'application/manifest+json',
  '.txt': 'text/plain' };

let echecs = 0, reussites = 0;
function ok(cond, nom) {
  if (cond) { reussites++; console.log('  ok    ' + nom); }
  else { echecs++; console.error('  ÉCHEC ' + nom); }
}

function serveur() {
  return http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split('?')[0].split('#')[0]);
    let f = path.join(RACINE, p);
    if (p.endsWith('/')) f = path.join(f, 'index.html');
    if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) {
      res.writeHead(404, { 'Content-Type': 'text/html' });
      res.end(fs.existsSync(path.join(RACINE, '404.html')) ? fs.readFileSync(path.join(RACINE, '404.html')) : 'introuvable');
      return;
    }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
    res.end(fs.readFileSync(f));
  });
}

(async () => {
  const srv = serveur();
  await new Promise(r => srv.listen(8731, r));
  const base = 'http://127.0.0.1:8731';
  const navigateur = await chromium.launch();
  const ctx = await navigateur.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const erreurs = [];
  page.on('console', m => { if (m.type() === 'error') erreurs.push(m.text()); });
  page.on('requestfailed', r => erreurs.push('requête échouée : ' + r.url()));
  page.on('response', r => { if (r.status() >= 400) erreurs.push('HTTP ' + r.status() + ' ' + r.url()); });
  page.on('pageerror', e => erreurs.push(String(e)));

  /* 1. l'accueil */
  await page.goto(base + '/', { waitUntil: 'networkidle' });
  ok((await page.title()).includes('Le Scrutin'), 'accueil : titre');
  ok(await page.locator('main h1').count() === 1, 'accueil : un seul h1');

  /* 2. le simulateur calcule */
  await page.goto(base + '/simulateur/', { waitUntil: 'networkidle' });
  await page.waitForSelector('#resultat-scrutin table', { timeout: 8000 });
  const total = await page.evaluate(() => {
    const sim = window.Scrutin.simuler(window.ScrutinDonnees, 'resultat2024', {});
    return Object.values(sim.assemblees.chambre.sieges).reduce((a, b) => a + b, 0);
  });
  ok(total === 150, 'simulateur : 150 sièges attribués');

  /* 3. sans report, le moteur retrouve la Chambre de 2024 */
  const identique = await page.evaluate(() => {
    const D = window.ScrutinDonnees;
    const sim = window.Scrutin.simuler(D, 'resultat2024', {});
    const off = {};
    D.assemblees.chambre.circonscriptions.forEach(c => {
      Object.keys(c.officiel).forEach(k => { off[k] = (off[k] || 0) + c.officiel[k]; });
    });
    return Object.keys(off).every(k => (sim.assemblees.chambre.sieges[k] || 0) === off[k]);
  });
  ok(identique, 'simulateur : sans report, la Chambre de 2024 est reproduite');

  /* 4. changer une échéance change le résultat */
  const avant = await page.locator('#resultat-scrutin table').first().innerText();
  await page.locator('input[name="conclave"][value="echec"]').check();
  await page.waitForTimeout(400);
  const apres = await page.locator('#resultat-scrutin table').first().innerText();
  ok(avant !== apres, 'simulateur : une échéance modifie le résultat');

  /* 5. les coalitions apparaissent et sont sélectionnables */
  await page.waitForSelector('#resultat-coalitions input[name="coalition"]');
  const nbCoal = await page.locator('#resultat-coalitions input[name="coalition"]').count();
  ok(nbCoal > 0, 'formation : au moins une coalition proposée');
  await page.locator('#resultat-coalitions input[name="coalition"]').nth(1).check();
  await page.waitForTimeout(400);
  ok(await page.locator('#resultat-coalitions table').count() >= 2, 'formation : le Conseil des ministres est réparti');

  /* 6. la parité de l'article 99 est respectée */
  const parite = await page.evaluate(() => {
    const D = window.ScrutinDonnees, S = window.Scrutin;
    const sim = S.simuler(D, D.sondageDefaut, {});
    const ch = sim.assemblees.chambre.sieges;
    const coals = S.coalitionsPossibles(ch, D.partis, ['vb'], 5).filter(c => c.minimale);
    if (!coals.length) return true;
    const m = S.ministeres(coals[0], ch, D.partis, D.portefeuilles);
    let fr = 0, nl = 0;
    m.postes.forEach((p, i) => {
      if (!p.liste || D.portefeuilles[i].code === 'pm') return;
      const com = D.partis[p.liste].communaute;
      if (com === 'fr') fr++; else if (com === 'fl') nl++;
    });
    return Math.abs(fr - nl) <= 1;
  });
  ok(parite, 'formation : parité linguistique du Conseil des ministres');

  /* 7. un chantier de charge spéciale est refusé sans les deux tiers */
  const refus = await page.evaluate(() => {
    const D = window.ScrutinDonnees, S = window.Scrutin;
    const sim = S.simuler(D, D.sondageDefaut, {});
    const ch = sim.assemblees.chambre.sieges;
    const coals = S.coalitionsPossibles(ch, D.partis, ['vb'], 5).filter(c => c.minimale && !c.loiSpeciale);
    if (!coals.length) return true;
    const l = S.legislature(coals[0], ['reforme-etat'], D.chantiers, D.cohesion, D.depart, coals[0]);
    return l.refuses.indexOf('reforme-etat') !== -1;
  });
  ok(refus, 'législature : une loi spéciale est refusée sans la majorité requise');

  /* 8. le procès-verbal est rempli */
  ok((await page.locator('#pv').innerText()).length > 400, 'procès-verbal : rempli');

  /* 9. la progression survit au rechargement */
  const urlAvant = page.url();
  ok(urlAvant.includes('#c='), 'carnet : la partie est codée dans l\'adresse');
  await page.goto(urlAvant, { waitUntil: 'networkidle' });
  await page.waitForTimeout(400);
  ok(await page.locator('input[name="conclave"][value="echec"]').isChecked(),
     'carnet : le choix est restauré depuis l\'adresse');
  ok(await page.locator('input[name="exclusion"][value="cordon"]').isChecked(),
     'carnet : les exclusions survivent au rechargement');
  const lignePremiere = await page.locator('#resultat-coalitions table tbody tr').first().innerText();
  ok(lignePremiere.indexOf('Vlaams Belang') === -1,
     'formation : une exclusion cochée retire bien la liste visée');

  /* 10. lisibilité sans JavaScript */
  const ctx2 = await navigateur.newContext({ javaScriptEnabled: false });
  const p2 = await ctx2.newPage();
  await p2.goto(base + '/simulateur/');
  const texte = await p2.locator('main').innerText();
  ok(texte.length > 4000, 'sans JavaScript : le simulateur reste lisible');
  ok(texte.includes('conclave') || texte.includes('Conclave'), 'sans JavaScript : les échéances sont écrites');
  await p2.goto(base + '/chambre/hainaut/');
  ok((await p2.locator('main table').count()) >= 2, 'sans JavaScript : les tableaux sont dans le HTML');

  /* 11. le néerlandais */
  await page.goto(base + '/nl/simulator/', { waitUntil: 'networkidle' });
  await page.waitForSelector('#resultat-scrutin table', { timeout: 8000 });
  ok((await page.locator('html').getAttribute('lang')) === 'nl', 'néerlandais : attribut lang');
  ok((await page.locator('#resultat-scrutin').innerText()).length > 200, 'néerlandais : le simulateur calcule');

  /* 12. aucune erreur de console sur les pages existantes */
  ok(erreurs.length === 0, 'aucune erreur de console (' + erreurs.slice(0, 3).join(' | ') + ')');

  /* 13. 404 : servie, et ses ressources restent absolues */
  await page.goto(base + '/chambre/nexistepas/');
  ok((await page.locator('main h1').innerText()).length > 3, '404 : page servie');
  const css404 = await page.locator('link[rel=stylesheet]').getAttribute('href');
  ok(css404.startsWith('https://'), '404 : la feuille de style est référencée en absolu');

  /* captures */
  const capt = path.join(RACINE, 'tools', 'captures');
  fs.mkdirSync(capt, { recursive: true });
  await page.goto(base + '/', { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(capt, 'accueil.png'), fullPage: false });
  await page.goto(base + '/simulateur/', { waitUntil: 'networkidle' });
  await page.waitForSelector('#resultat-scrutin table');
  await page.screenshot({ path: path.join(capt, 'simulateur.png'), fullPage: false });
  await page.locator('#resultat-scrutin').scrollIntoViewIfNeeded();
  await page.screenshot({ path: path.join(capt, 'scrutin.png') });
  await page.locator('#formation').scrollIntoViewIfNeeded();
  await page.screenshot({ path: path.join(capt, 'formation.png') });
  await page.goto(base + '/chambre/hainaut/', { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(capt, 'hainaut.png') });
  await page.goto(base + '/methode/', { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(capt, 'methode.png') });

  await navigateur.close();
  srv.close();
  console.log('\n' + reussites + ' assertion(s) réussie(s), ' + echecs + ' échec(s).');
  process.exit(echecs ? 1 : 0);
})();
