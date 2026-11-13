# Collaudo dei nomi dei rivali e del giocatore (1.2.33, docs/PROPOSTA-RIVALI-E-SPONSOR.md §14, criteri M1-M3 e N1-N4).
# (Non è collaudo_nomi.py, che dalla 1.2.11 controlla i nomi delle lezioni.)
#   M1: 20 tornei (seme fisso ciascuno): tre nomi diversi della lista zonale; i nomi nella presentazione del torneo, nel testo prima della regata,
#       nella classifica della regata, in acqua (cognome), nella classifica del torneo e nella scheda dei rivali (titolo, storia, pulsanti)
#   M2-M3: 200 tornei creati di fila (senza correrli): ogni nome ha sempre gli stessi tratti; ogni nome compare fra il 20% e il 40% dei tornei
#   N1: il nome del giocatore in almeno 5 posti; N2: nome vuoto = «Tu»; N3: a fine regata 0 px di eccesso; N4: «<b>x</b>» resta testo
# Uso: python tests/collaudo_nomi_rivali.py [--tornei N]   (BROWSER=firefox per Firefox)
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri() + "#collaudo"
NT = int(sys.argv[sys.argv.index("--tornei") + 1]) if "--tornei" in sys.argv else 20
LISTA = ["Marta Ferraresi", "Davide Lunardi", "Irene Moretto", "Tommaso Brunelli", "Lucia Pavan", "Nicola Serafini", "Sara Fontana", "Pietro Gallo", "Elena Zanin", "Matteo Bortolin"]
NUOVO = """(seme) => { const sv = __sv; window.confirm = () => true;
  const semina = s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; };
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(seme); sv.torApri(); const intro = document.getElementById('torBody').textContent; document.getElementById('torGo').click();
  return { av: sv.tor.av.map(a => ({ nome: a.nome, tr: a.ai.tr })), intro }; }"""
CORSA = """(seme) => { const sv = __sv, dt = 1 / 60;
  const semina = s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; };
  sv.fast(0); semina(seme + 7); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, brief = R.brief, nomi = R.boats.map(b => b.name), etich = R.boats.map(b => b.etich || null);
  while (R.t < 1500 && R.phase !== 'done'){ if (R.boats[0].fin === null) sv.pilota(dt); sv.run(dt, 1); }
  for (let j = 0; j < 30; j++) sv.run(dt, 1);
  return { brief, nomi, etich }; }"""

