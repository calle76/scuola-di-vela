# Triangolo del torneo (T2, 1.0.55, docs/PROPOSTA-TORNEI-1B.md §8). Pagina con #collaudo, passi di 1/60 s, Math.random a seme fisso, pilota sostitutivo.
# La regata 2 del torneo è un triangolo: la si apre mettendo nel torneo un primo risultato finto (stesso gioco di misura_triangolo.py).
#  T2h scenari fissi: per ognuna delle due boe e quattro direzioni del vento, la barca gira sull'arco esterno della boa (dalla direzione da cui
#      arriva a quella in cui riparte) con la boa a sinistra: deve contare +1 (lato dopo); sull'arco al contrario deve contare -1 (una boa
#      sbagliata, lato invariato). 16 casi, attesi 16 su 16. Il metro non dipende da `out`: gli archi si ricavano dalle posizioni delle boe.
#  T2b distacchi: a ogni giro di boa (e all'arrivo) il distacco(b) letto nell'istante del passaggio dell'ultima delle due barche contro la differenza
#      vera dei tempi di passaggio; coerente = segno giusto e errore entro 3 s. Soglia 100%, con il numero dei confronti stampato.
#  T2e disegno: boe gialle disegnate sul mare (tratti del canvas intercettati) 2 sul triangolo e 1 a bastone; un anello sulla boa da girare ora;
#      pannello a 1360x650 e riquadro delle istruzioni senza eccesso.
#  T2f registratore: la registrazione di un triangolo contiene «lato 2» e «lato 3» e il file è letto da analizza_sessione.py senza errori.
# Uso: collaudo_triangolo.py [semi_da semi_a [secondi_di_lettura]]   (predefinito 1-20, 10 s)
import asyncio, io, pathlib, sys, contextlib, importlib.util
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
APRI = """([seme, vento, tri]) => {   // apre la regata 2 del torneo (triangolo) o la 1 (bastone), con il vento dato
  const sv = __sv; sv.fast(0); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = "principianti"; sel.dispatchEvent(new Event("change"));
  sv.torApri(); document.getElementById("torGo").click();
  if (tri){ sv.tor.ris.push([{ fin: 1, pp: 0 }, { fin: 2, pp: 0 }, { fin: 3, pp: 0 }, { fin: 4, pp: 0 }]); sv.tor.regate[1] = { c: seme % 3, wind: vento }; }
  else sv.tor.regate[0] = { c: 0, wind: vento };
  __seed(seme); sv.simTime = 0; sv.openItem(["r", "t"]); return !!sv.R.tri; }"""
# giro: bearing da `a` a `b` in passi di 2° (b può essere minore: allora decresce) attorno alla boa k (raggio 8 m); ritorna lato e boe sbagliate
GIRO = """([k, da, a]) => {
  const sv = __sv, R = sv.R, me = R.boats[0], mk = R.marks[k - 1]; R.t = 5; R.phase = "race"; me.leg = k; me.rnd = 0; me.rndA = undefined; me.wrongMarks = 0; me.ocs = false; me.S.capsized = false;
  const n = Math.max(2, Math.round(Math.abs(a - da) / 2));
  for (let i = 0; i <= n; i++){ const br = (da + (a - da) * i / n) * Math.PI / 180; me.S.x = mk.x + 8 * Math.sin(br); me.S.y = mk.y - 8 * Math.cos(br); sv.run(1 / 600, 1); }
  return { leg: me.leg, wm: me.wrongMarks || 0 }; }"""
DATI = """() => { const R = __sv.R, f = (a, b) => (Math.atan2(b.x - a.x, -(b.y - a.y)) * 180 / Math.PI + 360) % 360;
  const m = R.marks, c = R.center; return [[f(m[0], c), f(m[0], m[1])], [f(m[1], m[0]), f(m[1], c)]]; }"""   # [direzione da cui si arriva, direzione in cui si riparte] di ogni boa
