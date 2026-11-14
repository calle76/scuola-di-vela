# Stagione del circuito zonale (1.2.36, docs/PROPOSTA-STAGIONE-ZONALE.md, soglie scritte nella fermata 1 e nella fermata 2 prima del codice).
#   Z1  tappe a numeri: semi 11-20 (10 gruppi di rivali mai guardati nella taratura di ST_B), 200 stagioni ciascuno, senza correre: ogni rivale vince
#       almeno 1 stagione su 200; in media chi ha dote in tutte e due le aree finisce davanti a chi ha difetto in tutte e due. (Semi 1-10: solo riportati.)
#   Z12 batterie: 200 stagioni nuove: la tua batteria ha 4 barche e ci sei tu; le altre differiscono al massimo di 1; ognuno in una batteria sola.
#   Z13 si incontrano tutti: nelle stesse 200 stagioni, in media almeno 8 dei 10 rivali corrono con te almeno una volta.
#   Z3  conti: in ogni tappa chiusa i posti sono 1..11 (somma 66) e il primo della classifica ha meno punti (o vince la parità con la regola scritta).
#   Z4  frasi vere: 20 stagioni intere chiuse con risultati del torneo scritti dal collaudo (320 regate col pilota sarebbero troppe per il PC: detto nella
#       fermata 2), passando da stChiudiTappa: ogni frase scritta si ricontrolla QUI sui dati salvati, 0 false; almeno una frase a fine stagione in 18 su 20.
#   Z5  salvataggio: pagina ricaricata dopo 2 tappe, stagione e circuito uguali; «Azzera i progressi» la cancella.
#   Z7  pannello: 0 px di eccesso a 1360x650 nelle finestre della stagione (presentazione, tappa, circuito con 3 frasi, stagione finita).
#   --pilota N: Z2 e Z14 su N tappe corse davvero col pilota (soglia: 20 tappe): la batteria nell'ordine della classifica del torneo mostrata,
#       e il vincitore scritto di ogni batteria = il primo di quella batteria nell'ordine della tappa.
#   --vera: pagina senza #collaudo in Chromium e Firefox: versione, finestra della stagione aperta e cominciata, 0 errori.
# Uso: python collaudo_stagione.py [--pilota N] [--vera] [--solo-pilota]
import asyncio, json, pathlib, re, sys
from playwright.async_api import async_playwright
QUI = pathlib.Path(__file__).resolve().parent
BASE = (QUI.parent / "index.html").as_uri()
PIL = int(sys.argv[sys.argv.index("--pilota") + 1]) if "--pilota" in sys.argv else 0
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
errori = []
def no(m): errori.append(m); print("  NO  " + m, flush=True)

async def pagina(b, url, coll=True):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650})
    pg = await ctx.new_page(); await pg.add_init_script(SEME)
    pg.on("pageerror", lambda e: errori.append("errore pagina: " + str(e)) or print("  NO  errore pagina:", e, flush=True))
    pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(url + ("#collaudo" if coll else "")); await pg.wait_for_timeout(200)
    return pg

# --- Z1: 200 stagioni a numeri per gruppo, con le funzioni del gioco (stEstrai, stClassifica) ---
Z1 = """seme => { const sv = __sv; __seed(seme); sv.progress.rivali = {}; sv.st.forza("Sara Fontana"); // nasce il gruppo
  const ids = ["*", ...Object.keys(sv.progress.rivali)], f = Object.fromEntries(ids.map(id => [id, sv.st.forza(id)])), vinte = Object.fromEntries(ids.map(id => [id, 0]));
  const pt2 = [0, 0], ptm2 = [0, 0];
  for (let k = 0; k < 200; k++){
    const S = { tappe: [0, 1, 2, 3].map(() => ({ bat: [ids.slice(0, 4), ids.slice(4, 8), ids.slice(8)], ord: sv.st.estrai(ids) })) };
    const cl = sv.st.classifica(S); vinte[cl[0].id]++;
    cl.forEach(x => { if (f[x.id] === 2 && x.id !== "*"){ pt2[0] += x.tot; pt2[1]++; } if (f[x.id] === -2){ ptm2[0] += x.tot; ptm2[1]++; } });
  }
  return { f, vinte, pt2, ptm2 }; }"""

