# Riepilogo di tests/misura_x4.py coi criteri di docs/PROPOSTA-COPPIE.md §16 (scritto prima di guardare i risultati).
# Uso: python3 tests/riepiloga_x4.py chromium.jsonl firefox.jsonl
import collections, json, pathlib, random, statistics, sys
src = (pathlib.Path(__file__).resolve().parent / "misura_x4.py").read_text()
G0 = {}; exec("import json, statistics, random\n" + src[src.index("def conta_riga"):src.index("def riepilogo")], G0); conta = G0["conta_riga"]
def carica(f):
    d = {}; righe = [json.loads(x) for x in open(f)]
    for r in righe: d[r["conf"], r["s"], r["k"]] = (conta(r), r)
    T = [s for s in sorted({k[1] for k in d}) if all((c, s, k) in d for c in ("off", "m4") for k in range(3))]
    return d, T, sum(r["err"] for r in righe)
def tot(d, c, T, f): return sum(d[c, s, k][0][f] for s in T for k in range(3))
def limiti(gr, f, n=4000):
    """gr: lista di (d, T). Ricampiona i tornei dentro ogni browser; rende aumento, 5% e 95%."""
    per = [{s: (tot(d, "off", [s], f), tot(d, "m4", [s], f)) for s in T} for d, T in gr]; G = random.Random(1); out = []
    a = sum(x for p in per for x, _ in p.values()); b = sum(y for p in per for _, y in p.values())
    for _ in range(n):
        x = y = 0
        for p in per:
            K = list(p)
            for _ in K:
                q = p[G.choice(K)]; x += q[0]; y += q[1]
        if x: out.append(y / x - 1)
    out.sort(); return a, b, (b / a - 1 if a else None), (out[int(.05 * len(out))] if out else None), (out[int(.95 * len(out))] if out else None)
def pc(x): return "-" if x is None else f"{100 * x:+.1f}%"
file = [carica(f) for f in sys.argv[1:]]
for f, (d, T, e) in zip(sys.argv[1:], file):
    print(f"\n{f}: {len(T)} tornei completi ({T[0]}-{T[-1]}), {3 * len(T)} regate per configurazione, errori di pagina {e}")
    for m in ("M1", "M2", "M3", "pil", "fuori", "nonarr", "piant", "copd"):
        a, b, q, lo, hi = limiti([(d, T)], m); print(f"  {m:7} {a:5} -> {b:5}  {pc(q):>8}   [{pc(lo)}, {pc(hi)}]")
    M4 = [statistics.median([t for s in T for k in range(3) for t in d[c, s, k][0]["arr"]]) for c in ("off", "m4")]
    print(f"  M4 arrivo mediano {M4[0]:.1f} -> {M4[1]:.1f} ({pc(M4[1] / M4[0] - 1)})")
    a1, b1 = tot(d, "off", T, "M1"), tot(d, "m4", T, "M1"); a2, b2 = tot(d, "off", T, "M2"), tot(d, "m4", T, "M2"); p0, p1 = tot(d, "off", T, "piant"), tot(d, "m4", T, "piant")
    print(f"  CRITERI del browser: M1 {'passa' if b1 <= .5 * a1 else 'NO'} | M2 {'non misurabile' if a2 < 15 else 'passa' if b2 <= .7 * a2 else 'NO'} | M4 {'passa' if M4[1] <= 1.02 * M4[0] else 'NO'} | piantati {'passa' if p1 <= p0 + 2 else 'NO'}")
    print(f"  soglie vecchie: M3 {'passa' if tot(d, 'm4', T, 'M3') <= tot(d, 'off', T, 'M3') else 'NO'} | fuori {'passa' if tot(d, 'm4', T, 'fuori') <= tot(d, 'off', T, 'fuori') + 2 else 'NO'} | non arrivati {'passa' if tot(d, 'm4', T, 'nonarr') <= tot(d, 'off', T, 'nonarr') + 2 else 'NO'}")
    for nome, resto in (("principianti", 1), ("esperti", 0)):
        TT = [s for s in T if s % 2 == resto]; print(f"  {nome}: " + ", ".join(f"{m} {tot(d, 'off', TT, m)}->{tot(d, 'm4', TT, m)}" for m in ("M1", "M3", "pil", "fuori", "nonarr")))
    for etic, chiave in (("regola", lambda c: c["r"]), ("quando", lambda c: "prima del via" if c["t"] < 0 else "primi 60 s" if c["t"] < 60 else "dopo"), ("vicino alla boa (12,6 m)", lambda c: c["dm"] < 12.6), ("colpa", lambda c: "pilota" if c["g"] == 0 else "rivale")):
        cc = {c: collections.Counter(str(chiave(x)) for s in T for k in range(3) for x in d[c, s, k][1]["log"]) for c in ("off", "m4")}
        print(f"  contatti per {etic}: " + ", ".join(f"{k} {cc['off'][k]}->{cc['m4'][k]}" for k in sorted(set(cc["off"]) | set(cc["m4"]))))
gr = [(d, T) for d, T, _ in file]
print(f"\nINSIEME, {sum(3 * len(T) for _, T in gr)} regate per configurazione (criterio: 95% al massimo +10%)")
for n, m in (("N1 contatti in tutto", "M3"), ("N2 fuori linea", "fuori"), ("N3 non arrivati", "nonarr")):
    a, b, q, lo, hi = limiti(gr, m); print(f"  {n:22} {a} -> {b}  {pc(q)}  [5% {pc(lo)}, 95% {pc(hi)}]  {'passa' if hi <= .10 else 'NO'}")
