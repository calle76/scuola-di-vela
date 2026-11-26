# Voce 88, passo 1 (banco): scrive motore88.js = js/motore.js (barca M, 1.3.59) + le onde di docs/PROPOSTA-ONDE.md, che js/ non vede.
# Le onde agiscono solo se E.onde esiste (O9: senza onde il motore e' M al bit). Uso: python3 sperimentale/onde-88/fa_motore88.py
import pathlib
q = pathlib.Path(__file__).parent; s = (q / "../../js/motore.js").read_text()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a); s = s.replace(a, b)
rep("function step(S, C, E, dt){", '''/* V88 (banco): onde da vento, SPM 1984 (F142) con fetch dato; 5 componenti di uguale ampiezza, periodi 0,7-1,5 Tp, fasi dal seme (IPOTESI);
   acqua profonda (IPOTESI: un lago o una baia piu' profondi di meta' onda); vanno dove va il vento medio. */
const V88 = { LWL: 3.381, BWL: 1.105, caw: 1.5, f45: 0.55, uCaw: 2, rp: [0.7, 0.9, 1.1, 1.3, 1.5] };
function onde88crea(tws, twd, fetch, seme){
  const g = 9.81, UA = 0.71 * Math.pow(tws, 1.23), x = g * fetch / (UA * UA);
  const Hs = Math.min(0.0016 * Math.sqrt(x), 0.243) * UA * UA / g, Tp = Math.min(0.286 * Math.cbrt(x), 8.13) * UA / g;
  let r = (seme >>> 0) || 1; const rnd = () => { r = r + 0x6D2B79F5 | 0; let t = Math.imul(r ^ r >>> 15, 1 | r); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const a = Hs / 4 * Math.sqrt(2 / V88.rp.length);
  const comps = V88.rp.map(p => { const T = Tp * p, w = 2 * Math.PI / T, k = w * w / g; return { a, k, c: w / k, ph: rnd() * 2 * Math.PI }; });
  return { dir: norm360(twd + 180), Hs, Tp, comps, t: 0 };
}
/* forza dell'onda lungo la prua (Harris, Thomas, Renilson 1999, F141: Froude-Krylov, peso x pendenza, ridotta da sinc(kL/2)) e resistenza in piu'
   con le onde da prua (F138 Caw per l'ILCA 6, x 0,55 a 45 gradi dalle onde, F143; col coseno fino al traverso e sotto 2 m/s: IPOTESI). Sbandamento,
   imbardata, beccheggio, velocita' orbitale dell'acqua: fuori (PROPOSTA-ONDE.md). Restituisce [spinta in avanti, resistenza in piu', elevazione]. */
function onde88(S, W){
  const h = S.h * D2R, d = W.dir * D2R, ct = Math.sin(h) * Math.sin(d) + Math.cos(h) * Math.cos(d), sp = S.x * Math.sin(d) - S.y * Math.cos(d);
  const vol = BOAT.mass / BOAT.rhoW, Le = V88.LWL * Math.abs(ct); let F = 0, eta = 0;
  for (const c of W.comps){ const ph = c.k * (sp - c.c * W.t) + c.ph, z = c.k * Le / 2, sinc = z > 1e-6 ? Math.sin(z) / z : 1;
    F += BOAT.rhoW * 9.81 * vol * c.a * c.k * sinc * Math.sin(ph); eta += c.a * Math.cos(ph); }
  const fr = Math.max(0, V88.f45 * (-ct) / Math.cos(45 * D2R));
  const Rw = V88.caw * BOAT.rhoW * 9.81 * (W.Hs * W.Hs / 8) * V88.BWL * V88.BWL / V88.LWL * fr * Math.min(1, Math.abs(S.u) / V88.uCaw) * Math.sign(S.u);
  return [F * ct, Rw, eta];
}

function step(S, C, E, dt){''')
rep("  S.u += (drive - res * heelDrag - Ri) / BOAT.mass * dt;",
    "  const o88 = E.onde ? onde88(S, E.onde) : null; if (o88){ S.fOnda = o88[0]; S.rOnda = o88[1]; S.eta = o88[2]; }\n"
    "  S.u += (drive - res * heelDrag - Ri + (o88 ? o88[0] - o88[1] : 0)) / BOAT.mass * dt;")
(q / "motore88.js").write_text("// Voce 88, banco: SCRITTO DA fa_motore88.py, non modificare a mano.\n" + s)
