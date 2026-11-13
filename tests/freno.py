# Freno termico: lancia un comando in un gruppo di processi suo e lo sospende (SIGSTOP) quando un core supera ALTO °C,
# lo riprende (SIGCONT) sotto BASSO °C. Uso: python freno.py ALTO BASSO comando...
import os, re, signal, subprocess, sys, time
alto, basso, cmd = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3:]
def caldo():
    try: return max(float(x) for x in re.findall(r"Core \d+:\s+\+([\d.]+)", subprocess.run(["sensors"], capture_output=True, text=True).stdout))
    except Exception: return 0
p = subprocess.Popen(cmd, start_new_session=True)
def discendenti(radice):
    figli = {}
    for d in os.listdir("/proc"):
        if d.isdigit():
            try: pp = int(open(f"/proc/{d}/stat").read().rsplit(")", 1)[1].split()[1]); figli.setdefault(pp, []).append(int(d))
            except Exception: pass
    out, coda = [], [radice]
    while coda:
        x = coda.pop(); out.append(x); coda += figli.get(x, [])
    return out
def segnala(sig):
    for q in discendenti(p.pid):
        try: os.kill(q, sig)
        except Exception: pass
fermo, pause, picco = False, 0, 0
while p.poll() is None:
    t = caldo(); picco = max(picco, t)
    if not fermo and t >= alto: segnala(signal.SIGSTOP); fermo = True; pause += 1
    elif fermo and t <= basso: segnala(signal.SIGCONT); fermo = False
    time.sleep(1)
    if fermo: segnala(signal.SIGSTOP)  # i processi nati nel frattempo
print(f"freno: {pause} pause, picco {picco:.0f} °C, uscita {p.returncode}", flush=True)
sys.exit(p.returncode)
