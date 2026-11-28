# Voce 98 (docs/PROPOSTA-REGOLA-17.md, oss. 154): un rivale che supera il giocatore da sottovento con le stesse mure, al lasco, nella regata nei salti (Deriva) senza salti.
# La barca del giocatore non è guidata: tiene una prua fissa (convergente di «conv» gradi verso il rivale) e la scotta fissa, come chi non si scansa.
# Il rivale punta l'arrivo (ultimo lato) con la boa messa in modo che la sua rotta sia a 106° dal vento, come la Blu della regata di Lucio del 28/11 00:05.
# Vento 10 nodi (quello della regata: i collaudi non possono cambiarlo; la proposta diceva 8/12/16, semplificazione dichiarata).
# Due scene, 20 varianti ciascuna con semi fissi (VARIANTI=0-19; 20-39 per la conferma, mai guardate prima della prova):
#  dietro     (la scena della proposta): il rivale parte 8 m dietro e 6-14 m sottovento, il giocatore va al 90-97% della velocità del rivale, convergenza 0-5°
#  affiancata (aggiunta dopo il passo A, dichiarata): già affiancati, il giocatore da 2 m dietro a 2 m avanti e 3-6 m sopravento, il giocatore va al 99-101% della velocità del rivale (uguali ±1%; con 97-100% il rivale passava davanti e i contatti venivano solo sopra il 99,6%), convergenza 1-5°
# La velocità del giocatore è legata a quella del rivale a ogni passo (dichiarato, 28 nov): con la scotta fissa la scena dipendeva dalla velocità del rivale sorteggiato
# (stessi semi: 4 contatti su 20 in Chromium, 0 in Firefox, rivali diversi). Il seme si fissa anche prima di aprire la regata, che sorteggia i rivali.
# Si conta in quante varianti c'è un contatto fra il giocatore e il rivale entro 90 s. Criterio 1 della proposta: con la correzione al massimo 2 su 20 e almeno il 50% in meno del gioco di oggi.
# Gioco di prima: RADICE=cartella (copia del gioco). SOGLIA=n: contatti ammessi (predefinito 2). SCENE=dietro,affiancata.
import asyncio, os, pathlib, sys
from playwright.async_api import async_playwright
RADICE = pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent)
URL = (RADICE / "index.html").as_uri() + "#collaudo"
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
SCENA = """([sc, v]) => { const sv = __sv; sv.fast(0); __seed(9800 + (sc === "dietro" ? 0 : 500) + v); sv.openItem(["r", 2]); __seed(9800 + (sc === "dietro" ? 0 : 500) + v); /* seme anche prima dell'apertura: il carattere dei rivali si sorteggia lì (prima Chromium e Firefox avevano rivali diversi) */ sv.setShifts(null); sv.simTime = 0;
  const R = sv.R, D = Math.PI / 180, me = R.boats[0], av = R.boats.filter(b => !b.me), twd = sv.windAt(0, 0).twd, dt = 1 / 60, rnd = Math.random;
  const n1 = a => ((a + 540) % 360) - 180, fwd = h => [Math.sin(h * D), -Math.cos(h * D)], stb = h => [Math.cos(h * D), Math.sin(h * D)];
  const [A, C, E] = av; R.t = 120; R.phase = "race";
  const put = (b, p, h, u, leg) => { Object.assign(b.S, { x: p.x, y: p.y, h: (h + 360) % 360, u, r: 0, heel: 0, capsized: false });
    Object.assign(b, { leg, ocs: false, goStart: true, fin: null, dnf: false, rnd: 0, side: Math.sign(n1(twd - h)), boardT: 0, boardMax: 999, virando: false }); if (b.ctl){ b.ctl.sheet = 0.5; b.ctl.tiller = 0; } };
  const dietro = sc === "dietro", lat = dietro ? 6 + 8 * rnd() : 3 + 3 * rnd(), avanti = dietro ? 8 : -2 + 4 * rnd(), conv = dietro ? 5 * rnd() : 1 + 4 * rnd(), fu = dietro ? 0.90 + 0.07 * rnd() : 0.99 + 0.02 * rnd(), scM = 0.6;
  const leg = R.marks.length + 1, [fx, fy] = sv.fromWF(A.startX * 0.8, 0), hA = twd - 106, hM = hA - conv;
  const pA = { x: fx - fwd(hA)[0] * 400, y: fy - fwd(hA)[1] * 400 }, pM = { x: pA.x + fwd(hA)[0] * avanti + stb(hA)[0] * lat, y: pA.y + fwd(hA)[1] * avanti + stb(hA)[1] * lat };
  put(A, pA, hA, 8.5 / 1.944, leg); put(me, pM, hM, 8.2 / 1.944, leg);
  put(C, { x: fx + 600, y: fy + 600 }, twd - 50, 0, 1); put(E, { x: fx - 600, y: fy + 600 }, twd - 50, 0, 1);
  sv.ctl.tiller = 0; sv.ctl.sheet = scM; R.contLog = [];
  const iA = R.boats.indexOf(A); let cont = null, minLat = 1e9, cede = 0;
  for (let n = 0; n * dt < 90 && !cont; n++){ me.S.h = (hM + 360) % 360; me.S.r = 0; me.S.u = A.S.u * fu; sv.run(dt, 1);
    const c = R.contLog.find(x => (x.i === 0 && x.j === iA) || (x.i === iA && x.j === 0)); if (c) cont = { t: +(n * dt).toFixed(1), r: c.r, colpa: c.g === 0 ? "Tu" : A.name };
    if (A.cedeA === me) cede += dt; const rx = me.S.x - A.S.x, ry = me.S.y - A.S.y, s = stb(A.S.h); minLat = Math.min(minLat, rx * s[0] + ry * s[1]); }
  return { cont, lat: +lat.toFixed(1), conv: +conv.toFixed(1), fu: +fu.toFixed(3), minLat: +minLat.toFixed(1), cede: +cede.toFixed(1), car: (A.char || "") + " " + (A.ai && A.ai.up) }; }"""
async def main():
    nome = os.environ.get("BROWSER", "chromium"); fall = False
    a, z = (int(x) for x in os.environ.get("VARIANTI", "0-19").split("-")); soglia = int(os.environ.get("SOGLIA", "2"))
    async with async_playwright() as p:
        b = await getattr(p, nome).launch(); errs = []
        for sc in os.environ.get("SCENE", "dietro,affiancata").split(","):
            es = []
            for v in range(a, z + 1):
                pg = await b.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); await pg.add_init_script(SEME); await pg.goto(URL); await pg.wait_for_timeout(150)
                es.append(await pg.evaluate(SCENA, [sc, v])); await pg.close()
            n = sum(1 for e in es if e["cont"])
            for v, e in zip(range(a, z + 1), es): print(f"  {sc} {v}: {e}", flush=True)
            print(f"scena {sc}: contatti {n} su {len(es)} (soglia {soglia})", flush=True)
            if n > soglia: fall = True; print(f"FALLITO scena {sc}: {n} contatti su {len(es)}", flush=True)
        print("errori:", errs[:1]); await b.close()
    print("ESITO", nome, "OK" if not (fall or errs) else "FALLITO"); sys.exit(1 if fall or errs else 0)
asyncio.run(main())
