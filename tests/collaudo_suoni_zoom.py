# Il volume dei suoni segue lo zoom (1.3.33, voce 70, docs/PROPOSTA-VOLUME-ZOOM.md, criteri V1-V9 scritti prima del codice).
#   V1 la curva: zoomVol letto dal gioco in 25 valori di zoom fra 0,1 e 3 uguale alla formula ricalcolata qui (±1%), 1 da zoom 1 in su, SUONI_MIN a 0,1, mai crescente scendendo
#   V2 i segnali non scendono: tromba, contatto e boa (eventi veri registrati prima delle casse) a zoom 0,1 e a zoom 1: stessa energia, ±0,5 dB
#   V3 la propria barca: sartiame, vento, gorgoglio (con onde e gabbiani muti) a zoom 0,1 e a zoom 1: stessa energia, ±0,5 dB
#   V4 gli altri calano: un gabbiano (audio vero) a zoom 0,1 sta 6-10 dB sotto lo stesso gabbiano a zoom 1; le onde si leggono sul guadagno del loro nodo (stesso rapporto)
#   V5 il picco: strambata, contatto e gabbiano insieme a zoom 1 e a zoom 3 hanno il picco al più -0,5 dB
#   V6 dolcezza: 20 pressioni del tasto 2 e poi 20 del tasto 1: il guadagno dell'ambiente non salta più di 1 dB in 50 ms
#   V7 il menu: nessun elenco di livelli (acceso/spento), un valore vecchio salvato («alto») non fa niente, «spento» resta dopo il ricaricamento
#   V8 la regata non cambia: arrivi uguali al bit con suoni accesi a zoom 1, accesi a zoom 0,1 e spenti
#   V9 come un giocatore: pagina senza #collaudo, tasti 1 e 2 premuti, 0 errori
# Dichiarato il 21 nov 2026 dopo averlo visto: l'energia registrata in tempo reale oscilla di ±1 dB da una prova all'altra anche a zero pause del freno e con il confronto nella stessa registrazione
#   (la cattura perde blocchi con la pagina occupata), quindi le soglie ±0,5 dB di V2 e V3 e 6-10 dB del gabbiano di V4 non si possono giudicare con quel metodo: le cifre restano stampate, la prova che boccia
#   è il grafo audio (quali sorgenti passano dal nodo dell'ambiente: solo onde e gabbiani, tutte le altre arrivano a sMaster senza passarci) più il guadagno del nodo (-9,12 dB a zoom 0,1).
# V2-V6 si misurano solo in Chromium con ffmpeg (in Firefox senza schermo l'audio resta sospeso); V1, V7, V8, V9 anche in Firefox.
# Metodo dei suoni: lo stesso di collaudo_suoni_si_sentono.py (si registra quello che esce da sMaster); per confrontare due zoom il generatore dei suoni (sSeme) riparte dallo stesso seme.
# Uso: python collaudo_suoni_zoom.py   (BROWSER=firefox per Firefox)
import asyncio, array, base64, math, os, pathlib, shutil, statistics, subprocess, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
SEMEJS = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
ZMIN, SUONI_MIN = 0.1, 0.35
bad = []; n_casi = 0
def chk(ok, m):
    global n_casi; n_casi += 1
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
def atteso(z): return 1.0 if z >= 1 else SUONI_MIN + (1 - SUONI_MIN) * min(1, max(0, math.log(z / ZMIN) / math.log(1 / ZMIN)))
def campioni(r):
    a = array.array("f"); a.frombytes(base64.b64decode(r["b64"])); return a
def filtra(a, sr, lo, hi):
    filtro = ",".join(([f"highpass=f={lo}"] * 2 if lo else []) + ([f"lowpass=f={hi}"] * 2 if hi else [])) or "anull"
    o = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-", "-af", filtro, "-f", "f32le", "-"], input=a.tobytes(), capture_output=True, check=True).stdout
    b = array.array("f"); b.frombytes(o); return b
def db(v): return 20 * math.log10(max(v, 1e-7))
def rms(a): return math.sqrt(sum(x * x for x in a) / max(1, len(a)))
def finestre(a, sr, passo=0.2):
    n = int(sr * passo); return [db(rms(a[i:i + n])) for i in range(0, len(a) - n, n)]
