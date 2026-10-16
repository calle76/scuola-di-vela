# Competizione (0.21): piazzamento salvato e taratura della scala dei punti delle regate.
#
# Parte 1, pilota sostituto (pagina con #collaudo). La barca del giocatore la guida __sv.pilota: la guida degli avversari
# principianti (aiControl) con lo stesso bersaglio degli avversari; dopo 1 s di scuffia raddrizza (ipotesi nostra: un giocatore
# che preme il tasto). Ogni regata in una pagina nuova (contesto nuovo, quindi salvataggio vuoto), Math.random a seme fisso,
# simTime a zero, fast(0), passi fissi di 1/60 s con __sv.run, 3 minuti di preparazione. Il piazzamento si legge da quello che
# il gioco ha salvato in localStorage (progress.race), e si confronta con un calcolo indipendente dai tempi d'arrivo.
# Punti di una regata: 4/3/2/1 per 1°/2°/3°/4°; regata non finita = 0. Dalla 0.23 senza il «+1 senza errori» (decisione di Ale,
# 14 ottobre 2026: meriti separati dalla classifica). Fino alla 0.22 c'era il +1, ma il sostituto non ha mai finito una regata pulita.
#
# Criteri scritti prima dei risultati (docs/PROPOSTA-ESAME-E-BREVETTO.md §4, decisioni di Ale per la 0.21), da non cambiare dopo:
#   C0 arrivate almeno il 90% delle regate per tipo (bastone, raffiche); sotto, la misura non vale: ci si ferma e si riporta.
#   C1 ogni piazzamento 1°-4° fra il 10% e il 40%, contato sulle regate arrivate dei due tipi insieme (denominatore stampato).
#   C2 coppia seme k (regata 1 + regata 2): almeno 3 punti in almeno il 60% delle coppie.
#   C3 finestre scorrenti di 3 semi consecutivi (1-3, 2-4, ...: si sovrappongono, quindi non sono indipendenti): migliore dei 3
#      per ogni regata, somma dei due almeno 3, in almeno il 90% delle finestre.
#   C4 punteggio massimo (fino alla 0.22 10 punti, dalla 0.23 8: due primi posti) in al massimo il 10% delle coppie.
#   C5 regate arrivate e coppie stampate; fallisce se zero; il sostituto deve aver mosso la barra in ogni regata.
# Semi 1-40: misura. Semi 41-80: conferma con le stesse soglie. Poi gli stessi semi con gli avversari esperti, solo riportati.
# Sempre: il piazzamento salvato coincide con quello calcolato dai tempi; con «nessuno» non si salva niente.
#
# Parte 2 (--tastiera), pagina senza #collaudo, come la carica un giocatore: un pilota da tastiera legge il pannello (prua,
# rilevamento, vento, scotta, barra, classifica) e il conto alla rovescia scritto sul mare, in tempo reale, 1 minuto di
# preparazione, regata a bastone (vento fisso da nord: il pilota lo sa, come chi guarda il riquadro del vento sul mare). Con avversari progress.race deve esserci, con «nessuno» no. Se il pilota non arriva in fondo
# l'esito è NON VALIDO, non FALLITO. Le due regate girano in parallelo, circa 10 minuti in tutto.
#
# Uso: python collaudo_competizione.py              # parte 1 completa (320 regate, circa 10 minuti nella sandbox)
#      python collaudo_competizione.py --veloce     # semi 1-3, solo salvataggio, barra e «nessuno»: soglie non valutate
#      python collaudo_competizione.py --tastiera   # parte 2 (circa 10 minuti: le due regate in parallelo)
import asyncio, pathlib, sys, time
from playwright.async_api import async_playwright

BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
STORE = "scuolaVelaSim.v1"
CHIAVI = ["r0.3", "r1.3"]   # recK("r0"), recK("r1"): KEYV in index.html
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""

