# Collaudo «guardiano» degli avversari (docs/PROPOSTA-GUARDIANO-AVVERSARI.md, 10 novembre 2026; rifatto il 14 novembre, §8).
# Le 4 regate del torneo, principianti ed esperti, semi fissi, con la stessa corsa di misura_avversari_rotta.py; i numeri G1-G9
# contro tests/guardiano_avversari_rif.json, che contiene il riferimento (mediana di più corse con i sorteggi spostati) e le soglie
# (intervallo di quelle corse, mai sotto i minimi del §3). Dal 14 novembre è SOLO INFORMATIVO (§9: la contro-prova non è passata):
# segna «OLTRE IL RUMORE» ma esce con 0; esce con 2 se la misura non è valida. Quando suona, confronto regata per regata (§7).
# Uso: python tests/collaudo_guardiano_avversari.py                     # il collaudo
#      python tests/collaudo_guardiano_avversari.py --misura f.json     # salva numeri e regate senza giudicarli
#      python tests/collaudo_guardiano_avversari.py --giudica f.json [--semi N]   # giudica una misura salvata (i primi N semi)
#      python tests/collaudo_guardiano_avversari.py --rumore N f1.json f2.json ... [--scrivi] [--informativo]  # riferimento e soglie dalle corse
#                     salvate (SPOSTA diverso in ognuna), sui primi N semi: solo per un riferimento nuovo, da dire nel CHANGELOG
# Manopole come in misura_avversari_rotta.py (SPOSTA=k, DOWNE=off, RDIR=40, RLAY=100 con la patch, RADICE=copia del gioco).
# GUARD_DA e GUARD_A cambiano i semi; senza, si usano quelli del riferimento.
import asyncio, hashlib, json, os, pathlib, re, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from misura_avversari_rotta import js_corsa, URL
from playwright.async_api import async_playwright

