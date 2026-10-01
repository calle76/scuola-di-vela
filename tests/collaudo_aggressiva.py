# Avversaria «aggressiva in partenza»: il giocatore si trova mure a sinistra davanti a lei, con la precedenza contro.
# Deve esistere sempre una manovra per evitarla. Il collaudo prova più manovre sullo STESSO incontro, salvando e
# rimettendo lo stato della regata, e chiede che almeno una eviti il contatto. Le manovre partono dopo un ritardo di
# reazione, contato da quando l'aggressiva comincia a puntare il giocatore.
# A passi fissi con __sv.run, quindi l'esito non dipende dal carico del computer (vedi COLLAUDI.md).
# Uso: python collaudo_aggressiva.py [incontri per distanza]
import asyncio, sys
from playwright.async_api import async_playwright
import pathlib
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
RIP = int(sys.argv[1]) if len(sys.argv) > 1 else 10
CONTATTO = 4.2   # metri: la distanza a cui il gioco conta un contatto
# manovre provate: nome, barra (negativa = poggia, positiva = orza con vento da sinistra), ritardo in secondi
MANOVRE = [("poggia subito", -0.6, 0), ("poggia dopo 1 s", -0.6, 1), ("orza dopo 1 s", 0.6, 1), ("non fa niente", 0, None)]

INCONTRO = """([spawn, manovre]) => {
  const D = Math.PI/180, R = __sv.R;
  const agg = R.boats.find(b => b.char === "aggressiva");
  if (!agg) return { err: "nessuna aggressiva in acqua" };
  const twa = h => ((__sv.twd - h + 540) % 360) - 180;              // >0: mure a dritta
  // si avanza fino a quando l'aggressiva risale alla linea mure a dritta, cioè con la precedenza in mano
  let k = 0;
  while (k < 60*500 && !(twa(agg.S.h) > 20 && R.t > -80)){ __sv.run(1/60, 1); k++; }
  if (!(twa(agg.S.h) > 20)) return { err: "l'aggressiva non è mai arrivata mure a dritta" };
  // il giocatore si ritrova davanti alla sua prua, mure a sinistra
  const ah = agg.S.h * D;
  __sv.S.x = agg.S.x + Math.sin(ah) * spawn; __sv.S.y = agg.S.y - Math.cos(ah) * spawn;
  __sv.S.h = (__sv.twd + 90) % 360; __sv.S.u = 2.2; __sv.S.vl = 0; __sv.S.r = 0; __sv.ctl.tiller = 0;
  const dist = () => Math.hypot(agg.S.x - __sv.S.x, agg.S.y - __sv.S.y);
  // L'incontro è in corso: lei mure a dritta prima del via, il giocatore mure a sinistra entro il raggio in cui lo
  // cerca (40 m) e nessun'altra barca mure a sinistra più vicina di lui. Il limite AGGRO_OFF NON entra qui: legare
  // l'inizio della manovra a quella soglia rendeva impossibile confrontare valori diversi, perché con una soglia
  // larga e un incontro ravvicinato la manovra non partiva mai e il giocatore restava fermo.
  const punta = () => {
    if (twa(agg.S.h) <= 0 || R.t >= 0 || twa(__sv.S.h) >= 0) return false;
    const d = dist(); if (d > 40) return false;
    for (const o of R.boats){
      if (o === agg || o.me || o.S.capsized) continue;
      if (twa(o.S.h) >= 0) continue;
      const od = Math.hypot(o.S.x - agg.S.x, o.S.y - agg.S.y);
      if (od <= 40 && od < d) return false;
    }
    return true;
  };
  // fotografia dello stato della regata, per riprovare lo stesso incontro con manovre diverse
  // (posizioni, comandi e contatori; restano fuori il tempo della simulazione e le scie, che non toccano i contatti)
  const CAMPI = ["leg","ocs","pen","fin","prevWY","side","boardT","boardMax","rp","rnd","rndA","preDesired"];
  const foto = () => ({ t: R.t, phase: R.phase, contacts: {...R.contacts}, signals: [...R.signals], reg: {...__sv.reg},
    boats: R.boats.map(b => ({ S: {...b.S}, ctl: {...b.ctl}, altro: Object.fromEntries(CAMPI.map(c => [c, b[c]])) })) });
  const rimetti = f => {
    R.t = f.t; R.phase = f.phase; R.contacts = {...f.contacts}; R.signals = new Set(f.signals);
    Object.assign(__sv.reg, f.reg);
    R.boats.forEach((b, i) => { const s = f.boats[i];
      Object.assign(b.S, s.S); Object.assign(b.ctl, s.ctl); Object.assign(b, s.altro); });
  };
  const inizio = foto();
  const esiti = [];
  for (const [nome, barra, ritardo] of manovre){
    rimetti(inizio);
    const d0 = dist(), con0 = __sv.reg.contacts, pen0 = __sv.reg.contactsPen;
    let dmin = d0, t0 = null, dPunta = null, dVia = null;
    for (let i = 0; i < 60*40; i++){
      const d = dist(); dmin = Math.min(dmin, d);
      if (t0 === null && punta()){ t0 = i; dPunta = d; }
      const pronto = ritardo !== null && t0 !== null && (i - t0) >= ritardo*60;
      if (pronto){ if (dVia === null) dVia = d; __sv.ctl.tiller = barra; } else __sv.ctl.tiller = 0;
      __sv.run(1/60, 1);
      if (R.t > 20) break;                                          // passato il via l'incontro è chiuso
    }
    // contatto con l'aggressiva: la distanza minima è scesa alla soglia del gioco. Gli altri contatti si contano a parte,
    // perché una manovra può portare il giocatore addosso a una terza barca, e quello è un esito diverso.
    const urtata = dmin <= %CONT%;
    esiti.push({ nome, d0: +d0.toFixed(1), dmin: +dmin.toFixed(1), contatto: urtata,
                 altri: __sv.reg.contacts - con0 - (urtata ? 1 : 0),
                 miaPenalita: __sv.reg.contactsPen - pen0, puntato: t0 !== null,
                 dPunta: dPunta === null ? null : +dPunta.toFixed(1), dVia: dVia === null ? null : +dVia.toFixed(1) });
  }
  return { nome: agg.name, esiti };
}""".replace("%CONT%", str(CONTATTO))

