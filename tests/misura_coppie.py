# Come nascono le coppie che si tengono (S8 di scene_strane.py, dopo il via): docs/PROPOSTA-COPPIE.md, parte sulla prevenzione. Non è un collaudo.
# Per ogni episodio S8 (n cede a x da almeno 10 s, entro 3 lunghezze, prue entro 20°) guarda i secondi prima che n cominciasse a cedere (t0).
# Categorie, scritte prima di guardare i numeri (8 novembre 2026):
#  A nata da una manovra: nei 10 s prima di t0 una delle due ha cambiato mure (virata o strambata) o ha cambiato lato (boa girata)
#  B prevedibile prima: niente manovra; a t0-5 s erano ad almeno 3 lunghezze e la previsione in linea retta da lì (15 s) passava sotto 2 lunghezze
#  C già vicine: niente manovra; a t0-5 s erano già sotto 3 lunghezze. Aggiunto dopo aver visto le 8 regate vere, prima del rigioco: «ripresa» se n cedeva
#    già a x nei 30 s prima (la stessa coppia che ricomincia), altrimenti «nuova»; e in A il passaggio della linea (lato 0 -> 1) si chiama «partenza», non «boa»
#  D il resto (niente manovra, lontane a t0-5 e la previsione da lì non vedeva il pericolo)
# Riporta anche: stesse mure o no a t0; chi delle due vira per prima dopo t0 (entro 40 s), e dopo quanto; previsione a 30 s da t0-10.
# Uso: python tests/misura_coppie.py file.txt [...]   (ogni argomento è una regata; i pezzi di una regata si uniscono con la virgola: pezzo-1.txt,pezzo-2.txt)
import collections, math, sys, statistics
import scene_strane as ss
L = 4.2

def vel(b): u = b["kn"] / 1.944; return math.sin(math.radians(b["h"])) * u, -math.cos(math.radians(b["h"])) * u

def prev(a, b, T):
    """distanza minima in linea retta entro T s, a prue e velocità costanti"""
    rx, ry = b["x"] - a["x"], b["y"] - a["y"]; (ax, ay), (bx, by) = vel(a), vel(b); wx, wy = bx - ax, by - ay; w2 = wx * wx + wy * wy
    t = 0 if w2 < 1e-6 else max(0, min(T, -(rx * wx + ry * wy) / w2)); return math.hypot(rx + wx * t, ry + wy * t)

def mure(b): return (b["twa"] > 0) - (b["twa"] < 0)

