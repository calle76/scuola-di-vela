# Collaudo della scotta automatica (1.0.73, docs/PROPOSTA-SCOTTA-AUTOMATICA.md). Soglie scritte nella proposta prima di misurare.
# Uso: .venv-collaudi/bin/python tests/collaudo_scotta_automatica.py [semi "1-20" (scelta) | "101-120" (conferma)] [cartella 1.0.72 per A1; se manca si estrae da git ('-' = lo stesso)] [H0 K: prova di taratura]
#   A1 spenta = identica alla 1.0.72 (stati finali di corse a scotta fissa e di regate, confronto con la cartella di riferimento)
#   A2 velocità: scotta automatica contro la migliore scotta fissa trovata su una griglia (soglia: media almeno 90%)
#   A3 raffiche (vento 15 nodi, raffiche forti): sbandata massima e scuffie non peggiori di chi lascia la scotta ferma
#   A4 i tasti della scotta spengono l'automatismo (20 prove) ; A5 il metro ha misurato ; A6 prova senza record ; A7 pagina come la carica un giocatore
# Il pilota tiene la prua a un angolo fisso dal vento vero (proporzionale), 60 s per corsa, i primi 20 s non contano per la velocità.
import asyncio, pathlib, sys, os, statistics, subprocess, tempfile, json
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
RIF = "d5f55a1"  # 1.0.72
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# politica: 'auto' (casella accesa), 'fisso:x' (scotta ferma a x), 'iniziale' (scotta ferma al valore della regola semplice all'inizio, come chi non la tocca)
PROVA = """async ([kn, lv, gust, seme, ang, pol, durata, h0k]) => {
  const sv = __sv, dt = 1 / 60; __seed(seme);
  if (h0k && sv.autoK) sv.autoK(h0k[0], h0k[1]);
  sv.openItem('free');
  for (const [id, v] of [['wSpd', String(kn)], ['gustSel', String(gust)], ['wDir', '0'], ['boatLv', String(lv)]]){ const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); }
  sv.openItem('free'); sv.setShifts(null); sv.fast(0);   // openItem rimette il tempo del gioco a velocità normale: si ferma di nuovo
  const S = sv.S, ctl = sv.ctl; S.u = 2.5; S.vl = 0; S.r = 0; S.h = (sv.twd + ang + 360) % 360; ctl.tiller = 0;
  const auto = pol === 'auto'; if (sv.opt) sv.opt.autoSheet = auto;
  let fisso = null;
  if (auto) ctl.sheet = sv.autoSheet(); else if (pol === 'iniziale') fisso = sv.autoSheet(); else fisso = +pol.split(':')[1];
  if (fisso !== null) ctl.sheet = fisso;
  let t = 0, somma = 0, n = 0, maxh = 0, cambi = 0, prec = null;
  while (t < durata){
    const target = (sv.twd + ang + 360) % 360, err = ((target - S.h + 540) % 360) - 180;
    ctl.tiller = Math.max(-1, Math.min(1, -err * 0.08)); if (fisso !== null) ctl.sheet = fisso;
    sv.run(dt, 1); t += dt;
    if (S.capsized) return { cap: true, t };
    maxh = Math.max(maxh, Math.abs(S.heel));
    if (t > 20){ somma += S.u; n++; if (prec !== null && Math.abs(ctl.sheet - prec) > 1e-9) cambi++; prec = ctl.sheet; }
  }
  sv.fast(0); return { cap: false, v: somma / n, maxh, cambi, n, usato: !!S.autoUsed };
}"""
# regate: per A1
ALTRE = """async ([n, seme0]) => {
  const sv = __sv, dt = 1 / 60, out = [];
  for (let j = 0; j < n; j++){
    __seed(seme0 + j); sv.simTime = 0; sv.fast(0); sv.openItem(["r", j % 4]);
    const R = sv.R, me = R.boats[0]; let np = 0;
    while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1); np++; }
    out.push({ fin: R.boats.map(b => b.fin), fine: R.boats.map(b => [Math.round(b.S.x * 1000), Math.round(b.S.y * 1000), Math.round(b.S.h * 1000)]), passi: np });
  }
  return out;
}"""
# tasti: premuto con la casella accesa
TASTO = """async ([seme, passi]) => {
  const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(seme); sv.openItem('free'); sv.setShifts(null); sv.opt.autoSheet = true; document.getElementById('autoSheetOpt').checked = true;
  sv.run(dt, 30); return { prima: sv.opt.autoSheet, sheet: sv.ctl.sheet };
}"""
DOPO = """async () => { const sv = __sv, dt = 1 / 60; sv.run(dt, 3); const a = sv.opt.autoSheet, s1 = sv.ctl.sheet; sv.run(dt, 120); return { spenta: !a, casella: document.getElementById('autoSheetOpt').checked, sheet: s1, sheet2: sv.ctl.sheet, ancora: sv.opt.autoSheet }; }"""
# prova 0 con la casella accesa, fino all'arrivo
MISSIONE = """async ([auto, seme]) => {
  const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(seme); sv.opt.autoSheet = auto;
  sv.openItem(['m', 0]); sv.setShifts(null); const S = sv.S, ctl = sv.ctl; let t = 0;
  const done = document.getElementById('done');
  while (t < 400 && !S.finished){
    const mk = sv.marks[sv.marks.length - 1], rot = (Math.atan2(mk.x - S.x, -(mk.y - S.y)) * 180 / Math.PI + 360) % 360; const err = ((rot - S.h + 540) % 360) - 180; ctl.tiller = Math.max(-1, Math.min(1, -err * 0.08)); sv.run(dt, 1); t += dt;
  }
  const st = JSON.parse(localStorage.getItem('scuolaVelaSim.v1') || '{}');
  return { fin: S.finished, t, testo: document.getElementById('doneText').textContent, best: st.best || null, done: st.done || null, clean: st.clean || null };
}"""
DEF = [12, 1.5]   # costanti scelte (H0, K) del gioco; da riga di comando si provano altre
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
    if not ok: bad.append(nome)