# --- Z12/Z13: batterie ---
Z12 = """() => { const sv = __sv; const out = { male: [], visti: 0 };
  for (let k = 0; k < 200; k++){ __seed(5000 + k); sv.progress.rivali = {}; const S = sv.st.nuova(), v = new Set();
    S.tappe.forEach((t, j) => { const L = t.bat.map(b => b.length), tutti = t.bat.flat();
      if (t.bat[0].length !== 4 || t.bat[0][0] !== "*") out.male.push([k, j, "la tua", t.bat[0]]);
      if (Math.max(...L.slice(1)) - Math.min(...L.slice(1)) > 1 || tutti.length !== 11 || new Set(tutti).size !== 11) out.male.push([k, j, L]);
      t.bat[0].slice(1).forEach(n => v.add(n)); });
    out.visti += v.size; }
  out.visti /= 200; return out; }"""

# --- una stagione intera chiusa con risultati scritti qui; restituisce la stagione salvata e le frasi dopo ogni tappa ---
STAGIONE_FINTA = """(seme, quante = 4) => { const sv = __sv; __seed(seme); sv.progress.rivali = {}; delete sv.progress.stagione;
  const S = sv.st.nuova(); sv.progress.stagione = S; const frasi = [], viste = [];
  for (let j = 0; j < quante; j++){
    const tp = S.tappe[j], av = tp.bat[0].slice(1).map(nome => ({ nome }));
    const ris = [0, 1, 2, 3].map(() => [0, 1, 2, 3].map(i => { const x = { fin: Math.random() < 0.05 ? null : Math.round((600 + Math.random() * 120) * 10) / 10, pp: 0 };
      if (i && Math.random() < 0.3) x.c = Math.random() < 0.5 ? "s" : "t"; return x; }));
    sv.st.chiudi({ av, ris, st: j });
    frasi.push(sv.st.frasi(S));
    sv.st.mostra("", false); viste.push(document.getElementById("torBody").innerText);
  }
  return { S: JSON.parse(JSON.stringify(S)), frasi, viste, nome: (localStorage.getItem("scuolaVelaSim.nome") || "") }; }"""

def classifica(S):   # ricalcolo QUI: punti = posto, parità: piazzamenti migliori, poi ultima tappa
    fatte = [t for t in S["tappe"] if t.get("ord")]
    ids = [x for b in S["tappe"][0]["bat"] for x in b]
    cl = [dict(id=i, p=[t["ord"].index(i) + 1 for t in fatte]) for i in ids]
    for x in cl: x["tot"] = sum(x["p"])
    return sorted(cl, key=lambda x: (x["tot"], sorted(x["p"]), list(reversed(x["p"]))))

