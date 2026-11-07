# Scene strane nelle regate registrate (docs/PROPOSTA-REGATE-VERE.md, parte B). Non è un collaudo: le scene dicono dove guardare, non cosa correggere.
# Legge il testo del registratore, lo stesso per le regate di Ale e per quelle simulate. Una scena per episodio: stessa scena e stesse barche entro 5 s si contano una volta.
#  S1 cede ma si avvicina: «cede:X» da almeno 2 s e distanza da X sotto 8,4 m (due lunghezze)
#  S2 curva grande per cedere: «cede:X» e la prua gira di oltre 60° in 5 s (dall'inizio del cedere o nella finestra di 5 s)
#  S3 contatto cedendo: contatto con X entro 5 s da un «cede:X»
#  S4 contatto senza che nessuno ceda: contatto fra due barche, nessuna «cede» l'altra nei 5 s prima
#  S5 ritorno di bolina: sul lato di poppa, oltre 100° dal vento e poi entro 12 s sotto 60°, con una barca entro 12,6 m (3 lunghezze)
#  S6 strambate ravvicinate: due cambi di mure oltre 120° dal vento in meno di 5 s
#  S7 ferma: evento avv_fermo (sotto 0,5 nodi per 5 s dopo il via)
#  S8 coppia che si tiene (docs/PROPOSTA-COPPIE.md): «cede:X» da almeno 10 s, X entro 12,6 m (3 lunghezze) e prue entro 20°: le due barche vanno insieme e nessuna si libera
# Uso: python tests/scene_strane.py file.txt [altri pezzi della stessa regata...]   (i pezzi si passano in ordine)
#      python tests/scene_strane.py --prova     casi costruiti: ogni scena deve scattare su un caso e tacere su uno simile
import collections, math, sys
L2, L3, CEDE_MIN, GIRO, GIRO_T, CONT_T, RIT_T, STR_T, EPIS = 8.4, 12.6, 2.0, 60, 5.0, 5.0, 12.0, 5.0, 5.0
COPPIA_T, COPPIA_A = 10.0, 20
NOMI = {"S1": "cede ma si avvicina", "S2": "curva grande per cedere", "S3": "contatto cedendo", "S4": "contatto senza che nessuno ceda", "S5": "ritorno di bolina", "S6": "strambate ravvicinate", "S7": "ferma", "S8": "coppia che si tiene"}

def ang(a, b): return abs((a - b + 180) % 360 - 180)

def leggi(righe):
    """righe di testo -> fotogrammi {t: {nome: barca}} e contatti/fermi; i fotogrammi ripetuti fra due pezzi si tengono una volta"""
    fot, cont, fermi = collections.OrderedDict(), [], []
    for r in righe:
        p = r.split()
        if len(p) < 3 or len(p[0]) != 1: continue
        try: t = float(p[1])
        except ValueError: continue
        if p[0] == "S" and len(p) > 7:
            fot.setdefault(t, {})["Tu"] = dict(x=float(p[2]), y=float(p[3]), h=float(p[4]), kn=float(p[5]), twa=float(p[7]), lato=None, cede=set(), via=p[-1] != "SC")
        elif p[0] == "B" and len(p) > 9:
            st = p[9]; cede = {x.split(":")[1] for x in st.split(",") if x.startswith("cede:")}
            fot.setdefault(t, {})[p[2]] = dict(x=float(p[3]), y=float(p[4]), h=float(p[5]), kn=float(p[6]), twa=float(p[7]), lato=int(p[8]), cede=cede, via=not any(k in st for k in ("arr", "dnf", "scuf")))
        elif p[0] == "E" and p[2] == "contatto_barche" and len(p) > 4:
            if (t, p[3], p[4]) not in cont: cont.append((t, p[3], p[4]))
        elif p[0] == "E" and p[2] == "avv_fermo" and len(p) > 3:
            if (t, p[3]) not in fermi: fermi.append((t, p[3]))
    return fot, cont, fermi

