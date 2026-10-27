# Esploratore: raccoglie dati, non promuove né boccia. Da lanciare più volte (anche per ore) con semi diversi e poi incollare il riepilogo.
# Non è in lancia_tutti.sh (il nome non comincia per collaudo_): è lungo e i suoi numeri non hanno soglie, li leggiamo insieme dopo.
# Parte 1 (sempre): pagina con #collaudo, passi fissi di 1/60 s, la barca del giocatore la guida __sv.pilota. Per ogni seme gira
#   ogni regata di RACES con avversari principianti ed esperti; ogni secondo simulato cerca numeri non finiti (NaN, Infinity) nello
#   stato di tutte le barche e conta i secondi senza cambio di tratto (barca «ferma»). Una riga JSON per corsa.
# Parte 2 (--scimmia N): pagina senza #collaudo, come la carica un giocatore, 1360x650; N secondi reali di tasti e clic a caso
#   (seme fisso), annotando errori della pagina e pagina che scorre (pixel in più di 1360x650).
#   Per ogni corsa annota anche versione del gioco e condizioni: carattere degli avversari, quanto gira il vento (gradi dal
#   vento iniziale, minimo e massimo), raffiche (quante al massimo insieme, la più forte), eccesso del pannello (ogni secondo, col momento e le righe del massimo).
#   La scimmia annota le ultime 30 azioni prima di ogni errore, per poterlo rifare.
# Uso: python esplora.py <primo seme> <ultimo seme> [--scimmia SECONDI]
#   es. python esplora.py 1 20            poi la volta dopo   python esplora.py 21 40 --scimmia 300
#      python esplora.py --scimmia 800    solo la scimmia, con un seme dei tasti nuovo ogni volta (scritto nel file)
#      python esplora.py --rigioca        rigioca le regate che avevano sforato il pannello + 100 di controllo, con il dettaglio dello sforamento\n#      python esplora.py --riassumi       riepilogo di TUTTI i file raccolti finora, diviso per versione del gioco
# Uscite: tests/output/esplora/<data-ora>.jsonl (tutto) e il riepilogo a schermo.
import asyncio, json, pathlib, random, statistics, sys, time
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
OUT = ROOT / "tests" / "output" / "esplora"; OUT.mkdir(parents=True, exist_ok=True)
FILE = OUT / (time.strftime("%Y%m%d-%H%M%S") + ".jsonl")
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""   # lo stesso generatore di collaudo_competizione.py

CORSA = """([race, seme, liv]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", race]);
  __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));   // riparte col seme
  const R = sv.R, me = R.boats[0], dt = 1 / 60;
  let visti = 0;   // numeri controllati: se resta 0 il controllo non ha misurato niente
  const nonFiniti = o => { const num = o ? Object.entries(o).filter(([k, v]) => typeof v === "number") : []; visti += num.length; return num.filter(([k, v]) => !isFinite(v)).map(([k]) => k); };
  const nan = new Set(), ferma = {}, ultimoTratto = {}, daQuando = {};
  let vMax = 0, n = 0, giroMin = 0, giroMax = 0, raffMax = 0, raffForte = 0, panMax = 0, panCaso = null;
  const twd0 = sv.twd, caratteri = R.boats.filter(b => !b.me).map(b => b.name + ":" + b.char);
  const pannello = () => { sv.panel(); const p = document.querySelector(".panel"), px = p ? p.scrollHeight - p.clientHeight : 0;
    if (px > panMax){ panMax = px;   // il momento del massimo sforamento: righe visibili (nome, altezza, inizio del testo) e stato
      panCaso = { t: Math.round(R.t), px, altezza: p.clientHeight, righe: [...p.children].filter(e => e.offsetParent).map(e => [e.id || e.className || e.tagName, e.offsetHeight, e.textContent.trim().replace(/\\s+/g, " ").slice(0, 50)]),
                  reg: Object.assign({}, sv.reg), scuffiata: !!sv.S.capsized }; } };
  const controlla = () => {
    const giro = ((sv.twd - twd0) % 360 + 540) % 360 - 180; giroMin = Math.min(giroMin, giro); giroMax = Math.max(giroMax, giro);
    const g = sv.gusts(); raffMax = Math.max(raffMax, g.length); g.forEach(x => raffForte = Math.max(raffForte, x[3]));
    pannello();   // ogni secondo (fino alla 1.0.35 ogni 10 s)
    R.boats.forEach(b => { nonFiniti(b.S).forEach(k => nan.add(b.name + "." + k));
      if (b.fin !== null || b.dnf) return;
      if (ultimoTratto[b.name] !== b.leg){ ultimoTratto[b.name] = b.leg; daQuando[b.name] = R.t; }
      ferma[b.name] = Math.max(ferma[b.name] || 0, Math.round(R.t - daQuando[b.name])); });
    vMax = Math.max(vMax, sv.S.u || 0);
  };
  while (me.fin === null && !me.dnf && R.t < 900){ sv.pilota(dt); sv.run(dt, 1); if (++n % 60 === 0) controlla(); }
  const reg = Object.assign({}, sv.reg), arrivo = me.fin;
  let k = 0; while (k < 60 * 400 && !R.boats.every(b => b.fin !== null || b.dnf)){ sv.run(dt, 1); if (++k % 60 === 0){ n += 60; controlla(); } }
  return { versione: typeof VERSIONE === "undefined" ? null : VERSIONE, caratteri, giroVento: [Math.round(giroMin), Math.round(giroMax)],
           raffiche: [raffMax, +raffForte.toFixed(2)], pannelloPx: panMax, pannelloCaso: panCaso, arrivo, ritirato: !!me.dnf, t: Math.round(R.t), vMax: +vMax.toFixed(2), reg, nan: [...nan].slice(0, 10), visti, fermaMax: ferma,
           barche: R.boats.map(b => [b.name, b.fin === null ? null : Math.round(b.fin), b.pen || 0, b.fin === null ? "tratto " + b.leg : ""]) };
}"""