def controlla_frasi(S, n, frasi, tag):
    T = dict(S); T["tappe"] = [dict(t) if k < n else {k2: v for k2, v in t.items() if k2 not in ("ord", "cont")} for k, t in enumerate(S["tappe"])]
    fatte = [t for t in T["tappe"] if t.get("ord")]; cl = classifica(T); riv = [x["id"] for x in cl if x["id"] != "*"]
    dav = lambda a, b: sum(1 for t in fatte if t["ord"].index(a) < t["ord"].index(b))
    tipi = 0
    for f in frasi:
        if m := re.fullmatch(r"La tua bestia nera: (.+), davanti a te in (\d+) tappe su (\d+)\.", f):
            x = m[1]; ok = int(m[2]) == int(m[3]) == n and dav(x, "*") == n and x == next(r for r in riv if dav(r, "*") == n); tipi |= 1
        elif m := re.fullmatch(r"Con (.+) ti sei toccato in (\d+) regate: colpa sua in (\d+), tua in (\d+)\.", f):
            x = m[1]; c = [sum(t.get("cont", {}).get(x, {}).get(k, 0) for t in fatte) for k in "nst"]; ok = c == [int(m[2]), int(m[3]), int(m[4])] and c[0] >= 2; tipi |= 2
        elif m := re.fullmatch(r"(?:Tu e (.+) vi giocate|(.+) e (.+) si giocano) il primo posto del circuito: (?:(\d+) punt[io] fra (?:voi|loro)|pari punti)\.", f):
            d = cl[1]["tot"] - cl[0]["tot"]; ids = {cl[0]["id"], cl[1]["id"]}
            nomi = {"*", m[1]} if m[1] else {m[2], m[3]}
            ok = n >= 2 and d <= 2 and ids == nomi and (int(m[4]) == d if m[4] else d == 0); tipi |= 4
        elif m := re.fullmatch(r"(.+) è in forma: tre podi di fila\.", f):
            ok = n >= 3 and all(t["ord"].index(m[1]) < 3 for t in fatte[-3:]); tipi |= 8
        elif m := re.fullmatch(r"Sei sempre arrivato davanti a (.+): (\d+) tappe su (\d+)\.", f):
            x = m[1]; ok = int(m[2]) == int(m[3]) == n and dav("*", x) == n and x == next(r for r in riv if dav("*", r) == n); tipi |= 16
        else: ok = False
        if not ok: no(f"{tag} tappa {n}: frase falsa o sconosciuta: {f}")
    if len(frasi) > 3: no(f"{tag} tappa {n}: {len(frasi)} frasi")
    return tipi

PANNELLO = """() => { const d = document.getElementById('torDlg'), q = document.getElementById('torBody'), r = d.getBoundingClientRect();
  const btn = [...q.querySelectorAll('.row button')].map(b => b.getBoundingClientRect().bottom);
  return { aperto: d.open, dentro: r.top >= 0 && r.bottom <= innerHeight, scorreRiquadro: d.scrollHeight - d.clientHeight, scorreContenuto: q.scrollHeight - q.clientHeight,
           larg: Math.max(d.scrollWidth - d.clientWidth, q.scrollWidth - q.clientWidth), pulsanti: btn.length && btn.every(b => b <= r.bottom && b <= innerHeight) }; }"""
def pannello(o, cosa):
    print(f"  Z7 {cosa}: {o}")
    if not o["aperto"] or not o["dentro"] or o["scorreRiquadro"] > 0 or o["scorreContenuto"] > 0 or o["larg"] > 0 or not o["pulsanti"]: no(f"Z7 {cosa}: {o}")