def episodi(righe):
    fot, _, _ = ss.leggi(righe); tempi = list(fot); es = [e for e in ss.scene(righe)[0] if e["s"] == "S8" and e["t"] >= 0]
    def a(t, n):  # fotogramma più vicino a t (entro 0,6 s) per la barca n
        i = min(range(len(tempi)), key=lambda k: abs(tempi[k] - t)) if tempi else None
        return fot[tempi[i]].get(n) if i is not None and abs(tempi[i] - t) <= 0.6 else None
    out = []
    for e in es:
        n, x = e["chi"]; t0 = e["t"]   # risale all'inizio del cedere (buchi fino a 1 s)
        ts = [t for t in tempi if t <= e["t"]]; k = len(ts) - 1
        while k > 0 and x in fot[ts[k - 1]].get(n, {}).get("cede", set()) and ts[k] - ts[k - 1] <= 1.01: k -= 1
        t0 = ts[k]
        bn, bx = a(t0, n), a(t0, x)
        if not bn or not bx: continue
        man = []
        for m in (n, x):
            prima = [fot[t][m] for t in tempi if t0 - 10 <= t <= t0 and m in fot[t]]
            if any(mure(p) and mure(q) and mure(p) != mure(q) for p, q in zip(prima, prima[1:])): man.append(f"{m} mure")
            for p, q in zip(prima, prima[1:]):
                if p["lato"] is not None and p["lato"] != q["lato"]: man.append(f"{m} {'partenza' if p['lato'] == 0 else 'boa'}"); break
        n5, x5 = a(t0 - 5, n), a(t0 - 5, x); n10, x10 = a(t0 - 10, n), a(t0 - 10, x)
        d5 = math.hypot(n5["x"] - x5["x"], n5["y"] - x5["y"]) if n5 and x5 else None
        p5 = prev(n5, x5, 15) if n5 and x5 else None; p10 = prev(n10, x10, 30) if n10 and x10 else None
        rip = any(x in fot[t].get(n, {}).get("cede", set()) for t in tempi if t0 - 30 <= t < t0 - 1.5)
        cat = "A" if man else ("D?" if d5 is None else ("C ripresa" if rip else "C nuova") if d5 < 3 * L else "B" if p5 < 2 * L else "D")
        primo = None   # chi cambia mure per primo dopo t0
        for t in [t for t in tempi if t0 < t <= t0 + 40]:
            for m in (n, x):
                p, q = a(t - 1, m), fot[t].get(m)
                if p and q and mure(p) and mure(q) and mure(p) != mure(q) and primo is None: primo = (m == n and "chi cede" or "chi ha la precedenza", round(t - t0, 1))
            if primo: break
        out.append(dict(t0=t0, n=n, x=x, cat=cat, man=man, stesse=mure(bn) == mure(bx), d0=math.hypot(bn["x"] - bx["x"], bn["y"] - bx["y"]), d5=d5, p5=p5, p10=p10, primo=primo, lato=bn["lato"], rip=rip))
    return out

def main():
    tutti = []
    for f in sys.argv[1:]:
        ep = episodi([r for g in f.split(",") for r in open(g, encoding="utf-8", errors="replace").read().splitlines()])
        for e in ep: e["file"] = f
        tutti += ep
    n = len(tutti); print(f"file {len(sys.argv) - 1}, episodi S8 dopo il via {n}")
    if not n: print("ATTENZIONE: nessun episodio, la misura non vale"); return
    c = collections.Counter(e["cat"] for e in tutti); print("categorie:", {k: f"{v} ({100 * v / n:.0f}%)" for k, v in sorted(c.items())})
    print("stesse mure a t0:", sum(e["stesse"] for e in tutti), "su", n, "| lato 1 (bolina):", sum(e["lato"] == 1 for e in tutti), "lato 2 (poppa):", sum(e["lato"] == 2 for e in tutti))
    man = collections.Counter(m.split()[1] + (" di chi cede" if m.split()[0] == e["n"] else " di chi ha la precedenza") for e in tutti for m in e["man"]); print("manovre in A:", dict(man))
    for k in sorted(c):
        g = [e for e in tutti if e["cat"] == k]; med = lambda v: f"{statistics.median(v):.1f}" if v else "-"
        print(f"  {k}: distanza a t0 mediana {med([e['d0'] for e in g])} m, a t0-5 {med([e['d5'] for e in g if e['d5'] is not None])} m; previsione 30 s da t0-10 sotto 2 L: {sum(1 for e in g if e['p10'] is not None and e['p10'] < 2 * L)} su {len(g)}")
    print("la stessa coppia si cedeva già nei 30 s prima:", {k: sum(e["rip"] for e in tutti if e["cat"] == k) for k in sorted(c)})
    print("cominciate entro 60 s dal via:", sum(e["t0"] < 60 for e in tutti), "su", n, {k: sum(e["t0"] < 60 for e in tutti if e["cat"] == k) for k in sorted(c)})
    pr = collections.Counter(e["primo"][0] if e["primo"] else "nessuna entro 40 s" for e in tutti); print("dopo t0 vira per prima:", dict(pr))
    print("  secondi mediani alla prima virata:", {k: statistics.median([e['primo'][1] for e in tutti if e['primo'] and e['primo'][0] == k]) for k in pr if k != "nessuna entro 40 s"})
if __name__ == "__main__": main()