def scrivi(riga):
    with open(FILE, "a", encoding="utf-8") as f: f.write(json.dumps(riga, ensure_ascii=False) + "\n")

async def parte1(b, semi, casi=None):
    pg = await b.new_page(viewport={"width": 1360, "height": 650}); await pg.add_init_script(SEME)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
    corse = []
    elenco = casi or [(seme, race, liv) for seme in semi for race in range(3) for liv in ("principianti", "esperti")]
    for seme, race, liv in elenco:
        if True:
            if True:
                prima = len(errs)
                try: r = await pg.evaluate(CORSA, [race, seme, liv])
                except Exception as e: r = {"eccezione": str(e)[:300]}
                r.update(seme=seme, race=race, liv=liv, errori=errs[prima:prima + 3]); corse.append(r); scrivi(r)
                print(f"seme {seme} regata {race} {liv}: arrivo {r.get('arrivo')} t={r.get('t')} nan={r.get('nan')} errori={len(r['errori'])}"
                      + (f" ECCEZIONE {r['eccezione'][:80]}" if "eccezione" in r else ""), flush=True)
    await pg.close()
    return corse

def rigioca(vecchie):
    """Le regate che avevano sforato il pannello + 100 che non sforavano (scelte con seme fisso), per rigiocarle con la registrazione nuova."""
    chiave = lambda c: (c["seme"], c["race"], c["liv"])
    r = [c for c in vecchie if "race" in c and "eccezione" not in c]
    sfora = sorted({chiave(c) for c in r if c.get("pannelloPx")}); altre = sorted({chiave(c) for c in r if not c.get("pannelloPx")} - set(sfora))
    return sfora, random.Random(1).sample(altre, min(100, len(altre)))

TASTI = ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Shift", "Space", "Enter", "Escape", "w", "s", "a", "d", "q", "e", "z", "x", "c", "v", "p", "h", "1", "2", "3", "Tab"]
async def parte2(b, secondi, seme):
    rnd = random.Random(seme)
    pg = await b.new_page(viewport={"width": 1360, "height": 650})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    await pg.goto(BASE); await pg.wait_for_timeout(500)
    sfori, azioni, fine, storia, casi = {}, 0, time.time() + secondi, [], []
    while time.time() < fine:
        nerr = len(errs)
        if rnd.random() < 0.15:   # clic su un pulsante visibile a caso (menu, istruzioni, fine prova)
            bott = await pg.query_selector_all("button:visible")
            if bott:
                x = rnd.choice(bott); storia.append("clic " + ((await x.inner_text()) or "?").strip()[:40])
                try: await x.click(timeout=500)
                except Exception: pass
        else:
            t, ms = rnd.choice(TASTI), rnd.randint(30, 1500); storia.append(f"{t} {ms} ms")
            await pg.keyboard.down(t); await pg.wait_for_timeout(ms); await pg.keyboard.up(t)
        azioni += 1; storia = storia[-30:]
        if len(errs) > nerr and len(casi) < 5: casi.append({"errore": errs[nerr][:200], "ultime_azioni": list(storia)})
        dw, dh, cosa = await pg.evaluate("""() => [document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight,
            [...document.querySelectorAll('h1,h2,.title')].filter(e => e.offsetParent).map(e => e.textContent.trim()).slice(0, 1).join('')]""")
        if dw > 0 or dh > 0: sfori[cosa[:60] or "?"] = max(sfori.get(cosa[:60] or "?", 0), dw, dh)
    r = {"scimmia": secondi, "seme": seme, "azioni": azioni, "errori": list(dict.fromkeys(errs))[:10], "sfori_px": sfori, "casi": casi,
         "versione": await pg.evaluate("typeof VERSIONE === 'undefined' ? null : VERSIONE")}; scrivi(r)
    await pg.close()
    return r

