# Prepara js/suoni-dati.js dalle registrazioni CC0 di Freesound (docs/PROPOSTA-SUONI-REGISTRATI.md, 1.2.7; docs/PROPOSTA-SUONI-FINE.md, 1.2.9).
# Non è un collaudo: rifà il file dei suoni registrati, sempre uguale a partire dagli stessi file.
#   vela:         377492 «Sailing boat - sail» (13FPanska_Mokrolusky_Tomas): i 16 colpi di tela, ritagliati uno per uno
#   acqua:        852108 «Sailboat Bow» (myLoop): 20 s dalla prua, rombo del vento sul microfono tolto, fine raccordata con l'inizio
#   vento:        659004 «Wind at Ocean shore» (Tom_Kaszuba): giro di 20 s
#   sciabordio:   637206 «boat knocks fiberglass water laps on hull» (kyles): giro di 20 s
#   sartiame:     463373 «Storm wind whistling through harbour boat masts» (dangale): giro di 12 s, solo il fischio
#   gorgoglio:    574866 «Water under boat gurgling waves» (TRP): giro di 10 s
#   gabbiani:     496203 «Seagull» (poodaddy69) e 510917 «Seagulls_short» (Lydmakeren): 5 versi ritagliati a mano
#   scricchiolii: 145721 «Mooring Rope» (Rmutt): 4 gruppi ritagliati a mano
#   1.2.10: tela (Z) 870603 CHallSmith; boma 630432 KaleidacousticsAudio; colpo 799644 KudoShimon; scafo 637207 kyles; boa 538009 bruno.auzet;
#           tuffo 469608 Sheyvan e 442773 qubodup; scolo 110593 korbel; tromba 131930 mcpable (docs/PROPOSTA-SUONI-FINE.md §7)
# Le anteprime pubbliche (MP3 di qualità alta) si scaricano senza account, tutte da https://cdn.freesound.org/previews/ :
#   377/377492_6999362-hq.mp3  852/852108_18387771-hq.mp3  659/659004_11673893-hq.mp3  637/637206_612689-hq.mp3  463/463373_2194924-hq.mp3
#   574/574866_97550-hq.mp3  496/496203_8923841-hq.mp3  510/510917_11157357-hq.mp3  145/145721_981371-hq.mp3
#   870/870603_18412227-hq.mp3  630/630432_13875907-hq.mp3  799/799644_7316601-hq.mp3  637/637207_612689-hq.mp3  538/538009_11519060-hq.mp3
#   469/469608_3248005-hq.mp3  442/442773_71257-hq.mp3  110/110593_1848499-hq.mp3  131/131930_1542102-hq.mp3
# Uso: python3 prepara_suoni.py cartella_con_i_mp3   (servono ffmpeg con libopus; scrive ../js/suoni-dati.js)
import sys, subprocess, array, math, base64, pathlib, tempfile, json

SR = 48000
CARTELLA = pathlib.Path(sys.argv[1]); USCITA = pathlib.Path(__file__).resolve().parent.parent / "js" / "suoni-dati.js"
VELA, ACQUA = CARTELLA / "377492_6999362-hq.mp3", CARTELLA / "852108_18387771-hq.mp3"

