# Misure sul registro di una sessione di torneo (formato 2, 1b): partenza, deriva prima dello sparo, giro della boa 1.
# Uso: python3 -I tests/analizza_registro_torneo.py FILE   (vento fisso per regata: preso da prua+twa al primo «via»)
import math, sys, collections
R = [l.split() for l in open(sys.argv[1]) if l[:2] in ("S ", "B ", "E ")]
AP = [float(r[1]) for r in R if r[0] == "E" and r[2] == "apre" and "regata" in r[3]]
AP = AP[:4] + [1e9]
reg = lambda t: next((i for i in range(4) if AP[i] <= t < AP[i + 1]), None)
LINE_HALF = 35
istr = {}                                   # fine delle istruzioni = inizio del conto alla rovescia di 180 s
for r in R:
    if r[0] == "E" and r[2] == "dialogo" and r[3] == "istruzioni_chiuso" and reg(float(r[1])) is not None: istr[reg(float(r[1]))] = float(r[1])
tr = collections.defaultdict(list)          # (regata, nome) -> (t, x, y, nodi, prua)
for r in R:
    t = float(r[1]); i = reg(t)
    if i is None: continue
    if r[0] == "B": tr[(i, r[2])].append((t, float(r[3]), float(r[4]), float(r[6]), float(r[5])))
    if r[0] == "S": tr[(i, "Tu")].append((t, float(r[2]), float(r[3]), float(r[5]), float(r[4])))
twd, gun, lat2 = {}, {}, {}
for i in range(4):
    via = min(float(r[1]) for r in R if r[0] == "B" and reg(float(r[1])) == i and "via" in r[-1])
    s = min((r for r in R if r[0] == "S" and reg(float(r[1])) == i), key=lambda r: abs(float(r[1]) - via))
    twd[i] = (float(s[4]) + float(s[7])) % 360; gun[i] = istr[i] + 180
for r in R:
    if r[0] == "E" and r[2] == "avv_lato" and r[4] == "2": lat2[(reg(float(r[1])), r[3])] = float(r[1])
    if r[0] == "E" and r[2] == "lato" and r[3] == "2": lat2[(reg(float(r[1])), "Tu")] = float(r[1])
def wf(i, x, y):
    a = math.radians(twd[i]); return x * math.sin(a) - y * math.cos(a), x * math.cos(a) + y * math.sin(a)  # [su, laterale]
print("== 1. Dove si taglia la linea (laterale in m, estremi ±%d)" % LINE_HALF)
for i in range(4):
    for n in ("Rossa", "Verde", "Blu", "Tu"):
        v = tr[(i, n)]; prev = None
        for t, x, y, _, _ in v:
            u, q = wf(i, x, y)
            if prev is not None and prev < 0 <= u and t > gun[i] - 30:
                print("regata %d %-5s t %7.1f  q %6.1f %s" % (i + 1, n, t, q, "FUORI" if abs(q) > LINE_HALF + 3 else "")); break
            prev = u
print("== 2. Laterale a 60/30/10/0 s dallo sparo (la deriva in attesa verso -q)")
for i in range(4):
    for n in ("Rossa", "Verde", "Blu"):
        q = []
        for d in (-60, -30, -10, 0):
            p = [x for x in tr[(i, n)] if abs(x[0] - (gun[i] + d)) < 0.6]
            q.append("%5.0f" % wf(i, p[0][1], p[0][2])[1] if p else "    -")
        print("regata %d %-5s" % (i + 1, n), *q)
print("== 3. Boa 1: giro totale di prua e percorso entro 40 m dalla boa, fino al lato 2")
boa = {}
for i in range(4):
    ps = [(x[1], x[2]) for k, v in tr.items() if k[0] == i and k in lat2 for x in v if abs(x[0] - lat2[k]) < 1.1]
    boa[i] = (sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps))
dh = lambda a, b: (b - a + 180) % 360 - 180
for k in sorted(tr):
    if k not in lat2: continue
    i, n = k; bx, by = boa[i]
    v = [x for x in tr[k] if x[0] <= lat2[k] and math.hypot(x[1] - bx, x[2] - by) <= 40]
    tot = lun = lenti = 0
    for a, b in zip(v, v[1:]):
        if b[0] - a[0] <= 1.2:      # i salti di più di 1,2 s sono pause del menu
            tot += abs(dh(a[4], b[4])); lun += math.hypot(b[1] - a[1], b[2] - a[2])
            if math.hypot(a[1] - bx, a[2] - by) <= 25 and a[3] < 1: lenti += b[0] - a[0]
    print("regata %d %-5s giro %4.0f gradi  percorso %3.0f m  sotto 1 nodo entro 25 m: %.1f s" % (i + 1, n, tot, lun, lenti))
