# Scheda dei rivali (1.2.30, docs/PROPOSTA-SCHEDA-RIVALI.md §3). Soglie scritte nella fermata 1.
#   S1 la guida non cambia: tornei interi col pilota a semi fissi, pagina nuova contro la pagina di riferimento (la 1.2.29, estratta da git):
#      tempi d'arrivo e penalità di tutte le barche, regata per regata, uguali al bit. Soglia: 40 tornei (160 regate), 0 differenze.
#   S2 la scheda dice il vero: ogni cella (arrivo, partenza, boa 1, contatto) confrontata con un calcolo fatto QUI, campionando a ogni passo lo stato
#      delle barche (leg, ocs) e leggendo i contatti dall'elenco delle penalità. Soglia: 0 celle sbagliate su almeno 160 regate; le celle
#      confrontate si contano per tipo e ognuna deve essere > 0 (il metro non deve dipendere da ciò che misura). Parità entro 0,05 s: non giudicate, contate.
#   S3 torneo a metà: pagina chiusa dopo la regata 2 e riaperta, scheda uguale.
# Uso: python collaudo_scheda_rivali.py [--semi N] [--rif cartella]   (la pagina di riferimento: git archive HEAD index.html js | tar -x -C cartella)
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
N = int(sys.argv[sys.argv.index("--semi") + 1]) if "--semi" in sys.argv else 40
RIF = (pathlib.Path(sys.argv[sys.argv.index("--rif") + 1]) / "index.html").as_uri() if "--rif" in sys.argv else None
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
errori = []
def no(m): errori.append(m); print("  NO  " + m, flush=True)

CORRI = """async () => {
  const sv = __sv, dt = 1 / 60;
  document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], camp = R.boats.map(() => ({ l: null, b: null, x: false }));
  const guarda = () => R.boats.forEach((b, i) => { const c = camp[i]; if (b.ocs) c.x = true; if (c.l === null && b.leg >= 1) c.l = R.t; if (c.b === null && b.leg >= 2) c.b = R.t; });
  let prev = null;
  while (R.t < 1500 && R.boats.some(b => b.fin === null && !b.dnf)){ if (me.fin === null && !me.dnf) sv.pilota(dt); sv.run(dt, 1); guarda(); }
  if (me.fin === null && !me.dnf) return { fallita: "pilota non arrivato" };
  const pen = R.penList.slice();
  document.getElementById("rTor").click();
  return { fin: R.boats.map(b => [b.fin, b.pp || 0, !!b.dnf, !!b.dsq]), camp, lim: R.torLim, pen, nomi: R.boats.map(b => b.name),
           dati: JSON.parse(JSON.stringify(sv.tor.ris[sv.tor.ris.length - 1])) };
}"""
SCHEDA = """() => { document.getElementById("torRivali").click();
  const out = [...document.querySelectorAll("#torBody .tor-sch")].map(d => ({ h: d.querySelector("h3").textContent,
    righe: [...d.querySelectorAll("tbody tr")].map(tr => [...tr.children].map(td => td.textContent)) }));
  document.getElementById("torIndietro").click(); return out; }"""

async def pagina(b, url):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650})
    pg = await ctx.new_page(); await pg.add_init_script(SEME)
    pg.on("pageerror", lambda e: errori.append("errore pagina: " + str(e)))
    pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(url + "#collaudo"); await pg.wait_for_timeout(150)
    return pg

async def torneo(pg, seme, scheda):
    await pg.evaluate("s => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); }", seme)
    reg = []
    for k in range(4):
        r = await pg.evaluate(CORRI)
        if "fallita" in r: no(f"seme {seme} regata {k + 1}: {r['fallita']}"); return reg
        if scheda: r["scheda"] = await pg.evaluate(SCHEDA)
        reg.append(r)
    return reg