CORSA = """([race, seme, liv, chiave]) => {
  const sv = __sv; sv.fast(0);
  sv.openItem(["r", race]);
  __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change")); // riparte col seme
  const R = sv.R, me = R.boats[0], t0 = R.t, dt = 1 / 60;
  let n = 0, moved = 0, prev = null, arrPos = null;
  while (me.fin === null && R.t < 900) {
    const t = sv.pilota(dt); if (prev !== null && Math.abs(t - prev) > 1e-9) moved++; prev = t;
    sv.run(dt, 1); n++;
  }
  const reg = Object.assign({}, sv.reg);                                          // registro degli errori all'arrivo (o al limite di tempo)
  if (me.fin !== null) {
    arrPos = sv.rank().findIndex(s => s.startsWith("Tu:")) + 1;                  // piazzamento all'istante dell'arrivo
    let k = 0; while (k < 60 * 400 && !R.boats.every(b => b.fin !== null)) { sv.run(dt, 1); k++; }  // poi fino all'arrivo di tutte, o 400 s
  }
  const all = R.boats.every(b => b.fin !== null);
  // calcolo indipendente: una barca mi batte se è arrivata con tempo netto minore; chi non è arrivata non può più (R.t >= me.fin)
  const indep = me.fin === null ? null : 1 + R.boats.filter(b => !b.me && b.fin !== null && b.fin < me.fin).length;
  let race_ = null; try { race_ = (JSON.parse(localStorage.getItem("%s") || "{}").race) || null; } catch (e) {}
  return { reg, t0, fin: me.fin, arrPos, indep, rt: R.t, all, n: R.boats.length, moved, passi: n,
           saved: race_ ? race_[chiave] || null : null, chiavi: race_ ? Object.keys(race_) : [] };
}""" % STORE

REG_NOMI = [("capsizes", "scuffie"), ("gybesV", "strambate a vela aperta"), ("irons", "piantato"), ("wrongMarks", "boe sbagliate"),
            ("contacts", "contatti"), ("ocs", "partenza anticipata"), ("outLine", "fuori linea")]

def punti(r):
    if r["fin"] is None or not r["saved"]: return 0
    return 5 - r["saved"]["pos"]

errori = []
def no(msg):
    errori.append(msg); print("  NO  " + msg, flush=True)

async def corsa(b, race, seme, liv):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650})
    pg = await ctx.new_page(); await pg.add_init_script(SEME)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(150)
    r = await pg.evaluate(CORSA, [race, seme, liv, CHIAVI[race] + ":" + liv])
    await ctx.close()
    if errs: no(f"regata {race + 1} seme {seme} {liv}: errore nella pagina {errs[0]}")
    if r["t0"] != -180: no(f"regata {race + 1} seme {seme}: preparazione {r['t0']} s invece di 180")
    if r["moved"] == 0: no(f"regata {race + 1} seme {seme} {liv}: il sostituto non ha mosso la barra")
    if liv == "nessuno":
        if r["chiavi"]: no(f"«nessuno», regata {race + 1} seme {seme}: progress.race non doveva esserci, trovato {r['chiavi']}")
    elif r["fin"] is not None:
        s = r["saved"]
        if not s: no(f"regata {race + 1} seme {seme} {liv}: arrivato ma piazzamento non salvato (chiavi {r['chiavi']})")
        elif s["pos"] != r["indep"] or s["n"] != r["n"]:
            no(f"regata {race + 1} seme {seme} {liv}: salvato {s} ma dai tempi {r['indep']}° su {r['n']}")
    return r

def riga(r):
    if r["fin"] is None: return "non arrivato"
    s = r["saved"] or {}
    return f"{s.get('pos')}° su {s.get('n')} {'pulita' if s.get('pulita') else 'con errori'} in {r['fin']:.1f} s, all'arrivo {r['arrPos']}°"

