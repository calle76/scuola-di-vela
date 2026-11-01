# Fallimenti noti (1 novembre 2026, docs/PROPOSTA-COLLAUDI-SU-GITHUB.md §10): dice se un collaudo FALLITO è fallito
# esattamente come già sappiamo, così il giro diventa rosso solo per un fallimento nuovo o cambiato.
# Uso (lo chiama tests/lancia_tutti.sh):
#   noti.py esito  <nome nel giro> <browser> <file di uscita>   -> stampa NOTO, TEMPO o NUOVO, e un motivo
#   noti.py c-e    <nome nel giro> <browser>                    -> esce con 0 se il collaudo ha una voce «noto» per quel browser
#   noti.py righe  <file di uscita>                             -> stampa le righe di fallimento (per scrivere una voce nuova)
# L'elenco è in tests/fallimenti_noti.txt.
import re, sys, pathlib

ELENCO = pathlib.Path(__file__).with_name("fallimenti_noti.txt")
# Una «riga di fallimento»: un controllo che dice NO o FALLITO, l'elenco dei casi sbagliati non vuoto, un errore di Python.
FALLIMENTO = re.compile(r"(^|\s|:)(NO|FALLITO)(\s|:|;|$)|ESITO: NON VALIDO|casi sbagliati: \[(?!\])|Traceback|Error:")
RIASSUNTO = re.compile(r"^\s*(ESITO:|casi sbagliati:)")   # righe che riassumono le altre


def voci():
    """Le voci dell'elenco: (tipo, nome, browser, motivo, righe). Tipo «noto» (righe esatte) o «tempo» (frammenti)."""
    out, cur = [], None
    for riga in ELENCO.read_text(encoding="utf-8").splitlines():
        if riga.startswith("#") or not riga.strip():
            continue
        m = re.match(r"^(==|~~) (.+?) \| (chromium|firefox|tutti) \| (.+)$", riga)
        if m:
            cur = ("noto" if m[1] == "==" else "tempo", m[2].strip(), m[3], m[4].strip(), [])
            out.append(cur)
        elif cur is not None:
            cur[4].append(riga.rstrip())
    return out


def righe_fallimento(testo):
    return [r.rstrip() for r in testo.splitlines() if FALLIMENTO.search(r)]


def per(nome, browser):
    return [v for v in voci() if v[1] == nome and v[2] in (browser, "tutti")]


def esito(nome, browser, file):
    testo = pathlib.Path(file).read_text(encoding="utf-8", errors="replace")
    tutte = set(r.rstrip() for r in testo.splitlines())
    fall = righe_fallimento(testo)
    if any("Traceback" in r for r in fall):
        return "NUOVO", "errore di Python nell'uscita"
    motivi = []
    for tipo, _, _, motivo, righe in per(nome, browser):
        if tipo == "noto":
            mancano = [r for r in righe if r not in tutte]
            in_piu = [r for r in fall if r not in righe]
            if not mancano and not in_piu:
                return "NOTO", motivo
            if mancano:
                motivi.append("fallimento noto cambiato, manca: " + mancano[0][:160])
            if in_piu:
                motivi.append("fallimento in più: " + in_piu[0][:160])
        else:
            singole = [r for r in fall if not RIASSUNTO.match(r)]
            if singole and all(any(f in r for f in righe) for r in singole):
                return "TEMPO", motivo
            fuori = [r for r in singole if not any(f in r for f in righe)]
            if fuori:
                motivi.append("non solo misure di tempo: " + fuori[0][:160])
    return "NUOVO", ("; ".join(motivi) if motivi else "non è nell'elenco dei fallimenti noti")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["esito"] and len(a) == 4:
        s, m = esito(a[1], a[2], a[3]); print(s + "\t" + m)
    elif a[:1] == ["c-e"] and len(a) == 3:
        sys.exit(0 if any(v[0] == "noto" for v in per(a[1], a[2])) else 1)
    elif a[:1] == ["righe"] and len(a) == 2:
        print("\n".join(righe_fallimento(pathlib.Path(a[1]).read_text(encoding="utf-8", errors="replace"))))
    else:
        print(__doc__ or "uso: vedi la testa del file", file=sys.stderr); sys.exit(2)