CONTA = dict(arrivo=0, partenza=0, boa=0, contatto=0, fuori=0, davanti=0, dietro=0, colpa_sua=0, colpa_tua=0, ambigue=0, rinvii=0)
def atteso_e_confronto(seme, k, r):
    cam, fin, lim = r["camp"], r["fin"], r["lim"]
    valido = lambda i: fin[i][0] is not None and not fin[i][3] and fin[i][0] <= lim
    for n, sch in enumerate(r["scheda"]):
        i = n + 1; righe = {x[0]: x[1:] for x in sch["righe"]}
        cella = lambda t: righe[t][k] if len(righe[t]) > k else None
        # arrivo
        pos = 1 + sum(1 for j in range(len(fin)) if valido(j) and fin[j][0] < fin[i][0]) if valido(i) else 0
        att = f"{pos}°" if pos else "non arr."; CONTA["arrivo"] += 1
        if cella("Arrivo") != att: no(f"seme {seme} R{k+1} {sch['h']}: arrivo {cella('Arrivo')} invece di {att}")
        # partenza
        c, m = cam[i], cam[0]; CONTA["partenza"] += 1
        if c["x"]: att = "fuori linea"; CONTA["fuori"] += 1
        elif c["l"] is None: att = "–"
        elif m["l"] is None: att = "davanti"
        elif abs(c["l"] - m["l"]) < 0.05: att = None; CONTA["ambigue"] += 1
        else: att = "davanti" if c["l"] < m["l"] else "dietro"
        if att and cella("Partenza") != att: no(f"seme {seme} R{k+1} {sch['h']}: partenza {cella('Partenza')} invece di {att}")
        if att in ("davanti", "dietro"): CONTA[att] += 1
        # boa 1
        CONTA["boa"] += 1
        if c["b"] is None: att = "–"
        elif m["b"] is None: att = "davanti"
        elif abs(c["b"] - m["b"]) < 0.05: att = None; CONTA["ambigue"] += 1
        else: att = "davanti" if c["b"] < m["b"] else "dietro"
        if att and cella("Boa 1") != att: no(f"seme {seme} R{k+1} {sch['h']}: boa 1 {cella('Boa 1')} invece di {att}")
        # contatto: dall'elenco delle penalità (testo del gioco)
        nome = r["nomi"][i]; CONTA["contatto"] += 1
        t = any(p.startswith("Tu, contatto con la " + nome) for p in r["pen"]); s = any(p.startswith("La " + nome + ", contatto con te") for p in r["pen"])
        att = "–" if not (t or s) else (("colpa tua" if t else "") + (" e " if t and s else "") + ("colpa sua" if s else ""))
        CONTA["colpa_tua"] += t; CONTA["colpa_sua"] += s
        if cella("Contatto") != att: no(f"seme {seme} R{k+1} {sch['h']}: contatto {cella('Contatto')} invece di {att}")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        # S2 (e S1 se c'è il riferimento)
        diff = 0; reg_tot = 0
        pg = await pagina(b, BASE); pr = await pagina(b, RIF) if RIF else None
        for seme in range(1, N + 1):
            nuovo = await torneo(pg, seme, True)
            for k, r in enumerate(nuovo): atteso_e_confronto(seme, k, r); reg_tot += 1
            if pr:
                vecchio = await torneo(pr, seme, False)
                for k, (a, v) in enumerate(zip(nuovo, vecchio)):
                    if a["fin"] != v["fin"]: diff += 1; no(f"S1 seme {seme} R{k+1}: tempi diversi dalla pagina di riferimento")
            if seme % 5 == 0: print(f"  semi 1-{seme} fatti, {len(errori)} errori", flush=True)
            await pg.reload(); await pg.wait_for_timeout(100)
            if pr: await pr.reload(); await pr.wait_for_timeout(100)
        print(f"\nS2: {reg_tot} regate; celle confrontate {CONTA}")
        for tipo in ("arrivo", "partenza", "boa", "contatto", "fuori", "davanti", "dietro", "colpa_sua", "colpa_tua"):
            if CONTA[tipo] == 0: no(f"il controllo «{tipo}» non ha confrontato nessun caso: il metro non misura")
        if RIF: print(f"S1: {reg_tot} regate confrontate con il riferimento, {diff} differenze")
        else: print("S1: saltato (manca --rif)")
        # S3: pagina chiusa dopo la regata 2 e riaperta, scheda uguale
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); await pg.add_init_script(SEME)
        pg.on("pageerror", lambda e: errori.append("errore pagina: " + str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(150)
        await pg.evaluate("s => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); }", 7)
        for k in range(2): await pg.evaluate(CORRI)
        prima = await pg.evaluate(SCHEDA)
        await pg.reload(); await pg.wait_for_timeout(200)
        await pg.evaluate("() => { __sv.fast(0); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); }")
        dopo = await pg.evaluate(SCHEDA)
        print("S3:", "scheda uguale dopo la chiusura" if prima == dopo and prima else f"DIVERSA o vuota: {prima} / {dopo}")
        if prima != dopo or not prima: no("S3 la scheda cambia dopo la chiusura della pagina")
        await b.close()
    print("\nESITO:", "OK" if not errori else f"FALLITO ({len(errori)})")
asyncio.run(main())