CORRI = """async () => { const sv = __sv, dt = 1 / 60;
  document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0];
  while (R.t < 1500 && R.boats.some(b => b.fin === null && !b.dnf)){ if (me.fin === null && !me.dnf) sv.pilota(dt); sv.run(dt, 1); }
  if (me.fin === null && !me.dnf) return { fallita: "pilota non arrivato" };
  document.getElementById("rTor").click(); return { ok: true }; }"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        if "--solo-pilota" not in sys.argv:
            pg = await pagina(b, BASE)
            await pg.evaluate("() => { __sv.fast(0); __sv.store = 'scuolaVelaSim.v1'; }")
            # Z1
            for gruppo, semi in (("taratura, semi 1-10 (solo riportati)", range(1, 11)), ("conferma, semi 11-20", range(11, 21))):
                minimo, p2, pm2 = 999, [0, 0], [0, 0]
                for s in semi:
                    r = await pg.evaluate(Z1, s)
                    mv = min(v for k, v in r["vinte"].items() if k != "*"); minimo = min(minimo, mv)
                    p2 = [p2[0] + r["pt2"][0], p2[1] + r["pt2"][1]]; pm2 = [pm2[0] + r["ptm2"][0], pm2[1] + r["ptm2"][1]]
                    if gruppo.startswith("conferma") and mv < 1: no(f"Z1 seme {s}: un rivale non vince mai ({r['vinte']}, forze {r['f']})")
                m2 = p2[0] / p2[1] if p2[1] else None; mm2 = pm2[0] / pm2[1] if pm2[1] else None
                print(f"Z1 {gruppo}: vittorie minime di un rivale su 200: {minimo}; punti medi a fine stagione: dote in tutte e due {m2 and round(m2, 1)} ({p2[1]} casi), difetto in tutte e due {mm2 and round(mm2, 1)} ({pm2[1]} casi)")
                if gruppo.startswith("conferma"):
                    if not p2[1] or not pm2[1]: no("Z1: nessun rivale con dote o difetto in tutte e due: il metro non misura")
                    elif m2 >= mm2: no("Z1: chi ha due doti non finisce davanti a chi ha due difetti")
            # Z12, Z13
            r = await pg.evaluate(Z12)
            print(f"Z12: batterie sbagliate {len(r['male'])} su 800 tappe; Z13: rivali incontrati in media {r['visti']} su 10")
            if r["male"]: no(f"Z12: {r['male'][:5]}")
            if r["visti"] < 8: no(f"Z13: {r['visti']} < 8")
            # Z3, Z4 (+ Z7 sul circuito)
            con_frase, tipi, nfrasi, peggio, peggio4 = 0, 0, 0, None, None
            for k in range(20):
                r = await pg.evaluate(STAGIONE_FINTA, 9000 + k); S = r["S"]
                for j, t in enumerate(S["tappe"]):
                    if sorted(t["ord"]) != sorted(x for bb in t["bat"] for x in bb) or len(t["ord"]) != 11: no(f"Z3 stagione {k} tappa {j}: ordine con {len(t['ord'])} concorrenti")
                cl = classifica(S)
                if sum(x["tot"] for x in cl) != 66 * 4: no(f"Z3 stagione {k}: somma {sum(x['tot'] for x in cl)} invece di 264")
                for j in range(4):
                    tipi |= controlla_frasi(S, j + 1, r["frasi"][j], f"Z4 stagione {k}"); nfrasi += len(r["frasi"][j])
                    # Z14 sul racconto delle batterie, letto dalla finestra
                    t = S["tappe"][j]
                    for i, col in enumerate(("gialla", "bianca", "arancione")):
                        primo = next(x for x in t["ord"] if x in t["bat"][i])
                        attesa = f"batteria {col}{' (la tua)' if i == 0 else ''}: {(r['nome'] or 'Tu') if primo == '*' else primo}"
                        if attesa not in r["viste"][j]: no(f"Z14 stagione {k} tappa {j}: manca «{attesa}»")
                    if j == 3 and S.get("fine", {}).get("pos") != [x["id"] for x in cl].index("*") + 1: no(f"Z3 stagione {k}: posto finale diverso dal ricalcolo")
                if r["frasi"][3]: con_frase += 1
                if len(r["frasi"][1]) == 3 and peggio is None: peggio = 9000 + k
                if len(r["frasi"][3]) == 3 and peggio4 is None: peggio4 = 9000 + k
            print(f"Z3: 80 tappe ricontrollate. Z4: {nfrasi} frasi controllate (tipi visti: {bin(tipi)}), stagioni con almeno una frase a fine stagione: {con_frase} su 20")
            if con_frase < 18: no(f"Z4: frasi in {con_frase} stagioni su 20 (< 18)")
            if nfrasi == 0: no("Z4: nessuna frase: il metro non misura")
            # Z7: le finestre della stagione nel caso peggiore che si trova (3 frasi dopo la tappa 2, il nome più lungo)
            await pg.evaluate("() => { localStorage.setItem('scuolaVelaSim.nome', 'Alessandro Massimiliano'); }")
            await pg.evaluate("() => { delete __sv.progress.stagione; delete __sv.progress.torneo; __sv.torApri(); }")
            await pg.evaluate("() => document.getElementById('stCirc').click()")
            pannello(await pg.evaluate(PANNELLO), "presentazione della stagione"); await pg.screenshot(path=str(QUI / "output" / "stagione_presentazione.png"))
            await pg.evaluate("() => document.getElementById('stInizia').click()")
            pannello(await pg.evaluate(PANNELLO), "tappa 1"); await pg.screenshot(path=str(QUI / "output" / "stagione_tappa1.png"))
            if peggio is not None:
                await pg.evaluate("""seme => { const sv = __sv; __seed(seme); sv.progress.rivali = {}; const S = sv.st.nuova(); sv.progress.stagione = S;
                  for (let j = 0; j < 2; j++){ const tp = S.tappe[j], av = tp.bat[0].slice(1).map(nome => ({ nome }));
                    const ris = [0, 1, 2, 3].map(() => [0, 1, 2, 3].map(i => { const x = { fin: Math.random() < 0.05 ? null : Math.round((600 + Math.random() * 120) * 10) / 10, pp: 0 };
                      if (i && Math.random() < 0.3) x.c = Math.random() < 0.5 ? "s" : "t"; return x; }));
                    sv.st.chiudi({ av, ris, st: j }); }
                  sv.torApri(); sv.st.mostra("", false); }""", peggio)
                pannello(await pg.evaluate(PANNELLO), "circuito dopo 2 tappe, 3 frasi"); await pg.screenshot(path=str(QUI / "output" / "stagione_circuito.png"))
            else: no("Z7: nessuna stagione con 3 frasi dopo la tappa 2: il caso peggiore non è stato provato")
            if peggio4 is None: no("Z7: nessuna stagione finita con 3 frasi: il caso peggiore non è stato provato")
            await pg.evaluate(STAGIONE_FINTA, peggio4 or 9000)
            await pg.evaluate("() => { __sv.st.mostra('', false); }")
            pannello(await pg.evaluate(PANNELLO), f"stagione finita, seme {peggio4}, 3 frasi"); await pg.screenshot(path=str(QUI / "output" / "stagione_finita.png"))
            # Z5
            await pg.evaluate("s => (" + STAGIONE_FINTA + ")(s, 2)", 9100)   # stChiudiTappa salva dopo ogni tappa, come nel gioco
            prima = await pg.evaluate("() => { __sv.torApri(); __sv.st.mostra('', false); return [JSON.stringify(__sv.progress.stagione), document.getElementById('torBody').innerText]; }")
            await pg.reload(); await pg.wait_for_timeout(300)
            dopo = await pg.evaluate("() => { __sv.fast(0); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); __sv.st.mostra('', false); return [JSON.stringify(__sv.progress.stagione), document.getElementById('torBody').innerText]; }")
            ok5 = prima == dopo and '"ord"' in prima[0]
            print("Z5 ricarica:", "stagione e circuito uguali" if ok5 else "DIVERSI")
            if not ok5: no(f"Z5: {prima[0][:200]} / {dopo[0][:200]}")
            via = await pg.evaluate("""() => { document.getElementById('torDlg').close(); __sv.showMenu ? __sv.showMenu() : null; const b = document.getElementById('resetProg'); if (!b) return 'manca il pulsante';
              b.click(); return __sv.progress.stagione === undefined ? 'cancellata' : 'ancora lì'; }""")
            print("Z5 azzera:", via)
            if via != "cancellata": no(f"Z5 azzera: {via}")
            await pg.close()
        # Z2, Z14 col pilota
        if PIL:
            pg = await pagina(b, BASE)
            fatte = 0; s = 0
            while fatte < PIL:
                s += 1
                await pg.evaluate("s => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; delete __sv.progress.stagione; delete __sv.progress.torneo; __sv.torApri(); document.getElementById('stCirc').click(); document.getElementById('stInizia').click(); }", 700 + s)
                for j in range(4):
                    if fatte >= PIL: break
                    for k in range(4):
                        await pg.evaluate("s => __seed(s)", (700 + s) * 100 + j * 10 + k)
                        r = await pg.evaluate(CORRI)
                        if "fallita" in r: no(f"seme {700 + s} tappa {j + 1} regata {k + 1}: {r['fallita']}"); break
                    tab = await pg.evaluate("() => [...document.querySelectorAll('#torBody table.tor tbody tr')].map(tr => tr.children[1].textContent)")
                    st = await pg.evaluate("() => JSON.parse(JSON.stringify(__sv.progress.stagione))")
                    tp = st["tappe"][j]; nome = await pg.evaluate("() => (localStorage.getItem('scuolaVelaSim.nome') || '').trim() || 'Tu'")
                    batt = [nome if x == "*" else x for x in tp["ord"] if x in tp["bat"][0]]
                    tabn = [re.sub(r" \(barca \w+\)$", "", x) for x in tab]
                    if batt != tabn: no(f"Z2 seme {700 + s} tappa {j + 1}: batteria {batt}, torneo {tabn}")
                    await pg.evaluate("() => document.getElementById('stCirc').click()")
                    vista = await pg.evaluate("() => document.getElementById('torBody').innerText")
                    for i, col in enumerate(("gialla", "bianca", "arancione")):
                        primo = next(x for x in tp["ord"] if x in tp["bat"][i])
                        att = f"batteria {col}{' (la tua)' if i == 0 else ''}: {nome if primo == '*' else primo}"
                        if att not in vista: no(f"Z14 seme {700 + s} tappa {j + 1}: manca «{att}»")
                    if j == 0 and s == 1:
                        pannello(await pg.evaluate(PANNELLO), "circuito dopo una tappa vera"); await pg.screenshot(path=str(QUI / "output" / "stagione_tappa_vera.png"))
                    await pg.evaluate("() => { document.getElementById('stIndietro').click(); document.getElementById('torMenu').click(); __sv.torApri(); }")
                    fatte += 1
                    print(f"  tappa {fatte}: batteria {batt}", flush=True)
            print(f"Z2/Z14: {fatte} tappe corse col pilota")
            await pg.close()
        await b.close()
        if "--vera" in sys.argv:
            for nome, bt in (("Chromium", p.chromium), ("Firefox", p.firefox)):
                br = await bt.launch(); n0 = len(errori)
                ctx = await br.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page()
                pg.on("pageerror", lambda e: errori.append(f"errore pagina {nome}: {e}")); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
                await pg.goto(BASE); await pg.wait_for_timeout(800)
                ver = await pg.evaluate("() => document.querySelector('.ver') && document.querySelector('.ver').textContent")
                await pg.evaluate("() => { const m = document.querySelector('#modoSel button[data-v=libero]'); m && m.click(); }")
                await pg.evaluate("() => document.getElementById('goTor').click()"); await pg.wait_for_timeout(100)
                await pg.evaluate("() => document.getElementById('stCirc').click()"); await pg.wait_for_timeout(100)
                await pg.evaluate("() => document.getElementById('stInizia').click()"); await pg.wait_for_timeout(100)
                tit = await pg.evaluate("() => document.getElementById('torTitle').textContent")
                o = await pg.evaluate(PANNELLO)
                print(f"pagina vera {nome}: {ver}, finestra «{tit}», {o}, errori {len(errori) - n0}")
                if tit != "Tappa 1 di 4" or len(errori) > n0: no(f"pagina vera {nome}: «{tit}»")
                await br.close()
    print("\nESITO:", "OK" if not errori else f"FALLITO ({len(errori)})")
asyncio.run(main())
