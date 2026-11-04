# Collaudo «si sentono» (1.2.9, docs/PROPOSTA-SUONI-FINE.md §4, criterio G6, soglie scritte prima): registra il suono vero che esce dal gioco e misura.
# collaudo_suoni.py legge i comandi dati; questo legge i campioni in uscita, prima delle casse: la 1.2.7 ha mostrato che un suono può partire senza sentirsi.
# La barca gira in tempo reale con il ciclo vero del gioco, a volume «bassi», in Chromium (in Firefox senza schermo l'audio resta sospeso). Ogni misura si fa 3 volte.
#   gabbiano:     un verso alza la banda 1,5-5 kHz di almeno 6 dB sul tratto prima
#   scricchiolio: un gruppo alza la banda 1-5 kHz di almeno 4 dB sul tratto prima
#   sartiame, sciabordio, gorgoglio: acceso contro spento, nella loro banda, almeno +2 dB
#   colpi di vela con la prua al vento: spicco sopra 1 kHz almeno 5,6 dB a 10 nodi e 2,9 dB a 15 (la 1.2.8 con lo stesso metro, 7,1 e 4,4, meno 1,5 dB)
#   volume generale al traverso a 10 nodi entro ±3 dB dalla 1.2.8; a volume «alto», caso peggiore, picco al più -0,5 dB
#   controprova del metro: con il volume generale a zero la registrazione è silenziosa; se l'audio non è acceso il collaudo fallisce
# Uso: python collaudo_suoni_si_sentono.py [--salva cartella]   (--salva: scrive le registrazioni in WAV, per la pagina d'ascolto)
#      SUONI_BASE=percorso/index.html misura un'altra copia del gioco (usato una volta per il riferimento della 1.2.8, che è scritto qui sotto)
import asyncio, array, base64, math, os, pathlib, shutil, statistics, subprocess, sys, wave
import metro
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = pathlib.Path(os.environ.get("SUONI_BASE", ROOT / "index.html")).as_uri()
RIF_128_TRAVERSO = -40.69   # livello complessivo della 1.2.8 al traverso a 10 nodi (dB), misurato con SUONI_BASE (3 giri)
# tiene la barca nello stato voluto (scena) e registra quello che esce da sMaster, prima delle casse
SCENA = """([kn, h, u, heel, sheet, tiller, muti, secondi, forza, liv]) => new Promise(fine => {
  const sv = __sv; sv.openItem("free"); env.tws = kn / KN; env.twd = 0; freshState(0, 0, h, u);
  if (typeof suoniMuta !== "undefined"){ for (const k in suoniMuta) delete suoniMuta[k]; for (const k of muti) suoniMuta[k] = true; if (sv.suoni.reset) sv.suoni.reset(); }
  if (liv) suoniImposta(liv);
  const tieni = () => { const S = sv.S; S.h = h; S.u = u; S.vl = 0; S.heel = heel; S.heelRate = 0; S.capsized = false; S.x = 0; S.y = 0; if ("r" in S) S.r = 0;
    sv.ctl.sheet = sheet === null ? sv.autoSheet() : sheet; sv.ctl.tiller = tiller; };
  const hold = setInterval(tieni, 5);
  const proc = actx.createScriptProcessor(4096, 2, 2), blocchi = []; let picco = 0, stalli = 0, letture = 0;
  const conta = setInterval(() => { letture++; if (sv.S.stall) stalli++; }, 50);
  proc.onaudioprocess = e => { const a = e.inputBuffer.getChannelData(0), b = e.inputBuffer.getChannelData(1), m = new Float32Array(a.length);
    for (let i = 0; i < a.length; i++){ m[i] = (a[i] + b[i]) / 2; picco = Math.max(picco, Math.abs(a[i]), Math.abs(b[i])); } blocchi.push(m); };
  const zero = actx.createGain(); zero.gain.value = 0; sMaster.connect(proc); proc.connect(zero); zero.connect(actx.destination);
  const c0 = suoniVal.colpi;
  if (forza) setTimeout(() => { if (typeof suoniMuta !== "undefined") delete suoniMuta[forza[0]]; forza[0] === "gabbiani" ? sv.suoni.gabbiano() : sv.suoni.scricchiolio(forza[1]); }, forza[2] * 1000);
  setTimeout(() => { clearInterval(hold); clearInterval(conta); proc.disconnect(); sMaster.disconnect(proc); zero.disconnect();
    const n = blocchi.reduce((x, y) => x + y.length, 0), tutto = new Float32Array(n); let p = 0; for (const b of blocchi){ tutto.set(b, p); p += b.length; }
    let s = ""; const u8 = new Uint8Array(tutto.buffer); for (let i = 0; i < u8.length; i += 32768) s += String.fromCharCode.apply(null, u8.subarray(i, i + 32768));
    fine({ b64: btoa(s), sr: actx.sampleRate, picco, stato: actx.state, colpi: suoniVal.colpi - c0, stalli, letture }); }, secondi * 1000);
})"""
bad = []; n_casi = 0
def chk(ok, m):
    global n_casi; n_casi += 1
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
def campioni(r):
    a = array.array("f"); a.frombytes(base64.b64decode(r["b64"])); return a