def scene(righe):
    fot, cont, fermi = leggi(righe); tempi = list(fot); out = []; ultimo = {}
    def segna(s, t, chi, testo):
        k = (s, chi)
        if t - ultimo.get(k, -1e9) > EPIS: out.append(dict(s=s, t=t, chi=chi, testo=testo))
        ultimo[k] = t
    storia = collections.defaultdict(list)   # nome -> [(t, h)]
    inizio = {}                              # (nome, X) -> inizio del cedere
    tCede = {}                               # (nome, X) -> ultimo istante visto cedere
    tPoppa, tkPrima, tStr = {}, {}, {}
    ic = 0; cont = sorted(cont)
    for t in tempi:
        f = fot[t]
        # i contatti prima dello stato di questo fotogramma: il «cede» deve venire prima
        while ic < len(cont) and cont[ic][0] <= t:
            tc, a, b = cont[ic]; ic += 1
            cA, cB = tc - tCede.get((a, b), -1e9) <= CONT_T, tc - tCede.get((b, a), -1e9) <= CONT_T
            if cA or cB: out.append(dict(s="S3", t=tc, chi=(a if cA else b, b if cA else a), testo=f"{a if cA else b} cedeva a {b if cA else a} e la tocca"))
            else: out.append(dict(s="S4", t=tc, chi=(a, b), testo=f"contatto {a}-{b}, nessuna delle due cedeva"))
        for n, b in f.items():
            if not b["via"]: continue
            storia[n].append((t, b["h"])); s = storia[n]
            while s and t - s[0][0] > GIRO_T: s.pop(0)
            for x in b["cede"]:
                if t - tCede.get((n, x), -1e9) > 1: inizio[(n, x)] = t
                tCede[(n, x)] = t
                o = f.get(x)
                if o is None: continue
                d = math.hypot(o["x"] - b["x"], o["y"] - b["y"])
                if d < L2 and t - inizio[(n, x)] >= CEDE_MIN: segna("S1", t, (n, x), f"{n} cede a {x} da {t - inizio[(n, x)]:.1f} s, a {d:.1f} m")
                g = max(ang(b["h"], h0) for t0, h0 in s if t0 >= inizio[(n, x)])
                if g > GIRO: segna("S2", t, (n, x), f"{n} cede a {x} girando di {g:.0f}° in 5 s")
                if d < L3 and ang(b["h"], o["h"]) < COPPIA_A and t - inizio[(n, x)] >= COPPIA_T: segna("S8", t, (n, x), f"{n} cede a {x} da {t - inizio[(n, x)]:.0f} s, affiancate a {d:.1f} m")
            if b["lato"] is None or abs(b["twa"]) is None: continue
            A = abs(b["twa"])
            if b["lato"] == 2:
                if A > 100: tPoppa[n] = t
                elif A < 60 and t - tPoppa.get(n, -1e9) <= RIT_T:
                    ds = [(math.hypot(o["x"] - b["x"], o["y"] - b["y"]), m) for m, o in f.items() if m != n and o["via"]]
                    if ds and min(ds)[0] < L3: segna("S5", t, (n,), f"{n} torna a {A:.0f}° dal vento, {min(ds)[1]} a {min(ds)[0]:.1f} m")
            tk = (b["twa"] > 0) - (b["twa"] < 0)
            if tk and tkPrima.get(n) and tk != tkPrima[n] and A > 120:
                if t - tStr.get(n, -1e9) < STR_T: segna("S6", t, (n,), f"{n} stramba di nuovo dopo {t - tStr[n]:.1f} s")
                tStr[n] = t
            if tk: tkPrima[n] = tk
    for tc, n in fermi: out.append(dict(s="S7", t=tc, chi=(n,), testo=f"{n} ferma"))
    return sorted(out, key=lambda e: e["t"]), len(tempi), len(cont), (tempi[0], tempi[-1]) if tempi else (0, 0)

