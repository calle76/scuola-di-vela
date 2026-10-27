# Contatto senza colpa (0.21.1, osservazione 28): un contatto senza colpa del giocatore si scrive ma non conta negli errori
# (regTotal = ... + contactsPen), quindi non toglie la «pulita», la stella e il bonus +1; un contatto con colpa sì.
#
# COSA È GUIDATO E COSA È COSTRUITO (scritto prima dei risultati):
#  - COSTRUITO (parte A): in regata, prima del via, la barca del giocatore e un avversario vengono messe a mano a 3 m l'una
#    dall'altra, con le mure volute (colpa dell'avversario, colpa del giocatore, stesse mure con il giocatore sopravento e
#    sottovento). Un passo di simulazione fa scattare contacts(). Questo prova il CONTEGGIO, non la guida.
#  - GUIDATO (parte B): il giocatore (pilota sostituto __sv.pilota, come in collaudo_competizione.py) punta l'avversario più vicino
#    finché c'è un contatto, in una regata vera con avversari principianti; si riportano i casi ottenuti senza e con colpa.
#    Qui nulla è messo a mano: il numero di casi di ciascun tipo è quello che esce.
#  - Poi la regata costruita (A) prosegue col pilota fino all'arrivo, con gli ALTRI errori azzerati a ogni passo (il sostituto
#    fa strambate a vela aperta e non sarebbe mai pulito): è COSTRUITO anche questo, serve a vedere stella, «pulita» salvata e testo
#    del riepilogo davvero scritti dal gioco.
#  - Registratore: con la registrazione accesa, righe «contatto_senza_colpa» / «errore contactsPen»; e la simulazione è identica al bit
#    (posizioni di tutte le barche dopo 300 passi) con registrazione accesa e spenta.
# Un controllo con zero casi FALLISCE (metro di misura): i casi ottenuti sono stampati.
# Uso: python collaudo_contatto_senza_colpa.py [semi guidati, predefinito 30]
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
URL = BASE + "#collaudo"
NG = int(sys.argv[1]) if len(sys.argv) > 1 else 30
STORE = "scuolaVelaSim.v1"; CH = "r0.4"
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""

APRI = """([seme]) => { const sv = __sv; sv.fast(0); sv.openItem(["r", 0]); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = "principianti"; sel.dispatchEvent(new Event("change")); }"""

