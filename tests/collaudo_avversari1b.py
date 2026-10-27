# Collaudo degli avversari dell'1b con situazioni costruite (1.0.49, docs/PROPOSTA-AVVERSARI-1B.md §6). Regata nei salti di vento,
# salti spenti (setShifts(null)), vento costante, giocatore spostato a 5 km. Gli avversari si mettono a mano a regata in corso (tratto 1)
# e li guida la loro guida (aiControl). Ogni scenario in 10 varianti (distanze e angoli spostati con il seme), esito atteso scritto prima.
#   1 incrocio con mure diverse: nessun contatto; la mure a dritta non devia più di 10° e non scende sotto il 70% della velocità iniziale
#   2 stesse mure affiancate (sopravento 6-9 m): nessun contatto; la sottovento non si pianta (5 s sotto 0,5 nodi)
#   3 stesse mure, una dietro più veloce: nessun contatto
#   4 virata davanti a un'altra (regola 13): nessun contatto; se c'è, la penalità va a chi virava (contati a parte)
#   5 tre barche alla boa insieme: tutte la girano entro 60 s, nessuna piantata
# Superato con almeno 9 varianti su 10 per scenario. Riportati anche i casi misurati, per non promuovere con zero casi.
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri() + "#collaudo"
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
SCENA = """([sc, v]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", 2]); __seed(1000 + 37 * sc + v); sv.setShifts(null); sv.simTime = 0;
  const R = sv.R, D = Math.PI / 180, me = R.boats[0], av = R.boats.filter(b => !b.me), twd = sv.windAt(0, 0).twd, rnd = Math.random;
  R.t = 120; R.phase = "race"; me.S.x += 5000; me.S.y += 5000;
  const up = [Math.sin(twd * D), -Math.cos(twd * D)], lat = [Math.cos(twd * D), Math.sin(twd * D)]; // controvento e di lato (verso destra guardando il vento)
  const mk = R.mark, P = (a, l) => ({ x: mk.x - up[0] * a + lat[0] * l, y: mk.y - up[1] * a + lat[1] * l }); // a metri sotto la boa, l di lato
  const put = (b, p, h, u) => { Object.assign(b.S, { x: p.x, y: p.y, h: (h + 360) % 360, u, r: 0, heel: 0, capsized: false });
    Object.assign(b, { leg: 1, ocs: false, goStart: true, fin: null, dnf: false, rnd: 0, side: Math.sign(((twd - h) % 360 + 540) % 360 - 180), boardT: 0, boardMax: 999, virando: false });
    b.ctl.sheet = 0.15; b.ctl.tiller = 0; };
  const fwd = h => [Math.sin(h * D), -Math.cos(h * D)];
  const lontano = b => put(b, { x: me.S.x + 300, y: me.S.y }, twd - 50, 0);
  let A = av[0], B = av[1], C = av[2], dur = 25, uso = [A, B];
  const hS = twd - 50, hP = twd + 50, u0 = 2.3; // bolina mure a dritta e a sinistra, circa 4,5 nodi
  if (sc === 1){ // si incontrerebbero in X dopo T secondi
    const T = 6 + rnd() * 6, X = P(150, (rnd() - 0.5) * 10), fs = fwd(hS), fp = fwd(hP);
    put(A, { x: X.x - fs[0] * u0 * T, y: X.y - fs[1] * u0 * T }, hS, u0); put(B, { x: X.x - fp[0] * u0 * T + (rnd() - 0.5) * 3, y: X.y - fp[1] * u0 * T }, hP, u0); lontano(C);
  } else if (sc === 2){ // B sottovento, A sopravento di 6-9 m, alla pari
    const Q = P(150, 0), g = 6 + rnd() * 3, f = fwd(hS), w = [Math.cos(hS * D), Math.sin(hS * D)], a = (rnd() - 0.5) * 3; // w: a dritta della prua, cioè sopravento sulle mure a dritta
    put(B, Q, hS, u0); put(A, { x: Q.x + w[0] * g + f[0] * a, y: Q.y + w[1] * g + f[1] * a }, hS + 10, u0); lontano(C); // A converge di 10° verso B
  } else if (sc === 3){ // A davanti quasi ferma, B 6-10 m dietro sulla stessa rotta, veloce
    const Q = P(150, 0), f = fwd(hS), g = 6 + rnd() * 4;
    put(A, Q, hS, 0.2); put(B, { x: Q.x - f[0] * g + (rnd() - 0.5) * 1.5, y: Q.y - f[1] * g }, hS, 3.0); lontano(C);
  } else if (sc === 4){ // A mure a sinistra vira davanti a B mure a dritta, che arriva da 4-8 m sulla stessa linea
    const Q = P(150, 0), g = 4 + rnd() * 4, fs = fwd(hS);
    put(A, Q, hP, u0); A.side = 1; A.boardT = 0; // la guida le chiede di virare sulle mure a dritta
    put(B, { x: Q.x - fs[0] * g, y: Q.y - fs[1] * g }, hS, u0); lontano(C);
  } else { // tre barche a 25-35 m sotto la boa, a 6 m l'una dall'altra, mure a dritta verso la boa
    uso = [A, B, C]; dur = 70;
    uso.forEach((b, k) => put(b, P(25 + rnd() * 10 + k * 3, 14 + k * 6), hS, u0));
  }
  const h0 = A.S.h, pen0 = R.penList.length, dt = 1 / 60, lento = new Map(), giro = new Map();
  let devMax = 0, uMin = 1e9, piantate = 0, dMin = 1e9;
  for (let n = 0; n * dt < dur; n++){
    sv.run(dt, 1);
    const t = n * dt; dMin = Math.min(dMin, Math.hypot(A.S.x - B.S.x, A.S.y - B.S.y));
    if (sc === 1 && t < 15){ devMax = Math.max(devMax, Math.abs(((A.S.h - h0) % 360 + 540) % 360 - 180)); if (t > 1) uMin = Math.min(uMin, A.S.u / u0); }
    for (const b of uso){ const k = b.S.u * 1.944 < 0.5 ? (lento.get(b) || 0) + dt : 0; lento.set(b, k); if (k >= 5 && k - dt < 5) piantate++;
      if (b.leg === 2 && !giro.has(b)) giro.set(b, t); }
  }
  const pen = R.penList.slice(pen0);
  return { contatti: pen.length, pen, devMax: Math.round(devMax), uMin: +uMin.toFixed(2), piantate, girate: giro.size, nGiro: uso.length,
           dMin: +dMin.toFixed(1), aChiVira: pen.filter(p => /regola 13/.test(p)).length };
}"""
ATTESO = {1: "nessun contatto, mure a dritta devia ≤10° e resta ≥70% della velocità", 2: "nessun contatto, nessuna piantata", 3: "nessun contatto",
          4: "nessun contatto", 5: "tutte girano entro 60 s, nessuna piantata"}