async def gruppo(b, semi, liv, soglie, nome):
    print(f"\n== {nome}: avversari {liv}, semi {semi[0]}-{semi[-1]}" + ("" if soglie else " (solo riportato, senza soglie)"), flush=True)
    t0 = time.time(); res = {0: {}, 1: {}}
    for race in (0, 1):
        for s in semi:
            r = await corsa(b, race, s, liv); res[race][s] = r
            print(f"  regata {race + 1} seme {s}: {riga(r)} · barra mossa in {r['moved']} passi su {r['passi']}", flush=True)
    arr = {race: [s for s in semi if res[race][s]["fin"] is not None] for race in (0, 1)}
    diff = sum(1 for race in (0, 1) for s in arr[race] if res[race][s]["arrPos"] != (res[race][s]["saved"] or {}).get("pos"))
    tot_arr = len(arr[0]) + len(arr[1])
    print(f"  arrivate: bastone {len(arr[0])} su {len(semi)}, raffiche {len(arr[1])} su {len(semi)}; "
          f"piazzamento all'arrivo diverso da quello finale: {diff} su {tot_arr}; tempo reale {time.time() - t0:.0f} s", flush=True)
    regate = [res[r][s] for r in (0, 1) for s in semi]
    print("  errori del registro, regate in cui compaiono (su %d): " % len(regate) + ", ".join(
        f"{nome_e} {sum(1 for x in regate if x['reg'].get(k, 0) > 0)}" for k, nome_e in REG_NOMI), flush=True)
    print(f"  regate senza errori (pulite): {sum(1 for x in regate if x['saved'] and x['saved']['pulita'])} su {tot_arr} arrivate", flush=True)
    esito = []
    def crit(nome_c, ok, testo):
        print(f"  {'OK ' if ok else 'NO '} {nome_c}: {testo}", flush=True)
        if soglie: esito.append((nome_c, ok))
    # C5 prima: senza regate o coppie gli altri criteri non hanno misurato niente
    coppie = len(semi)
    crit("C5", tot_arr > 0 and coppie > 0 and all(res[r][s]["moved"] > 0 for r in (0, 1) for s in semi),
         f"regate arrivate {tot_arr}, coppie {coppie}, barra mossa in tutte le {2 * len(semi)} regate")
    c0 = [len(arr[r]) / len(semi) for r in (0, 1)]
    crit("C0", min(c0) >= 0.9, f"arrivate bastone {c0[0]:.0%}, raffiche {c0[1]:.0%} (soglia 90% per tipo)")
    if soglie and min(c0) < 0.9:
        print("  C0 sotto soglia: la misura non vale. Mi fermo qui.", flush=True)
        return esito, False
    pos = [res[r][s]["saved"]["pos"] for r in (0, 1) for s in arr[r] if res[r][s]["saved"]]
    quote = [pos.count(p) / len(pos) if pos else 0 for p in (1, 2, 3, 4)]
    for r in (0, 1):
        pr = [res[r][s]["saved"]["pos"] for s in arr[r] if res[r][s]["saved"]]
        print(f"      regata {r + 1}: " + ", ".join(f"{p}° {pr.count(p)}" for p in (1, 2, 3, 4)) + f" su {len(pr)} arrivate", flush=True)
    crit("C1", bool(pos) and all(0.10 <= q <= 0.40 for q in quote),
         ", ".join(f"{p}° {pos.count(p)} ({q:.0%})" for p, q in zip((1, 2, 3, 4), quote)) + f" su {len(pos)} arrivate (fascia 10-40%)")
    P = {r: {s: punti(res[r][s]) for s in semi} for r in (0, 1)}
    somme = [P[0][s] + P[1][s] for s in semi]
    c2 = sum(1 for x in somme if x >= 3) / len(somme)
    crit("C2", c2 >= 0.6, f"coppie con almeno 3 punti {sum(1 for x in somme if x >= 3)} su {len(somme)} ({c2:.0%}, soglia 60%); "
         f"punti per coppia: " + " ".join(map(str, somme)))
    fin = [semi[i:i + 3] for i in range(len(semi) - 2)]
    ok3 = sum(1 for w in fin if max(P[0][s] for s in w) + max(P[1][s] for s in w) >= 3)
    crit("C3", ok3 / len(fin) >= 0.9, f"finestre scorrenti (sovrapposte) con almeno 3 punti {ok3} su {len(fin)} ({ok3 / len(fin):.0%}, soglia 90%)")
    c4 = sum(1 for x in somme if x == 8)
    crit("C4", c4 / len(somme) <= 0.1, f"coppie a 8 punti (due primi posti) {c4} su {len(somme)} ({c4 / len(somme):.0%}, soglia al massimo 10%)")
    return esito, True

async def parte1(veloce):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        print("== «nessuno»: una regata a bastone, seme 1: niente piazzamento salvato", flush=True)
        r = await corsa(b, 0, 1, "nessuno")
        print(f"  arrivato: {r['fin'] is not None}; chiavi di progress.race: {r['chiavi']}", flush=True)
        if r["fin"] is None: no("«nessuno»: il sostituto non è arrivato, il controllo non ha misurato niente")
        tutti = []
        if veloce:
            await gruppo(b, list(range(1, 4)), "principianti", False, "veloce")
        else:
            for semi, nome in ((list(range(1, 41)), "misura"), (list(range(41, 81)), "conferma")):
                esito, valida = await gruppo(b, semi, "principianti", True, nome)
                tutti += [(nome, c, ok) for c, ok in esito]
                if not valida: break
            else:
                for semi in (list(range(1, 41)), list(range(41, 81))):
                    await gruppo(b, semi, "esperti", False, "esperti")
        await b.close()
    print("\n== riepilogo", flush=True)
    for nome, c, ok in tutti: print(f"  {nome} {c}: {'OK' if ok else 'NO'}")
    print(f"  controlli del salvataggio e della barra: {len(errori)} errori", flush=True)
    sbagliati = [t for t in tutti if not t[2]] + errori
    print("ESITO: " + ("OK" if not sbagliati else "FALLITO"), flush=True)
    sys.exit(1 if sbagliati else 0)

