# Voce 82 (docs/PROPOSTA-RIVALI-CHE-CRESCONO.md, regole 1-7): carriere a soli numeri, due livelli da 24 posti (zonale 12, nazionale 12), il giocatore "*" è uno dei 24 di Deriva con una bravura fissa.
# 300 mondi da 30 stagioni, seme fisso; nessuna barca in acqua: ordine di ogni tappa estratto col modello del gioco, peso e^(0,2*(doti + F*c/100)). F misurato in acqua (tests/misura_bravura.py).
# Uso: python3 tests/simula_carriere_rivali.py F [mondi] [bravura del giocatore]
# Varianti (solo per prove dichiarate): SEME, QUOTA, RUGGINE, TETTO_ZONALE=min-max, CRESCITA (fattore) nell'ambiente; senza, valgono i numeri della proposta.
import os, random, math, statistics as st, sys
F = float(sys.argv[1]) if len(sys.argv) > 1 else 4; NM = int(sys.argv[2]) if len(sys.argv) > 2 else 300; GIO = float(sys.argv[3]) if len(sys.argv) > 3 else 50
E = os.environ.get; STAG = 30; QUOTA = float(E("QUOTA", 0.4)); RUGGINE = float(E("RUGGINE", 10)); CRE = float(E("CRESCITA", 1)); TZ = [float(x) for x in E("TETTO_ZONALE", "50-100").split("-")]; SEME = int(E("SEME", 11))
class P:
    def __init__(s, i, liv, naz):
        s.id = i; s.tetto = random.uniform(75, 100) if naz else random.uniform(*TZ)
        s.c = {liv: random.uniform(45, 75) if naz else random.uniform(10, 40)}
        s.tr = {k: sum(random.choices([1, 0, -1], [4, 4, 2] if naz else [3, 4, 3], k=2)) for k in "DF"}
def forza(p, liv): return (GIO if p.id == "*" else p.c[liv]) * F / 100 + (0 if p.id == "*" else p.tr[liv])
def stagione(g, liv):
    pt = dict.fromkeys(g, 0); vit = dict.fromkeys(g, 0)
    for _ in range(4):
        r = list(g); pos = 1
        while r:
            i = random.choices(r, [math.exp(0.2 * forza(x, liv)) for x in r])[0]; r.remove(i); pt[i] += pos; vit[i] += pos == 1; pos += 1
    return sorted(g, key=lambda x: (pt[x], random.random())), vit
def cresci(g, vit, liv):
    for p in g:
        if p.id == "*": continue
        q = max(0, 1 - p.c[liv] / p.tetto); p.c[liv] = min(p.tetto, p.c[liv] + CRE * (2.4 * 4 * q * q + 3 * vit[p] * q))
