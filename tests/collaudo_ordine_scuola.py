# Coerenza della scheda «La barca» (1.2.14, Ale, 6 novembre 2026: non usare cose prima di averle spiegate). Criteri scritti prima di cambiare i testi.
#  O1 ordine e numeri: lezioni 1-7 e prove nell'ordine nuovo; «Il timone che stalla» dopo «Spingere il boma» e prima della prova 3.
#  O2 ogni «lezione N» nei testi del gruppo punta alla lezione giusta (tabella RIMANDI: per ogni passo i numeri attesi, quindi anche nessun rimando in più o in meno).
#  O3 ogni parola, la prima volta che compare seguendo l'ordine del menu, sta in un testo che la spiega (tabella PAROLE); le 11 parole vanno trovate tutte.
#  O4 frasi che si contraddicevano: non ci sono più; ci sono quelle che le sostituiscono.
#  O5 «Ripartire» si completa come un giocatore: tenendo la freccia del poggiare e rilasciando verso il traverso, dopo Ricomincia, 5 semi su 5.
# Uso: BROWSER=firefox python collaudo_ordine_scuola.py
import asyncio, os, pathlib, re, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri() + "#collaudo"
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
ORDINE = ["Lezione 1 La barca e il vento", "Lezione 2 Il timone", "Lezione 3 Andature e mure", "Prova Al traverso", "Prova Lasco e poppa",
          "Lezione 4 Vento reale e apparente", "Lezione 5 Virata e strambata", "Lezione 6 Spingere il boma", "Lezione 7 Il timone che stalla", "Prova Risalire il vento", "Prova Il giro di boa"]
RIMANDI = {"1 Poggiare": ["2", "5"], "2 Barra sottovento: si orza": ["3"], "2 Tenere la rotta": ["10"], "2 Navigazione libera": ["3"], "3 Poppa": ["5", "8"], "3 Le mure": ["12"], "Lasco ": ["5"]}
PAROLE = {"bolina": "più vicina al vento", "lasco": "da dietro il fianco", "scuff": "rovescia", "sband": "inclin", "nodi": "1,85", "boe": "galleggiant", "rosa": "basso a sinistra",
          "vir": "attraversa il vento", "strambata": "boma", "orziera": "salire da sola", "abbrivio": "velocità che ha già"}
TESTI = """() => { const pulisci = t => (typeof t === "function" ? t() : t).replace(/<[^>]+>/g, ""), out = [];
  for (const [g, i] of GRUPPI[0][1]) {
    if (g === "m") { out.push(["Prova " + MISSIONS[i].title, "", MISSIONS[i].text]); continue; }
    const L = LESSONS[i]; openItem(["l", i]);
    L.steps.forEach((st, k) => { showStep(k); out.push([L.name + " " + L.title, st.title, [...st.text.map(pulisci), st.done ? pulisci(st.done) : ""].join(" ")]); }); }
  return out; }"""
MENU = """() => GRUPPI[0][1].map(([g, i]) => g === "m" ? "Prova " + MISSIONS[i].title : LESSONS[i].name + " " + LESSONS[i].title)"""
RIPARTI = """(seme) => { const sv = __sv, nn = a => ((a + 180) % 360 + 360) % 360 - 180; __seed(seme); sv.fast(0); sv.openItem(["l", 0]); sv.showStep(8); document.getElementById("lRetry").click();
  const su = (tipo, key) => dispatchEvent(new KeyboardEvent(tipo, { key, bubbles: true }));
  const vento = nn(sv.twd - sv.S.h) < 0, key = vento ? "ArrowLeft" : "ArrowRight"; let t = 0, giu = false;
  while (t < 60 * 60 && !sv.stepDone) { const twa = Math.abs(nn(sv.S.h - sv.twd));
    if (twa < 85 && !giu) { su("keydown", key); giu = true; } else if (twa >= 85 && giu) { su("keyup", key); giu = false; }
    sv.run(1 / 60, 1); t++; }
  if (giu) su("keyup", key); return [sv.stepDone, +(t / 60).toFixed(1)]; }"""
async def main():
    nome = os.environ.get("BROWSER", "chromium"); fall = []
    def chk(n, ok, msg):
        print(("ok  " if ok else "NO  ") + n + " " + msg)
        if not ok: fall.append(n)
    async with async_playwright() as p:
        b = await getattr(p, nome).launch(); errs = []
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.add_init_script(SEME); await pg.goto(URL); await pg.wait_for_timeout(300)
        m = await pg.evaluate(MENU); chk("O1", m == ORDINE, f"ordine: {m if m != ORDINE else 'come atteso'}")
        tx = await pg.evaluate(TESTI)
        rim = {}
        for chi, pas, q in tx:
            n = re.findall(r"\blezione (\d+)", q)
            if n: rim[chi.split()[1] + " " + pas] = n
        chk("O2", rim == RIMANDI, f"rimandi letti {sum(map(len, rim.values()))}, " + ("come attesi" if rim == RIMANDI else f"letti {rim}"))
        trovate, sb = 0, []
        for parola, spieg in PAROLE.items():
            pat = re.compile(r"\b" + parola, re.I)
            prima = next(((c, q, t) for c, q, t in tx if pat.search(t)), None)
            if prima is None: sb.append((parola, "mai")); continue
            trovate += 1
            if spieg not in prima[2]: sb.append((parola, prima[0], prima[1]))
        chk("O3", trovate == len(PAROLE) and not sb, f"parole trovate {trovate} su {len(PAROLE)}, senza spiegazione alla prima volta: {sb}")
        tutto = " ".join(t for _, _, t in tx)
        sorg = (pathlib.Path(__file__).resolve().parent.parent / "js" / "contenuti.js").read_text(encoding="utf-8")
        vietate = ["in alto a destra c'è la bussola", "Da qui la vela non si regola più", "Da qui la vela la regoli tu", "il timone non serve", "rosetta", "Consulta il glossario", "lasciandola a sinistra"]
        volute = ["In basso a destra c'è la bussola", "finché la barca si muove", "W e S", "sposta la barra verso il boma"]
        sb = [v for v in vietate if v in tutto] + ["manca: " + v for v in volute if v not in tutto] + ([ "vela a collo"] if "vela a collo" in sorg else []) + ([ "segnavento senza spiegazione"] if "dal segnavento" in sorg else [])
        chk("O4", not sb, f"frasi: {sb}")
        es = [await pg.evaluate(RIPARTI, s) for s in range(1, 6)]
        chk("O5", all(e[0] for e in es), f"Ripartire guidando con la freccia: {sum(e[0] for e in es)} su 5, secondi {[e[1] for e in es]}")
        chk("errori", not errs, str(errs[:1])); await b.close()
    print("ESITO", nome, "OK" if not fall else "FALLITO: " + ", ".join(fall)); sys.exit(1 if fall else 0)
asyncio.run(main())