# ---------------------------------------------------------------- parte 2: pagina senza #collaudo, pilota da tastiera
TESTO = """(() => { window.__testi = []; const f = CanvasRenderingContext2D.prototype.fillText;
  CanvasRenderingContext2D.prototype.fillText = function (t, ...a) { if (typeof t === "string" && /^(Partenza tra|Alla linea)/.test(t)) window.__testi.push(t);
    if (window.__testi.length > 50) window.__testi.splice(0, 25); return f.call(this, t, ...a); }; })();"""
LEGGI = """() => { const $ = id => document.getElementById(id), tx = id => $(id).textContent;
  const me = document.querySelector("#standings li.me span"), t = window.__testi;
  const conto = [...t].reverse().find(s => s.startsWith("Partenza tra")), linea = [...t].reverse().find(s => s.startsWith("Alla linea"));
  window.__testi = [];
  return { hdg: parseFloat(tx("iHdg")), brg: parseFloat(tx("iBrg")), twa: parseFloat(tx("iTw")), awa: parseFloat(tx("iAw")), spd: parseFloat(tx("iSpd")),
           heel: parseFloat(tx("iHeel")), tiller: +$("tiller").value / 100, sheet: +$("sheet").value / 100, stato: me ? me.textContent : "",
           conto: conto || null, linea: linea || null, cap: !$("capOverlay").hidden, sv: typeof window.__sv }; }"""

def n180(a): return (a + 180) % 360 - 180