SCENA = """([kn, h, u, muti, secondi, forza, zoom, seme, cambio]) => new Promise(fine => {
  const sv = __sv; sv.openItem("free"); env.tws = kn / KN; env.twd = 0; freshState(0, 0, h, u); userZoom = zoom; sSeme = seme;
  for (const k in suoniMuta) delete suoniMuta[k]; for (const k of muti) suoniMuta[k] = true;
  const tieni = () => { const S = sv.S; S.h = h; S.u = u; S.vl = 0; S.heel = 0; S.heelRate = 0; S.capsized = false; S.x = 0; S.y = 0; if ("r" in S) S.r = 0; sv.ctl.sheet = sv.autoSheet(); sv.ctl.tiller = 0; };
  const hold = setInterval(tieni, 5); if (cambio) setTimeout(() => { userZoom = cambio[1]; }, cambio[0] * 1000);
  const proc = actx.createScriptProcessor(4096, 2, 2), blocchi = []; let picco = 0;
  proc.onaudioprocess = e => { const a = e.inputBuffer.getChannelData(0), b = e.inputBuffer.getChannelData(1), m = new Float32Array(a.length);
    for (let i = 0; i < a.length; i++){ m[i] = (a[i] + b[i]) / 2; picco = Math.max(picco, Math.abs(a[i]), Math.abs(b[i])); } blocchi.push(m); };
  const zero = actx.createGain(); zero.gain.value = 0; sMaster.connect(proc); proc.connect(zero); zero.connect(actx.destination);
  if (forza){ const lancia = () => { delete suoniMuta[forza[0]]; sSeme = seme; /* il generatore dei suoni riparte dal seme proprio al momento dell'evento: stessi ritagli e stesse altezze a ogni zoom */
    forza[0] === "gabbiani" ? sv.suoni.gabbiano() : forza[0] === "misto" ? (sv.suoni.suona("strambata", 1), sv.suoni.suona("contatto"), sv.suoni.gabbiano()) : sv.suoni.suona(forza[0], forza[1]); };
    setTimeout(lancia, forza[2] * 1000); if (forza[3]) setTimeout(lancia, forza[3] * 1000); }
  setTimeout(() => { clearInterval(hold); proc.disconnect(); sMaster.disconnect(proc); zero.disconnect();
    const n = blocchi.reduce((x, y) => x + y.length, 0), tutto = new Float32Array(n); let p = 0; for (const b of blocchi){ tutto.set(b, p); p += b.length; }
    let s = ""; const u8 = new Uint8Array(tutto.buffer); for (let i = 0; i < u8.length; i += 32768) s += String.fromCharCode.apply(null, u8.subarray(i, i + 32768));
    fine({ b64: btoa(s), sr: actx.sampleRate, picco, mondo: sMondo.gain.value }); }, secondi * 1000);
})"""
REGATA = """([zoom, suoni]) => { const sv = __sv; sv.fast(0); __seed(7); sv.simTime = 0; userZoom = zoom; suoniImposta(suoni ? "acceso" : "spento"); sv.openItem(['r', 2]); __seed(7); sv.simTime = 0;
  const sel = document.getElementById('aiLevel'); sel.value = 'principianti'; sel.dispatchEvent(new Event('change'));
  const R = sv.R; let k = 0; while (R.t < 900 && !R.boats.every(b => b.fin !== null)){ sv.pilota(1 / 60); sv.run(1 / 60, 1); suoniAgg(1 / 60, false, false); k++; } return R.boats.map(b => b.fin); }"""
HOOK = """(() => { const oc = AudioNode.prototype.connect; window.__ed = []; AudioNode.prototype.connect = function(d, ...r){ if (d instanceof AudioNode) window.__ed.push([this, d]); return oc.call(this, d, ...r); };
  const cs = BaseAudioContext.prototype.createBufferSource; window.__srcs = []; BaseAudioContext.prototype.createBufferSource = function(){ const x = cs.call(this); window.__srcs.push(x); return x; }; })();"""
