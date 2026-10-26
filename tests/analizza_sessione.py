# Legge un file del registratore di sessione (0.18) e stampa un riassunto.
# Ricalcola dalle righe eventi, suggerimenti e marcatori e li confronta con il riassunto scritto dal gioco:
# sono due conti indipendenti, quindi devono coincidere. Il tempo per andatura qui è stimato dalle righe di stato
# (una al secondo), quindi è solo approssimato.
# Uso: python analizza_sessione.py file.txt     (esce con 1 se i due riassunti non coincidono)
#      python analizza_sessione.py --prova      (controllo su un file d'esempio incluso)
import re, sys
from collections import Counter

def leggi(testo):
    head, rows = [], []
    for r in testo.splitlines():
        if r.startswith("#"): head.append(r)
        elif r.strip():
            k, t, *resto = r.split(" ", 2) + [""]
            rows.append((k, float(t), resto[0]))
    return head, rows

def riassunto_gioco(head):
    g = {"eventi": Counter(), "msg": Counter(), "marcatori": []}
    for h in head:
        if h.startswith("#  eventi: ") and "nessuno" not in h:
            for p in h[11:].split(" · "):
                nome, n = p.rsplit(" ", 1); g["eventi"][nome] = int(n)
        m = re.match(r"#   «(.*)» (\d+)× · \d+ s$", h)
        if m and int(m[2]): g["msg"][m[1]] = int(m[2])
        if h.startswith("#  marcatori: ") and "nessuno" not in h:
            g["marcatori"] = [p.split(" ")[0] for p in h[14:].split(" · ")]
    return g

def mmss(s): return f"{int(s // 60)}:{int(s % 60):02d}"

def avversari(rows, durata, out):
    """Formato 2 (1.0.52): per ogni avversario righe B, tempo fermo, contatti, penalità, secondi passati a cedere. Ritorna il riepilogo."""
    B = [(t, d.split(" ")) for k, t, d in rows if k == "B"]
    nomi = sorted({c[0] for _, c in B})
    res = {}
    if not nomi: return res
    out("Avversari (righe B, una al secondo):")
    for n in nomi:
        mie = [(t, c) for t, c in B if c[0] == n]
        ferma, aperto = 0.0, None
        for k, t, d in rows:
            if k != "E": continue
            p = d.split(" ")
            if p[0] == "avv_fermo" and p[1] == n: aperto = t
            elif p[0] == "avv_riparte" and p[1] == n and aperto is not None: ferma += t - aperto; aperto = None
        if aperto is not None: ferma += max(0, (mie[-1][0] if mie else durata) - aperto)
        cont = sum(1 for k, t, d in rows if k == "E" and d.startswith("contatto_barche") and n in d.split(" ")[1:])
        pen = [d for k, t, d in rows if k == "E" and d.startswith("avv_penalita " + n + " ")]
        cede = sum(1 for _, c in mie if "cede:" in c[-1])
        res[n] = {"righe": len(mie), "ferma": ferma, "contatti": cont, "penalita": len(pen), "cede": cede}
        out(f"  {n}: {len(mie)} righe · ferma {ferma:.0f} s · contatti {cont} · penalità {len(pen)} · a cedere {cede} s")
    return res