async def incontro(b, spawn, foto=None):
    pg = await b.new_page(viewport={"width":1280,"height":800})
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(URL); await pg.wait_for_timeout(300)
    await pg.click("[data-r='0']"); await pg.wait_for_timeout(150)
    await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#aiLevel", "esperti"]); await pg.wait_for_timeout(150)
    await pg.evaluate("a=>{const e=document.querySelector(a[0]);e.value=a[1];e.dispatchEvent(new Event('change'))}", ["#cdSel", "180"]); await pg.wait_for_timeout(200)
    r = await pg.evaluate(INCONTRO, [spawn, [[n, t, rr] for n, t, rr in MANOVRE]])
    if foto: await pg.screenshot(path=str(OUT / foto))
    await pg.close()
    return r, errs

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for spawn in [18, 24, 30, 38]:
            print(f"--- il giocatore compare a {spawn} m dalla prua dell'aggressiva, mure a sinistra ---", flush=True)
            cont = {n: 0 for n, _, _ in MANOVRE}; dmins = {n: [] for n, _, _ in MANOVRE}; altri = {n: 0 for n, _, _ in MANOVRE}
            salvati = 0; saltati = 0; err = []
            for i in range(RIP):
                r, errs = await incontro(b, spawn, f"aggressiva_{spawn}.png" if i == 0 else None); err += errs[:1]
                if r.get("err"): saltati += 1; print(f"  {i+1}: {r['err']}", flush=True); continue
                for e in r["esiti"]:
                    if e["contatto"]: cont[e["nome"]] += 1
                    altri[e["nome"]] += e["altri"]
                    dmins[e["nome"]].append(e["dmin"])
                scampate = [e["nome"] for e in r["esiti"] if not e["contatto"] and e["nome"] != "non fa niente"]
                if scampate: salvati += 1
                p0 = r["esiti"][0]
                print(f"  {i+1}: {r['nome']} | puntato a {p0['dPunta']} m | " +
                      " | ".join(f"{e['nome']}: min {e['dmin']} m{' CONTATTO' if e['contatto'] else ''}{' (+%d con altre)' % e['altri'] if e['altri'] else ''}" for e in r["esiti"]) +
                      f" | manovre che evitano: {', '.join(scampate) if scampate else 'NESSUNA'}", flush=True)
            fatti = RIP - saltati
            print(f"{spawn} m: incontri {fatti} (saltati {saltati}); con almeno una manovra che evita il contatto {salvati} su {fatti};" +
                  "".join(f" [{n}: contatti con l'aggressiva {cont[n]}/{fatti}, con altre {altri[n]}, distanza minima {min(dmins[n]) if dmins[n] else '—'} m]" for n, _, _ in MANOVRE) +
                  f"; errori {err[:1]}", flush=True)
        await b.close()
asyncio.run(main())
