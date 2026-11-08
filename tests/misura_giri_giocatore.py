# Rifà sul file di una regata il conto dei giri di penalità del giocatore (regola del gioco in js/regate.js, giriPenalita), con una finestra a scelta.
# Serve alla proposta sui giri (docs/PROPOSTA-GIRI-GIOCATORE.md). Non è un collaudo. Prua dalle righe S, virate e strambate dagli eventi E, debito dai «Tu, contatto».
# Controllo dello strumento: con la finestra di 20 s (quella del gioco) i giri trovati devono essere quelli degli eventi «giro_penalita» del file.
# Uso: python tests/misura_giri_giocatore.py FINESTRA_S file-pezzo-1.txt [pezzo-2 ...]        regola di oggi (finestra di FINESTRA_S secondi)
#      python tests/misura_giri_giocatore.py --nuovo SOSTA_S file-pezzo-1.txt [pezzo-2 ...]  modello proposto (sosta massima SOSTA_S secondi)
import sys
VERSO, GRADI = 20, 360
def giri(righe, finestra):
    S, ev, debito, fatti_file = [], [], [], []
    for r in righe:
        p = r.split()
        if len(p) < 3 or len(p[0]) != 1: continue
        try: t = float(p[1])
        except ValueError: continue
        if p[0] == "S" and len(p) > 8: S.append((t, float(p[4])))
        elif p[0] == "E" and p[2] in ("virata",): ev.append((t, "v"))
        elif p[0] == "E" and p[2] in ("strambata", "strambata_vela_aperta"): ev.append((t, "s"))
        elif p[0] == "E" and p[2] == "giro_penalita": fatti_file.append(t)
        elif p[0] == "Q" and r.split(None, 2)[2].startswith("Tu, contatto"): debito.append(t)
    S = sorted(set(S)); ev = sorted(set(ev)); fatti_file = sorted(set(fatti_file)); debito = sorted(set(debito))
    out = []; need = 2 * len(debito); done = base = 0; dirz = 0
    g = None; ultimo = -1e9
    for i, (t, h) in enumerate(S):
        if debito and t >= debito[0] and g is None: g = dict(h=h, cum=0, buf=[], last=-1e9)
        if g is None or done >= need: continue
        g["cum"] += ((h - g["h"] + 540) % 360) - 180; g["h"] = h
        tk = sum(1 for te, k in ev if k == "v" and te <= t); gy = sum(1 for te, k in ev if k == "s" and te <= t)
        if t - g["last"] >= 0.5:
            g["buf"].append((t, g["cum"], tk, gy)); g["last"] = t
            while g["buf"] and t - g["buf"][0][0] > finestra: g["buf"].pop(0)
        o = g["buf"][0]; net = g["cum"] - o[1]
        if abs(net) < GRADI or tk <= o[2] or gy <= o[3]: continue
        v = 1 if net > 0 else -1; pk = 0; ok = True
        for e in g["buf"]:
            x = (e[1] - o[1]) * v
            if x > pk: pk = x
            elif pk - x > VERSO: ok = False; break
        if not ok or pk - net * v > VERSO: continue
        done = base + 1 if dirz and v != dirz else done + 1; dirz = v; out.append(round(t, 1))
        g = dict(h=h, cum=0, buf=[], last=-1e9)
        if done >= need: base = need; dirz = 0
    return out, fatti_file, need
if __name__ == "__main__" and sys.argv[1] != "--nuovo":
    fin = float(sys.argv[1]); righe = [r for f in sys.argv[2:] for r in open(f, encoding="utf-8", errors="replace")]
    trovati, nel_file, need = giri(righe, fin)
    print(f"finestra {fin:.0f} s | debito {need} giri | giri contati da questa misura a t = {trovati} | giri contati dal gioco (eventi del file) a t = {nel_file}")

# ---- modello proposto (docs/PROPOSTA-GIRI-GIOCATORE.md): il giro comincia quando la prua ruota, riparte se il verso si inverte di oltre VERSO gradi
# o se la prua non avanza nel verso del giro per più di pausa secondi; conta a 360° con una virata e una strambata fatte durante il giro ----
AVANZA = 5   # gradi: sotto, la prua «non avanza» (disturbo delle onde); ipotesi nostra
def giri2(righe, pausa, debito_finto=False):
    S, ev, debito = [], [], []
    for r in righe:
        p = r.split()
        if len(p) < 3 or len(p[0]) != 1: continue
        try: t = float(p[1])
        except ValueError: continue
        if p[0] == "S" and len(p) > 8: S.append((t, float(p[4])))
        elif p[0] == "E" and p[2] == "virata": ev.append((t, "v"))
        elif p[0] == "E" and p[2] in ("strambata", "strambata_vela_aperta"): ev.append((t, "s"))
        elif p[0] == "Q" and r.split(None, 2)[2].startswith("Tu, contatto"): debito.append(t)
    S = sorted(set(S)); ev = sorted(set(ev)); debito = sorted(set(debito))
    t0 = (S[0][0] if S else 0) if debito_finto else (debito[0] if debito else None)
    if t0 is None: return []
    need = 10**9 if debito_finto else 2 * len(debito)
    out = []; done = 0; dirz = 0; base = 0
    cur = None; prev = None
    def nuovo(t, h): return dict(t=t, cum=0.0, pk=0.0, anc=0.0, v=0, tPk=t, tk=sum(1 for te, k in ev if k == "v" and te <= t), gy=sum(1 for te, k in ev if k == "s" and te <= t))
    for t, h in S:
        if t < t0 or done >= need: prev = h; continue
        if cur is None: cur = nuovo(t, h); prev = h; continue
        d = ((h - prev + 540) % 360) - 180; prev = h
        if cur["v"] == 0:
            cur["cum"] += d
            if abs(cur["cum"]) >= AVANZA: cur["v"] = 1 if cur["cum"] > 0 else -1; cur["cum"] = cur["pk"] = cur["anc"] = abs(cur["cum"]); cur["tPk"] = t
            continue
        cur["cum"] += d * cur["v"]
        cur["pk"] = max(cur["pk"], cur["cum"])
        if cur["cum"] >= cur["anc"] + AVANZA: cur["tPk"] = t; cur["anc"] = cur["cum"]   # la prua è avanzata di AVANZA gradi dall'ultimo avanzamento
        if cur["pk"] - cur["cum"] > VERSO or t - cur["tPk"] > pausa: cur = nuovo(t, h); continue
        tk = sum(1 for te, k in ev if k == "v" and cur["t"] < te <= t); gy = sum(1 for te, k in ev if k == "s" and cur["t"] < te <= t)
        if cur["cum"] >= GRADI and tk and gy:
            v = cur["v"]; done = base + 1 if dirz and v != dirz else done + 1; dirz = v; out.append(round(t, 1)); cur = nuovo(t, h)
            if not debito_finto and done >= need: base = need; dirz = 0
    return out
if __name__ == "__main__" and sys.argv[1] == "--nuovo":
    righe = [r for f in sys.argv[3:] for r in open(f, encoding="utf-8", errors="replace")]
    print(f"modello proposto, sosta massima {sys.argv[2]} s | giri contati a t = {giri2(righe, float(sys.argv[2]))}")
