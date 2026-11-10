# Collaudo «guardiano» degli avversari (docs/PROPOSTA-GUARDIANO-AVVERSARI.md, 10 novembre 2026).
# Le 4 regate del torneo, principianti ed esperti, semi fissi, con la stessa corsa di misura_avversari_rotta.py; i numeri G1-G9
# contro tests/guardiano_avversari_rif.json: esce con 1 se uno peggiora oltre la sua soglia, 2 se la misura non è valida.
# Uso: python tests/collaudo_guardiano_avversari.py              # il collaudo
#      python tests/collaudo_guardiano_avversari.py --aggiorna   # riscrive il riferimento (solo per una modifica voluta, da dire nel CHANGELOG)
#      python tests/collaudo_guardiano_avversari.py --misura f.json   # salva i numeri senza giudicarli (per la scelta delle soglie)
# Manopole come in misura_avversari_rotta.py (DOWNE=off, RDIR=40, RLAY=100 con la patch, RADICE=copia del gioco): servono alla contro-prova.
import asyncio, hashlib, json, os, pathlib, re, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from misura_avversari_rotta import js_corsa, URL
from playwright.async_api import async_playwright

SEMI = range(int(os.environ.get("GUARD_DA", 1491)), int(os.environ.get("GUARD_A", 1502)) + 1)
RIF = pathlib.Path(__file__).resolve().parent / "guardiano_avversari_rif.json"
PAGINE = 2
# soglie: G-numero -> (nome, quanto può salire al massimo). Scelte con la regola del §3 della proposta (scritta prima di misurare)
# 10 novembre 2026, 1.2.24, semi 1491-1502 (proposta §6): due volte il peggioramento più grande di R_DIR 40 e 80, o il minimo del §3
SOGLIE = {
    'G1 arrivo mediano (s)': 1.78,
    'G2 bolina persi media (s)': 1.3,
    'G3 poppa persi mediana (s)': 1.51,
    'G4 lasco persi media (s)': 0.5,
    'G5 contatti dopo il via': 6,
    'G6 boa toccata': 18,
    'G6 boe sbagliate': 2,
    'G7 non arrivati': 1,
    'G7 squalificati': 1,
    'G8 scuffiate': 2,
    'G9 taglio mediano (s)': 0.5,
}

async def corri():
    lavori = [(k, liv, seme) for k in range(4) for liv in ("principianti", "esperti") for seme in SEMI]
    ris, errori = {}, []
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        async def pagina(parte):
            pg = await br.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errori.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(400)
            for n, (k, liv, seme) in enumerate(lavori):
                if n % PAGINE != parte: continue
                ris[(k, liv, seme)] = await pg.evaluate(js_corsa(os.environ), [k, liv, seme])
        await asyncio.gather(*(pagina(i) for i in range(PAGINE)))
        await br.close()
    return [{"reg": k, "liv": liv, "seme": seme, **ris[(k, liv, seme)]} for (k, liv, seme) in lavori if (k, liv, seme) in ris], errori

def numeri(R):
    lati = lambda tipo: [x for r in R for b in r["barche"] for x in b["lati"]
                         if (["bolina", "poppa"][x["lato"]] if r["reg"] % 2 == 0 else ["bolina", "lasco", "lasco"][x["lato"]]) == tipo]
    pers = lambda g: [x["vero"] - x["ott"] for x in g]
    ba = [b for r in R for b in r["barche"]]
    fin = [b["fin"] for b in ba if b["fin"] is not None and not b["dsq"]]
    tg = [b["taglio"] for b in ba if b["taglio"] is not None]
    M = [b["m40"] for b in ba if b.get("m40")]
    impronta = hashlib.sha1(json.dumps([[r["reg"], r["liv"], r["seme"], [b["fin"] for b in r["barche"]], r["contatti"]] for r in R]).encode()).hexdigest()[:12]
    return {
        "G1 arrivo mediano (s)": statistics.median(fin),
        "G2 bolina persi media (s)": statistics.mean(pers(lati("bolina"))),
        "G3 poppa persi mediana (s)": statistics.median(pers(lati("poppa"))),
        "G4 lasco persi media (s)": statistics.mean(pers(lati("lasco"))),
        "G5 contatti dopo il via": sum(r["contatti"] for r in R),
        "G6 boa toccata": sum(b["toccate"] for b in ba),
        "G6 boe sbagliate": sum(b["sbagliate"] for b in ba),
        "G7 non arrivati": sum(b["fin"] is None and not b["dsq"] for b in ba),
        "G7 squalificati": sum(b["dsq"] for b in ba),
        "G8 scuffiate": sum(b["scuffiate"] for b in ba),
        "G9 taglio mediano (s)": statistics.median(tg),
        "(info) virate per lato di bolina": statistics.mean(x["vir"] for x in lati("bolina")),
        "(info) ultimi 40 m dalla boa 1, persi media (s)": statistics.mean(m["vero"] - m["ott"] for m in M),
        "(info) regate": len(R), "(info) impronta": impronta,
    }

def main():
    R, errori = asyncio.run(corri())
    if errori or len(R) != 8 * len(SEMI):
        print(f"NON VALIDO: {len(R)} regate su {8 * len(SEMI)}, errori della pagina {errori[:3]}"); sys.exit(2)
    N = numeri(R)
    versione = re.search(r'VERSIONE = "([^"]+)"', (pathlib.Path(os.environ.get("RADICE") or RIF.parent.parent) / "js" / "gioco.js").read_text()).group(1)
    if "--misura" in sys.argv:
        pathlib.Path(sys.argv[sys.argv.index("--misura") + 1]).write_text(json.dumps({"versione": versione, "numeri": N}, indent=1)); print(json.dumps(N, indent=1)); return
    if "--aggiorna" in sys.argv:
        RIF.write_text(json.dumps({"versione": versione, "semi": [SEMI.start, SEMI.stop - 1], "numeri": N}, indent=1) + "\n"); print(f"riferimento riscritto ({versione})"); return
    rif = json.loads(RIF.read_text())
    print(f"Guardiano degli avversari: {len(R)} regate del torneo, semi {SEMI.start}-{SEMI.stop - 1}, contro il riferimento della {rif['versione']}")
    print("identico al riferimento al bit: " + ("sì" if N["(info) impronta"] == rif["numeri"]["(info) impronta"] else "no"))
    male = []
    for nome, v in N.items():
        if nome.startswith("(info) impronta") or nome == "(info) regate": continue
        r = rif["numeri"][nome]; d = v - r
        s = SOGLIE.get(nome) if SOGLIE else None
        esito = "" if s is None else ("  PEGGIORA OLTRE LA SOGLIA" if d > s + 1e-9 else "  ok")
        if esito.strip().startswith("PEGGIORA"): male.append(nome)
        print(f"  {nome:48s} {r:9.2f} -> {v:9.2f}  ({d:+.2f}{'' if s is None else f', soglia +{s:g}'}){esito}")
    if SOGLIE is None: print("ESITO: soglie non ancora scelte, solo numeri"); return
    print("ESITO: " + ("OK" if not male else "FALLITO (" + ", ".join(male) + ")")); sys.exit(1 if male else 0)

if __name__ == "__main__": main()
