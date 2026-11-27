# 27 nov 2026 (barca della giuria attraversata dai rivali, segnalazione di Lucio): righe CB per ogni rivale il cui scafo (prua, centro, poppa) entra nella barca della giuria (stessi punti CB_PTS di js/regate.js) fra -60 e +40 s; righe TOCCA (con la correzione, 1.3.76) per chi tocca la giuria entro 120 s: tocchi e secondi di fila a contatto. Copia di sperimentale/oss-147/misura_r16.py, a sua volta copia di sperimentale/caso-81/misura_bolina_coppie.py con in più una riga CONT per ogni contatto: regola della colpa, se il colpevole è un rivale, se in quel momento la sua guida sapeva di cedere all'altra (cedeA), lato, gradi dal vento, metri dalla boa, gradi girati negli ultimi 5 s.
# Copia di tests/misura_manovre.py (27 nov 2026, voce 2, caso 81, PROPOSTA-AVVERSARI-DERIVA.md §13.7-13.8; righe FERMO per l'oss. 150: rivali sotto 0,5 m/s per almeno 5 s mentre cedono): stampa anche le coppie dopo il via (righe EP) e, per ogni rivale, il tempo di bolina (secondi dallo sparo alla prima boa) e [secondi in cessione, virate] in bolina (righe BOL).
# Misura della voce 4 (1.3.11, docs/PROPOSTA-REGOLE-15-16.md, versione B, criteri M1-M5 scritti prima).
# Le 4 regate del torneo col pilota (come collaudo_rotta_assoluta.py: semi dispari principianti, pari esperti), con la versione B spenta (__sv.manovre(false),
# cioè la 1.3.10) e accesa con RINVIO_MAX 4, 8 o 12 s; stessi semi per tutte. Registro dei contatti del gioco (R.contLog, solo #collaudo).
#   M1 contatti dopo il via in cui un rivale della coppia aveva cominciato una virata nei 5 s prima
#   M2 contatti fra -5 s e il via in cui un rivale della coppia aveva deciso di partire nei 5 s prima
#   M3 contatti in tutto; M4 arrivo mediano dei rivali (s dallo sparo); M5 rivali piantati (sotto 0,2 m/s per 15 s di fila dopo il via), fuori linea, non arrivati
#   coppie_dopo_via (23 nov): episodi S8 che arrivano a 10 s dopo il via (il K1 di PROPOSTA-COPPIE.md); «coppie» conta anche prima del via
#   coppie (16 nov): la scena S8 di tests/scene_strane.py, un rivale che cede a X da almeno 10 s con X entro 12,6 m e le prue a meno di 20°: coppie diverse per regata
#   configurazioni: off (versione B spenta), 4 / 8 / 12 (RINVIO_MAX), nocono (versione B spenta e cono d'ombra spento, solo per contare le coppie)
# Uso: python tests/misura_manovre.py --semi 2201-2230 --conf off,4,8,12 [--lungo]   (BROWSER=firefox); stampa una riga JSON per configurazione
import asyncio, json, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]  # sperimentale/giuria/ -> radice del repo
GIOCO = pathlib.Path(os.environ["RADICE"]).resolve() if os.environ.get("RADICE") else ROOT  # 23 nov: RADICE=cartella per una copia del gioco
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
a, b_ = arg("--semi", "2201-2230").split("-"); SEMI = range(int(a), int(b_) + 1)
CONF = arg("--conf", "off,4,8,12").split(",")
LUNGO = "--lungo" in sys.argv  # 23 nov: regate lunghe come nel torneo vero (__sv.lungo, 3 regate da circa 10 minuti invece di 4 corte)
NK = 3 if LUNGO else 4
src = (ROOT / "tests" / "collaudo_rotta_assoluta.py").read_text().split("async def main")[0]
A = {"__file__": str(ROOT / "tests" / "collaudo_rotta_assoluta.py")}; exec(src, A)
# la corsa di collaudo_rotta_assoluta.py, con in più il conto dei piantati (campione ogni secondo)
CORSA = A["CORSA"].replace("while (R.t < 1500 && R.phase !== 'done'){ if (R.boats[0].fin === null) sv.pilota(dt); sv.run(dt, 1); }",
  "const bolT = R.boats.map(() => null), lenti = R.boats.map(() => 0), piant = new Set(), cop = new Set(); let acc = 0; window.__cop = cop; window.__copDopo = 0;\n  while (R.t < 1500 && R.phase !== 'done'){ if (R.boats[0].fin === null) sv.pilota(dt); sv.run(dt, 1); acc += dt; const cl = R.contLog || []; for (let q = window.__cl0 || 0; q < cl.length; q++){ const e = cl[q], G = R.boats[e.g], O = R.boats[e.g === e.i ? e.j : e.i], h0 = G.storiaH && G.storiaH.length ? G.storiaH[0][1] : G.S.h; e.riv = !G.me; e.ced = G.cedeA === O; e.leg = G.leg; e.twa = Math.round(norm180(windAt(G.S.x, G.S.y).twd - G.S.h)); e.otwa = Math.round(norm180(windAt(O.S.x, O.S.y).twd - O.S.h)); e.gir = Math.round(norm180(G.S.h - h0)); e.gn = G.name; e.on = O.name; } window.__cl0 = cl.length; if (R.t < 40 && R.cb){ const P = [[0, -4], [1.6, -1.5], [1.5, 4], [-1.5, 4], [-1.6, -1.5]], hh = windAt(R.cb.x, R.cb.y).twd * Math.PI / 180, cc = Math.cos(hh), ss = Math.sin(hh), W = P.map(([x, y]) => [R.cb.x + x * cc - y * ss, R.cb.y + x * ss + y * cc]); const dentro = (px, py) => { let c = false; for (let a = 0, z = W.length - 1; a < W.length; z = a++){ const [xa, ya] = W[a], [xz, yz] = W[z]; if ((ya > py) !== (yz > py) && px < (xz - xa) * (py - ya) / (yz - ya) + xa) c = !c; } return c; }; const cbx = window.__cbx || (window.__cbx = new Map()); R.boats.forEach((b, i) => { if (!i) return; const fx = Math.sin(b.S.h * Math.PI / 180), fy = -Math.cos(b.S.h * Math.PI / 180); if ([-2.1, 0, 2.1].some(k => dentro(b.S.x + fx * k, b.S.y + fy * k))){ const e = cbx.get(i) || { t0: R.t, t1: R.t, u: b.S.u, leg: b.leg, nome: b.name }; e.t1 = R.t; cbx.set(i, e); } }); }  if (R.t < 120){ const tu = window.__tu || (window.__tu = new Map()); R.boats.forEach((b, i) => { const e = tu.get(i) || { n: 0, run: 0, max: 0, prima: false, nome: b.name }; if (b.urtoCb){ if (!e.prima) e.n++; e.run += dt; e.max = Math.max(e.max, e.run); } else e.run = 0; e.prima = !!b.urtoCb; tu.set(i, e); }); }\n"
  "    const cz = window.__cz || (window.__cz = R.boats.map(() => ({ cede: 0, vir: 0, v0: false, dev: 0, rin: 0 }))); const fz = window.__fz || (window.__fz = R.boats.map(() => ({ s: 0, t0: 0, o: '', md: false, tw: 0 }))), fe = window.__fe || (window.__fe = []); if (R.t > 0) R.boats.forEach((b, i) => { if (!i || b.fin !== null || b.dnf) return; const f = fz[i]; if (b.cedeA && b.S.u < 0.5){ if (!f.s){ f.t0 = R.t; f.o = b.cedeA.name; f.md = tackOf(b) !== tackOf(b.cedeA); f.tw = Math.round(norm180(windAt(b.S.x, b.S.y).twd - b.S.h)); } f.s += dt; } else { if (f.s >= 5) fe.push({ t: Math.round(f.t0), dur: +f.s.toFixed(1), b: b.name, o: f.o, mureDiverse: f.md, twa: f.tw, leg: b.leg }); f.s = 0; } }); if (R.t > 0) R.boats.forEach((b, i) => { if (!i || b.leg !== 1 || b.fin !== null) return; const c = cz[i]; if (b.cedeA) c.cede += dt; if (b.virando && !c.v0) c.vir++; c.v0 = !!b.virando; c.rin = b.rinvio || 0; }); if (R.t > 0) R.boats.forEach((b, i) => { if (i && bolT[i] === null && b.leg >= 2) bolT[i] = R.t; }); window.__bolT = bolT; window.__czOut = cz; if (acc >= 1){ acc = 0; if (R.t > 0) R.boats.forEach((b, i) => { if (i && b.fin === null && !b.dnf){ lenti[i] = b.S.u < 0.2 ? lenti[i] + 1 : 0; if (lenti[i] >= 15) piant.add(i); } }); } }\n"
  "  window.__piant = piant.size;").replace("if (acc >= 1){ acc = 0;",
  "if (acc >= 1){ acc = 0; R.boats.forEach((b, i) => { if (!i) return; const o = b.cedeA, k = o ? i + '-' + R.boats.indexOf(o) : null;"
  " const ok = o && Math.hypot(o.S.x - b.S.x, o.S.y - b.S.y) < 12.6 && Math.abs(norm180(o.S.h - b.S.h)) < 20; b.__cp = ok && b.__ck === k ? (b.__cp || 0) + 1 : ok ? 1 : 0; b.__ck = k; if (b.__cp >= 10) cop.add(k); if (b.__cp === 10 && R.t >= 0){ window.__copDopo++; (window.__ep = window.__ep || []).push({ t: Math.round(R.t), b: b.name, o: o.name, leg: b.leg, oleg: o.leg, d: +Math.hypot(o.S.x - b.S.x, o.S.y - b.S.y).toFixed(1), twa: Math.round(norm180(windAt(b.S.x, b.S.y).twd - b.S.h)), otwa: Math.round(norm180(windAt(b.S.x, b.S.y).twd - o.S.h)), u: +b.S.u.toFixed(1), ou: +o.S.u.toFixed(1) }); } });").replace("return { fin: R.boats[0].fin };",
  "return { log: R.contLog || [], fin: R.boats.slice(1).map(b => b.fin), fuori: R.boats.slice(1).filter(b => b.fuori).length, piant: window.__piant, coppie: window.__cop.size, copDopo: window.__copDopo, tu: window.__tu ? [...window.__tu.values()].filter(e => e.n).map(e => ({ n: e.n, max: +e.max.toFixed(1), nome: e.nome })) : [], cbx: window.__cbx ? [...window.__cbx.values()].map(e => ({ t0: +e.t0.toFixed(1), dur: +(e.t1 - e.t0).toFixed(1), u: +e.u.toFixed(1), leg: e.leg, nome: e.nome })) : [], fermi: window.__fe || [], bol: (window.__bolT || []).slice(1), cz: (window.__czOut || []).slice(1).map(c => [+c.cede.toFixed(1), c.vir]), ep: window.__ep || [], lib: R.nLibera || 0, ins: R.nInsegue || 0 };")