RIF = pathlib.Path(__file__).resolve().parent / "guardiano_avversari_rif.json"
_rs = json.loads(RIF.read_text())["semi"] if RIF.exists() else [1491, 1502]
SEMI = range(int(os.environ.get("GUARD_DA", _rs[0])), int(os.environ.get("GUARD_A", _rs[1])) + 1)
PAGINE = 2
# minimi delle soglie (§3, scritti il 10 novembre prima di misurare): la soglia di un numero non scende mai sotto questi
MINIMI = {
    'G1 arrivo mediano (s)': lambda r: 1.0,
    'G2 bolina persi media (s)': lambda r: 0.5,
    'G3 poppa persi mediana (s)': lambda r: 0.3,
    'G4 lasco persi media (s)': lambda r: 0.5,
    'G5 contatti dopo il via': lambda r: max(0.10 * r, 3),
    'G6 boa toccata': lambda r: 3,
    'G6 boe sbagliate': lambda r: 2,
    'G7 non arrivati': lambda r: 1,
    'G7 squalificati': lambda r: 1,
    'G8 scuffiate': lambda r: 2,
    'G9 taglio mediano (s)': lambda r: 0.5,
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

def versione():
    return re.search(r'VERSIONE = "([^"]+)"', (pathlib.Path(os.environ.get("RADICE") or RIF.parent.parent) / "js" / "gioco.js").read_text()).group(1)

def giudica(N, rif, intest):
    print(intest)
    print("identico al riferimento al bit: " + ("sì" if N["(info) impronta"] == rif["numeri"].get("(info) impronta") else "no (normale: il riferimento è una mediana)"))
    male = []
    for nome, v in N.items():
        if nome in ("(info) impronta", "(info) regate"): continue
        r = rif["numeri"][nome]; d = v - r; s = rif["soglie"].get(nome)
        esito = "" if s is None else (("  OLTRE IL RUMORE" if rif.get("informativo") else "  PEGGIORA OLTRE LA SOGLIA") if d > s + 1e-9 else "  ok")
        if s is not None and d > s + 1e-9: male.append(nome)
        print(f"  {nome:48s} {r:9.2f} -> {v:9.2f}  ({d:+.2f}{'' if s is None else f', soglia +{s:g}'}){esito}")
    if rif.get("informativo"):   # §8: la contro-prova non è passata né con 12 né con 24 semi, quindi il guardiano non boccia
        print("ESITO: OK (solo informativo, PROPOSTA-GUARDIANO-AVVERSARI.md §9" + ("; oltre il rumore: " + ", ".join(male) if male else "") + ")"); return []
    print("ESITO: " + ("OK" if not male else "FALLITO (" + ", ".join(male) + ")"))
    return male

def rumore(n, files):
    D = [json.loads(pathlib.Path(f).read_text()) for f in files]
    tieni = lambda d: [r for r in d["regate"] if r["seme"] < d["semi"][0] + n]
    NN = [numeri(tieni(d)) for d in D]
    imp = [x["(info) impronta"] for x in NN]
    if len(set(imp)) != len(imp): print(f"NON VALIDO (Q4): corse con la stessa impronta {imp}"); sys.exit(2)
    if any(len(tieni(d)) != 8 * n for d in D): print("NON VALIDO (Q4): regate mancanti"); sys.exit(2)
    med, soglie = {}, {}
    for nome in NN[0]:
        if nome in ("(info) impronta",): continue
        v = [x[nome] for x in NN]; med[nome] = statistics.median(v)
        if nome in MINIMI:
            soglie[nome] = round(max(max(v) - min(v), MINIMI[nome](med[nome])), 3)
            print(f"  {nome:48s} mediana {med[nome]:8.2f}  da {min(v):8.2f} a {max(v):8.2f}  intervallo {max(v) - min(v):6.2f}  soglia +{soglie[nome]:g}")
    med["(info) impronta"] = "mediana"
    s0 = D[0]["semi"][0]
    out = {"versione": D[0]["versione"], "semi": [s0, s0 + n - 1], "corse": [d.get("sposta") for d in D], "informativo": "--informativo" in sys.argv, "numeri": med, "soglie": soglie}
    if "--scrivi" in sys.argv: RIF.write_text(json.dumps(out, indent=1) + "\n"); print(f"riferimento riscritto ({out['versione']}, {n} semi, {len(D)} corse)")
    return out

def main():
    if "--rumore" in sys.argv:
        i = sys.argv.index("--rumore"); rumore(int(sys.argv[i + 1]), [f for f in sys.argv[i + 2:] if not f.startswith("--")]); return
    rif = json.loads(RIF.read_text())
    if "--giudica" in sys.argv:
        d = json.loads(pathlib.Path(sys.argv[sys.argv.index("--giudica") + 1]).read_text())
        n = int(sys.argv[sys.argv.index("--semi") + 1]) if "--semi" in sys.argv else rif["semi"][1] - rif["semi"][0] + 1
        R = [r for r in d["regate"] if rif["semi"][0] <= r["seme"] < rif["semi"][0] + n]
        if len(R) != 8 * n or d["semi"][0] != rif["semi"][0]: print(f"NON VALIDO: {len(R)} regate su {8 * n}"); sys.exit(2)
        male = giudica(numeri(R), rif, f"Guardiano (misura salvata, {d['versione']}, sposta {d.get('sposta')}): {len(R)} regate, semi {rif['semi'][0]}-{rif['semi'][0] + n - 1}, contro il riferimento della {rif['versione']}")
        sys.exit(1 if male else 0)
    R, errori = asyncio.run(corri())
    if errori or len(R) != 8 * len(SEMI):
        print(f"NON VALIDO: {len(R)} regate su {8 * len(SEMI)}, errori della pagina {errori[:3]}"); sys.exit(2)
    N = numeri(R)
    if "--misura" in sys.argv:
        pathlib.Path(sys.argv[sys.argv.index("--misura") + 1]).write_text(json.dumps({"versione": versione(), "semi": [SEMI.start, SEMI.stop - 1], "sposta": int(os.environ.get("SPOSTA") or 0), "env": {k: os.environ[k] for k in ("DOWNE", "RLAY", "RDIR", "RADICE") if k in os.environ}, "numeri": N, "regate": R}))
        print(json.dumps(N, indent=1)); return
    male = giudica(N, rif, f"Guardiano degli avversari: {len(R)} regate del torneo, semi {SEMI.start}-{SEMI.stop - 1}, contro il riferimento della {rif['versione']}")
    sys.exit(1 if male else 0)

if __name__ == "__main__": main()
