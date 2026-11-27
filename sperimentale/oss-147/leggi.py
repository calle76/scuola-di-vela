# Legge le uscite di misura_r16.py (giro «Misura»): python3 leggi.py gioco.txt prova.txt
# K1 contatti con colpa di un rivale per le regole 15-16; K2 contatti in tutto; K3 bolina degli esperti (semi pari) barca per barca e M4 (mediana delle mediane dei pezzi, approssimazione dichiarata); K5 coppie dopo il via
import json, statistics, sys

def leggi(f):
    d = {"cont": [], "bol": {}, "json": []}
    for r in open(f, encoding="utf-8"):
        r = r.strip()
        if r.startswith("CONT "):
            _, s, k, j = r.split(" ", 3); e = json.loads(j); e["s"], e["k"] = int(s), int(k); d["cont"].append(e)
        elif r.startswith("BOL "):
            p = r.split(" ", 3); s, k = int(p[1]), int(p[2]); bol = json.loads(p[3].split("] [")[0] + "]") if "] [" in p[3] else json.loads(p[3])
            d["bol"][(s, k)] = bol
        elif r.startswith("{"):
            d["json"].append(json.loads(r))
    return d

def riass(d, nome):
    c = d["cont"]; r1516 = [e for e in c if e["riv"] and e["r"] in (15, 16)]
    r16ced = [e for e in r1516 if e["ced"]]
    esp = [t for (s, k), v in d["bol"].items() if s % 2 == 0 for t in v if t is not None]
    print(f"{nome}: regate {sum(j['regate'] for j in d['json'])}, contatti {len(c)} (dai pezzi: {sum(j['M3'] for j in d['json'])}), rivale colpevole per 15-16: {len(r1516)} (di cui la guida sapeva di cedere: {len(r16ced)}; entro 30 m dalla boa: {sum(1 for e in r1516 if (e['dm'] or 1e9) < 30)})")
    print(f"   coppie dopo il via {sum(j['coppie_dopo_via'] for j in d['json'])}, M4 mediana dei pezzi {statistics.median(j['M4'] for j in d['json'] if j['M4'])}, non arrivati {sum(j['non_arrivati'] for j in d['json'])}, piantati {sum(j['piantati'] for j in d['json'])}, bolina esperti mediana {statistics.median(esp):.1f} s ({len(esp)})")
    return r1516

g, p = leggi(sys.argv[1]), leggi(sys.argv[2])
a = riass(g, "gioco"); b = riass(p, "prova")
diff = [y - x for key in g["bol"] if key[0] % 2 == 0 and key in p["bol"] for x, y in zip(g["bol"][key], p["bol"][key]) if x is not None and y is not None]
print(f"bolina esperti barca per barca: mediana {statistics.median(diff):+.1f} s, media {statistics.mean(diff):+.2f} s ({len(diff)} barche)")
for nome, l in (("gioco", a), ("prova", b)):
    print(nome, "casi 15-16:", [(e["s"], e["k"], round(e["t"]), e["r"], e["leg"], e["twa"], e["gir"], round(e["dm"] or 0)) for e in l][:40])