assert "__piant" in CORSA and "contLog" in CORSA and "__cop" in CORSA and "cop.add" in CORSA

# 23 nov (voci 4B e 3 insieme, docs/PROPOSTA-COPPIE.md §15): configurazioni come elenco di pezzi uniti da «+»: off; m4 / m8 / m12 (versione B intera, RINVIO_MAX);
# v4 / v8 (solo la parte delle virate, senza l'attesa alla partenza); c10 / c15 / c20 (voce 3, T_LIBERO); nocono. v* e c* solo con la patch
# sperimentale/coppie-4b-3/voce3_e_4b.patch applicata (git apply), altrimenti lo strumento si ferma con un errore. Un numero solo («4») vale m4, come prima.
# Pagina nuova per ogni regata (prima una pagina per configurazione: lo stato della pagina cambiava le regate, memoria «evaluate separati»).
def imposta(conf):
    m, part, c, cono = None, True, None, True
    for x in conf.split("+"):
        if x == "off": pass
        elif x == "nocono": cono = False
        elif x.isdigit(): m = int(x)
        elif x[0] == "m": m = int(x[1:])
        elif x[0] == "v": m, part = int(x[1:]), False
        elif x[0] == "c": c = int(x[1:])
        else: raise SystemExit("configurazione sconosciuta: " + x)
    serve = c is not None or not part  # c* e v* esistono solo con sperimentale/coppie-4b-3/voce3_e_4b.patch applicata
    return ("if (!__sv.coppie) throw new Error('serve la patch sperimentale/coppie-4b-3'); " if serve else "") + f"__sv.ombra({str(cono).lower()}); __sv.manovre({'true' if m else 'false'}, {m or 8}, {str(part).lower()}); if (__sv.coppie) __sv.coppie({'true' if c else 'false'}, {c or 15});"