def riepilogo(righe):
    corse = [c for c in righe if "race" in c]; scim = [c for c in righe if "scimmia" in c]
    for ver in sorted({c.get("versione") or "?" for c in righe}):
        cv = [c for c in corse if (c.get("versione") or "?") == ver]; sv = [c for c in scim if (c.get("versione") or "?") == ver]
        semi = sorted({c["seme"] for c in cv})
        print(f"\n--- versione {ver}: {len(cv)} corse" + (f", {len(semi)} semi ({semi[0]}-{semi[-1]})" if semi else "") + f", {len(sv)} giri di scimmia")
        for race in range(3):
            for liv in ("principianti", "esperti"):
                g = [c for c in cv if c["race"] == race and c["liv"] == liv and "eccezione" not in c]
                if not g: continue
                arr = [c["arrivo"] for c in g if c["arrivo"] is not None]
                avv = [x for c in g for x in c["barche"][1:]]
                fin_avv = [x[1] for x in avv if x[1] is not None]
                reg = {}
                for c in g:
                    for k, v in (c["reg"] or {}).items():
                        if isinstance(v, (int, float)): reg[k] = round(reg.get(k, 0) + v, 1)
                ferma = max([v for c in g for v in c["fermaMax"].values()] or [0])
                lenti = sorted(g, key=lambda c: -(c["arrivo"] or 1e9))[:3]
                print(f"regata {race} {liv}: pilota arrivato {len(arr)}/{len(g)}"
                      + (f", mediana {statistics.median(arr):.0f} s (min {min(arr):.0f}, max {max(arr):.0f})" if arr else "")
                      + f"; avversari arrivati {len(fin_avv)}/{len(avv)}" + (f", mediana {statistics.median(fin_avv):.0f} s" if fin_avv else "")
                      + f", penalità {sum(x[2] for x in avv)}; secondi max senza cambio di tratto {ferma}"
                      + f"; pannello oltre di {max(c.get('pannelloPx', 0) for c in g)} px al massimo"
                      + f"; semi più lenti {[c['seme'] for c in lenti]}; registro del pilota {reg}")
        nan = [(c["seme"], c["race"], c["liv"], c["nan"]) for c in cv if c.get("nan")]
        ecc = [(c["seme"], c["race"], c["liv"], c["eccezione"][:100]) for c in cv if "eccezione" in c]
        err = list(dict.fromkeys(e for c in cv for e in c.get("errori", [])))
        bloc = [(c["seme"], c["race"], c["liv"], x[0], x[3]) for c in cv if "barche" in c for x in c["barche"] if x[1] is None]
        print(f"numeri non finiti: {len(nan)} corse {nan[:5]} (numeri controllati: {sum(c.get('visti', 0) for c in cv)})")
        print(f"barche non arrivate: {len(bloc)} {bloc[:5]}")
        print(f"eccezioni: {len(ecc)} {ecc[:3]}")
        print(f"errori della pagina (diversi): {len(err)} {err[:3]}")
        for s in sv:
            print(f"scimmia seme {s['seme']}, {s['scimmia']} s, {s['azioni']} azioni: errori {len(s['errori'])} {s['errori'][:3]}; pagina che scorre {s['sfori_px']}")

async def main():
    args = sys.argv[1:]
    if "--riassumi" in args:
        righe = [json.loads(l) for f in sorted(OUT.glob("*.jsonl")) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        print(f"===== RIEPILOGO DI TUTTI I FILE ({len(list(OUT.glob('*.jsonl')))} in {OUT.relative_to(ROOT)})"); riepilogo(righe); return
    if "--rigioca" in args:
        vecchie = [json.loads(l) for f in sorted(OUT.glob("*.jsonl")) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        px_prima = {(c["seme"], c["race"], c["liv"]): c.get("pannelloPx", 0) for c in vecchie if "race" in c}
        sfora, ctrl = rigioca(vecchie)
        async with async_playwright() as p:
            b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch(); nuove = await parte1(b, [], sfora + ctrl); await b.close()
        ns = {(c["seme"], c["race"], c["liv"]): c for c in nuove}
        print(f"\n===== RIGIOCATE: {len(sfora)} che sforavano + {len(ctrl)} di controllo")
        print("sforanti: prima -> ora (px)", [(k, px_prima[k], ns[k].get("pannelloPx")) for k in sfora if k in ns])
        print("tornate a sforare:", sum(1 for k in sfora if k in ns and ns[k].get("pannelloPx")), "su", len(sfora),
              "| controllo che ora sfora:", sum(1 for k in ctrl if k in ns and ns[k].get("pannelloPx")), "su", len(ctrl))
        for k in sfora:
            c = ns.get(k, {}).get("pannelloCaso")
            if c: print(k, json.dumps(c, ensure_ascii=False))
        return
    sc = 0
    if "--scimmia" in args: i = args.index("--scimmia"); sc = int(args[i + 1]); del args[i:i + 2]
    semi = list(range(int(args[0]), int(args[1]) + 1)) if len(args) >= 2 else ([] if sc else [1, 2, 3])
    t0 = time.time()
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        corse = await parte1(b, semi) if semi else []
        scim = await parte2(b, sc, semi[0] if semi else int(time.time()) % 100000) if sc else None
        await b.close()
    print(f"\n===== RIEPILOGO ESPLORA ({len(corse)} corse, {time.time() - t0:.0f} s reali) — dati in {FILE.relative_to(ROOT)}")
    riepilogo(corse + ([scim] if scim else []))

asyncio.run(main())