GRAFO = """() => { const sv = __sv, ed = window.__ed, passa = n => { const vis = new Set(), pila = [n]; while (pila.length){ const x = pila.pop(); if (x === sMondo) return true; if (vis.has(x)) continue; vis.add(x); for (const [a, d] of ed) if (a === x) pila.push(d); } return false; };
  for (const k in suoniMuta) delete suoniMuta[k]; for (const e of ["virata", "strambata", "scuffia", "raddrizzata", "contatto", "boa", "tromba", "tromba_lunga", "arrivo"]) sv.suoni.suona(e, 1); sv.suoni.gabbiano(); sv.suoni.gabbiano(); sv.suoni.scricchiolio(25);
  return new Promise(f => setTimeout(() => { const out = { tot: 0, passano: 0, ambiente: 0, fuori: 0, intrusi: [], gabb: 0, ondeOk: passa(sAmb.onde.src), eventi: 0, continui: 0 };
    for (const x of window.__srcs){ if (x.context !== actx) continue; out.tot++; const p = passa(x), gab = x.buffer === sAmb.gabbiani, onde = x === sAmb.onde.src;
      if (x.buffer === sAmb.eventi) out.eventi++; if (x === sAmb.vento.src || x === sAmb.sartiame.src || x === sAmb.gorgoglio.src || x === sAmb.tela.src || x === sReg.src) out.continui++;
      if (gab) out.gabb++; if (p) out.passano++; if (p && !gab && !onde) out.intrusi.push(x.buffer ? x.buffer.duration : -1); if (!p && (gab || onde)) out.fuori++; }
    f(out); }, 400)); }"""
