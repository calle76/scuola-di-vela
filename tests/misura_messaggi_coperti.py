# Voce 35 (25 nov 2026): nelle registrazioni di Ale e Lucio quanto resta sullo schermo un messaggio importante (contatto del giocatore, boa dal lato sbagliato,
# partenza anticipata, boa toccata) prima che un altro lo copra. Righe «T tempo testo» del registratore. Durata normale 2,6 s (4,5 per la partenza anticipata in alcuni casi).
# Si lancia dalla cartella registrazioni/: python3 -I ../tests/misura_messaggi_coperti.py
import collections, glob, re
IMP = re.compile(r"^(Contatto! |Contatto: |Hai toccato |Boa girata dal lato|Partenza anticipata|Sei passato fuori)")
n = collections.Counter(); cop = collections.defaultdict(list); file_con = set(); nf = 0
visti = set()
for f in sorted(glob.glob("regata-*-intera.txt")):
    T = []
    for l in open(f, errors="replace"):
        m = re.match(r"T (-?[\d.]+) (.*)", l)
        if m: T.append((float(m.group(1)), m.group(2).strip()))
    if T: nf += 1
    for i, (t, x) in enumerate(T):
        if not IMP.match(x): continue
        k = IMP.match(x).group(1); n[k] += 1
        if i + 1 < len(T) and 0 <= T[i + 1][0] - t < 2.6: cop[k].append((round(T[i + 1][0] - t, 2), x[:50], T[i + 1][1][:60], f))
print(nf, "file con messaggi")
for k in n: print(f"{k!r}: {n[k]} messaggi, coperti prima di 2,6 s: {len(cop[k])}, entro 1 s: {sum(c[0] < 1 for c in cop[k])}")
for k in cop:
    for c in cop[k]: print("  ", *c, sep=" | ")
