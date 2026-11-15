# Controllo dei commenti che si mangiano il codice (16 novembre 2026). Due volte il 15 novembre un commento // aggiunto a metà riga ha trasformato in
# commento il codice che seguiva sulla stessa riga (1.3.3: releaseKeys(); finShow(); nella chiusura della moviola; 1.3.10: metà dell'oggetto R della regata).
# Cerca nei commenti // dei file js/ quello che sembra codice: una chiamata chiusa da «);», due coppie «nome: valore,» di fila, un getter «get nome(){»,
# «}, nome:» o una funzione a freccia con un'istruzione (dal 16 nov, dopo il caso di avvio.js nella 1.3.11, che la prima versione non vedeva).
# Le righe già note e giuste si riconoscono dal testo (NOTE_OK_TESTO; i numeri di riga cambiano). Esce con 1 se trova righe sospette nuove.
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
CODICE = re.compile(r"[A-Za-z_$][\w$.]*\([^()]*\);\s*\S|[A-Za-z_$][\w$]*: [^,;]{1,40}, [A-Za-z_$][\w$]*: [^,;]{1,40},"
                    r"|\bget [A-Za-z_$][\w$]*\(\)\s*\{|\}\s*,\s*[A-Za-z_$][\w$]*\s*[:(]|=>\s*\{[^}]*;")   # 16 nov: anche getter, «}, nome:» e funzioni a freccia (avvio.js, 1.3.11)
def commento(riga):   # il testo dopo il primo // che non sta dentro una stringa o un'espressione regolare (approssimato: fuori dalle virgolette)
    q = None; i = 0
    while i < len(riga) - 1:
        c = riga[i]
        if q: 
            if c == "\\": i += 2; continue
            if c == q: q = None
        elif c in "\"'`": q = c
        elif riga[i:i + 2] == "//" and (i == 0 or riga[i - 1] != ":"): return riga[i + 2:]
        i += 1
    return None
NOTE_OK_TESTO = ("Un profilo: {", "valori: { hullScale", "con lo stesso step(); null", "con lo stesso step(); ricalcolata", "ritorna { cede:", "{ tempo, lati:")
sospette = []
for f in sorted((ROOT / "js").glob("*.js")):
    if f.name in ("suoni-dati.js", "rotta-dati.js"): continue
    for n, riga in enumerate(f.read_text().splitlines(), 1):
        c = commento(riga)
        if c and CODICE.search(c) and not any(t in c for t in NOTE_OK_TESTO): sospette.append(f"{f.name}:{n}: //{c[:140]}")
print(f"righe con un commento che contiene codice: {len(sospette)}")
for s in sospette: print("  " + s)
print("ESITO: " + ("FALLITO" if sospette else "OK")); sys.exit(1 if sospette else 0)