async def main():
    nome = os.environ.get("BROWSER", "chromium"); falli = []; posti = set()
    async with async_playwright() as p:
        br = await getattr(p, nome).launch()
        pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE); await pg.wait_for_timeout(500)
        await pg.evaluate("() => { localStorage.clear(); }"); await pg.reload(); await pg.wait_for_timeout(500)
        # M2-M3: 200 tornei creati di fila
        tr, conta = {}, {n: 0 for n in LISTA}
        for t in range(200):
            r = await pg.evaluate(NUOVO, 5000 + t)
            nn = [a["nome"] for a in r["av"]]
            if len(set(nn)) != 3 or any(n not in LISTA for n in nn): falli.append(f"M1 torneo {t}: nomi {nn}")
            for a in r["av"]:
                conta[a["nome"]] += 1
                if a["nome"] in tr and tr[a["nome"]] != a["tr"]: falli.append(f"M2 {a['nome']}: tratti {a['tr']} invece di {tr[a['nome']]} (torneo {t})")
                tr.setdefault(a["nome"], a["tr"])
        for area in (0, 1):  # gruppo bilanciato (§15): per area 3 doti, 4 medie, 3 difetti
            v = sorted(tr[n][area] for n in tr)
            if len(tr) == 10 and v != [0, 0, 0, 1, 1, 1, 1, 2, 2, 2]: falli.append(f"M2 gruppo non bilanciato nell'area {area}: {v}")
        mai = [n for n in LISTA if conta[n] == 0]
        if mai: falli.append(f"M2 non misurato: mai comparsi {mai}")
        fuori = {n: c for n, c in conta.items() if not 40 <= c <= 80}
        if fuori: falli.append(f"M3 fuori dal 20-40% su 200 tornei: {fuori}")
        print(f"  M2-M3: 200 tornei; presenze {conta}; tratti {tr}", flush=True)
        # M1, N1, N2, N3, N4: tornei corsi (una regata ciascuno)
        for t in range(NT):
            gioc = ["", "Ale", "<b>x</b>", "Nome Lungo Ventichar"][t % 4]
            await pg.evaluate("v => __sv.nomeSet(v)", gioc)
            r = await pg.evaluate(NUOVO, 6000 + t); nn = [a["nome"] for a in r["av"]]
            for k, n in enumerate(nn):
                if n + " (barca " + ["rossa", "verde", "blu"][k] + ")" not in r["intro"]: falli.append(f"M1 t{t}: presentazione senza «{n} (barca …)»")
            c = await pg.evaluate(CORSA, 6000 + t)
            for k, n in enumerate(nn):
                if c["nomi"][k + 1] != n: falli.append(f"M1 t{t}: in regata la barca {k} si chiama {c['nomi'][k + 1]} invece di {n}")
                if c["etich"][k + 1] != n.split(" ")[-1]: falli.append(f"M1 t{t}: in acqua {c['etich'][k + 1]} invece del cognome")
                if n not in c["brief"]: falli.append(f"M1 t{t}: testo prima della regata senza {n}")
            await pg.wait_for_timeout(400)
            atteso = gioc.strip() or "Tu"
            if c["nomi"][0] != atteso: falli.append(f"N1/N2 t{t}: in regata il giocatore è {c['nomi'][0]!r} invece di {atteso!r}")
            ecc = await pg.evaluate("() => { const p = document.querySelector('.panel'); return Math.max(document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight, p.scrollWidth - p.clientWidth, 0); }")
            if ecc > 0: falli.append(f"N3 t{t}: a fine regata {ecc} px di eccesso (giocatore {gioc!r})")
            st = await pg.evaluate("() => ({ html: document.getElementById('standings').innerHTML, txt: document.getElementById('standings').textContent, fin: document.getElementById('finList').textContent })")
            if atteso not in st["txt"]: falli.append(f"N1 t{t}: classifica della regata senza {atteso!r}")
            else: posti.add("classifica della regata")
            if atteso in st["fin"]: posti.add("schermata finale")
            if "<b>x</b>" in gioc and "&lt;b&gt;x&lt;/b&gt;" not in st["html"]: falli.append(f"N4 t{t}: nella classifica della regata il nome non è testo")
            for n in nn:
                if n not in st["txt"]: falli.append(f"M1 t{t}: classifica della regata senza {n}")
            await pg.click("#finTor"); await pg.wait_for_timeout(300)
            tb = await pg.evaluate("() => ({ txt: document.getElementById('torBody').textContent, html: document.getElementById('torBody').innerHTML })")
            if atteso not in tb["txt"]: falli.append(f"N1 t{t}: classifica del torneo senza {atteso!r}")
            else: posti.add("classifica del torneo")
            if "<b>x</b>" in gioc and "&lt;b&gt;x&lt;/b&gt;" not in tb["html"]: falli.append(f"N4 t{t}: classifica del torneo, nome non testo")
            for n in nn:
                if n not in tb["txt"]: falli.append(f"M1 t{t}: classifica del torneo senza {n}")
            await pg.click("#torRivali"); await pg.wait_for_timeout(200)
            for k, n in enumerate(nn):
                await pg.click(f".tor-ling >> nth={k}"); await pg.wait_for_timeout(100)
                s = await pg.evaluate("() => { const v = [...document.querySelectorAll('.tor-sch')].find(x => !x.hidden); return { h3: v.querySelector('h3').textContent, storia: (v.querySelector('.tor-storia') || {}).textContent || '', bott: document.querySelectorAll('.tor-ling')[%d].textContent }; }" % k)
                if not s["h3"].startswith(n) or "barca " + ["rossa", "verde", "blu"][k] not in s["storia"] or s["bott"] != n or len(s["storia"]) < 15:
                    falli.append(f"M1 t{t}: scheda {k} {s} per {n}")
            await pg.click("#torIndietro"); await pg.wait_for_timeout(100)
            await pg.evaluate("() => document.getElementById('torDlg').close()")
            if t % 4 == 1:  # registrazione e libretto, col nome «Ale»
                testo = await pg.evaluate("() => { const P = regPezzi.slice().sort((a, b) => b.reg - a.reg || b.n - a.n); return P.length ? P[0].testo : ''; }")
                righe = [r for r in testo.splitlines() if r.startswith(("B ", "F "))]
                if any(len(r.split(" ")) < 3 or r.split(" ")[2] not in ("Tu", "Rossa", "Verde", "Blu") for r in righe) or not righe: falli.append(f"registrazione t{t}: righe B/F con nomi diversi dal solito o assenti ({len(righe)} righe)")
                if "# giocatore: Ale" in testo: posti.add("registrazione")
                else: falli.append(f"N1 t{t}: intestazione della registrazione senza il nome ({testo[:200]!r})")
                lib = await pg.evaluate("() => { const d = document.createElement('div'); d.innerHTML = librettoHtml(); return d.querySelector('h2').textContent; }")
                if lib == "Libretto di Ale": posti.add("libretto")
                else: falli.append(f"N1 t{t}: libretto {lib!r}")
            print(f"  t{t}: giocatore {gioc!r}, rivali {nn}", flush=True)
        # torneo pulito alla fine
        await pg.evaluate("() => { window.confirm = () => true; if (__sv.tor){ __sv.torApri(); document.getElementById('torRit').click(); } __sv.nomeSet(''); }")
        await br.close()
    if len(posti) < 5: falli.append(f"N1: il nome compare solo in {len(posti)} posti: {sorted(posti)}")
    if errs: falli.append(f"errori della pagina: {errs[:3]}")
    print(f"{nome}: posti del nome {sorted(posti)}; " + ("ESITO: OK" if not falli else "FALLITO"))
    for x in falli[:40]: print("  ", x)
    sys.exit(0 if not falli else 1)
asyncio.run(main())