async def main():
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); errs = []
        for conf in CONF:
            js = imposta(conf)
            m1 = m2 = m3 = fuori = piant = nonarr = coppie = lib = ins = copd = 0; arrivi = []
            for s in SEMI:
                for k in range(NK):
                    pg = await br.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errs.append(str(e)))
                    await pg.goto((GIOCO / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
                    await pg.evaluate("v => { __sv.lungo = v; }", LUNGO); await pg.evaluate("() => { " + js + " }")
                    r = await pg.evaluate(CORSA, [k, s, 0]); await pg.close()
                    for c in r["log"]:
                        m3 += 1; riv = [x for x, idx in ((0, c["i"]), (1, c["j"])) if idx != 0]
                        if c["t"] >= 0 and any(c["vir"][x] <= 5 for x in riv): m1 += 1
                        if -5 <= c["t"] < 0 and any(c["go"][x] <= 5 for x in riv): m2 += 1
                    arrivi += [f for f in r["fin"] if f is not None]; nonarr += sum(f is None for f in r["fin"]); fuori += r["fuori"]; piant += r["piant"]; coppie += r["coppie"]
                    lib += r.get("lib", 0); copd += r["copDopo"]; ins += r.get("ins", 0)
                    for c in r["log"]: print("CONT", s, k, json.dumps({x: c.get(x) for x in ("t", "r", "r0", "riv", "ced", "leg", "twa", "otwa", "gir", "dm", "gn", "on")}), flush=True)
                    for e in r["tu"]: print("TOCCA", s, k, json.dumps(e), flush=True)
                    for e in r["cbx"]: print("CB", s, k, json.dumps(e), flush=True)
                    for e in r["fermi"]: print("FERMO", s, k, json.dumps(e), flush=True)
                    print("BOL", s, k, json.dumps(r["bol"]), json.dumps(r["cz"]), flush=True)
                    for e in r["ep"]: print("EP", s, k, json.dumps(e), flush=True)
            out = {"conf": conf, "semi": f"{SEMI[0]}-{SEMI[-1]}", "regate": NK * len(SEMI), "lungo": LUNGO, "M1": m1, "M2": m2, "M3": m3, "M4": round(statistics.median(arrivi), 1) if arrivi else None,
                   "piantati": piant, "coppie": coppie, "coppie_dopo_via": copd, "fuori": fuori, "non_arrivati": nonarr, "liberate": lib, "insegue": ins, "errori": len(errs)}
            print(json.dumps(out), flush=True)
        await br.close()
asyncio.run(main())