CORSA = """([seme, RIT]) => {   // letture a RIT s dal giro dell'ultima delle due barche (giocatore e un avversario) a ogni boa; e, come informazione, nell'istante del giro
  const sv = __sv, dt = 1 / 60, R = sv.R, me = R.boats[0], pronti = [], ev = [], letture = [], fineT = {}, let0 = { v: 0 }, ult = new Map(R.boats.map(b => [b, 0])), T = new Map(R.boats.map(b => [b, {}]));
  while (R.t < 1500 && R.boats.some(b => b.fin === null)){
    sv.pilota(dt); sv.run(dt, 1);
    if (Math.floor(R.t * 2) !== let0.v){ let0.v = Math.floor(R.t * 2); letture.push([R.t, R.boats.filter(b => !b.me).map(b => [b.name, distacco(b)])]); }
    for (const b of R.boats) if (b.fin !== null && fineT[b.name] === undefined) fineT[b.name] = b.fin - b.pen;
    for (const b of R.boats){ if (b.me) continue; const l = b.fin !== null ? 9 : b.leg; if (l > ult.get(b) && l < 9){ ult.set(b, l); T.get(b)[l] = R.t;
      const altro = T.get(me)[l], mio = b.me;
      if (altro !== undefined){ pronti.push({ due: R.t + RIT, b, l, vero: altro - R.t }); } } }   // (b è già passata prima o dopo di me: i due tempi sono noti)
    if (me.leg > ult.get(me) && me.leg < 9){ ult.set(me, me.leg); T.get(me)[me.leg] = R.t;
      for (const o of R.boats) if (!o.me && T.get(o)[me.leg] !== undefined){ pronti.push({ due: R.t + RIT, b: o, l: me.leg, vero: R.t - T.get(o)[me.leg] }); ev.push([me.leg, o.name, distacco(o), R.t - T.get(o)[me.leg]]); } }
    for (let i = pronti.length - 1; i >= 0; i--) if (R.t >= pronti[i].due){ const x = pronti.splice(i, 1)[0];
      if (me.fin === null && x.b.fin === null) ev.push(["+10 s", x.l, x.b.name, distacco(x.b), x.vero]); }
  }
  return { ev, letture, fineT, arrivato: me.fin !== null, t: R.t }; }"""