# tipo: "avv" colpa dell'avversario, "mia" colpa del giocatore, "sopra"/"sotto" stesse mure, giocatore sopravento/sottovento
COSTRUITO = """([tipo, finisci, seme]) => {
  __seed(seme);                                          // 0.21.1: seme rimesso qui, nello stesso evaluate dei passi: nessun frame del browser (2 Math.random ciascuno in draw) cade fra seme e inizio
  const sv = __sv, R = sv.R, me = R.boats[0], o = R.boats[1], D = Math.PI / 180, dt = 1 / 60;
  sv.run(dt, 60 * 5);                                    // qualche secondo di preparazione, avversari in moto
  const tw = sv.twd, S = me.S, O = o.S;
  const hDritta = (tw - 90 + 360) % 360, hSin = (tw + 90) % 360;   // mure a dritta (precedenza) / mure a sinistra
  const su = [Math.sin(tw * D), -Math.cos(tw * D)];                // verso il vento, in x y
  S.x = 0; S.y = 0; S.u = 2; S.vl = 0; S.r = 0; O.u = 2; O.vl = 0; O.r = 0;
  if (tipo === "avv"){ S.h = hDritta; O.h = hSin; O.x = 3; O.y = 0; }
  else if (tipo === "mia"){ S.h = hSin; O.h = hDritta; O.x = 3; O.y = 0; }
  else { S.h = hDritta; O.h = hDritta; const sg = tipo === "sopra" ? 1 : -1; O.x = -sg * 3 * su[0]; O.y = -sg * 3 * su[1]; }
  const c0 = sv.reg.contacts, p0 = sv.reg.contactsPen;
  sv.run(dt, 1);
  const r1 = Object.assign({}, sv.reg), toast = sv.toast;
  sv.run(dt, 120); sv.panel();
  const err = document.getElementById("stErr");
  const r2 = { contatti: r1.contacts - c0, pen: r1.contactsPen - p0, testo: err.textContent, rosso: err.classList.contains("some"),
               tot: r1.capsizes + r1.gybesV + r1.irons + r1.wrongMarks + r1.contactsPen + r1.ocs + r1.outLine };
  sv.run(dt, 300 - 121);                                  // posizione di tutte le barche al passo 300 dopo il contatto: impronta per il confronto registrazione sì/no
  const imp = R.boats.map(b => [b.S.x, b.S.y, b.S.h, b.S.u].map(v => v.toFixed(9)).join(",")).join(";");
  let fine = null;
  if (finisci){
    let n = 0;
    while (me.fin === null && R.t < 900){
      for (const k in sv.reg) if (k !== "contacts" && k !== "contactsPen") sv.reg[k] = 0;   // COSTRUITO: via gli altri errori del sostituto
      if (tipo === "avv") sv.reg.contactsPen = r1.contactsPen;   // 1.0.11: anche i contatti con colpa presi DOPO quello costruito sono «altri errori»
      sv.pilota(dt); sv.run(dt, 1); n++;                        // (con la barca nuova capitavano in 6 regate su 6; cambio deciso dopo aver visto il risultato)
    }
    for (const k in sv.reg) if (k !== "contacts" && k !== "contactsPen") sv.reg[k] = 0;
    if (tipo === "avv") sv.reg.contactsPen = r1.contactsPen;
    let k = 0; while (k < 60 * 400 && !R.boats.every(b => b.fin !== null)){ sv.run(dt, 1); k++; }   // il piazzamento si salva quando è definitivo
    const P = JSON.parse(localStorage.getItem("@S") || "{}");
    fine = { fin: me.fin, clean: !!(P.clean && P.clean["@C"]), race: (P.race || {})["@C:principianti"] || null,
             riepilogo: document.getElementById("rDoneText").textContent, reg: Object.assign({}, sv.reg) };
  }
  return { r2, imp, fine, toast, ses: sv.ses.lines.filter(l => /contatto_senza_colpa|errore contacts/.test(l)) };
}""".replace("@S", STORE).replace("@C", CH)

# guidato: punta l'avversario più vicino finché c'è un contatto; poi un po' di tempo perché il registro si fermi
GUIDATO = """([seme]) => {
  __seed(seme);                                          // idem: seme rimesso subito prima dei passi
  const sv = __sv, R = sv.R, me = R.boats[0], dt = 1 / 60; let n = 0;
  sv.pilota(dt);                                                    // prepara i campi del sostituto
  while (sv.reg.contacts === 0 && me.fin === null && R.t < 200 && n < 60 * 400){
    const near = R.boats.slice(1).sort((a, b) => Math.hypot(a.S.x - me.S.x, a.S.y - me.S.y) - Math.hypot(b.S.x - me.S.x, b.S.y - me.S.y))[0];
    const D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
    const brg = Math.atan2(near.S.x - me.S.x, -(near.S.y - me.S.y)) / D, rel = n180(brg - sv.twd);
    let want = brg; if (Math.abs(rel) < 45) want = sv.twd + Math.sign(rel || 1) * 50;
    if (me.S.capsized){ sv.pilota(dt); } else sv.ctl.tiller = Math.max(-1, Math.min(1, n180(me.S.h - want) / 20));
    if (!me.S.capsized) sv.ctl.sheet = sv.autoSheet();
    sv.run(dt, 1); n++;
  }
  sv.run(dt, 60); sv.panel();
  const r = sv.reg;
  return { contatti: r.contacts, pen: r.contactsPen, tot: r.capsizes + r.gybesV + r.irons + r.wrongMarks + r.contactsPen + r.ocs + r.outLine,
           extra: r.capsizes + r.gybesV + r.irons + r.wrongMarks + r.ocs + r.outLine, testo: document.getElementById("stErr").textContent,
           rosso: document.getElementById("stErr").classList.contains("some") };   // «some» = regTotal() > 0, calcolato dal gioco
}"""

fallite = []
def ok(nome, cond, det=""):
    print(("  ok  " if cond else "  NO  ") + nome + ("  " + det if det else ""), flush=True)
    if not cond: fallite.append(nome)