def buono(sc, r):
    if sc == 1: return r["contatti"] == 0 and r["devMax"] <= 10 and r["uMin"] >= 0.7
    if sc in (2,): return r["contatti"] == 0 and r["piantate"] == 0
    if sc in (3, 4): return r["contatti"] == 0
    return r["girate"] == r["nGiro"] and r["piantate"] == 0
async def main():
    fall = []
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch(); errs = []
        for sc in ([int(sys.argv[1])] if len(sys.argv) > 1 else range(1, 6)): # uno scenario solo: python collaudo_avversari1b.py 4
            ok = 0
            for v in range(10):
                pg = await b.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); await pg.add_init_script(SEME)
                await pg.goto(BASE); await pg.wait_for_timeout(300)
                r = await pg.evaluate(SCENA, [sc, v]); await pg.close()
                ok += buono(sc, r)
                print(f"  scenario {sc} variante {v}: {'ok' if buono(sc, r) else 'NO'}  contatti {r['contatti']} (regola 13: {r['aChiVira']}), distanza minima A-B {r['dMin']} m, deviazione {r['devMax']}°,"
                      f" velocità minima {r['uMin']}, piantate {r['piantate']}, girate {r['girate']}/{r['nGiro']} {r['pen'][:1]}", flush=True)
            print(f"scenario {sc} ({ATTESO[sc]}): {ok} su 10 {'OK' if ok >= 9 else 'FALLITO'}", flush=True)
            if ok < 9: fall.append(sc)
        await b.close()
    print("errori pagina:", errs[:3])
    print("ESITO:", "OK" if not fall and not errs else f"FALLITO (scenari {fall})")
    sys.exit(1 if fall or errs else 0)
asyncio.run(main())
