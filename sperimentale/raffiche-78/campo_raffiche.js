// Voce 78: copia in Node del campo di raffiche delle regate lunghe del torneo (js/gioco.js: spawnGust, updateGusts, ventoDa con gustLevel 1, gustAll, gustZona).
// Solo il vento (niente barche): le raffiche nascono sopravento a un punto a caso del campo (nel gioco: a una barca a caso). Stesso metro di tests/misura_raffiche_vere.py:
// 16 punti fissi, lettura ogni 0,5 s, intervalli di 2 e 8 minuti, fattore = picco della media mobile di 5 s / media. Uso: node sperimentale/raffiche-78/campo_raffiche.js [variante] [primo seme]
// Varianti (argomento): oggi | sat (somma che satura: 1 − Π(1 − f·k)) | max (conta la raffica più forte e metà delle altre; max4, max3: 0,4 e 0,3 delle altre) | k30 (k da 0,2-0,3 invece di 0,2-0,4)
const VAR = process.argv[2] || "oggi", KN = 1.943844, D2R = Math.PI / 180;
const RAFF_R = [80, 80], RAFF_VITA = [120, 120], RAFF_INT = 7, RAFF_DIST = [150, 150], RAFF_LAT = 3;
function q(v, p){ v = [...v].sort((a, b) => a - b); return v[Math.min(v.length - 1, Math.floor(p * v.length))]; }
function corsa(seme, up){
  let s = seme >>> 0; const rnd = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  const tws = (rnd() < 0.5 ? 10 : 12) / KN, gusts = []; let timer = 3;
  const spawn = (dist, lat, mature) => { const P = { x: (rnd() - 0.5) * 400, y: -rnd() * up };
    gusts.push({ x: P.x - 0 * dist - 1 * lat * 0, y: P.y - dist, xl: lat, r: RAFF_R[0] + rnd() * RAFF_R[1], k: VAR === "k30" ? 0.2 + rnd() * 0.1 : 0.2 + rnd() * 0.2, age: mature ? 3 : 0, ttl: RAFF_VITA[0] + rnd() * RAFF_VITA[1], life: mature ? 1 : 0 });
    gusts[gusts.length - 1].x = P.x + lat; };
  for (let i = 0; i < 4; i++) spawn(RAFF_DIST[0] + rnd() * RAFF_DIST[1], (rnd() - 0.5) * 90 * RAFF_LAT, true);
  const P = []; for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) P.push([-150 + i * 100, -up * (0.15 + 0.7 * j / 3)]);
  const L = P.map(() => []), dt = 0.5;
  for (let t = -60; t < 660; t += dt){
    for (const g of gusts){ g.y += tws * 0.8 * dt; g.age += dt; g.life = Math.max(0, Math.min(1, g.age / 3, (g.ttl - g.age) / 3)); }
    for (let i = gusts.length - 1; i >= 0; i--) if (gusts[i].age > gusts[i].ttl) gusts.splice(i, 1);
    timer -= dt; if (timer <= 0 && gusts.length < 12){ timer = 4 * (0.6 + rnd() * 0.8) * RAFF_INT; spawn(RAFF_DIST[0] + rnd() * RAFF_DIST[1], (rnd() - 0.5) * 90 * RAFF_LAT, false); }
    if (t >= 0) P.forEach(([x, y], n) => { const fs = [];
      for (const g of gusts){ const al = (y - g.y) / (g.r * 1.4), ac = (x - g.x) / g.r, d2 = al * al + ac * ac; if (d2 < 1) fs.push((1 - d2) ** 2 * g.life * g.k); }
      let k = 0;
      if (VAR === "sat") k = 1 - fs.reduce((p, f) => p * (1 - f), 1);
      else if (VAR.startsWith("max")){ const w = VAR === "max" ? 0.5 : +VAR.slice(3) / 10; fs.sort((a, b) => b - a); k = fs.reduce((p, f, i) => p + (i ? w : 1) * f, 0); }
      else k = fs.reduce((p, f) => p + f, 0);
      L[n].push(tws * (1 + k)); });
  }
  return L; }
function fattori(serie, n){ const out = []; for (const s of serie) for (let a = 0; a + n <= s.length; a += n){ const w = s.slice(a, a + n), m = w.reduce((p, v) => p + v, 0) / n;
  let mx = 0; for (let i = 0; i + 10 <= n; i++){ let z = 0; for (let j = i; j < i + 10; j++) z += w[j]; mx = Math.max(mx, z / 10); } out.push(mx / m); } return out; }
const F2 = [], F8 = []; let kmax = 0;
const S0 = +(process.argv[3] || 1); for (let seme = S0; seme < S0 + 200; seme++){ const L = corsa(seme, seme % 2 ? 560 : 440); F2.push(...fattori(L, 240)); F8.push(...fattori(L, 960)); }
const r = (n, F) => `${n}: casi ${F.length}; 25° ${q(F, .25).toFixed(2)}, mediana ${q(F, .5).toFixed(2)}, 75° ${q(F, .75).toFixed(2)}, 90° ${q(F, .9).toFixed(2)}, 99° ${q(F, .99).toFixed(2)}, massimo ${Math.max(...F).toFixed(2)}`;
console.log(`variante ${VAR} (200 regate di 10 minuti, semi ${S0}-${S0 + 199})`); console.log(r("2 minuti", F2)); console.log(r("8 minuti", F8));
