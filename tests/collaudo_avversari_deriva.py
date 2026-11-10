# Avversari di Deriva: i casi visti giocando (docs/PROPOSTA-AVVERSARI-DERIVA.md, V8; OSSERVAZIONI-GIOCANDO 80-83), 10 varianti ciascuno, superato con almeno 9 su 10.
# La barca del giocatore non è guidata: va dritta, come chi non si scansa. I 4 casi vanno provati anche sul gioco di prima, se no non distinguono: RADICE=cartella.
#  80 chi ha la precedenza, in poppa piena (174°), con l'altra che arriva sul suo lato, non torna a meno di 60° dal vento nei 15 s
#  81 chi cede a una barca che arriva a 2-3,2 s, quindi vicinissima, non prende penalità
#  82 due barche mure opposte, ciascuna con la barca ferma del giocatore più vicina nel tempo, non si urtano fra loro
#  83 giocatore fermo vicino allo spillo al via: al massimo una barca su tre esce dalla linea entro 30 s
import asyncio, os, pathlib, sys
from playwright.async_api import async_playwright
RADICE = pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent)
URL = (RADICE / "index.html").as_uri() + "#collaudo"
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
SCENA = """([sc, v]) => { const sv = __sv; sv.fast(0); sv.openItem(["r", sc === 83 ? 0 : 2]); __seed(5000 + sc * 37 + v); if (sc !== 83) sv.setShifts(null); sv.simTime = 0;
  const R = sv.R, D = Math.PI / 180, me = R.boats[0], av = R.boats.filter(b => !b.me), twd = sv.windAt(0, 0).twd, rnd = Math.random, dt = 1 / 60;
  const n1 = a => ((a + 540) % 360) - 180, fwd = h => [Math.sin(h * D), -Math.cos(h * D)];
  const [A, C, E] = av;
  if (sc === 83){ const pin = R.pin, L = fwd(twd + 90); while (R.t < -25) sv.run(dt, 1);
    const verso = Math.sign((0 - pin.x) * L[0] + (0 - pin.y) * L[1]) || 1, q = { x: pin.x + L[0] * verso * (10 + rnd() * 5) - fwd(twd)[0] * 5, y: pin.y + L[1] * verso * (10 + rnd() * 5) - fwd(twd)[1] * 5 };
    const fuori = new Set(); while (R.t < 30){ Object.assign(me.S, { x: q.x, y: q.y, u: 0, h: (twd + 60 + 360) % 360 }); sv.run(dt, 1); for (const b of av) if (b.ocs) fuori.add(b.name); }
    return { ok: fuori.size <= 1, dato: "fuori " + fuori.size }; }
  R.t = 120; R.phase = "race"; const mk = R.mark, up = fwd(twd), lat = [Math.cos(twd * D), Math.sin(twd * D)], Q = { x: mk.x - up[0] * 120 + lat[0] * 30, y: mk.y - up[1] * 120 + lat[1] * 30 };
  const put = (b, p, h, u, leg) => { Object.assign(b.S, { x: p.x, y: p.y, h: (h + 360) % 360, u, r: 0, heel: 0, capsized: false });
    Object.assign(b, { leg, ocs: false, goStart: true, fin: null, dnf: false, rnd: 0, side: Math.sign(n1(twd - h)), boardT: 0, boardMax: 999, virando: false }); if (b.ctl){ b.ctl.sheet = 0.3; b.ctl.tiller = 0; } };
  const via = (h, u, T) => { const f = fwd(h); return { x: Q.x - f[0] * u * T, y: Q.y - f[1] * u * T }; };
  put(E, { x: Q.x + 400, y: Q.y + 400 }, twd - 50, 0, 1); sv.ctl.tiller = 0; sv.ctl.sheet = 0.3;
  let minA = 1e9; const pen0 = R.penList.length;
  if (sc === 80){ const T = 3 + rnd() * 2, hm = twd + 130 - rnd() * 20; put(A, via(twd - 174, 2.4, T), twd - 174, 2.4, 2); put(me, via(hm, 2.6, T), hm, 2.6, 2); put(C, { x: Q.x - 400, y: Q.y }, twd - 50, 0, 1);
    for (let n = 0; n * dt < 15; n++){ sv.run(dt, 1); minA = Math.min(minA, Math.abs(n1(A.S.h - twd))); } return { ok: minA >= 60, dato: "minimo " + Math.round(minA) + "°" }; }
  if (sc === 81){ const T = 2 + rnd() * 1.2; put(A, via(twd + 95, 2.8, T), twd + 95, 2.8, 1); put(me, via(twd - 50, 2.3, T), twd - 50, 2.3, 1); put(C, { x: Q.x - 400, y: Q.y }, twd - 50, 0, 1);
    for (let n = 0; n * dt < 15; n++) sv.run(dt, 1); const p = R.penList.slice(pen0).filter(x => x.includes(A.name)); return { ok: !p.length, dato: p.length + " penalità" }; }
  const T = 7 + rnd() * 2; put(A, via(twd - 50, 2.3, T), twd - 50, 2.3, 1); put(C, via(twd + 50, 2.3, T), twd + 50, 2.3, 1); put(me, { x: Q.x - up[0] * 8, y: Q.y - up[1] * 8 }, twd - 50, 0, 1);
  for (let n = 0; n * dt < 18; n++){ me.S.u = 0; sv.run(dt, 1); } const p = R.penList.slice(pen0).filter(x => x.includes(A.name) && x.includes(C.name)); return { ok: !p.length, dato: p.length + " contatti fra loro" }; }"""
async def main():
    nome = os.environ.get("BROWSER", "chromium"); fall = False
    async with async_playwright() as p:
        b = await getattr(p, nome).launch(); errs = []
        for sc in (80, 81, 82, 83):
            es = []
            for v in range(10):
                pg = await b.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); await pg.add_init_script(SEME); await pg.goto(URL); await pg.wait_for_timeout(150)
                es.append(await pg.evaluate(SCENA, [sc, v])); await pg.close()
            n = sum(e["ok"] for e in es); print(f"caso {sc}: {n} su 10 | {[e['dato'] for e in es]}", flush=True)
            if n < 9: fall = True; print(f"FALLITO caso {sc}: {n} su 10 (soglia 9)", flush=True)   # riga per tests/fallimenti_noti.txt: se il numero cambia, il giro lo dice
        print("errori:", errs[:1]); await b.close()
    print("ESITO", nome, "OK" if not (fall or errs) else "FALLITO"); sys.exit(1 if fall or errs else 0)
asyncio.run(main())
