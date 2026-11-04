# Collaudo dei suoni (1.2.5, docs/PROPOSTA-SUONI.md §5: criteri S1-S6 scritti prima del codice).
# I computer dei collaudi non hanno casse: si leggono il registro degli eventi suonati (__sv.suoni.reg) e i volumi calcolati (__sv.suoni.val),
# chiamando __sv.suoni.agg a ogni passo come fa il ciclo del gioco a ogni fotogramma.
#   S1: la simulazione non cambia: la stessa regata a seme fisso con e senza la lettura dei suoni dà gli stessi arrivi e la stessa barca, al bit.
#       (Il confronto con la 1.2.4 lo fa arrivi_regate.py, lanciato a parte.)
#   S2: un suono per ogni evento, entro 0,1 s: virate, strambate, contatti, boe toccate, arrivi visti dal collaudo stesso a ogni passo; segnali di partenza
#       agli istanti della regola 26 (5, 3 e 1 minuto); la X con un suono solo se qualcuno è in anticipo; scuffia, raddrizzata, passo, prova; controprova a barca ferma.
#   S3: i volumi seguono i numeri: vento col vento apparente, acqua con la velocità, vela solo quando sbatte.
#   S4: costo per fotogramma (con l'audio acceso, dove il browser lo accende) al più +10%.
#   S5: nessun audio prima del primo tasto; «spenti» spegne e resta dopo il ricaricamento; un browser senza audio gioca muto, senza errori.
#   S6: impostazioni a 1360x650 dentro la finestra, senza scorrere.
# Dalla 1.2.7 (docs/PROPOSTA-SUONI-REGISTRATI.md §4) anche acqua e vela registrate:
#   R2: giro d'acqua più veloce e più chiaro con la barca veloce; colpi di vela in 60 s crescenti col vento apparente (4, 8, 12, 16 nodi) ed entro il 20%
#       degli attesi (1 + 0,35 × nodi al secondo); controprova: nessun colpo con la vela regolata, a barca scuffiata, in pausa.
#   R3: suoni «registrati» nella pagina con e senza #collaudo; col decodificatore rotto apposta restano i sintetici, senza errori.
#   R4: js/suoni-dati.js al massimo 300 KB; decodifica al primo tasto al massimo 300 ms. (R1 = S1; R6 = S1-S6 verdi.)
# Dalla 1.2.9 (docs/PROPOSTA-SUONI-FINE.md §4) anche vento, sciabordio, sartiame, gorgoglio, gabbiani, scricchiolii:
#   G2: ogni lettura uguale alla formula; sartiame solo sopra i 12 nodi; gorgoglio solo in stallo vero, con la barca guidata; scricchiolii e gabbiani entro il 25% e il 20% degli attesi, 10 finestre.
#   G3: tutto decodificato con e senza #collaudo; seconda decodifica rotta apposta: acqua e colpi registrati, vento sintetico, nessun errore.
#   G4: seconda decodifica al più 1.500 ms; js/suoni-dati.js al più 700 KB (R4 diceva 300, con due suoni soli: cambiata prima di costruire il file, detto nella proposta).
#   G5: acqua e colpi identici a quelli della 1.2.8. (G1 = S1; che si sentano davvero lo misura collaudo_suoni_si_sentono.py.)
# Uso: python collaudo_suoni.py [--semi 1-10]   (BROWSER=firefox per Firefox)
import asyncio, hashlib, json, os, pathlib, re, sys
import metro   # controlli che cadono anche a zero casi (docs/PROPOSTA-TEST-DEI-TEST.md)
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]; BASE = (ROOT / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# una regata guidata dal pilota fino all'arrivo di tutti; il collaudo annota da sé gli eventi a ogni passo (oss) e legge il registro dei suoni
REGATA = """([race, seme, cd, liv, suoni, anticipo]) => {
  const sv = __sv, dt = 1 / 60; sv.fast(0); sv.opt.countdown = cd; sv.opt.aiLevel = liv; __seed(seme); sv.simTime = 0; sv.openItem(["r", race]);
  const R = sv.R, me = R.boats[0], oss = [], reg0 = sv.suoni.reg.length;
  let p = null, xVisto = false;
  const leggi = () => ({ v: sv.S.tacks, g: (sv.S.gybesV || 0) + (sv.S.gybesC || 0), c: Object.assign({}, R.contacts), b: R.nBoa || 0, f: R.boats.map(o => o.fin !== null) });
  if (suoni) sv.suoni.agg(dt, false);
  for (let k = 0; k < 60 * 1300 && !R.boats.every(o => o.fin !== null || o.dnf); k++){
    if (anticipo && R.t >= -1 && R.t < 0){ const [x, y] = fromWF(0, -4); sv.S.x = x; sv.S.y = y; }   // apposta oltre la linea un secondo prima del via
    if (me.fin === null && !me.dnf) sv.pilota(dt);
    sv.run(dt, 1); if (suoni) sv.suoni.agg(dt, false);
    if (R.segnali && bandiereR().X) xVisto = true;
    const n = leggi(), t = +R.t.toFixed(3);
    if (p){ if (n.v > p.v) oss.push([t, "virata"]); if (n.g > p.g) oss.push([t, "strambata"]); for (const key in n.c) if (n.c[key] !== p.c[key]) oss.push([t, "contatto"]);
      if (n.b > p.b) oss.push([t, "boa"]); n.f.forEach((f, i) => { if (f && !p.f[i]) oss.push([t, "arrivo"]); }); }
    p = n;
  }
  const S = sv.S;
  return { oss, reg: sv.suoni.reg.slice(reg0).map(r => [r[2], r[1]]), fin: R.boats.map(o => o.fin), stato: [S.x, S.y, S.h, S.u, S.heel], ocs0: xVisto };   // la X vista salire durante la regata (alla fine la lista è già vuota)
}"""
bad = []; casi = {}
def chk(parte, ok, m):
    casi[parte] = casi.get(parte, 0) + 1
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
def coppie(oss, reg, nomi):
    """stessi eventi, ognuno con il suo suono entro 0,1 s (in ordine di tempo, per nome)"""
    for nome in nomi:
        a = sorted(t for t, n in oss if n == nome); b = sorted(t for t, n in reg if n == nome)
        if len(a) != len(b) or any(abs(x - y) > 0.1 for x, y in zip(a, b)): return False, nome, len(a), len(b)
    return True, None, None, None
TROMBE = {300: [(-300, "tromba"), (-240, "tromba"), (-60, "tromba_lunga"), (0, "tromba")], 180: [(-180, "tromba"), (-120, "tromba"), (-60, "tromba_lunga"), (0, "tromba")], 60: [(-60, "tromba"), (0, "tromba")]}
async def pagina(b, hash_="#collaudo", init=None):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
    if init: await ctx.add_init_script(init)
    if hash_: await ctx.add_init_script("window.requestAnimationFrame = () => 0;")
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE + hash_); await pg.wait_for_timeout(400)
    return ctx, pg, errs
