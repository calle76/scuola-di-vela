# Prepara js/suoni-dati.js dalle due registrazioni CC0 di Freesound (docs/PROPOSTA-SUONI-REGISTRATI.md, 1.2.7).
# Non è un collaudo: rifà il file dei suoni registrati, sempre uguale a partire dagli stessi due file.
#   vela:  377492 «Sailing boat - sail» (13FPanska_Mokrolusky_Tomas, CC0): i 16 colpi di tela, ritagliati uno per uno
#   acqua: 852108 «Sailboat Bow» (myLoop, CC0): 20 s dalla prua, rombo del vento sul microfono tolto, fine raccordata con l'inizio
# Le anteprime pubbliche (MP3 di qualità alta) si scaricano senza account:
#   https://cdn.freesound.org/previews/377/377492_6999362-hq.mp3   https://cdn.freesound.org/previews/852/852108_18387771-hq.mp3
# Uso: python3 prepara_suoni.py cartella_con_i_due_mp3   (servono ffmpeg con libopus; scrive ../js/suoni-dati.js)
import sys, subprocess, array, math, base64, pathlib, tempfile

SR = 48000
CARTELLA = pathlib.Path(sys.argv[1]); USCITA = pathlib.Path(__file__).resolve().parent.parent / "js" / "suoni-dati.js"
VELA, ACQUA = CARTELLA / "377492_6999362-hq.mp3", CARTELLA / "852108_18387771-hq.mp3"

def leggi(f, filtro, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + (["-t", str(t)] if t else []) + ["-i", str(f), "-ac", "1", "-ar", str(SR), "-af", filtro, "-f", "s16le", "-"]
    a = array.array("h"); a.frombytes(subprocess.run(cmd, capture_output=True, check=True).stdout); return [x / 32768 for x in a]

def opus(x):  # campioni -> Ogg Opus mono 48 kbit/s -> base64
    a = array.array("h", [int(max(-1, min(1, v)) * 32767) for v in x])
    with tempfile.TemporaryDirectory() as d:
        o = pathlib.Path(d) / "x.ogg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "libopus", "-b:a", "48k", "-map_metadata", "-1", "-fflags", "+bitexact", str(o)], input=a.tobytes(), check=True)
        b = o.read_bytes()
    return base64.b64encode(b).decode(), len(b)

rms = lambda x: math.sqrt(sum(v * v for v in x) / len(x))

# ---- vela: i colpi ----
v = leggi(VELA, "highpass=f=150")
n = SR // 100; e = [rms(v[i:i + n]) for i in range(0, len(v) - n, n)]   # inviluppo a 10 ms
fondo = sorted(e)[len(e) // 5]; picchi = []; i = 0
while i < len(e):   # un colpo: l'inviluppo supera 4 volte il fondo; il picco nei 150 ms dopo; il colpo dopo almeno 250 ms più in là
    if e[i] > 4 * fondo:
        j = max(range(i, min(i + 15, len(e))), key=lambda k: e[k]); picchi.append((j, 20 * math.log10(e[j] / fondo))); i = j + 25
    else: i += 1
SLOT, LUNGO = 0.6, 0.5   # ogni colpo occupa 0,5 s in uno spazio di 0,6 s del file (il resto è silenzio)
colpi, forti = [], []
for k, (j, dB) in enumerate(picchi):
    i0 = max(0, j * n - int(0.04 * SR)); c = v[i0:i0 + int(LUNGO * SR)]
    c = [s * min(1, t / (0.01 * SR)) * min(1, (len(c) - t) / (0.2 * SR)) for t, s in enumerate(c)]   # dissolvenze: 10 ms in entrata, 200 ms in uscita
    forte = dB >= 30; pk = max(abs(s) for s in c); c = [s * (0.8 if forte else 0.35) / pk for s in c]   # stesso picco per tutti i forti e per tutti i deboli
    colpi += c + [0.0] * (int(SLOT * SR) - len(c)); forti.append(1 if forte else 0)

# ---- acqua: il giro ----
L, F = 20.0, 1.0
x = leggi(ACQUA, "highpass=f=120", 20, L + F + 0.1)
NL, NF = int(L * SR), int(F * SR)
y = x[:NL]
for t in range(NF):   # i primi 1 s: dissolvenza fra l'inizio e quello che segue la fine, così il giro riparte senza stacco
    w = t / NF; y[t] = x[t] * math.sqrt(w) + x[NL + t] * math.sqrt(1 - w)
g = 0.1 / rms(y); y = [s * g for s in y]   # livello medio -20 dB, vicino a quello del fruscio sintetico che sostituisce

ba, na = opus(y); bc, nc = opus(colpi)
testo = (f"// Scuola di vela, suoni-dati.js — Suoni registrati (dalla 1.2.7, docs/PROPOSTA-SUONI-REGISTRATI.md): acqua e colpi di vela, Ogg Opus in base64. Fatto da tests/prepara_suoni.py, non si scrive a mano.\n"
         f"// Fonti CC0 (FONTI-PUBBLICHE.md F42, F43): vela Freesound 377492, 13FPanska_Mokrolusky_Tomas; acqua Freesound 852108, myLoop.\n"
         f"  const SUONI_DATI = {{\n"
         f"    colpi: {{ n: {len(forti)}, spazio: {SLOT}, lungo: {LUNGO}, forti: {forti} }},   // {len(forti)} colpi, uno ogni {SLOT} s del file; forti: 1 = colpo forte, 0 = rimbalzo debole\n"
         f"    acqua: {{ giro: {L} }},\n"
         f"    ogg: {{\n      acqua: \"{ba}\",\n      colpi: \"{bc}\"\n    }}\n  }};\n")
USCITA.write_text(testo, encoding="utf-8")
print(f"colpi: {len(forti)} ({sum(forti)} forti), {nc} byte; acqua: {L} s, {na} byte; {USCITA.name}: {len(testo.encode())} byte")
print("livelli dei colpi sopra il fondo (dB):", [round(d, 1) for _, d in picchi])