def leggi(f, filtro, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + (["-t", str(t)] if t else []) + ["-i", str(f), "-ac", "1", "-ar", str(SR), "-af", filtro, "-f", "s16le", "-"]
    a = array.array("h"); a.frombytes(subprocess.run(cmd, capture_output=True, check=True).stdout); return [x / 32768 for x in a]

def opus(x, kbit=48):  # campioni -> Ogg Opus mono -> base64
    a = array.array("h", [int(max(-1, min(1, v)) * 32767) for v in x])
    with tempfile.TemporaryDirectory() as d:
        o = pathlib.Path(d) / "x.ogg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "libopus", "-b:a", f"{kbit}k", "-map_metadata", "-1", "-fflags", "+bitexact", str(o)], input=a.tobytes(), check=True)
        b = o.read_bytes()
    return base64.b64encode(b).decode(), len(b)

rms = lambda x: math.sqrt(sum(v * v for v in x) / len(x))

def giro(f, filtro, ss, L, livello=0.1, F=1.0):  # un giro di L s: i primi F s raccordati con quello che segue la fine, così riparte senza stacco; livello medio fissato
    x = leggi(f, filtro, ss, L + F + 0.1)
    NL, NF = int(L * SR), int(F * SR)
    y = x[:NL]
    for t in range(NF):
        w = t / NF; y[t] = x[t] * math.sqrt(w) + x[NL + t] * math.sqrt(1 - w)
    g = livello / rms(y); return [s * g for s in y]

def pezzi(lista, picco=0.8):  # ritagli a mano [(file, filtro, inizio, durata)] uno dopo l'altro, stesso picco, dissolvenze 20 ms / 150 ms; -> campioni e [[inizio, durata], ...] nel file
    tutto, indice = [], []
    for f, filtro, ss, t in lista:
        c = leggi(f, filtro, ss, t)
        c = [s * min(1, i / (0.02 * SR)) * min(1, (len(c) - i) / (0.15 * SR)) for i, s in enumerate(c)]
        pk = max(abs(s) for s in c); c = [s * picco / pk for s in c]
        indice.append([round(len(tutto) / SR, 3), round(len(c) / SR, 3)])
        tutto += c + [0.0] * int(0.05 * SR)
    return tutto, indice

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
y = giro(ACQUA, "highpass=f=120", 20, L, 0.1, F)   # livello medio -20 dB, vicino a quello del fruscio sintetico che sostituisce

ba, na = opus(y); bc, nc = opus(colpi)

# ---- 1.2.9: gli altri suoni (punti di taglio scelti leggendo l'inviluppo di ogni file) ----
C = CARTELLA
altri = {
    "vento":     (giro(C / "659004_11673893-hq.mp3", "highpass=f=100", 20, 20.0, 0.13), 32),
    "onde":      (giro(C / "637206_612689-hq.mp3", "highpass=f=80", 4, 20.0), 32),
    "sartiame":  (giro(C / "463373_2194924-hq.mp3", "highpass=f=800", 36, 12.0), 32),   # solo il fischio: il rombo della tempesta sta sotto gli 800 Hz
    "gorgoglio": (giro(C / "574866_97550-hq.mp3", "highpass=f=150", 29, 10.0), 32),
}
G1, G2 = C / "496203_8923841-hq.mp3", C / "510917_11157357-hq.mp3"
gabb, ind_g = pezzi([(G1, "highpass=f=700", 0.45, 1.25), (G1, "highpass=f=700", 1.85, 1.45), (G2, "highpass=f=1000", 3.1, 1.7), (G2, "highpass=f=1000", 4.8, 2.0), (G2, "highpass=f=1000", 6.8, 2.2)])
S = C / "145721_981371-hq.mp3"
scr, ind_s = pezzi([(S, "highpass=f=300", 31.0, 2.0), (S, "highpass=f=300", 36.2, 2.4), (S, "highpass=f=300", 55.8, 1.8), (S, "highpass=f=300", 58.9, 2.2)])
altri["gabbiani"] = (gabb, 48); altri["scricchioli"] = (scr, 32)
# ---- 1.2.10: Z e gli eventi (tutti in un solo file, con l'indice dei ritagli per nome) ----
altri["tela"] = (giro(C / "870603_18412227-hq.mp3", "highpass=f=150", 1.5, 8.0), 32)
BOMA, COLPO, SCAFO, BOA, SCOLO, TROMBA = (C / x for x in ("630432_13875907-hq.mp3", "799644_7316601-hq.mp3", "637207_612689-hq.mp3", "538009_11519060-hq.mp3", "110593_1848499-hq.mp3", "131930_1542102-hq.mp3"))
RITAGLI = {
    "boma":   [(BOMA, "highpass=f=150", 14.0, 1.3), (BOMA, "highpass=f=150", 30.75, 1.5)],
    "colpo":  [(COLPO, "highpass=f=60", 4.5, 0.6), (COLPO, "highpass=f=60", 5.65, 0.6), (COLPO, "highpass=f=60", 9.95, 0.6)],
    "scafo":  [(SCAFO, "highpass=f=60", 0.25, 0.8), (SCAFO, "highpass=f=60", 1.75, 0.8), (SCAFO, "highpass=f=60", 6.0, 0.9), (SCAFO, "highpass=f=60", 14.0, 0.8)],
    "boa":    [(BOA, "highpass=f=200", 3.6, 0.9), (BOA, "highpass=f=200", 14.2, 1.0), (BOA, "highpass=f=200", 19.6, 0.9)],
    "tuffo":  [(C / "469608_3248005-hq.mp3", "highpass=f=50", 0, 2.0), (C / "442773_71257-hq.mp3", "highpass=f=50", 0, 2.2)],
    "scolo":  [(SCOLO, "highpass=f=200", 3.0, 3.5)],
    "tromba": [(TROMBA, "highpass=f=100", 0.28, 0.75)],
    "tromba_lunga": [(TROMBA, "highpass=f=100", 0.28, 1.75)],
    "arrivo": [(TROMBA, "highpass=f=100", 0.28, 0.4)],
}
ev, ind_ev = [], {}
for nome, lista in RITAGLI.items():
    x, idx = pezzi(lista); ind_ev[nome] = [[round(a + len(ev) / SR, 3), b] for a, b in idx]; ev += x
altri["eventi"] = (ev, 32)
ogg = {k: opus(x, kb) for k, (x, kb) in altri.items()}

testo = (f"// Scuola di vela, suoni-dati.js — Suoni registrati (dalla 1.2.7, docs/PROPOSTA-SUONI-REGISTRATI.md; dalla 1.2.9 docs/PROPOSTA-SUONI-FINE.md): Ogg Opus in base64. Fatto da tests/prepara_suoni.py, non si scrive a mano.\n"
         f"// Fonti CC0 (FONTI-PUBBLICHE.md F42-F59): vela 377492, acqua 852108, vento 659004, sciabordio 637206, sartiame 463373, gorgoglio 574866, gabbiani 496203 e 510917, scricchiolii 145721, tela 870603, boma 630432, colpo 799644, scafo 637207, boa 538009, tuffo 469608 e 442773, scolo 110593, tromba 131930 (numeri di Freesound).\n"
         f"  const SUONI_DATI = {{\n"
         f"    colpi: {{ n: {len(forti)}, spazio: {SLOT}, lungo: {LUNGO}, forti: {forti} }},   // {len(forti)} colpi, uno ogni {SLOT} s del file; forti: 1 = colpo forte, 0 = rimbalzo debole\n"
         f"    acqua: {{ giro: {L} }},\n"
         f"    gabbiani: {json.dumps(ind_g)},   // [inizio, durata] di ogni verso, in s\n"
         f"    scricchioli: {json.dumps(ind_s)},   // [inizio, durata] di ogni gruppo, in s\n"
         f"    eventi: {json.dumps(ind_ev)},   // 1.2.10: i ritagli di ogni suono breve, [inizio, durata] in s\n"
         f"    ogg: {{\n      acqua: \"{ba}\",\n      colpi: \"{bc}\",\n"
         + "".join(f"      {k}: \"{ogg[k][0]}\",\n" for k in altri) +
         f"    }}\n  }};\n")
USCITA.write_text(testo, encoding="utf-8")
print(f"colpi: {len(forti)} ({sum(forti)} forti), {nc} byte; acqua: {L} s, {na} byte; {USCITA.name}: {len(testo.encode())} byte")
print("livelli dei colpi sopra il fondo (dB):", [round(d, 1) for _, d in picchi])
print("altri (byte):", {k: ogg[k][1] for k in altri})