def filtra(a, sr, lo, hi):
    filtro = ",".join(([f"highpass=f={lo}"] * 2 if lo else []) + ([f"lowpass=f={hi}"] * 2 if hi else [])) or "anull"
    o = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-", "-af", filtro, "-f", "f32le", "-"], input=a.tobytes(), capture_output=True, check=True).stdout
    b = array.array("f"); b.frombytes(o); return b
def db(v): return 20 * math.log10(max(v, 1e-7))
def rms(a): return math.sqrt(sum(x * x for x in a) / max(1, len(a)))
def finestre(a, sr, passo=0.05):   # livello in dB ogni «passo» secondi
    n = int(sr * passo); return [db(rms(a[i:i + n])) for i in range(0, len(a) - n, n)]
def pct(xs, q): s = sorted(xs); return s[min(len(s) - 1, int(q * len(s)))]
def salva(cart, nome, a, sr):
    if not cart: return
    with wave.open(str(pathlib.Path(cart) / f"{nome}.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(array.array("h", [int(max(-1, min(1, v)) * 32767) for v in a]).tobytes())
async def main():
    if os.environ.get("BROWSER", "chromium") != "chromium":   # si misura solo in Chromium: nel giro di Firefox non c'è niente da fare, e lo dice
        print("Solo Chromium: in Firefox senza schermo l'audio resta sospeso. Niente misure in questo giro."); return
    if not shutil.which("ffmpeg"):   # serve per filtrare il suono registrato: senza, nessuna misura (su GitHub lo installa collaudi.yml)
        print("FALLITO ffmpeg non è installato: senza non si misura niente."); print("\ncasi sbagliati: ffmpeg mancante"); sys.exit(1)
    a = sys.argv[1:]; cart = a[a.index("--salva") + 1] if "--salva" in a else None
    solo128 = "SUONI_BASE" in os.environ
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(400)
        await pg.click("#goFree"); await pg.keyboard.press("Enter")
        for _ in range(100):
            if await pg.evaluate("() => suoniFonte === 'registrati' && (typeof sAmbFonte === 'undefined' || sAmbFonte === 'registrati' || sAmbFonte.startsWith('errore'))"): break
            await pg.wait_for_timeout(100)
        stato = await pg.evaluate("() => [actx && actx.state, suoniFonte, typeof sAmbFonte === 'undefined' ? '-' : sAmbFonte, suoniLiv]")
        print("audio:", stato)
        chk(stato[0] == "running" and stato[1] == "registrati" and stato[2] in ("registrati", "-"), f"l'audio è acceso e i suoni decodificati: {stato}")
        if stato[0] != "running":
            await b.close(); print("\ncasi sbagliati:", bad); sys.exit(1)
        async def scena(kn, h, u, heel=0, sheet=None, tiller=0, muti=(), sec=6, forza=None, liv=None):
            return await pg.evaluate(SCENA, [kn, h, u, heel, sheet, tiller, list(muti), sec, forza, liv])

        # ---- controprova del metro: il silenzio deve misurarsi come silenzio ----
        await pg.evaluate("() => sMaster.gain.setValueAtTime(0, actx.currentTime)")
        r = await scena(10, 90, 2, sec=2); x = campioni(r)
        await pg.evaluate("() => sMaster.gain.setValueAtTime(SUONI_LIV[suoniLiv], actx.currentTime)"); await pg.wait_for_timeout(200)
        # il volume a zero è sulla stessa catena della registrazione: lì dentro non passa niente solo se il metro legge davvero dopo sMaster
        chk(len(x) > r["sr"] and db(rms(x)) < -70, f"controprova: volume generale a zero, {len(x) / r['sr']:.1f} s registrati a {db(rms(x)):.1f} dB (sotto -70)")

        # ---- riferimento: volume generale e colpi ----
        vol, sp10, sp15 = [], [], []
        for i in range(3):
            r = await scena(10, 90, 2, sec=8); x = campioni(r); vol.append(db(rms(x))); salva(cart, f"traverso10_{i + 1}", x, r["sr"]); sr = r["sr"]
        for kn, lista in ((10, sp10), (15, sp15)):
            for i in range(3):
                r = await scena(kn, 0, 0.3, sheet=1, sec=6); x = campioni(r); f = finestre(filtra(x, sr, 1000, None), sr)[20:]
                lista.append(pct(f, 0.95) - pct(f, 0.5)); colpi = r["colpi"]; salva(cart, f"prua_al_vento{kn}_{i + 1}", x, sr)
            print(f"  colpi di vela a {kn} nodi: ultimo giro {colpi} colpi in 6 s; spicco {[round(v, 1) for v in lista]}", flush=True)
        print(f"  livello al traverso a 10 nodi: {[round(v, 1) for v in vol]} dB", flush=True)
        if solo128:
            print("\nRIFERIMENTO per", BASE, ": traverso", round(statistics.mean(vol), 2), "spicco 10 e 15 nodi", round(statistics.mean(sp10), 2), round(statistics.mean(sp15), 2))
            await b.close(); return
        chk(metro.tutti(v >= 5.6 for v in sp10), f"colpi a 10 nodi: spicco {[round(v, 1) for v in sp10]} dB (almeno 5,6)")
        chk(metro.tutti(v >= 2.9 for v in sp15), f"colpi a 15 nodi: spicco {[round(v, 1) for v in sp15]} dB (almeno 2,9)")
        if RIF_128_TRAVERSO is not None:
            chk(metro.tutti(abs(v - RIF_128_TRAVERSO) <= 3 for v in vol), f"volume generale al traverso a 10 nodi: {[round(v, 1) for v in vol]} dB, la 1.2.8 {RIF_128_TRAVERSO} dB (entro ±3)")

        # ---- gabbiano e scricchiolio: un evento contro il tratto prima ----
        for nome, kn, heel, lo, hi, soglia, forza in (("gabbiani", 10, 0, 1500, 5000, 6, ["gabbiani", 0, 4]), ("scricchioli", 10, 25, 1000, 5000, 4, ["scricchioli", 25, 4])):
            dd = []
            for i in range(6 if nome == "gabbiani" else 3):   # i gabbiani hanno 5 versi e volumi a caso: qualche giro in più
                r = await scena(kn, 90, 2, heel=heel, muti=[nome], sec=7, forza=forza); x = campioni(r); f = finestre(filtra(x, sr, lo, hi), sr, 0.2)
                dd.append(max(f[20:32]) - statistics.median(f[3:18])); salva(cart, f"{nome}_{i + 1}", x, sr)
            chk(metro.tutti(d >= soglia for d in dd), f"{nome}: l'evento alza la banda {lo}-{hi} Hz di {[round(d, 1) for d in dd]} dB (almeno {soglia})")

        # ---- sartiame, sciabordio, gorgoglio: acceso contro spento ----
        CASI = (("sartiame", dict(kn=20, h=90, u=2), 1000, 3500), ("onde", dict(kn=4, h=90, u=0), 100, 2000), ("gorgoglio", dict(kn=12, h=90, u=2.5, tiller=1), 200, 1500))
        for nome, sc, lo, hi in CASI:
            dd, st = [], []
            for i in range(3):
                r1 = await scena(sec=6, **sc); x1 = campioni(r1)
                r0 = await scena(sec=6, muti=[nome], **sc); x0 = campioni(r0)
                dd.append(db(rms(filtra(x1, sr, lo, hi)[int(sr):])) - db(rms(filtra(x0, sr, lo, hi)[int(sr):]))); st.append(f"{r1['stalli']}/{r1['letture']}")
                salva(cart, f"{nome}_acceso_{i + 1}", x1, sr)
            extra = f"; letture in stallo {st}" if nome == "gorgoglio" else ""
            chk(metro.tutti(d >= 2 for d in dd), f"{nome}: acceso contro spento, banda {lo}-{hi} Hz, {[round(d, 1) for d in dd]} dB (almeno +2){extra}")

        # ---- non satura: volume «alto», caso peggiore ----
        pp = []
        for i in range(3):
            r = await scena(20, 0, 0.3, sheet=1, sec=7, forza=["gabbiani", 0, 1], liv="alto"); pp.append(db(r["picco"])); salva(cart, f"alto_{i + 1}", campioni(r), sr)
        await pg.evaluate("() => suoniImposta('basso')")
        chk(metro.tutti(v <= -0.5 for v in pp), f"volume «alto», 20 nodi con la prua al vento e un gabbiano: picco {[round(v, 1) for v in pp]} dB (al più -0,5)")
        chk(not errs, f"errori della pagina {errs[:1]}")
        await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad or n_casi == 0 else 0)
asyncio.run(main())