def analizza(testo, out=print):
    head, rows = leggi(testo)
    for h in head[:5]: out(h[2:])
    ev = Counter(d.split(" ")[0] for k, _, d in rows if k == "E" and not d.startswith("registrazione_"))
    msg = Counter(d for k, _, d in rows if k == "H")
    marc = [(t, d) for k, t, d in rows if k == "M"]
    # pause: i secondi scritti negli eventi di riaccensione devono dare il totale scritto in testa
    pause = [int(m[1]) for k, _, d in rows if k == "E" for m in [re.match(r"registrazione_accesa pausa (\d+)s$", d)] if m]
    stato = [(t, d.split(" ")) for k, t, d in rows if k == "S"]
    durata = rows[-1][1] if rows else 0
    out(f"\nRighe {len(rows)} · durata registrata {mmss(durata)} · stato {len(stato)} righe")
    out("Eventi: " + (" · ".join(f"{k} {n}" for k, n in ev.most_common()) or "nessuno"))
    # tempo per andatura stimato: ogni riga di stato vale fino alla successiva, al massimo 1,5 s
    andT = Counter()
    for i, (t, c) in enumerate(stato):
        dt = min(1.5, stato[i + 1][0] - t) if i + 1 < len(stato) else 1
        andT[c[-1]] += dt
    out("Tempo per andatura (stimato dallo stato): " + (" · ".join(f"{k} {mmss(v)}" for k, v in andT.most_common()) or "nessuno"))
    out("Suggerimenti più visti:")
    for m, n in msg.most_common(10): out(f"  {n}× «{m}»")
    passi = [(t, d) for k, t, d in rows if k == "L"]
    if passi:
        out("Passi di lezione (fino al passo o alla schermata successiva):")
        fine = [t for k, t, d in rows if k == "L" or (k == "E" and d.startswith("apre"))] + [durata]
        for t, d in passi:
            nxt = min(x for x in fine if x > t) if any(x > t for x in fine) else durata
            out(f"  {d}: {mmss(nxt - t)}")
    # dove la barca rallenta: velocità scesa di oltre metà in 5 s, partendo da almeno 1 nodo (soglia nostra)
    out("Rallentamenti (oltre metà della velocità persa in 5 s):")
    n_ral, salta = 0, -1
    for i, (t, c) in enumerate(stato):
        if t < salta or float(c[3]) < 1: continue
        for t2, c2 in stato[i + 1:]:
            if t2 - t > 5: break
            if float(c2[3]) < float(c[3]) / 2:
                vicini = [f"{k} {tt:.1f} {d}" for k, tt, d in rows if k in "ETHKM" and t - 3 <= tt <= t2 + 1]
                out(f"  {t:.1f}-{t2:.1f} s: da {c[3]} a {c2[3]} nodi ({c2[-1]})" + ("; vicino: " + " | ".join(vicini[:6]) if vicini else ""))
                n_ral += 1; salta = t2 + 5; break
    if not n_ral: out("  nessuno")
    avversari_res = avversari(rows, durata, out)
    out("Marcatori:" + ("" if marc else " nessuno"))
    for t, d in marc:
        out(f"  M{d.split(' ')[0]} a {mmss(t)} ({t:.1f} s). Dieci secondi prima e dopo:")
        for k, tt, dd in rows:
            if t - 10 <= tt <= t + 10 and k != "M": out(f"    {k} {tt:.1f} {dd}")
    # confronto con il riassunto del gioco
    g = riassunto_gioco(head)
    diff = []
    if g["eventi"] != ev: diff.append(f"eventi: gioco {dict(g['eventi'])} | righe {dict(ev)}")
    if g["msg"] != msg: diff.append(f"suggerimenti: gioco {dict(g['msg'])} | righe {dict(msg)}")
    tot = next((h for h in head if h.startswith("# pause della registrazione")), "")
    m = re.search(r": (\d+) s in totale$", tot)
    if (int(m[1]) if m else 0) != sum(pause): diff.append(f"pause: gioco {tot!r} | righe {pause}")
    if g["marcatori"] != [f"M{d.split(' ')[0]}" for _, d in marc]: diff.append(f"marcatori: gioco {g['marcatori']} | righe {len(marc)}")
    out("\nConfronto con il riassunto del gioco: " + ("coincide" if not diff else "DIVERSO"))
    for d in diff: out("  " + d)
    return {"eventi": ev, "msg": msg, "marcatori": marc, "pause": pause, "andT": andT, "rallentamenti": n_ral, "diff": diff, "stato": stato, "avversari": avversari_res}