async def main(a, b, RIT=10):
    ok_tot = True; errori = []
    def esito(nome, ok, dett=""):
        nonlocal ok_tot; ok_tot = ok_tot and ok; print(("OK       " if ok else "FALLITO  ") + nome + (" — " + dett if dett else ""))
    async with async_playwright() as p:
        br = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        async def pagina(w=1280, h=800):
            ctx = await br.new_context(viewport={"width": w, "height": h}); await ctx.add_init_script(SEME)
            pg = await ctx.new_page(); pg.on("pageerror", lambda e: errori.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(200); return ctx, pg
        # T2h
        casi = []
        for vento in (0, 90, 180, 270):
            ctx, pg = await pagina(); assert await pg.evaluate(APRI, [7, vento, True])
            ba = await pg.evaluate(DATI)
            for k in (1, 2):
                da, a_ = ba[k - 1]
                d = (da - a_) % 360   # ampiezza dell'arco esterno, sempre meno di un giro
                casi.append((vento, k, "giusto", await pg.evaluate(GIRO, [k, da, da - d]), 1))   # arco esterno, bearing decrescente: boa a sinistra
                casi.append((vento, k, "contrario", await pg.evaluate(GIRO, [k, da - d, da]), -1))
            await ctx.close()
        buoni = 0
        for vento, k, nome, r, atteso in casi:
            leg0 = k
            ok = (r["leg"] == k + 1 and r["wm"] == 0) if atteso == 1 else (r["leg"] == k and r["wm"] == 1)
            buoni += ok
            if not ok: print("   caso sbagliato: vento", vento, "boa", k, nome, r)
        esito("T2h: giro delle due boe da 4 direzioni del vento, giusto (+1) e al contrario (-1)", buoni == len(casi) == 16, f"{buoni} casi su {len(casi)}")
        # T2b
        conf = giusti = segno = 0; d1 = [0, 0]; d1_peggio = 0.0; peggio = 0.0; per_lato = {1: 0, 2: 0, 3: 0}; buoni_lato = {1: 0, 2: 0, 3: 0}; arrivati = 0; ist = [0, 0]
        for seme in range(a, b + 1):
            ctx, pg = await pagina(); assert await pg.evaluate(APRI, [seme, (seme % 8) * 45, True]); await pg.evaluate("__sv.R.tor = false")
            r = await pg.evaluate(CORSA, [seme, RIT]); arrivati += r["arrivato"]
            if r["arrivato"]:    # D1 di collaudo_distacchi.py sul triangolo: 5 s prima del mio arrivo, la barca arrivata subito prima di me
                tm = r["fineT"]["Tu"]; prima = sorted((t, n) for n, t in r["fineT"].items() if n != "Tu" and t < tm)
                if prima and tm - prima[-1][0] < 60:
                    lett = [x for x in r["letture"] if x[0] <= tm - 5][-1]; d = dict(lett[1]).get(prima[-1][1])
                    if d is not None: d1[0] += 1; d1[1] += abs(d - (tm - prima[-1][0])) <= 3; d1_peggio = max(d1_peggio, abs(d - (tm - prima[-1][0])))
            for e in r["ev"]:
                if e[0] != "+10 s":                                     # nell'istante del giro: solo informazione (vedi sotto)
                    ist[0] += 1; ist[1] += (e[2] is not None and (e[2] > 0) == (e[3] > 0) and abs(e[2] - e[3]) <= 3); continue
                _, l, nome, d, vero = e
                if d is None: continue
                conf += 1; per_lato[l] += 1
                s_ok = (d > 0) == (vero > 0) or abs(vero) < 0.5; segno += s_ok
                if s_ok and abs(d - vero) <= 3: giusti += 1; buoni_lato[l] += 1
                else: print(f"   seme {seme} dopo {["il via", "la boa 1", "la boa 2"][l - 1]} {nome}: distacco {d:.1f} s, vero {vero:.1f} s")
                peggio = max(peggio, abs(d - vero))
            await ctx.close()
        print(f"   informazione, nell'istante del giro (tra l'abeam e il giro la strada resta ferma): {ist[1]} confronti su {ist[0]} entro 3 s col segno giusto")
        esito("T2b/D1: 5 s prima dell'arrivo il distacco dalla barca arrivata subito prima è entro 3 s dalla differenza vera dei tagli (soglia 90% di collaudo_distacchi.py)", d1[0] > 0 and d1[1] >= 0.9 * d1[0],
              f"{d1[1]} su {d1[0]} regate (peggiore {d1_peggio:.1f} s)")
        esito(f"T2b: distacchi coerenti (segno giusto, errore entro 3 s) a {RIT} s da ogni giro di boa", conf > 0 and giusti == conf,
              f"{giusti} su {conf} confronti ({segno} col segno giusto), entro 3 s dopo il via {buoni_lato[1]}/{per_lato[1]}, dopo la boa 1 {buoni_lato[2]}/{per_lato[2]}, dopo la boa 2 {buoni_lato[3]}/{per_lato[3]}, errore massimo {peggio:.1f} s, giocatore arrivato in {arrivati} regate su {b - a + 1}")
        # T2e
        for tri in (True, False):
            ctx, pg = await pagina(1360, 650)
            await pg.evaluate("""() => { window.__gialle = 0; window.__anelli = 0; const P = CanvasRenderingContext2D.prototype, fi = P.fill, st = P.stroke;
              P.fill = function(...a){ if (String(this.fillStyle).toLowerCase() === "#f2d43c") window.__gialle++; return fi.apply(this, a); };   // la boa gialla è il solo disco di quel colore
              P.stroke = function(...a){ if (this.strokeStyle === "rgba(255, 255, 255, 0.9)" && Math.abs(this.lineWidth - 0.2) < 1e-6) window.__anelli++; return st.apply(this, a); }; }""")
            await pg.evaluate(APRI, [3, 0, tri]); await pg.evaluate("__sv.R.tor = false")
            n = await pg.evaluate("__sv.R.t = 5; __sv.R.boats[0].leg = 1; __sv.run(1/60, 2); window.__gialle = window.__anelli = 0; __sv.draw(1/60); [window.__gialle, window.__anelli]")   # una sola chiamata: il ciclo del browser disegna fra una chiamata e l altra
            esito(f"T2e: boe gialle disegnate {'sul triangolo' if tri else 'sul bastone'}", n[0] == (2 if tri else 1) and n[1] == (1 if tri else 0), f"boe {n[0]}, anelli {n[1]}")
            await ctx.close()
        ctx, pg = await pagina(1360, 650); assert await pg.evaluate(APRI, [5, 45, True]); eccesso = 0
        PH = "() => { const p = document.querySelector('.panel'); return p.scrollHeight - p.clientHeight; }"
        for i in range(60):
            await pg.evaluate("for (let k = 0; k < 360; k++){ __sv.pilota(1 / 60); __sv.run(1 / 60, 1); } __sv.panel()"); eccesso = max(eccesso, await pg.evaluate(PH))
            if await pg.evaluate("__sv.R.boats[0].fin !== null"): break
        await ctx.close(); ctx, pg = await pagina(1360, 650); await pg.evaluate("__sv.skipBrief = false"); assert await pg.evaluate(APRI, [5, 45, True]); await pg.wait_for_timeout(300)
        # il riquadro delle istruzioni del torneo scorre già a bastone (overlay con overflow-y: auto, 1.0.34): qui si controlla che il pulsante «Parti» resti nella finestra
        riq = await pg.evaluate("(() => { const e = document.getElementById('briefOv'), g = document.getElementById('bGo').getBoundingClientRect(); return [e.scrollHeight - e.clientHeight, Math.round(g.bottom)]; })()")
        esito("T2e: pannello a 1360x650 nel triangolo senza eccesso, e «Parti» dentro la finestra con il riquadro delle istruzioni", eccesso <= 0 and riq[1] <= 650,
              f"eccesso del pannello {eccesso} px (misurato {i + 1} volte, fino all'arrivo); il riquadro scorre di {riq[0]} px (a bastone, stesso metodo: 267), «Parti» arriva a {riq[1]} px su 650")
        await ctx.close()
        # T2f
        ctx, pg = await pagina(); assert await pg.evaluate(APRI, [11, 90, True]); await pg.evaluate("__sv.R.tor = false")
        r = await pg.evaluate("""() => { const sv = __sv; sv.reg; const o = document.getElementById('sesOn'); o.checked = true; o.dispatchEvent(new Event('change')); const R = sv.R;
          while (R.t < 1500 && R.boats[0].fin === null){ sv.pilota(1 / 60); sv.run(1 / 60, 1); } return sv.ses.lines.join('\\n'); }""")
        lato = [x for x in r.split("\n") if " lato " in x or "\tlato" in x]
        esito("T2f: nel file del registratore compaiono «lato 2» e «lato 3»", any(x.rstrip().endswith("lato 2") for x in lato) and any(x.rstrip().endswith("lato 3") for x in lato), f"{[x[:40] for x in lato][:5]}")
        tmp = pathlib.Path(__file__).resolve().parent / "output" / "triangolo_sessione.txt"; tmp.parent.mkdir(exist_ok=True); tmp.write_text(r)
        spec = importlib.util.spec_from_file_location("analizza", ROOT / "tests" / "analizza_sessione.py"); m = importlib.util.module_from_spec(spec)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                sys.argv = ["analizza_sessione.py", str(tmp)]; spec.loader.exec_module(m)
                if hasattr(m, "main"): m.main()
            esito("T2f: analizza_sessione.py legge il file del triangolo senza errori", "Traceback" not in buf.getvalue(), buf.getvalue().strip().split("\n")[0][:80])
        except SystemExit:
            esito("T2f: analizza_sessione.py legge il file del triangolo senza errori", True, "uscito")
        except Exception as e:
            esito("T2f: analizza_sessione.py legge il file del triangolo senza errori", False, repr(e)[:120])
        await ctx.close(); await br.close()
    esito("nessun errore della pagina", not errori, str(errori[:2]))
    sys.exit(0 if ok_tot else 1)
asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 2 else 1, int(sys.argv[2]) if len(sys.argv) > 2 else 20, int(sys.argv[3]) if len(sys.argv) > 3 else 10))
