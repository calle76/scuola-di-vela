# Legge le uscite di misura_r17.py (giro «Misura», allegato misura-tutto): python3 leggi.py gioco.txt patch.txt
# Criteri 2 e 5 di docs/PROPOSTA-REGOLA-17.md: contatti in tutto (max +5%), con colpa del giocatore pilota (invariati o in calo), arrivo mediano dei rivali (M4, mediana
# delle mediane dei pezzi, approssimazione dichiarata come in oss-147; max +2 s), bolina degli esperti (semi pari) barca per barca (mediana max +2 s), coppie dopo il via (max +20%),
# partenze anticipate («fuori», rivali oltre la linea allo sparo; max +10%); strumento: contatti dopo il via con le stesse mure e la barca sottovento arrivata da dietro nei 30 s prima.
import json, statistics, sys

def leggi(f):
    d = {"cont": [], "bol": {}, "json": []}
    for r in open(f, encoding="utf-8"):
        r = r.strip()
        if r.startswith("CONT "):
            _, s, k, j = r.split(" ", 3); e = json.loads(j); e["s"], e["k"] = int(s), int(k); d["cont"].append(e)
        elif r.startswith("BOL "):
            p = r.split(" ", 3); s, k = int(p[1]), int(p[2]); d["bol"][(s, k)] = json.loads(p[3].split("] [")[0] + "]") if "] [" in p[3] else json.loads(p[3])
        elif r.startswith("{"):
            d["json"].append(json.loads(r))
    return d

def riass(d, nome):
    c = d["cont"]; J = d["json"]
    sorp = [e for e in c if e["t"] >= 0 and e.get("st") and e.get("dietro")]
    esp = [t for (s, k), v in d["bol"].items() if s % 2 == 0 for t in v if t is not None]
    out = {"regate": sum(j["regate"] for j in J), "contatti": len(c), "colpa_pilota": sum(1 for e in c if not e["riv"]), "colpa_rivale": sum(1 for e in c if e["riv"]),
           "M4": statistics.median(j["M4"] for j in J if j["M4"]), "coppie_dopo_via": sum(j["coppie_dopo_via"] for j in J), "fuori": sum(j["fuori"] for j in J),
           "non_arrivati": sum(j["non_arrivati"] for j in J), "piantati": sum(j["piantati"] for j in J), "bolina_esperti": round(statistics.median(esp), 1),
           "sorpassi_sottovento": len(sorp), "di_cui_col_giocatore": sum(1 for e in sorp if "Tu" in (e["gn"], e["on"])), "di_cui_colpa_rivale": sum(1 for e in sorp if e["riv"])}
    print(nome, json.dumps(out, ensure_ascii=False))
    return out, sorp

g, a = riass(leggi(sys.argv[1]), "gioco"); p, b = riass(leggi(sys.argv[2]), "patch ")
G, P = leggi(sys.argv[1]), leggi(sys.argv[2])
diff = [y - x for key in G["bol"] if key[0] % 2 == 0 and key in P["bol"] for x, y in zip(G["bol"][key], P["bol"][key]) if x is not None and y is not None]
pc = lambda x, y: f"{(y - x) / x * 100:+.1f}%" if x else "n/d"
print(f"contatti {g['contatti']} -> {p['contatti']} ({pc(g['contatti'], p['contatti'])}, soglia +5%)")
print(f"colpa del pilota {g['colpa_pilota']} -> {p['colpa_pilota']} (soglia: non in aumento)")
print(f"arrivo mediano {g['M4']} -> {p['M4']} ({p['M4'] - g['M4']:+.1f} s, soglia +2 s)")
print(f"bolina esperti barca per barca: mediana {statistics.median(diff):+.1f} s, media {statistics.mean(diff):+.2f} s ({len(diff)} barche, soglia +2 s)")
print(f"coppie dopo il via {g['coppie_dopo_via']} -> {p['coppie_dopo_via']} ({pc(g['coppie_dopo_via'], p['coppie_dopo_via'])}, soglia +20%)")
print(f"fuori linea allo sparo {g['fuori']} -> {p['fuori']} ({pc(g['fuori'], p['fuori'])}, soglia +10%)")
print(f"strumento: sorpassi da sottovento con contatto {g['sorpassi_sottovento']} -> {p['sorpassi_sottovento']} (se il gioco ne ha meno di 10 i criteri sui contatti non distinguono)")
for nome, l in (("gioco", a), ("patch", b)):
    print(nome, "sorpassi:", [(e["s"], e["k"], round(e["t"]), e["r"], e["gn"], e["on"], e["sott"]) for e in l][:30])
