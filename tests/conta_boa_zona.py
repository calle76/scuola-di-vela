# Conta, nelle registrazioni formato 3, cosa succede vicino alla boa 1: contatti e barche ingaggiate nella zona (3 lunghezze).
# Uso: python3 -I tests/conta_boa_zona.py registrazioni   (16 nov 2026, voce 49 di docs/DA-FARE.md; boa stimata dai punti di giro degli avversari, a 1,8 m in mediana)
import sys, re, glob, math, collections
L = 4.2; ZONA = 3 * L; VICINO = 25.0
def leggi(files):
    pos = collections.defaultdict(dict)  # t -> nome -> (x,y,prua)
    lato = {}; giro = {}; contatti = []; titolo = None; versione = None
    for f in files:
        for r in open(f, encoding='utf-8'):
            if r.startswith('# gioco') and titolo is None:
                m = re.search(r'gioco ([0-9.]+).*«([^»]*)»', r); versione, titolo = m.group(1), m.group(2)
            if r.startswith('S '):
                p = r.split(); t = round(float(p[1]), 1); pos[t]['Tu'] = (float(p[2]), float(p[3]), float(p[4]))
            elif r.startswith('B '):
                p = r.split(); t = round(float(p[1]), 1); n = p[2]
                pos[t][n] = (float(p[3]), float(p[4]), float(p[5])); lt = p[8]
                if lato.get(n) == '1' and lt == '2' and n not in giro: giro[n] = (t, float(p[3]), float(p[4]))
                lato[n] = lt
            elif r.startswith('E ') and ('contatto_barche' in r):
                p = r.split(); contatti.append((round(float(p[1]), 1), p[3], p[4]))
            elif r.startswith('T ') and 'Boa 1 girata' in r:
                t = round(float(r.split()[1]), 1); giro.setdefault('Tu', (t, None, None))
    return titolo, versione, pos, giro, contatti
def vicino_t(pos, t):
    if t in pos: return pos[t]
    k = min(pos, key=lambda u: abs(u - t)); return pos[k]
def ingaggiate(a, b):
    h = math.radians(a[2]); ux, uy = math.sin(h), -math.cos(h)  # y verso sud
    dx, dy = b[0] - a[0], b[1] - a[1]; along = dx * ux + dy * uy
    return abs(along) < L and abs(((a[2] - b[2] + 180) % 360) - 180) < 60
gruppi = collections.defaultdict(list)
for f in sorted(glob.glob(sys.argv[1] + '/*.txt')):
    if not open(f, encoding='utf-8').readline().strip().endswith('formato 3'): continue
    k = re.sub(r'-(pezzo-\d+|intera)\.txt$', '', f); gruppi[k].append(f)
tot = collections.Counter(); righe = []
for k, fs in gruppi.items():
    intere = [f for f in fs if f.endswith('intera.txt')]
    fs = intere[:1] if intere else sorted(fs)
    titolo, ver, pos, giro, contatti = leggi(fs)
    pts = [(x, y) for n, (t, x, y) in giro.items() if x is not None]
    if len(pts) < 2: continue
    bx = sum(p[0] for p in pts) / len(pts); by = sum(p[1] for p in pts) / len(pts)
    tot['regate'] += 1
    for n, (tg, _, _) in giro.items():  # ogni giro della boa: all'ingresso nella zona c'era un'altra barca ingaggiata?
        tz = None
        for t in sorted(u for u in pos if tg - 60 <= u <= tg):
            q = pos[t].get(n)
            if q and math.hypot(q[0] - bx, q[1] - by) < ZONA: tz = t; break
        if tz is None: continue
        tot['giri'] += 1; P = pos[tz]
        if any(m != n and math.hypot(P[m][0] - bx, P[m][1] - by) < ZONA + 2 * L and ingaggiate(P[n], P[m]) for m in P): tot['giri_ingaggiati'] += 1
    for (t, a, b) in contatti:
        P = vicino_t(pos, t)
        if a not in P or b not in P: tot['contatti_senza_pos'] += 1; continue
        d = min(math.hypot(P[a][0] - bx, P[a][1] - by), math.hypot(P[b][0] - bx, P[b][1] - by))
        tot['contatti'] += 1
        if d < VICINO:
            tot['contatti_boa'] += 1
            if d < ZONA + L: tot['contatti_zona'] += 1
            n3 = sum(1 for m in P if math.hypot(P[m][0] - bx, P[m][1] - by) < ZONA + L)
            righe.append(f'  {k.split("/")[-1]} {titolo} t={t} {a}-{b} a {d:.0f} m dalla boa, barche in zona: {n3}')
            if n3 >= 3: tot['contatti_boa_3barche'] += 1
print(dict(tot)); print('\n'.join(righe))
