# Riassunto dell'uscita di misura_partenze_torneo.py: python3 -I tests/riassumi_partenze_torneo.py FILE.json [FILE2.json ...]
import json, sys, statistics as st
r = [x for f in sys.argv[1:] for x in json.load(open(f))]
q = [(x["seme"], x["k"], n, v) for x in r for n, v in x["crossQ"].items()]
fuori = [t for t in q if abs(t[3]) > 38]
reg = {(x["seme"], x["k"]) for x in r}; regf = {(t[0], t[1]) for t in fuori}
t = [v for x in r for v in x.get("crossT", {}).values()]
lenti = sum(1 for x in r if any(v > 0 for v in x["lenti"].values()))
print("regate %d · tagli misurati %d · oltre 3 m fuori %d (%.1f%%) · regate con almeno una %d (%.1f%%) · massimo %d m" % (
    len(reg), len(q), len(fuori), 100 * len(fuori) / max(1, len(q)), len(regf), 100 * len(regf) / len(reg), max(abs(t[3]) for t in q)))
print("tempo medio del taglio %.1f s · barca lenta alla boa 1 in %d regate (%.1f%%) · penalità per regata %.2f · non arrivati %d · boe girate male %d" % (
    st.mean(t) if t else float("nan"), lenti, 100 * lenti / len(r), st.mean(len(x.get("pen", [])) if isinstance(x.get("pen"), list) else x["pen"] for x in r),
    sum(x["dnf"] for x in r), sum(sum(1 for w in x["wm"] if w) for x in r)))
n = sum(len(x["gunQ"]) for x in r)
if r and r[0].get("gunU"):
    pre = sum(1 for x in r for u in x["gunU"] if u > 0.5)      # già oltre la linea allo sparo (partenza anticipata)
    mancano = n - len(q) - pre                                 # non hanno tagliato entro 90 s dopo lo sparo
    tardi = sum(1 for x in r for v in x["crossT"].values() if v > 20)
    print("barche %d · oltre la linea allo sparo %d (%.1f%%) · senza taglio entro 90 s %d (%.1f%%) · taglio dopo 20 s %d (%.1f%%)" % (n, pre, 100 * pre / n, mancano, 100 * mancano / n, tardi, 100 * tardi / n))