def mondo(giocatore_da=0):
    per = []; n = 0; C = {}
    for liv in "DF":
        for circ, naz in (("z", False), ("n", True)):
            C[liv + circ] = [P(f"{liv}{circ}{k}", liv, naz) for k in range(12)]
    io = P("*", "D", False); io.c = {"D": GIO}; io.tetto = 100
    err = 0; titoli = {"D": {}, "F": {}}; passati = {}; dist = {}; medie = {}; stessi = []; torn = []; qual = {1: None, 10: None}; tornati = {}
    entra = 0; gen = {}
    sost = C["Dz"][0]; C["Dz"][0] = io   # il giocatore prende un posto dello zonale
    tutti = [p for g in C.values() for p in g]
    n0 = len(tutti)
    for s in range(1, STAG + 1):
        if giocatore_da and s == 10 and io not in C["Dz"]: pass
        O = {}; V = {}
        for k in C: O[k], V[k] = stagione(C[k], k[0])
        for liv in "DF": v = O[liv + "n"][0]; titoli[liv][v.id] = titoli[liv].get(v.id, 0) + 1
        if s <= 10: 
            for p in C["Dn"]: passati[p.id] = 1
        for k in C: cresci(C[k], V[k], k[0])
        pos_io = [x.id for x in O["Dz"]].index("*") + 1 if io in C["Dz"] else None
        # qualificazione: i primi 9 del nazionale e i primi 3 dello zonale; per S6 il giocatore accetta sempre
        nuovo = {}
        for liv in "DF":
            nz = O[liv + "n"]; zn = O[liv + "z"]; via = None
            if liv == "D":   # lo sponsor chiama un rivale fra i primi tre del nazionale
                cand = [p for p in nz[:3] if p.id != "*"]; via = random.choice(cand) if cand else None
                sale = via
            resti = [p for p in nz if p is not via]
            nuovo[liv + "n"] = resti[:9] + zn[:3]; nuovo[liv + "z"] = resti[9:] + zn[3:]
        # l'ultimo dello zonale del Fiocco torna in Deriva, il chiamato va nello zonale del Fiocco
        giu = nuovo["Fz"][-1]; nuovo["Fz"].remove(giu)
        nuovo["Fz"].append(sale); sale.c["F"] = max(sale.c.get("F", 0), QUOTA * sale.c["D"]); sale.tr.setdefault("F", 0)
        prima = giu.c.get("D"); giu.c["D"] = max(0, prima - RUGGINE) if prima is not None else max(QUOTA * giu.c["F"], 10)   # chi è nato nel Fiocco e scende: 40% di quello che sa, almeno 10 (ipotesi)
        nuovo["Dz"].append(giu); tornati.setdefault(giu.id, (s, giu, prima is not None))
        C = nuovo
        ids = [p.id for g in C.values() for p in g]
        if any(len(g) != 12 for g in C.values()) or len(ids) != len(set(ids)) or len(ids) != n0: err += 1
        if any(len(g) != 12 for g in C.values()) and not gen: gen["perche"] = {k: len(v) for k, v in C.items()}
        # S5: chi è tornato si è qualificato al nazionale di Deriva?
        for i, (sg, p, gia) in list(tornati.items()):
            if p in C["Dn"]: torn.append((s - sg, gia)); del tornati[i]
            elif s - sg >= 2 or p in C["Fz"] or p in C["Fn"]: torn.append((99, gia)); del tornati[i]
        if s in (3, 6, 9):
            pass
        for part in (1, 10):
            if qual[part] is None and s >= part and s < part + 3:
                if io in C["Dn"]: qual[part] = s - part + 1
            if part == 10 and s == 9 and io in C["Dn"]: # alla 10 si riparte dallo zonale
                r = C["Dz"][-1]; C["Dn"][C["Dn"].index(io)] = r; C["Dz"][C["Dz"].index(r)] = io
        if s in (1, 5, 10, 30):
            D = [p for k in ("Dz", "Dn") for p in C[k] if p.id != "*"]
            m = lambda g: st.mean(p.c["D"] for p in g if p.id != "*")
            medie[s] = (m(C["Dz"]), m(C["Dn"])); dist[s] = max(p.c["D"] for p in D) - min(p.c["D"] for p in D)
        gen.setdefault("stor", []).append({k: {p.id for p in g} for k, g in C.items()})
    S = gen["stor"]
    stessi = [len(S[a]["Dz"] & S[a + 3]["Dz"] - {"*"}) / len(S[a]["Dz"] - {"*"}) for a in range(0, STAG - 3)]
    return dict(err=err, tit={k: max(v.values()) / STAG for k, v in titoli.items()}, passati=len(passati) - ("*" in passati), stessi=st.mean(stessi), medie=medie, dist=dist, torn=torn, q1=qual[1], q10=qual[10], perche=gen.get("perche"))
random.seed(SEME); R = [mondo() for _ in range(NM)]
print(f"F = {F}, {NM} mondi da {STAG} stagioni, giocatore a {GIO:.0f}, seme {SEME}; quota {QUOTA} ruggine {RUGGINE} crescita x{CRE} tetto zonale {TZ}")
print("S1 circuiti sbagliati", sum(r["err"] for r in R), R[0]["perche"] or "")
print("S2 titoli al più vincente (Deriva, Fiocco)", [f"{st.mean(r['tit'][l] for r in R):.0%}" for l in "DF"])
print(f"S3 stessi rivali nello zonale di Deriva dopo 3 stagioni {st.mean(r['stessi'] for r in R):.0%}; rivali diversi passati dal nazionale in 10 stagioni {st.mean(r['passati'] for r in R):.1f}")
print("S4 distanza alla 30", round(st.mean(r["dist"][30] for r in R), 1), "; media zonale/nazionale", {s: (round(st.mean(r["medie"][s][0] for r in R)), round(st.mean(r["medie"][s][1] for r in R))) for s in (1, 5, 10, 30)})
tt = [x for r in R for x in r["torn"]]; print(f"S5 tornati dal Fiocco: {len(tt)}, qualificati al nazionale entro 2 stagioni {sum(x <= 2 for x, _ in tt) / max(1, len(tt)):.0%}; di cui {sum(g for _, g in tt)} che la Deriva l'avevano già fatta {sum(x <= 2 for x, g in tt if g) / max(1, sum(g for _, g in tt)):.0%}, nati nel Fiocco {sum(x <= 2 for x, g in tt if not g) / max(1, sum(not g for _, g in tt)):.0%}")
q = lambda k: sum(r[k] is not None for r in R) / NM
print(f"S6 il giocatore si qualifica entro 3 stagioni: dalla 1 {q('q1'):.0%}, dalla 10 {q('q10'):.0%}")