async def pagina(b, seme, rec):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650})
    pg = await ctx.new_page(); await pg.add_init_script(SEME)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(URL); await pg.wait_for_timeout(200)
    if rec:
        await pg.evaluate("() => { const c = document.getElementById('sesOn'); c.checked = true; c.dispatchEvent(new Event('change')); }")
    await pg.evaluate(APRI, [seme]); return ctx, pg, errs

async def costruito(b, tipo, seme, finisci, rec):
    ctx, pg, errs = await pagina(b, seme, rec)
    r = await pg.evaluate(COSTRUITO, [tipo, finisci, seme]); await ctx.close()
    if errs: ok(f"{tipo}: nessun errore nella pagina", False, errs[0])
    return r

async def main():
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        print("== A. COSTRUITO: barche messe a mano, un passo fa scattare contacts() ==", flush=True)
        esito = {}
        for tipo in ["avv", "mia", "sopra", "sotto"]:
            r = await costruito(b, tipo, 7, False, True); esito[tipo] = r
            x = r["r2"]; print(f"  {tipo}: contatti {x['contatti']} con penalità {x['pen']} | totale errori {x['tot']} | rosso {x['rosso']} | «{x['testo']}»", flush=True)
        a, m = esito["avv"]["r2"], esito["mia"]["r2"]
        ok("senza colpa: 1 contatto, 0 penalità, totale errori 0, riga non rossa", (a["contatti"], a["pen"], a["tot"], a["rosso"]) == (1, 0, 0, False))
        ok("senza colpa: il testo dice «senza colpa, non conta»", "1 contatto senza colpa, non conta" in a["testo"] and a["testo"].startswith("Errori: nessuno"), a["testo"])
        ok("con colpa: 1 contatto, 1 penalità, totale errori 1, riga rossa", (m["contatti"], m["pen"], m["tot"], m["rosso"]) == (1, 1, 1, True))
        ok("con colpa: il testo dice «con penalità» e non «non conta»", "con penalità" in m["testo"] and "non conta" not in m["testo"], m["testo"])
        s = [esito["sopra"]["r2"]["pen"], esito["sotto"]["r2"]["pen"]]
        ok("stesse mure: la colpa è di uno solo dei due (sopravento/sottovento)", sorted(s) == [0, 1] and all(esito[t]["r2"]["contatti"] == 1 for t in ("sopra", "sotto")), f"penalità giocatore sopravento {s[0]}, sottovento {s[1]}")
        sl = esito["avv"]["ses"]; ml = esito["mia"]["ses"]
        ok("registratore, senza colpa: riga contatto_senza_colpa +1 e nessun «errore contacts»", any("contatto_senza_colpa +1" in l for l in sl) and not any("errore contacts" in l for l in sl), "; ".join(sl))
        ok("registratore, con colpa: errore contactsPen +1 e nessun «errore contacts»", any("errore contactsPen +1" in l for l in ml) and not any("errore contacts " in l or "contatto_senza_colpa" in l for l in ml), "; ".join(ml))

        print("== A1. COSTRUITO, solo controllo di TESTO (non di guida): valori scritti a mano in sv.reg, sv.panel(), lettura di #stErr ==", flush=True)
        ctx, pg, errs = await pagina(b, 7, False)
        casi_t = [({"contacts": 2, "contactsPen": 0}, "Errori: nessuno (2 contatti senza colpa, non contano)", False),
                  ({"contacts": 3, "contactsPen": 1}, "Errori: 1 contatto con penalità · 2 contatti senza colpa, non contano", True),
                  ({"contacts": 3, "contactsPen": 3}, "Errori: 3 contatti con penalità", True),
                  ({"contacts": 1, "contactsPen": 1, "irons": 1, "ironsSec": 3}, None, True)]
        for vals, atteso, rosso in casi_t:
            r = await pg.evaluate("""(vals) => { const sv = __sv; for (const k in sv.reg) sv.reg[k] = 0; Object.assign(sv.reg, vals); sv.panel();
              const e = document.getElementById('stErr'); return { testo: e.textContent, rosso: e.classList.contains('some') }; }""", vals)
            if atteso: ok(f"testo {vals}", r["testo"] == atteso and r["rosso"] == rosso and (("senza colpa" not in r["testo"]) or vals["contacts"] > vals["contactsPen"]), f"«{r['testo']}» rossa {r['rosso']}")
            else: ok(f"testo {vals}: contiene «piantato» e «1 contatto con penalità»", "piantato" in r["testo"] and "1 contatto con penalità" in r["testo"] and r["rosso"] == rosso, f"«{r['testo']}» rossa {r['rosso']}")
        ok("testo: nessun errore nella pagina", not errs, str(errs)); await ctx.close()

        print("== registratore sola lettura: stessa impronta con registrazione accesa e spenta (2 tipi: avv, mia) ==", flush=True)
        for tipo in ["avv", "mia"]:
            on = (await costruito(b, tipo, 7, False, True))["imp"]; off = (await costruito(b, tipo, 7, False, False))["imp"]
            ok(f"{tipo}: posizioni di tutte le barche identiche al bit", on == off and len(on) > 50, on[:60])

        print("== A2. COSTRUITO: regata portata fino all'arrivo (altri errori azzerati), 6 semi per tipo ==", flush=True)
        for tipo in ["avv", "mia"]:
            pul = tot = 0; incoer = []
            for seme in range(1, 7):
                f = (await costruito(b, tipo, seme, True, False))["fine"]; g = f["reg"]
                if f["fin"] is None: incoer.append(f"seme {seme}: non arrivata"); continue
                tot += 1; attesa = g["contactsPen"] == 0                      # attesa letta dal registro, non da regTotal
                pul += attesa
                libero = g["contacts"] > g["contactsPen"]
                if (f["clean"], f["race"] and f["race"]["pulita"], "★ senza errori" in f["riepilogo"], "senza colpa, non cont" in f["riepilogo"]) != (attesa, attesa, attesa, libero):
                    incoer.append(f"seme {seme}: stella {f['clean']} salvato {f['race']} «{f['riepilogo']}» registro {g['contacts']}/{g['contactsPen']}")
                print(f"  {tipo} seme {seme}: contatti {g['contacts']} con penalità {g['contactsPen']} | stella {f['clean']} | «{f['riepilogo']}»", flush=True)
            print(f"  {tipo}: arrivate {tot} su 6, finite pulite (nessun contatto con penalità) {pul}", flush=True)
            ok(f"{tipo}: stella, pulita salvata e riepilogo coerenti col registro in ogni caso", tot > 0 and not incoer, "; ".join(incoer))
            if tipo == "avv": ok("avv: almeno una regata con stella nonostante il contatto senza colpa (metro di misura)", pul > 0, f"{pul} su {tot}")
            else: ok("mia: almeno una regata senza stella per il contatto con colpa (metro di misura)", tot - pul > 0, f"{tot - pul} su {tot}")

        print(f"== B. GUIDATO: il giocatore punta l'avversario, {NG} semi (1..{NG}), principianti, niente messo a mano ==", flush=True)
        senza = con = zero = 0; incoer = 0
        for seme in range(1, NG + 1):
            ctx, pg, errs = await pagina(b, seme, False)
            r = await pg.evaluate(GUIDATO, [seme]); await ctx.close()
            if r["contatti"] == 0: zero += 1; continue
            if r["pen"] == 0: senza += 1
            else: con += 1
            if r["rosso"] != (r["pen"] + r["extra"] > 0): incoer += 1
            print(f"  seme {seme}: contatti {r['contatti']} con penalità {r['pen']} totale errori {r['tot']} rossa {r['rosso']} | «{r['testo']}»", flush=True)
        print(f"  casi: senza colpa {senza}, con colpa {con}, nessun contatto {zero} (su {NG} semi)", flush=True)
        ok("guidato: almeno un contatto ottenuto (metro di misura)", senza + con > 0, f"{senza + con} su {NG}")
        ok("guidato: riga errori rossa se e solo se penalità + altri errori > 0 (regTotal calcolato dal gioco)", incoer == 0, f"{incoer} incoerenti su {senza + con}")
        print("  (senza colpa o con colpa guidati: riportati, nessuna soglia; i casi sono quelli che escono)", flush=True)
        await b.close()
    print(f"\n{'TUTTO OK' if not fallite else 'FALLITI: ' + ', '.join(fallite)}")
    sys.exit(1 if fallite else 0)

asyncio.run(main())
