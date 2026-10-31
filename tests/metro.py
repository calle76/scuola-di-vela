# Metro comune dei collaudi (dalla proposta «test dei test», 1 novembre 2026, docs/PROPOSTA-TEST-DEI-TEST.md).
# tutti(prove, minimo=1): come all(), ma è vero solo se le prove sono almeno «minimo». Un controllo «tutti i casi
#   vanno bene» scritto con all() è vero anche con zero casi: questo no.
# nessuno(prove, minimo=1): come «not any()», con lo stesso minimo di casi.
# Alla fine del collaudo stampa una riga «METRO:» con quanti controlli a conteggio ha fatto e il numero di casi
# più piccolo visto; se un controllo ha avuto meno casi del minimo lo nomina (riga del file e casi), e quel
# controllo è già falso, quindi il collaudo cade per conto suo.
import atexit, os, sys

_visti = []   # (file:riga, casi, minimo)

def _segna(n, minimo):
    f = sys._getframe(2)
    _visti.append(("%s:%d" % (os.path.basename(f.f_code.co_filename), f.f_lineno), n, minimo))

def tutti(prove, minimo=1):
    lista = list(prove); _segna(len(lista), minimo)
    return len(lista) >= minimo and all(lista)

def nessuno(prove, minimo=1):
    lista = list(prove); _segna(len(lista), minimo)
    return len(lista) >= minimo and not any(lista)

@atexit.register
def _riepilogo():
    if not _visti: return
    sotto = [v for v in _visti if v[1] < v[2]]
    print("METRO: %d controlli a conteggio, casi da %d a %d%s" % (len(_visti), min(v[1] for v in _visti), max(v[1] for v in _visti),
          "" if not sotto else "; SOTTO IL MINIMO: " + ", ".join("%s (%d casi, minimo %d)" % v for v in sotto[:12])))