async def regata_tastiera(b, liv):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650})
    pg = await ctx.new_page(); await pg.add_init_script(TESTO)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(BASE); await pg.wait_for_timeout(300)
    if await pg.evaluate("typeof window.__sv") != "undefined": no("senza #collaudo window.__sv esiste")
    await pg.click("[data-r='0']"); await pg.wait_for_timeout(200)
    await pg.select_option("#aiLevel", liv); await pg.wait_for_timeout(150)
    await pg.select_option("#cdSel", "60"); await pg.wait_for_timeout(150)
    await pg.click("#bGo"); await pg.click("#c"); await pg.wait_for_timeout(100)
    giu = set()
    async def tasto(k, on):
        if on and k not in giu: await pg.keyboard.down(k); giu.add(k)
        elif not on and k in giu: await pg.keyboard.up(k); giu.discard(k)
    side, giro, inizio, t_end, t_via, traccia, dist = 1, False, time.time(), None, None, 0, 40
    while time.time() - inizio < 720:
        s = await pg.evaluate(LEGGI)
        if s["cap"]:
            await pg.keyboard.press("r"); await pg.wait_for_timeout(300); continue
        if "arrivata" in s["stato"]:
            t_end = time.time(); break
        twd = 0   # il pannello scrive l'angolo del vento senza segno: la regata a bastone ha il vento fisso da nord (RACES[0]), come mostra il riquadro del vento sul mare
        if s["brg"] != s["brg"]: s["brg"] = twd   # rilevamento «—»
        rel = n180(s["brg"] - twd)
        if s["conto"]:   # il conto si legge solo se il gioco l'ha disegnato da poco: si ricorda l'ora prevista del via
            m, sec = s["conto"].replace("Partenza tra ", "").split(":"); t_via = time.time() + int(m) * 60 + int(sec)
        conto = t_via - time.time() if t_via is not None else None
        if time.time() - traccia > 60:
            traccia = time.time(); print(f"    [{liv}] {time.time() - inizio:.0f} s: {s['stato']}, prua {s['hdg']}°, rilevamento {s['brg']}°, {s['spd']} kn", flush=True)
        if s["linea"]: dist = float(s["linea"].split(":")[1].split("m")[0])   # anche la distanza dalla linea si ricorda
        want, lasca = None, False
        if conto is not None and conto > dist / 1.3 + 8:   # prima del via: ferma quasi di bolina con la vela che sbatte
            want, lasca = twd + 62 * side, True
        elif "di bolina" in s["stato"]:                      # verso la boa: arrivo mure a sinistra da destra, poi le giro attorno a sinistra
            relb = n180(s["brg"] - s["hdg"])
            if giro or relb < -100:
                giro = True; want = s["brg"] + 90
            else:
                if rel > -12: side = 1
                elif rel < -55: side = -1
                want = twd + side * 48
        else:                                                # partenza, ritorno dietro la linea, arrivo: verso il rilevamento
            giro = False; want = s["brg"]
            if abs(rel) < 48:
                if abs(rel) > 12: side = 1 if rel > 0 else -1
                want = twd + side * 48
            cur = n180(s["hdg"] - twd)
            if abs(rel) > 165 and abs(cur) > 90: want = twd + (1 if cur > 0 else -1) * 165
        d = n180(want - twd)
        if abs(d) < 46: want = twd + (1 if d >= 0 else -1) * 46   # mai nell'angolo morto
        if abs(s["twa"]) < 44 and s["spd"] < 1.2: want, lasca = twd + (1 if n180(s["hdg"] - twd) > 0 else -1) * 95, True   # piantata: poggia sulle sue mure con la vela lascata
        err = n180(s["hdg"] - want)
        tt = max(-1, min(1, err / 25)) * (-1 if s["spd"] < 0 else 1)   # all'indietro la barra agisce al contrario
        await tasto("ArrowRight", s["tiller"] < tt - 0.08); await tasto("ArrowLeft", s["tiller"] > tt + 0.08)
        st = 1 if lasca else max(0, min(1, (max(14, abs(s["awa"]) - 17) - 14) / 71))
        if s["heel"] > 22: st = min(1, st + 0.2)
        await tasto("ArrowUp", s["sheet"] > st + 0.05); await tasto("ArrowDown", s["sheet"] < st - 0.05)
        await pg.wait_for_timeout(80)
    for k in list(giu): await tasto(k, False)
    arrivato = t_end is not None
    if arrivato: await pg.wait_for_timeout(60000)   # il piazzamento si salva quando è definitivo: entro la mia penalità
    store = await pg.evaluate(f"JSON.parse(localStorage.getItem('{STORE}') || '{{}}')")
    stato = await pg.evaluate("(document.querySelector('#standings li.me span') || {}).textContent || ''")
    await ctx.close()
    if errs: no(f"tastiera, {liv}: errore nella pagina {errs[0]}")
    return arrivato, store, stato, time.time() - inizio

async def parte2():
    validi = True
    async with async_playwright() as p:
        b = await p.chromium.launch()
        esiti = await asyncio.gather(*(regata_tastiera(b, liv) for liv in ("principianti", "nessuno")))   # in parallelo: circa 10 minuti invece di 18
        for liv, (arrivato, store, stato, durata) in zip(("principianti", "nessuno"), esiti):
            race = store.get("race")
            print(f"== tastiera, avversari {liv}: {'arrivato' if arrivato else 'NON ARRIVATO'} ({stato}) in {durata:.0f} s reali; "
                  f"progress.race = {race}; done.r0 = {store.get('done', {}).get('r0')}", flush=True)
            if not arrivato:
                validi = False; print("  NON VALIDO: il pilota da tastiera non è arrivato in fondo", flush=True); continue
            if liv == "nessuno":
                if race: no(f"«nessuno» senza #collaudo: progress.race non doveva esserci, trovato {race}")
                else: print("  OK  nessun piazzamento salvato", flush=True)
            else:
                v = (race or {}).get("r0.3:principianti")
                if not v or set(v) != {"pos", "n", "pulita"} or v["n"] != 4: no(f"principianti senza #collaudo: piazzamento atteso in r0.3:principianti, trovato {race}")
                else: print(f"  OK  piazzamento salvato: {v}", flush=True)
        await b.close()
    print("ESITO: " + ("FALLITO" if errori else "OK" if validi else "NON VALIDO"), flush=True)
    sys.exit(1 if errori else 0)

if __name__ == "__main__":
    if "--tastiera" in sys.argv: asyncio.run(parte2())
    else: asyncio.run(parte1("--veloce" in sys.argv))
