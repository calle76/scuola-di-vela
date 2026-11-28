# Voce 100: legge le uscite di misura_r100.py (versione «patch», con b.dProp) e conta i casi della regola 17 come scritto in LEGGIMI.md prima di misurare.
# Uso: python3 conta17.py patch.txt [altro.txt ...]
import json, sys
G17, DUE_L = 5, 8.4
for f in sys.argv[1:]:
    cont, regate = [], 0
    for r in open(f, encoding="utf-8"):
        if r.startswith("CONT "):
            _, s, k, j = r.split(" ", 3); e = json.loads(j); e["s"], e["k"] = int(s), int(k); cont.append(e)
        elif r.startswith("{"): regate += json.loads(r)["regate"]
    base = [e for e in cont if e["t"] >= 0 and e.get("st") and e.get("dietro") and e.get("lat0") is not None and e["lat0"] <= DUE_L and e.get("sott") != "Tu"]
    c17 = [e for e in base if e.get("sopra") is not None and e["sopra"] > G17]
    pil = [e for e in c17 if e["gn"] == "Tu"]
    print(f"{f}: {regate} regate, {len(cont)} contatti; tetto (senza la condizione sulla rotta propria) {len(base)}; casi 17 {len(c17)}, "
          f"di cui con colpa oggi al pilota {len(pil)} (1 ogni {regate / len(pil):.0f} regate)" if pil else f"{f}: {regate} regate, {len(cont)} contatti; tetto {len(base)}; casi 17 {len(c17)}, con colpa oggi al pilota 0")
    print("  regole della colpa oggi nei casi 17:", sorted({str(e['r']) for e in c17}), "| colpevole rivale sopravento:", sum(1 for e in c17 if e["gn"] != "Tu" and e["gn"] != e["sott"]),
          "| colpevole già la sottovento:", sum(1 for e in c17 if e["gn"] == e["sott"]))
    print("  sopra (gradi) nel tetto:", sorted(e["sopra"] for e in base if e.get("sopra") is not None))