# ---- casi costruiti (R2): ogni scena scatta su un caso e tace su uno simile ----
def _b(t, n, x, y, h, twa, lato=1, st="-"): return f"B {t:.2f} {n} {x} {y} {h} 5.0 {twa} {lato} {st}"
def _s(t, x, y, h, twa): return f"S {t:.2f} {x} {y} {h} 5.0 1 {twa} 12 100 8 0 50 BL"
def _film(f, durata=10.0, passo=0.1): return [r for i in range(int(durata / passo) + 1) for r in f(round(i * passo, 2))]
def casi():
    c = {}
    lontano = lambda t: _b(t, "Blu", 500, 500, 0, 50)
    c["S1"] = (_film(lambda t: [_s(t, 0, 0, 0, 50), _b(t, "Rossa", 7, 0, 0, 50, 1, "cede:Tu")]), _film(lambda t: [_s(t, 0, 0, 0, 50), _b(t, "Rossa", 20, 0, 0, 50, 1, "cede:Tu")]))
    c["S2"] = (_film(lambda t: [_s(t, 0, 0, 0, 50), _b(t, "Rossa", 30, 0, 20 * t, 50, 1, "cede:Tu")]), _film(lambda t: [_s(t, 0, 0, 0, 50), _b(t, "Rossa", 30, 0, 5 * t, 50, 1, "cede:Tu")]))
    film = lambda st: _film(lambda t: [_s(t, 0, 0, 0, 50), _b(t, "Rossa", 30, 0, 0, 50, 1, st)]) + ["E 9.00 contatto_barche Tu Rossa"]
    c["S3"] = (film("cede:Tu"), film("-"))
    c["S4"] = (film("-"), film("cede:Tu"))
    def rit(vicino): return _film(lambda t: [_s(t, 8 if vicino else 200, 0, 0, 150), _b(t, "Rossa", 0, 0, 0, 150 if t < 5 else 40, 2)])
    c["S5"] = (rit(True), rit(False))
    c["S6"] = (_film(lambda t: [_b(t, "Rossa", 0, 0, 0, 170 if t < 3 else -170 if t < 6 else 170, 2)]), _film(lambda t: [_b(t, "Rossa", 0, 0, 0, 170 if t < 1 else -170 if t < 9 else 170, 2)]))
    c["S8"] = (_film(lambda t: [_s(t, 0, 0, 0, 50), _b(t, "Rossa", 5, 0, 0, 50, 1, "cede:Tu")], 12), _film(lambda t: [_s(t, 0, 0, 0, 50), _b(t, "Rossa", 5, 0, 90, 50, 1, "cede:Tu")], 12))
    c["S7"] = (["E 3.00 avv_fermo Rossa lato 1"] + _film(lambda t: [lontano(t)]), ["E 3.00 avv_riparte Rossa"] + _film(lambda t: [lontano(t)]))
    return c
def prova():
    ko = 0
    for s, (si, no) in casi().items():
        a = sum(e["s"] == s for e in scene(si)[0]); b = sum(e["s"] == s for e in scene(no)[0]); ok = a >= 1 and b == 0; ko += not ok
        print(f"{s} {NOMI[s]}: sul caso {a}, sul caso simile {b} -> {'OK' if ok else 'SBAGLIATO'}")
    print("ESITO", "OK" if not ko else "FALLITO"); sys.exit(1 if ko else 0)

def main():
    if sys.argv[1] == "--prova": prova()
    righe = [r for f in sys.argv[1:] for r in open(f, encoding="utf-8", errors="replace")]
    es, nf, nc, (a, b) = scene(righe)
    print(f"file {len(sys.argv) - 1}, da t={a:.1f} a t={b:.1f}, fotogrammi {nf}, contatti {nc}, scene {len(es)}: {dict(sorted(collections.Counter(e['s'] for e in es).items()))}")
    if nf == 0: print("ATTENZIONE: nessun fotogramma letto, la misura non vale")
    for e in es: print(f"  t={e['t']:7.1f} {e['s']} {NOMI[e['s']]}: {e['testo']}")
if __name__ == "__main__": main()