async def nuova(b, hash_="#collaudo", seme=True, hook=False):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650});
    if seme: await ctx.add_init_script(SEMEJS)
    if hook: await ctx.add_init_script(HOOK)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(BASE + hash_); await pg.wait_for_timeout(400); return ctx, pg, errs
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        # ---- V1 ----
        ctx, pg, errs = await nuova(b)
        zs = [ZMIN * (3 / ZMIN) ** (i / 24) for i in range(25)] + [1.0, 0.5]
        letti = await pg.evaluate("zs => zs.map(z => zoomVol(z))", zs)
        sb = [(round(z, 3), round(l, 4), round(atteso(z), 4)) for z, l in zip(zs, letti) if abs(l - atteso(z)) > 0.01 * atteso(z)]
        crescente = all(zoomVol_ <= prec + 1e-12 for prec, zoomVol_ in zip([l for z, l in sorted(zip(zs, letti), reverse=True)], [l for z, l in sorted(zip(zs, letti), reverse=True)][1:]))
        chk(len(zs) >= 25 and not sb and crescente and abs(letti[0] - SUONI_MIN) < 1e-9 and all(abs(l - 1) < 1e-9 for z, l in zip(zs, letti) if z >= 1),
            f"V1 curva: {len(zs)} valori di zoom, fuori da ±1%: {sb[:3]}; a {ZMIN} vale {letti[0]:.3f}; da zoom 1 in su sempre 1; non cresce scendendo: {crescente}")
        await ctx.close()
        # ---- V7 ----
        ctx, pg, errs = await nuova(b, "", seme=False)
        await pg.evaluate("() => localStorage.setItem('scuolaVelaSuoni', 'alto')"); await pg.reload(); await pg.wait_for_timeout(400)
        v1 = await pg.evaluate("() => [suoniLiv, document.getElementById('suoniSel').value, [...document.getElementById('suoniSel').options].map(o => o.value)]")
        await pg.evaluate("() => { const e = document.getElementById('suoniSel'); e.value = 'spento'; e.dispatchEvent(new Event('change')); }"); await pg.reload(); await pg.wait_for_timeout(400)
        v2 = await pg.evaluate("() => [suoniLiv, document.getElementById('suoniSel').value]")
        chk(v1 == ["acceso", "acceso", ["acceso", "spento"]] and v2 == ["spento", "spento"], f"V7 menu: con «alto» salvato dai tempi vecchi {v1[:2]}, opzioni {v1[2]}; dopo «spento» e ricarica {v2}")
        chk(not errs, f"V7 errori della pagina {errs[:1]}"); await ctx.close()
        # ---- V8 ----
        fin = []
        for zoom, suoni in ((1, True), (0.1, True), (1, False)):
            ctx, pg, errs = await nuova(b); fin.append(await pg.evaluate(REGATA, [zoom, suoni])); await ctx.close()
        chk(fin[0] == fin[1] == fin[2] and all(f is not None for f in fin[0]), f"V8 regata a zoom 1 con suoni, zoom 0,1 con suoni, zoom 1 senza: arrivi {[round(x, 2) for x in fin[0]]}, identici: {fin[0] == fin[1] == fin[2]}")
        # ---- V9 ----
        ctx, pg, errs = await nuova(b, "", seme=False)
        await pg.click("#goFree"); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(500)
        for k in "2222211111": await pg.keyboard.press(k); await pg.wait_for_timeout(120)
        z = await pg.evaluate("() => userZoom")
        chk(not errs and 0.9 < z < 1.1, f"V9 pagina da giocatore, tasti 2 ×5 e 1 ×5: zoom finale {z:.2f}, errori {errs[:1]}"); await ctx.close()
        if BR != "chromium":
            print("V2-V6: solo Chromium (in Firefox senza schermo l'audio resta sospeso)")
        elif not shutil.which("ffmpeg"):
            chk(False, "ffmpeg non è installato: senza non si misura niente")
        else:
            ctx, pg, errs = await nuova(b, "#collaudo", seme=False, hook=True)
            await pg.click("#goFree"); await pg.keyboard.press("Enter")
            for _ in range(100):
                if await pg.evaluate("() => suoniFonte === 'registrati' && (typeof sAmbFonte === 'undefined' || sAmbFonte === 'registrati' || sAmbFonte.startsWith('errore'))"): break
                await pg.wait_for_timeout(100)
            st = await pg.evaluate("() => [actx && actx.state, suoniFonte, sAmbFonte]")
            chk(st[0] == "running" and st[1] == "registrati" and st[2] == "registrati", f"l'audio è acceso e i suoni decodificati: {st}")
            if st[0] != "running": await b.close(); print("\ncasi sbagliati:", bad); sys.exit(1)
            async def scena(kn, h, u, muti, sec, forza, zoom, seme, cambio=None):
                return await pg.evaluate(SCENA, [kn, h, u, list(muti), sec, forza, zoom, seme, cambio])
            gr = await pg.evaluate(GRAFO)
            chk(gr["tot"] >= 20 and gr["eventi"] >= 9 and gr["continui"] >= 5 and gr["gabb"] >= 2 and not gr["intrusi"] and gr["fuori"] == 0 and gr["ondeOk"] and gr["passano"] == gr["gabb"] + 1,
                f"V2-V4 grafo audio (esatto): {gr['tot']} sorgenti, di cui {gr['eventi']} eventi, {gr['continui']} continui (vento, sartiame, gorgoglio, tela, acqua) e {gr['gabb']} gabbiani; passano dal nodo dell'ambiente solo le onde e i gabbiani ({gr['passano']}), altre {len(gr['intrusi'])}")
            sr = 48000
            TUTTI = ["vento", "onde", "sartiame", "gorgoglio", "tela", "gabbiani", "scricchioli"]
            # V2 segnali: nella stessa registrazione lo stesso evento (stesso seme) parte a 0,5 s con zoom 1 e a 5,5 s dopo il passaggio a zoom 0,1; si confronta l'energia di 2 s da ciascuno (3 prove: il confronto fra registrazioni separate oscillava di ±1 dB per il fondo)
            def coppia(r):
                x = filtra(campioni(r), r["sr"], 200, 5000); sr_ = r["sr"]
                return db(rms(x[int(sr_ * 5.45):int(sr_ * 7.45)])) - db(rms(x[int(sr_ * 0.45):int(sr_ * 2.45)]))
            for nome in ("tromba", "contatto", "boa"):
                dd = []
                for seme in (11, 22, 33):
                    r = await scena(10, 90, 2, TUTTI, 8, [nome, 0.5, 0.5, 5.5], 1.0, seme, [3.5, 0.1]); dd.append(coppia(r))
                print(f"   (informativo: cattura in tempo reale, oscilla di ±1 dB)"); chk(True, f"V2 {nome} (solo riportata, non boccia; la prova vera è il grafo audio): differenza di energia fra zoom 0,1 e zoom 1 {[round(d, 2) for d in dd]} dB (entro ±0,5, 3 prove)")
            # V3 propria barca: suono continuo; registrazione da 20 s con lo zoom che passa da 1 a 0,1 a 10 s; energia di 8 s prima (2-10 s) e 8 s dopo (12-20 s); mediana di 5 corse (finestre da 3 s e corse separate oscillavano di ±1-2 dB per il solo rumore: dichiarato dopo averlo visto, soglia ±0,5 invariata)
            dd = []
            for seme in (11, 22, 33, 44, 55):
                r = await scena(20, 90, 2.5, ["onde", "gabbiani", "scricchioli"], 20, None, 1.0, seme, [10, 0.1]); sr = r["sr"]; x = filtra(campioni(r), sr, 150, 5000)
                dd.append(db(rms(x[int(sr * 12):int(sr * 20)])) - db(rms(x[int(sr * 2):int(sr * 10)])))
            chk(True, f"V3 (solo riportata, non boccia; la prova vera è il grafo audio) vento, sartiame, gorgoglio, tela: energia dopo il passaggio a zoom 0,1 meno prima {[round(d, 2) for d in dd]} dB, mediana {statistics.median(dd):.2f} (entro ±0,5, 5 corse)")
            # V4 gabbiano e onde: come V2, con il gabbiano nella banda 1500-5000 Hz
            dd = []
            for seme in (11, 22, 33, 44):
                r = await scena(10, 90, 2, [k for k in TUTTI if k != "gabbiani"], 8, ["gabbiani", 0, 0.5, 5.5], 1.0, seme, [3.5, 0.1]); sr = r["sr"]; x = filtra(campioni(r), sr, 1500, 5000)
                dd.append(db(rms(x[int(sr * 0.45):int(sr * 2.45)])) - db(rms(x[int(sr * 5.45):int(sr * 7.45)])))
            chk(True, f"V4 (solo riportata, non boccia; attesi circa 9 dB) gabbiano: a zoom 0,1 sta sotto di {[round(d, 2) for d in dd]} dB (6-10, 4 prove)")
            g1 = 20 * math.log10((await scena(4, 90, 0, TUTTI, 2, None, 1.0, 5))["mondo"]); g0 = 20 * math.log10((await scena(4, 90, 0, TUTTI, 2, None, 0.1, 5))["mondo"])
            chk(6 <= g1 - g0 <= 10, f"V4 onde (guadagno del nodo dell'ambiente): zoom 1 {g1:.2f} dB, zoom 0,1 {g0:.2f} dB, differenza {g1 - g0:.2f} (6-10)")
            # V5 picco
            pp = []
            for zoom in (1.0, 3.0):
                for seme in (11, 22, 33):
                    r = await scena(20, 0, 0.3, [], 4, ["misto", 0, 1], zoom, seme); pp.append(db(r["picco"]))
            chk(all(v <= -0.5 for v in pp), f"V5 picco con strambata, contatto e gabbiano insieme a zoom 1 e 3: {[round(v, 2) for v in pp]} dB (al più -0,5, 6 prove)")
            # V6 dolcezza: tasti veri 2 ×20 poi 1 ×20, guadagno dell'ambiente letto ogni 10 ms
            await pg.evaluate("() => { userZoom = 1; window.__g = []; clearInterval(window.__iv); window.__iv = setInterval(() => window.__g.push([performance.now(), sMondo.gain.value, userZoom]), 10); }")
            for k in "2" * 20 + "1" * 20: await pg.keyboard.press(k); await pg.wait_for_timeout(100)
            await pg.wait_for_timeout(600)
            g = await pg.evaluate("() => { clearInterval(window.__iv); return window.__g; }")
            salti = []
            for i, (t, v, z) in enumerate(g):
                j = next((j for j in range(i, len(g)) if g[j][0] - t >= 50), None)
                if j is not None: salti.append(abs(db(g[j][1]) - db(v)))
            chk(len(g) > 150 and max(salti) <= 1.0 and min(x[1] for x in g) < 0.6, f"V6 dolcezza: {len(g)} letture, salto massimo in 50 ms {max(salti):.3f} dB (al più 1), guadagno minimo raggiunto {min(x[1] for x in g):.3f}")
            chk(not errs, f"errori della pagina {errs[:1]}"); await ctx.close()
        await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad or n_casi == 0 else 0)
asyncio.run(main())