async def attendi(pg, cond, s=10):   # aspetta al più s secondi; se non succede, il controllo dopo lo dice (con lo stato letto), senza fermare il collaudo
    for _ in range(s * 10):
        if await pg.evaluate(cond): return
        await pg.wait_for_timeout(100)
AMB_FINITA = "() => suoniFonte.startsWith('errore') || sAmbFonte === 'registrati' || sAmbFonte.startsWith('errore')"
async def main():
    a = sys.argv[1:]; x, y = (a[a.index("--semi") + 1] if "--semi" in a else "1-10").split("-"); semi = list(range(int(x), int(y) + 1))
    BR = os.environ.get("BROWSER", "chromium")
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        ctx, pg, errs = await pagina(b)
        # ---- S1 ----
        r1 = await pg.evaluate(REGATA, [0, 5, 180, "principianti", True, False]); r0 = await pg.evaluate(REGATA, [0, 5, 180, "principianti", False, False])
        chk("S1", r1["fin"] == r0["fin"] and r1["stato"] == r0["stato"] and len(r1["reg"]) > 10, f"S1 regata a bastone seme 5 con e senza i suoni: arrivi {r1['fin']} e {r0['fin']}, suoni registrati {len(r1['reg'])}")
        # ---- S2: regate ----
        tot = {}
        for cd, ss in ((180, semi), (300, semi[:3]), (60, semi[:3])):
            for s in ss:
                r = await pg.evaluate(REGATA, [3, s, cd, "principianti", True, False])
                ok, nome, na, nb = coppie(r["oss"], r["reg"], ["virata", "strambata", "contatto", "boa", "arrivo"])
                for t, n in r["oss"]: tot[n] = tot.get(n, 0) + 1
                tr = sorted((round(t, 1), n) for t, n in r["reg"] if n.startswith("tromba"))
                att = TROMBE[cd] + ([(0, "tromba")] if r["ocs0"] else [])   # con un anticipo al via sale la X: un suono in più allo zero
                ok_t = len(tr) == len(att) and all(abs(t - te) <= 0.1 and n == ne for (t, n), (te, ne) in zip(tr, sorted(att)))
                chk("S2", ok, f"S2 regata dei giri, {cd} s, seme {s}: un suono per evento" + ("" if ok else f" — {nome}: eventi {na}, suoni {nb}"))
                chk("S2", ok_t, f"S2 regata dei giri, {cd} s, seme {s}: trombe {tr}" + (" (con la X)" if r["ocs0"] else ""))
        print("eventi visti nelle regate:", tot)
        chk("S2", metro.tutti(tot.get(n, 0) > 0 for n in ("virata", "strambata", "contatto", "arrivo")), f"S2 il collaudo ha visto davvero virate, strambate, contatti e arrivi: {tot}")
        # X: da soli, apposta oltre la linea un secondo prima del via; controprova: stessa partenza senza anticipo
        rx = await pg.evaluate(REGATA, [3, 1, 60, "nessuno", True, True]); rn = await pg.evaluate(REGATA, [3, 1, 60, "nessuno", True, False])
        zx = [n for t, n in rx["reg"] if t is not None and abs(t) <= 0.1 and n == "tromba"]; zn = [n for t, n in rn["reg"] if t is not None and abs(t) <= 0.1 and n == "tromba"]
        chk("S2", rx["ocs0"] and len(zx) == 2 and not rn["ocs0"] and len(zn) == 1, f"S2 X: in anticipo due trombe allo zero (via e X): {len(zx)}; senza anticipo una: {len(zn)}")
        # boa toccata: esercizio della lezione «Boe e giri di penalità», si punta la boa finché non la si tocca
        rb = await pg.evaluate("""() => { const sv = __sv, dt = 1 / 60, n180 = a => ((a % 360) + 540) % 360 - 180; __seed(3); sv.openItem(["l", 17]);
            const si = LESSONS[17].steps.findIndex(s => s.esercizio); for (let k = 0; k < si; k++) document.getElementById("lNext").click(); document.getElementById("lEs").click();
            const R = sv.R, r0 = sv.suoni.reg.length; sv.suoni.agg(dt, false);
            for (let k = 0; k < 60 * 60 && !(R.nBoa >= 1); k++){ const S = sv.S, want = Math.atan2(R.mark.x - S.x, -(R.mark.y - S.y)) * 180 / Math.PI;
              sv.ctl.tiller = Math.max(-1, Math.min(1, n180(S.h - want) / 20)); sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); sv.suoni.agg(dt, false); }
            for (let k = 0; k < 30; k++){ sv.run(dt, 1); sv.suoni.agg(dt, false); }
            return { nBoa: R.nBoa || 0, boa: sv.suoni.reg.slice(r0).filter(r => r[1] === "boa").length }; }""")
        chk("S2", rb["nBoa"] == 1 and rb["boa"] == 1, f"S2 boa toccata una volta: suoni «boa» {rb['boa']}")
        # scuffia e raddrizzata: navigazione libera con vento forte e vela cazzata al traverso, poi A (rightBoat)
        rs = await pg.evaluate("""() => { const sv = __sv, dt = 1 / 60; __seed(2); sv.openItem("free"); env.tws = 22 / KN; env.twd = 0; freshState(0, 0, 90, 0); sv.suoni.agg(dt, false);
            const r0 = sv.suoni.reg.length, c0 = sv.S.capsizes || 0; let k = 0;
            for (; k < 60 * 60 && !sv.S.capsized; k++){ sv.ctl.sheet = 0; sv.ctl.tiller = 0; sv.run(dt, 1); sv.suoni.agg(dt, false); }
            const scuf = sv.S.capsized; rightBoat(); for (let j = 0; j < 60 * 20 && sv.S.capsized; j++){ sv.run(dt, 1); sv.suoni.agg(dt, false); }
            const reg = sv.suoni.reg.slice(r0).map(r => r[1]);
            return { scuf, dritta: !sv.S.capsized, scuffie: (sv.S.capsizes || 0) - c0, nScuf: reg.filter(n => n === "scuffia").length, nRadd: reg.filter(n => n === "raddrizzata").length }; }""")
        chk("S2", rs["scuf"] and rs["dritta"] and rs["nScuf"] == rs["scuffie"] == 1 and rs["nRadd"] == 1, f"S2 scuffia e raddrizzata: {rs}")
        # passo e prova: il completamento di un passo pratico e la fine di una prova (stato messo dal collaudo: qui si prova solo il collegamento)
        rp = await pg.evaluate("""() => { const sv = __sv, dt = 1 / 60; sv.openItem(["l", 1]); const i = LESSONS[1].steps.findIndex(s => s.cond); sv.showStep(i); sv.suoni.agg(dt, false); sv.suoni.agg(dt, false);
            const r0 = sv.suoni.reg.length; sv.completeStep(); sv.suoni.agg(dt, false); sv.suoni.agg(dt, false); const passo = sv.suoni.reg.slice(r0).map(r => r[1]);
            sv.startMission(0, 0); sv.suoni.agg(dt, false); const r1 = sv.suoni.reg.length; sv.S.finished = true; sv.suoni.agg(dt, false); sv.suoni.agg(dt, false);
            return { passo, prova: sv.suoni.reg.slice(r1).map(r => r[1]) }; }""")
        chk("S2", rp["passo"] == ["passo"] and rp["prova"] == ["prova"], f"S2 passo completato e prova finita: {rp}")
        # controprova: barca ferma, vela lascata, un minuto: nessun evento
        rq = await pg.evaluate("""() => { const sv = __sv, dt = 1 / 60; sv.openItem("free"); env.tws = 6 / KN; env.twd = 0; freshState(0, 0, 90, 1); sv.suoni.agg(dt, false); const r0 = sv.suoni.reg.length;
            for (let k = 0; k < 3600; k++){ sv.ctl.sheet = 1; sv.ctl.tiller = 0; sv.run(dt, 1); sv.suoni.agg(dt, false); } return sv.suoni.reg.slice(r0).map(r => r[1]); }""")
        chk("S2", rq == [], f"S2 controprova: barca ferma per un minuto, suoni {rq}")
        # ---- S3 ----
        r3 = await pg.evaluate("""() => { const sv = __sv, dt = 1 / 60, v = [], a = [], vela = {};
            for (let kn = 0; kn <= 20; kn += 2){ sv.openItem("free"); env.tws = kn / KN; env.twd = 0; freshState(0, 0, 90, 0.4);
              for (let k = 0; k < 120; k++){ sv.ctl.sheet = sv.autoSheet(); sv.ctl.tiller = 0; sv.run(dt, 1); sv.suoni.agg(dt, false); v.push([info.aws, sv.suoni.val.vento]); a.push([Math.abs(sv.S.u), sv.suoni.val.acqua]); } }
            for (const [nome, h, sh] of [["regolata", 90, null], ["prua al vento", 0, 1], ["troppo lascata", 60, 1]]){ sv.openItem("free"); env.tws = 10 / KN; env.twd = 0; freshState(0, 0, h, 0.4); let m = 0;
              for (let k = 0; k < 180; k++){ sv.ctl.sheet = sh === null ? sv.autoSheet() : sh; sv.ctl.tiller = 0; sv.run(dt, 1); sv.suoni.agg(dt, false); if (k > 30) m = Math.max(m, sv.suoni.val.vela); } vela[nome] = m; }
            return { v, a, vela }; }""")
        mono = lambda xs: all(y2 >= y1 - 1e-9 for (x1, y1), (x2, y2) in zip(sorted(xs), sorted(xs)[1:]))
        chk("S3", len(r3["v"]) > 1000 and mono(r3["v"]) and max(y for _, y in r3["v"]) > 2 * min(y for _, y in r3["v"]), f"S3 vento: cresce sempre col vento apparente ({len(r3['v'])} letture, da {min(y for _, y in r3['v']):.2f} a {max(y for _, y in r3['v']):.2f})")
        chk("S3", mono(r3["a"]) and max(y for _, y in r3["a"]) > 2 * min(y for _, y in r3["a"]), f"S3 acqua: cresce sempre con la velocità (da {min(y for _, y in r3['a']):.2f} a {max(y for _, y in r3['a']):.2f})")
        chk("S3", r3["vela"]["regolata"] == 0 and r3["vela"]["prua al vento"] > 0.1 and r3["vela"]["troppo lascata"] > 0.1, f"S3 vela: {r3['vela']}")
        chk("S5", not errs, f"S1-S3 errori della pagina {errs[:1]}"); await ctx.close()
        # ---- S4: costo. 2 nov 2026, dopo il primo giro (detto): fotogrammi con e senza alternati davano +23,5% solo per rumore (60 fotogrammi da 573 a 1176 ms
        # da soli), quindi si misurano a parte la lettura dei suoni (10.000 volte) e il fotogramma (mediana di 8 giri da 60). L'audio si accende con un clic.
        ctx, pg, errs = await pagina(b); await pg.click("#goFree"); await pg.keyboard.press("Enter"); await attendi(pg, AMB_FINITA)   # 1.2.9: il costo si misura con tutti i suoni accesi
        r4 = await pg.evaluate("""() => { const sv = __sv, dt = 1 / 60; let t0 = performance.now(); for (let k = 0; k < 10000; k++) sv.suoni.agg(dt, false); const agg = (performance.now() - t0) / 10000;
            const tf = []; for (let g = 0; g < 8; g++){ const t1 = performance.now(); for (let k = 0; k < 60; k++) sv.frame(dt); tf.push((performance.now() - t1) / 60); }
            return { agg, frame: tf.sort((x, y) => x - y)[4], attivi: sv.suoni.attivi }; }""")
        rap = r4["agg"] / r4["frame"]
        chk("S4", rap <= 0.10, f"S4 costo: lettura dei suoni {r4['agg'] * 1000:.1f} µs contro {r4['frame']:.1f} ms di un fotogramma (+{rap * 100:.2f}%), audio acceso: {r4['attivi']}")
        await ctx.close()
        # ---- S5 e S6: pagina come la carica un giocatore ----
        ctx, pg, errs = await pagina(b, "")
        prima = await pg.evaluate("() => [!!actx, suoniLiv, document.getElementById('suoniSel').value]")
        await pg.click("#goFree"); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(500)
        dopo = await pg.evaluate("() => [!!actx, actx && actx.state]")
        await pg.evaluate("() => document.getElementById('setDlg').showModal()"); await pg.wait_for_timeout(150)
        D6 = "() => { const d = document.getElementById('setDlg'), r = d.getBoundingClientRect(); return [r.top, r.bottom, innerHeight, d.scrollHeight - d.clientHeight]; }"
        d6 = await pg.evaluate(D6)
        # 1.2.6: anche il caso peggiore, registrazione accesa (riga della nota) con la riga dei marcatori: lì la 1.2.5 scorreva di 21 px (collaudo_registratore)
        await pg.click("#sesOn"); await pg.evaluate("() => { const m = document.getElementById('sesMarks'); m.hidden = false; m.textContent = m.textContent || 'Momenti segnati: 2'; }")
        d6p = await pg.evaluate(D6); await pg.click("#sesOn"); await pg.evaluate("() => { document.getElementById('sesMarks').hidden = true; }")
        await pg.select_option("#suoniSel", "spento"); await pg.wait_for_timeout(100)
        spento = await pg.evaluate("() => [suoniLiv, localStorage.getItem('scuolaVelaSuoni'), suoniAttivi()]")
        await pg.reload(); await pg.wait_for_timeout(400); await pg.keyboard.press("Shift"); await pg.wait_for_timeout(200)
        ric = await pg.evaluate("() => [suoniLiv, document.getElementById('suoniSel').value, !!actx]")
        chk("S5", prima == [False, "basso", "basso"] and dopo[0], f"S5 all'inizio «bassi» e nessun audio; dopo il primo tasto l'audio esiste ({dopo[1]})")
        chk("S5", spento == ["spento", "spento", False] and ric == ["spento", "spento", False], f"S5 «spenti»: {spento}; dopo il ricaricamento {ric}")
        chk("S6", d6[0] >= 0 and d6[1] <= d6[2] and d6[3] <= 0, f"S6 impostazioni dentro la finestra: da {d6[0]:.0f} a {d6[1]:.0f} su {d6[2]}, scorre di {d6[3]} px")
        chk("S6", d6p[0] >= 0 and d6p[1] <= d6p[2] and d6p[3] <= 0, f"S6 caso peggiore (registrazione accesa e marcatori): da {d6p[0]:.0f} a {d6p[1]:.0f} su {d6p[2]}, scorre di {d6p[3]} px")
        chk("S5", not errs, f"S5-S6 errori della pagina {errs[:1]}"); await ctx.close()
        ctx, pg, errs = await pagina(b, "", "delete window.AudioContext; delete window.webkitAudioContext;")
        await pg.click("#goFree"); await pg.keyboard.press("Enter"); await pg.keyboard.down("ArrowLeft"); await pg.wait_for_timeout(1500); await pg.keyboard.up("ArrowLeft")
        mut = await pg.evaluate("() => [!!actx, typeof S.u === 'number' && simTime > 0.5]")
        chk("S5", mut == [False, True] and not errs, f"S5 browser senza audio: si gioca muti, senza errori ({mut}, {errs[:1]})")
        await ctx.close()
        # ---- R2-R4 (1.2.7, docs/PROPOSTA-SUONI-REGISTRATI.md §4, criteri scritti prima del codice): acqua e vela registrate ----
        ctx, pg, errs = await pagina(b)
        r2 = await pg.evaluate("""() => { const sv = __sv, dt = 1 / 60, a = [], colpi = {}, attesi = {};
            for (let kn = 0; kn <= 20; kn += 2){ sv.openItem("free"); env.tws = kn / KN; env.twd = 0; freshState(0, 0, 90, 0.4);
              for (let k = 0; k < 120; k++){ sv.ctl.sheet = sv.autoSheet(); sv.ctl.tiller = 0; sv.run(dt, 1); sv.suoni.agg(dt, false); a.push([Math.abs(sv.S.u), sv.suoni.val.acquaVel, sv.suoni.val.acquaFiltro]); } }
            for (const kn of [4, 8, 12, 16]){ sv.openItem("free"); env.tws = kn / KN; env.twd = 0; freshState(0, 0, 0, 0); const c0 = sv.suoni.val.colpi; let att = 0, aw = 0;
              for (let k = 0; k < 3600; k++){ sv.ctl.sheet = 1; sv.ctl.tiller = 0; sv.run(dt, 1); sv.suoni.agg(dt, false); att += sv.suoni.val.ritmo * dt; aw += info.aws * KN / 3600; }
              colpi[kn] = sv.suoni.val.colpi - c0; attesi[kn] = [+att.toFixed(1), +aw.toFixed(1)]; }
            const contro = {};
            sv.openItem("free"); env.tws = 10 / KN; env.twd = 0; freshState(0, 0, 90, 0.4); let c0 = sv.suoni.val.colpi;
            for (let k = 0; k < 3600; k++){ sv.ctl.sheet = sv.autoSheet(); sv.ctl.tiller = 0; sv.run(dt, 1); sv.suoni.agg(dt, false); } contro.regolata = sv.suoni.val.colpi - c0;
            freshState(0, 0, 0, 0); sv.S.capsized = true; c0 = sv.suoni.val.colpi; for (let k = 0; k < 3600; k++) sv.suoni.agg(dt, false); contro.scuffiata = sv.suoni.val.colpi - c0;
            freshState(0, 0, 0, 0); c0 = sv.suoni.val.colpi; for (let k = 0; k < 3600; k++) sv.suoni.agg(dt, true); contro.in_pausa = sv.suoni.val.colpi - c0;
            return { a, colpi, attesi, contro }; }""")
        # 1.2.7, detto: il primo giro chiedeva anche «giro da min a max più largo di 0,2»; ma qui la barca parte a 1,5 m/s e non scende sotto 1,2, quindi il giro
        # va da 0,96 a 1,12 per forza. Sostituito con un controllo più stretto: ogni lettura uguale alla formula del §3 (0,85 + 0,27 × min(1, u/3); 1.200 + 4.800 × min(1, u/3) Hz).
        formula = [abs(v - (0.85 + 0.27 * min(1, u / 3))) < 1e-9 and abs(f - (1200 + 4800 * min(1, u / 3))) < 1e-6 for u, v, f in r2["a"]]
        chk("R2", len(r2["a"]) > 1000 and mono([(u, v) for u, v, _ in r2["a"]]) and mono([(u, f) for u, _, f in r2["a"]]) and metro.tutti(formula),
            f"R2 acqua: velocità del giro e filtro crescono sempre con la velocità della barca, ogni lettura come la formula del §3 ({len(r2['a'])} letture, giro da {min(v for _, v, _ in r2['a']):.2f} a {max(v for _, v, _ in r2['a']):.2f}, filtro da {min(f for _, _, f in r2['a']):.0f} a {max(f for _, _, f in r2['a']):.0f} Hz)")
        ck = [r2["colpi"][str(k)] for k in (4, 8, 12, 16)]
        # attesi dal §3: (1 + 0,35 × vento apparente in nodi) colpi al secondo, integrati sui 60 s; entro il 20%
        dentro = [abs(r2["colpi"][str(k)] - r2["attesi"][str(k)][0]) <= 0.2 * r2["attesi"][str(k)][0] for k in (4, 8, 12, 16)]
        chk("R2", all(x < y for x, y in zip(ck, ck[1:])) and ck[0] > 0, f"R2 vela: colpi in 60 s prua al vento a 4, 8, 12, 16 nodi: {ck}, crescono sempre")
        chk("R2", metro.tutti(dentro), f"R2 vela: colpi entro il 20% degli attesi (attesi, vento apparente medio in nodi): {r2['attesi']}")
        chk("R2", r2["contro"] == {"regolata": 0, "scuffiata": 0, "in_pausa": 0}, f"R2 controprova: nessun colpo con la vela regolata, a barca scuffiata, in pausa: {r2['contro']}")
        chk("R6", not errs, f"R2 errori della pagina {errs[:1]}"); await ctx.close()
        # R3-R4: la decodifica, nella pagina con e senza #collaudo; e col decodificatore che fallisce apposta (devono restare i suoni sintetici, senza errori)
        peso = (ROOT / "js" / "suoni-dati.js").stat().st_size
        chk("R4", peso <= 700 * 1024, f"G4 js/suoni-dati.js: {peso / 1024:.0f} KB (al massimo 700, dalla 1.2.9)")
        dati = (ROOT / "js" / "suoni-dati.js").read_text(encoding="utf-8")   # G5: il testo di acqua e colpi come nella 1.2.8
        for nome, h in (("acqua", "8238e8312bfd97143abd2bdb58c052e6bc372b5929dea138a24d0132dac8b353"), ("colpi", "4e26ce6139136616082d5873aa89f717fa2f9373ff1589c4363c1dd228547c04")):
            chk("G5", hashlib.sha256(re.search(nome + r': "([^"]+)"', dati).group(1).encode()).hexdigest() == h, f"G5 {nome}: identico alla 1.2.8")
        for h in ("", "#collaudo"):
            ctx, pg, errs = await pagina(b, h); await pg.click("#goFree"); await pg.keyboard.press("Enter")
            await attendi(pg, AMB_FINITA)
            r3 = await pg.evaluate("() => [suoniFonte + ' (audio: ' + (actx ? actx.state : 'nessuno') + ')', sReg ? sReg.ms : null]")
            r3[0] = r3[0].replace(" (audio: running)", "").replace(" (audio: suspended)", "") if r3[0].startswith("registrati") else r3[0]
            chk("R3", r3[0] == "registrati" and not errs, f"R3 pagina {'con' if h else 'senza'} #collaudo: suoni {r3[0]}, errori {errs[:1]}")
            chk("R4", r3[1] is not None and r3[1] <= 300, f"R4 decodifica al primo tasto: {r3[1]} ms (al massimo 300)")
            am = await pg.evaluate("() => [sAmbFonte, sAmbMs, !!sAmb]")
            chk("G3", am[0] == "registrati" and am[2], f"G3 pagina {'con' if h else 'senza'} #collaudo: altri suoni {am[0]}")
            chk("G4", am[1] is not None and am[1] <= 1500, f"G4 seconda decodifica: {am[1]} ms (al massimo 1500)")
            await ctx.close()
        # G3: la seconda decodifica rotta apposta (si rompono le chiamate dopo le prime due): acqua e colpi registrati, vento sintetico, nessun errore
        ctx, pg, errs = await pagina(b, "", "if (window.AudioContext){ const o = AudioContext.prototype.decodeAudioData; let n = 0; AudioContext.prototype.decodeAudioData = function(b, ok, no){ if (++n <= 2) return o.call(this, b, ok, no); const e = new Error('rotto apposta'); if (no) no(e); return Promise.reject(e); }; }")
        await pg.click("#goFree"); await pg.keyboard.press("Enter"); await attendi(pg, AMB_FINITA); await pg.keyboard.down("ArrowLeft"); await pg.wait_for_timeout(800); await pg.keyboard.up("ArrowLeft")
        ge = await pg.evaluate("() => [suoniFonte, sAmbFonte, !!sReg, !!sAmb, simTime > 0.3]")
        chk("G3", ge[0] == "registrati" and ge[1].startswith("errore") and ge[2] and not ge[3] and ge[4] and not errs, f"G3 seconda decodifica rotta apposta: {ge}, errori della pagina {errs[:1]}")
        await ctx.close()
        ctx, pg, errs = await pagina(b, "", "if (window.AudioContext) AudioContext.prototype.decodeAudioData = function(b, ok, no){ const e = new Error('rotto apposta'); if (no) no(e); return Promise.reject(e); };")
        await pg.click("#goFree"); await pg.keyboard.press("Enter")
        await attendi(pg, "() => suoniFonte.startsWith('errore')"); await pg.keyboard.down("ArrowLeft"); await pg.wait_for_timeout(800); await pg.keyboard.up("ArrowLeft")
        r3e = await pg.evaluate("() => [suoniFonte, !!actx, simTime > 0.3]")
        chk("R3", r3e[0].startswith("errore") and r3e[1] and r3e[2] and not errs, f"R3 decodifica rotta apposta: {r3e}, si gioca coi suoni sintetici, errori della pagina {errs[:1]}")
        await ctx.close()
        # ---- G2 (1.2.9, docs/PROPOSTA-SUONI-FINE.md §4): i suoni nuovi seguono i numeri ----
        ctx, pg, errs = await pagina(b)
        g2 = await pg.evaluate("""() => { const sv = __sv, dt = 1 / 60, L = [], val = sv.suoni.val, leggi = stallo => L.push([info.aws, local.tws, Math.abs(sv.S.u), !!sv.S.stall, !!sv.S.capsized, val.vento, val.ventoFiltro, val.ventoVel, val.onde, val.sartiame, val.sartiameVel, val.gorgoglio]);
            for (let kn = 0; kn <= 24; kn += 2){ sv.openItem("free"); env.tws = kn / KN; env.twd = 0; freshState(0, 0, 0, 0.5);
              for (let k = 0; k < 120; k++){ sv.ctl.sheet = 1; sv.ctl.tiller = 0; sv.run(dt, 1); sv.suoni.agg(dt, false); leggi(); } }
            // la barca guidata in stallo vero: al lasco veloce, barra a fondo alternata (la pala stalla quando la barca non segue ancora)
            sv.openItem("free"); env.tws = 12 / KN; env.twd = 0; freshState(0, 0, 90, 3); let inStallo = 0;
            for (let k = 0; k < 3600; k++){ sv.ctl.sheet = sv.autoSheet(); sv.ctl.tiller = Math.floor(k / 90) % 2 ? 1 : -1; sv.run(dt, 1); sv.suoni.agg(dt, false); if (sv.S.stall) inStallo++; leggi(); if (sv.S.capsized) rightBoat(); }
            const fine = { scr: [], scr10: 0, gab: [], gabPausa: 0, gabMenu: 0, scrScuf: 0, gorScuf: 0 };
            sv.openItem("free"); env.tws = 10 / KN; env.twd = 0; freshState(0, 0, 90, 2);
            for (let w = 0; w < 10; w++){ sv.suoni.reset(1000 + w); sv.S.heel = 25; const c0 = val.scricchioli; for (let k = 0; k < 3600; k++) sv.suoni.agg(dt, false); fine.scr.push(val.scricchioli - c0); }
            sv.suoni.reset(1100); sv.S.heel = 10; let c0 = val.scricchioli; for (let k = 0; k < 3600; k++) sv.suoni.agg(dt, false); fine.scr10 = val.scricchioli - c0;
            for (let w = 0; w < 10; w++){ sv.suoni.reset(2000 + w); const c = val.gabbiani; for (let k = 0; k < 24000; k++) sv.suoni.agg(0.1, false); fine.gab.push(val.gabbiani - c); }
            c0 = val.gabbiani; for (let k = 0; k < 24000; k++) sv.suoni.agg(0.1, true); fine.gabPausa = val.gabbiani - c0;
            c0 = val.gabbiani; for (let k = 0; k < 24000; k++) sv.suoni.agg(0.1, true, true); fine.gabMenu = val.gabbiani - c0;
            sv.suoni.reset(1200); sv.S.heel = 25; sv.S.capsized = true; sv.S.stall = true; sv.S.u = 2; c0 = val.scricchioli; for (let k = 0; k < 3600; k++){ sv.suoni.agg(dt, false); fine.gorScuf = Math.max(fine.gorScuf, val.gorgoglio); } fine.scrScuf = val.scricchioli - c0;
            return { L, inStallo, fine }; }""")
        L, fi = g2["L"], g2["fine"]
        ok_f = lambda x, y: abs(x - y) < 1e-9
        vento = [ok_f(r[5], 0.03 + 0.42 * min(1.5, max(0, r[0]) / 10) ** 1.5) and ok_f(r[6], 1000 + 350 * max(0, r[0])) and ok_f(r[7], 0.9 + 0.2 * min(1, max(0, r[0]) / 10)) for r in L]
        onde = [ok_f(r[8], 0.10 + 0.08 * min(1, r[1] / 8)) for r in L]
        kn = await pg.evaluate("() => KN")
        sart = [ok_f(r[9], 0.22 * min(1, max(0, max(0, r[0]) * kn - 12) / 10)) and ok_f(r[10], 0.9 + 0.2 * min(1, max(0, max(0, r[0]) * kn - 12) / 10)) for r in L]
        gorg = [ok_f(r[11], 0.8 * min(1, r[2] / 3) if r[3] and not r[4] else 0) for r in L]
        sopra = [r for r in L if r[9] > 0]; sotto = [r for r in L if r[0] * kn < 12]
        chk("G2", len(L) > 1000 and metro.tutti(vento) and metro.tutti(onde) and metro.tutti(sart) and metro.tutti(gorg), f"G2 vento, sciabordio, sartiame, gorgoglio: ogni lettura come la formula ({len(L)} letture; vento da {min(r[5] for r in L):.2f} a {max(r[5] for r in L):.2f}, sciabordio da {min(r[8] for r in L):.2f} a {max(r[8] for r in L):.2f}, sartiame fino a {max(r[9] for r in L):.2f})")
        chk("G2", len(sotto) >= 100 and metro.tutti(r[9] == 0 for r in sotto) and len(sopra) >= 100, f"G2 sartiame: 0 sotto i 12 nodi ({len(sotto)} letture), sopra 0 in {len(sopra)} letture")
        fuori = [r for r in L if not r[3]]
        chk("G2", g2["inStallo"] >= 30 and metro.tutti(r[11] == 0 for r in fuori), f"G2 gorgoglio: barca guidata in stallo vero per {g2['inStallo']} letture (almeno 30), volume 0 nelle {len(fuori)} senza stallo")
        ATT_S, ATT_G = 60 / 4.25, 2400 / 47.5
        chk("G2", metro.tutti(abs(x - ATT_S) <= 0.25 * ATT_S for x in fi["scr"]) and fi["scr10"] == 0, f"G2 scricchiolii in 60 s a 25° (attesi {ATT_S:.1f} ±25%, 10 finestre): {fi['scr']}; a 10°: {fi['scr10']}")
        chk("G2", metro.tutti(abs(x - ATT_G) <= 0.2 * ATT_G for x in fi["gab"]) and fi["gabPausa"] == 0 and fi["gabMenu"] == 0, f"G2 gabbiani in 40 minuti (attesi {ATT_G:.1f} ±20%, 10 finestre): {fi['gab']}; in pausa {fi['gabPausa']}, nel menu {fi['gabMenu']}")
        chk("G2", fi["scrScuf"] == 0 and fi["gorScuf"] == 0, f"G2 controprova a barca scuffiata: scricchiolii {fi['scrScuf']}, gorgoglio {fi['gorScuf']}")
        chk("G2", not errs, f"G2 errori della pagina {errs[:1]}"); await ctx.close()
        await b.close()
    print("casi per parte:", casi)
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad or any(casi.get(k, 0) == 0 for k in ("S1", "S2", "S3", "S4", "S5", "S6", "R2", "R3", "R4", "G2", "G3", "G4", "G5")) else 0)
asyncio.run(main())