ESEMPIO = """# SCUOLA DI VELA - registrazione di sessione, formato 1
# gioco 0.18 · inizio 2026-10-05 15:00 · durata 0:12 (in simulazione 0:12)
# impostazioni all'inizio: vento=0° 10kn
# nota: M1 la barca si ferma
# pause della registrazione (spenta e riaccesa): 70 s in totale
#  eventi: apre 1 · virata 1
#   «Vela gonfia e regolata.» 1× · 5 s
#  marcatori: M1 a 0:07
E 0.0 registrazione_accesa
E 0.0 apre «Prova 1»
S 0.1 0 0 45 3.4 8 45 10 30 8 0 30 BS
H 0.2 Vela gonfia e regolata.
S 1.1 0 -2 45 3.4 8 45 10 30 8 0 30 BS
S 2.1 0 -4 45 3.0 8 45 10 30 8 0 30 BS
K 2.5 → giù
S 3.1 0 -5 20 1.2 0 20 10 15 9 60 30 AM
E 3.4 registrazione_spenta
E 3.4 registrazione_accesa pausa 70s
E 3.5 virata mure_a_sinistra 1.0kn
S 4.1 0 -5 -20 0.8 0 -20 10 -15 9 60 30 AM
M 7.0 1 0 -5
S 8.1 0 -6 -60 2.0 5 -60 10 -40 8 0 40 BL
"""

ESEMPIO2 = """# SCUOLA DI VELA - registrazione di sessione, formato 2
# gioco 1.0.52 · inizio 2026-10-26 21:00 · durata 0:12 (in simulazione 0:12)
# impostazioni all'inizio: vento=0° 10kn
# nota: (nessuna)
# pause della registrazione (spenta e riaccesa): nessuna
#  eventi: apre 1 · avv_fermo 1 · avv_riparte 1 · contatto_barche 1 · avv_penalita 1
E 0.0 registrazione_accesa
E 0.0 apre regata «Regata a bastone»
S 1.0 0 0 45 3.4 8 45 10 30 8 0 30 BS
B 1.0 Rossa 5.0 3.0 90 3.0 45 1 -
B 1.0 Blu 8.0 3.0 90 3.0 45 1 cede:Rossa
E 2.0 avv_fermo Blu lato 1 8.0 3.0
B 2.0 Blu 8.0 3.0 90 0.1 45 1 cede:Rossa
E 5.0 contatto_barche Blu Rossa
Q 5.0 La Blu, contatto con la Rossa: era mure a sinistra e doveva lasciare strada a chi era mure a dritta.
E 5.0 avv_penalita Blu +15s
E 6.0 avv_riparte Blu
B 6.0 Blu 8.0 3.0 90 2.0 45 1 -
"""

def prova():
    righe = []
    r = analizza(ESEMPIO, righe.append)
    assert r["eventi"] == Counter({"apre": 1, "virata": 1}), r["eventi"]
    assert len(r["marcatori"]) == 1 and r["marcatori"][0][0] == 7.0
    assert r["rallentamenti"] == 1, r["rallentamenti"]          # da 3,4 a 1,2 nodi fra 1,1 e 3,1 s
    assert abs(r["andT"]["BS"] - 3) < 1e-9 and abs(r["andT"]["AM"] - 2.5) < 1e-9, r["andT"]   # 1+1+1, poi 1 e 1,5 (buco di 4 s tagliato)
    assert r["pause"] == [70], r["pause"]
    assert not r["diff"], r["diff"]
    assert analizza(ESEMPIO.replace("70 s in", "60 s in"), righe.append)["diff"], "il totale delle pause sbagliato deve essere visto"
    r = analizza(ESEMPIO.replace("virata 1", "virata 2"), righe.append)
    assert r["diff"], "il confronto deve accorgersi di un riassunto sbagliato"
    righe2 = []
    r2 = analizza(ESEMPIO2, righe2.append)
    assert r2["avversari"]["Blu"] == {"righe": 3, "ferma": 4.0, "contatti": 1, "penalita": 1, "cede": 2}, r2["avversari"]
    assert r2["avversari"]["Rossa"]["righe"] == 1 and r2["avversari"]["Rossa"]["contatti"] == 1
    assert not r2["diff"], r2["diff"]
    assert analizza(ESEMPIO2.replace("contatto_barche 1", "contatto_barche 2"), righe2.append)["diff"], "il confronto deve accorgersi di un conteggio sbagliato nel formato 2"
    print("prova superata (anche formato 2, righe B): eventi, marcatori, rallentamenti, tempo per andatura e confronto (anche quando è sbagliato)")

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__ or "uso: python analizza_sessione.py file.txt | --prova")
    if sys.argv[1] == "--prova": prova(); sys.exit(0)
    r = analizza(open(sys.argv[1], encoding="utf-8").read())
    sys.exit(1 if r["diff"] else 0)