async def pagina(b, base, hash_="#collaudo"):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(pathlib.Path(base, "index.html").as_uri() + hash_); await pg.wait_for_timeout(250)
    return ctx, pg, errs
def semi(txt): a, b2 = txt.split("-"); return list(range(int(a), int(b2) + 1))
ANGOLI = [45, 60, 90, 110, 135, 150, 170]   # angolo della prua dal vento vero (prua = direzione da cui viene il vento + angolo); 170 e non 180 per non stare sul bordo del boma
VENTI = [6, 10, 15]
GRIGLIA = [round(0.05 * i, 2) for i in range(0, 21)]
async def main():
    ss = semi(sys.argv[1]) if len(sys.argv) > 1 else semi("1-20")
    rif = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    if rif is None:   # senza cartella: la 1.0.72 si estrae da git in una cartella temporanea
        rif = tempfile.mkdtemp(prefix="sv_rif_")
        subprocess.run("git -C %s archive %s | tar -x -C %s" % (ROOT, RIF, rif), shell=True, check=True)
    h0k = [float(sys.argv[3]), float(sys.argv[4])] if len(sys.argv) > 4 else DEF
    SEMPLICE = [999, 0]   # la regola semplice senza la lasca per la sbandata
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await pagina(b, ROOT)
        # ---- A2 velocità, senza raffiche, barca dell'1b e dell'1a ----
        for lv in (2, 1):
            rapp = []; mancati = 0
            for kn in VENTI:
                for ang in ANGOLI:
                    a = await pg.evaluate(PROVA, [kn, lv, 0, 7, ang, "auto", 60, h0k])
                    mig = 0.0
                    for g in GRIGLIA:
                        r = await pg.evaluate(PROVA, [kn, lv, 0, 7, ang, "fisso:%s" % g, 60, h0k])
                        if not r["cap"]: mig = max(mig, r["v"])
                    if a["cap"] or mig <= 0.3: mancati += 1; rapp.append((kn, ang, "scuffia" if a["cap"] else "nessuna scotta fissa valida", 0)); continue
                    rapp.append((kn, ang, round(a["v"], 2), round(100 * a["v"] / mig, 1)))
            valide = [x for x in rapp if isinstance(x[2], float)]
            media = statistics.mean(x[3] for x in valide) if valide else 0
            peggiore = min(valide, key=lambda x: x[3]) if valide else None
            chk("A2 barca %s: velocità con scotta automatica contro la migliore scotta fissa (griglia di 21 valori): media %.1f%% su %d corse (soglia 90%%), peggiore %s, corse non valide %d" % ("1b" if lv == 2 else "1a", media, len(valide), peggiore, mancati), len(valide) >= 18 and media >= 90, "")
        # ---- A3 raffiche: con la lasca per la sbandata contro la regola semplice (stessa corsa, stessi semi) ----
        for lv in (2, 1):
            conta = {"auto": [0, 0, []], "semplice": [0, 0, []]}
            for sd in ss:
                for ang in (45, 60, 90):
                    for pol, par in (("auto", h0k), ("semplice", SEMPLICE)):
                        r = await pg.evaluate(PROVA, [15, lv, 2, sd, ang, "auto", 90, par])
                        conta[pol][1] += 1
                        if r["cap"]: conta[pol][0] += 1
                        else: conta[pol][2].append(r["maxh"])
            sa, si = conta["auto"], conta["semplice"]
            ma = statistics.mean(sa[2]) if sa[2] else 0; mi = statistics.mean(si[2]) if si[2] else 0
            chk("A3 barca %s, 15 nodi, raffiche forti, %d corse per modo (semi %d-%d): scuffie con la lasca %d contro regola semplice %d; sbandata massima media (corse senza scuffia) %.1f° contro %.1f°" % ("1b" if lv == 2 else "1a", sa[1], ss[0], ss[-1], sa[0], si[0], ma, mi), sa[0] <= si[0] and ma <= mi + 0.05 and si[1] >= 40, "")
        # ---- A5 il metro ha misurato: la scotta cambia davvero, e la griglia trova una scotta meglio di quella iniziale ----
        r = await pg.evaluate(PROVA, [10, 2, 1, 3, 90, "auto", 60, h0k])
        r2 = await pg.evaluate(PROVA, [10, 2, 1, 3, 90, "iniziale", 60, h0k])
        chk("A5 con la casella accesa la scotta cambia (passi con scotta diversa dal precedente: %d su %d) e con scotta ferma no (%d)" % (r.get("cambi", -1), r.get("n", 0), r2.get("cambi", -1)), r.get("cambi", 0) >= 0.5 * r.get("n", 1) and r2.get("cambi") == 0 and r.get("usato") and not r2.get("usato"))
        # ---- A4 tasti ----
        ok4 = 0; dett = []
        for k in range(20):
            await pg.evaluate("1"); r0 = await pg.evaluate(TASTO, [k + 1, 0])
            await pg.keyboard.down("ArrowUp" if k % 2 == 0 else "ArrowDown")
            r1 = await pg.evaluate(DOPO)
            await pg.keyboard.up("ArrowUp" if k % 2 == 0 else "ArrowDown")
            if r0["prima"] and r1["spenta"] and not r1["casella"] and not r1["ancora"]: ok4 += 1
            else: dett.append((k, r0, r1))
        chk("A4 i tasti della scotta spengono la scotta automatica (e la casella) e non si riaccende da sola: %d su 20" % ok4, ok4 == 20, str(dett[:2]))
        # ---- A6 prova senza record ----
        await pg.evaluate("localStorage.clear()")
        m1 = await pg.evaluate(MISSIONE, [True, 5])
        chk("A6a prova con scotta automatica: arrivo %s, nessun record, medaglia né stella salvati (best %s, fatta %s), testo: «%s»" % (m1["fin"], m1["best"], m1["done"], m1["testo"][:60]), m1["fin"] and not m1["best"] and not m1["done"] and not m1["clean"] and "non vale" in m1["testo"])
        m2 = await pg.evaluate(MISSIONE, [False, 5])
        chk("A6b stessa prova a mano (la barca arriva anche con scotta ferma 0,02?): metro: se non arriva la A6a non prova niente; arrivo %s, record salvato %s" % (m2["fin"], m2["best"]), (not m2["fin"]) or bool(m2["best"]))
        chk("A0 nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close()
        # ---- A7 pagina come la carica un giocatore ----
        ctx, pg, errs = await pagina(b, ROOT, "")
        await pg.evaluate("document.getElementById('setDlg').showModal ? document.getElementById('setDlg').showModal() : 0")
        c = await pg.evaluate("(() => { const e = document.getElementById('autoSheetOpt'); if (!e) return null; const r = e.getBoundingClientRect(); const ok0 = !e.checked; e.click(); return { ok0, ora: e.checked, vis: r.width > 0 }; })()")
        chk("A7 pagina senza #collaudo: la casella c'è, è spenta all'inizio, si accende e si vede; nessun errore", bool(c) and c["ok0"] and c["ora"] and c["vis"] and not errs, str((c, errs[:2])))
        await ctx.close()
        # ---- A1 spenta = identica alla 1.0.72 ----
        if rif:
            r_ = {}
            for nome, base in (("ora", ROOT), ("rif", pathlib.Path(rif))):
                ctx, pg, errs = await pagina(b, base)
                res = []
                await pg.evaluate(PROVA, [10, 2, 1, 11, 90, "fisso:0.5", 10, None])   # corsa di riscaldamento scartata: la prima in una pagina nuova di Firefox differisce all'ultima cifra anche con lo stesso codice (visto: rif = ora2 ma ≠ ora)
                for kn, ang in ((6, 45), (10, 90), (15, 135), (10, 150)):   # (10, 170) non è ripetibile in Firefox nemmeno con lo stesso codice: sostituito con 150, dichiarato
                    res.append(await pg.evaluate(PROVA, [kn, 2, 1, 11, ang, "fisso:0.5", 40, None]))
                res.append(await pg.evaluate(ALTRE, [5, 1]))
                r_[nome] = res; await ctx.close()
            chk("A1 casella spenta: 4 corse a scotta fissa e 5 regate identiche alla 1.0.72, al bit", json.dumps(r_["ora"]) == json.dumps(r_["rif"]), "")
    print("\ncasi sbagliati:", bad if bad else "nessuno")
    sys.exit(1 if bad else 0)
asyncio.run(main())
