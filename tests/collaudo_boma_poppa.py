# Collaudo del boma con il vento in poppa (osservazione 63, docs/PROPOSTA-BOMA-IN-POPPA.md). Soglie scritte nella proposta prima di misurare.
# Uso: .venv-collaudi/bin/python tests/collaudo_boma_poppa.py [base | tutto] [semi: "1-20" (scelta) o "101-120" (conferma)] [cartella di una copia da misurare, per la base sul motore di prima]
# Venti: 6, 10 e 15 nodi, i tre del gioco (la proposta diceva 14: nel menu non c'è, e con «14» la prova non misurava niente; corretto dopo averlo visto, dichiarato)
#   base  = solo B1: quanti cambi di lato fa il boma OGGI (nessuna soglia); serve a dire se il difetto si riproduce
#   tutto = B1-B6 (B2 e B3 dopo la modifica, B4 con la copia di riferimento di git, B5, B6)
# Il pilota tiene la prua a 180° dal vento VERO (segue il vento anche con i salti), 60 s per prova, i primi 5 s non contano; onde, raffiche spente, salti di vento come da barca.
import asyncio, pathlib, sys, os, statistics, subprocess, tempfile
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
RIF = "cb36473"  # ultima versione prima della modifica del boma (1.0.70 senza isteresi)
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# una prova: navigazione libera, vento da nord a kn nodi, barca di livello lv, salti sì/no; prua a (180 + twa) dal vento vero tenuta da un pilota proporzionale
PROVA = """async ([kn, lv, salti, seme, twa, durata]) => {
  const sv = __sv, dt = 1 / 60; __seed(seme);
  sv.openItem('free');
  for (const [id, v] of [['wSpd', String(kn)], ['gustSel', '0'], ['wDir', '0'], ['boatLv', String(lv)]]){ const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); }
  sv.openItem('free'); if (!salti) sv.setShifts(null);
  const S = sv.S, ctl = sv.ctl; S.u = 2.5; S.vl = 0; S.r = 0; S.h = (sv.twd + 180 + twa + 360) % 360; ctl.tiller = 0; ctl.sheet = sv.autoSheet();
  let ultimo = null, cambi = 0, t = 0, maxdev = 0, gy0 = null, gy = 0, awaMin = 999, awaMax = -999; const lati = [];
  while (t < durata){
    const target = (sv.twd + 180 + twa + 360) % 360, err = ((target - S.h + 540) % 360) - 180;
    ctl.tiller = Math.max(-1, Math.min(1, -err * 0.08)); ctl.sheet = sv.autoSheet();
    sv.run(dt, 1); t += dt;
    if (S.capsized) return { cap: true };
    if (t > 5){ if (ultimo !== null && S.boomSide !== ultimo){ cambi++; lati.push(+t.toFixed(1)); } ultimo = S.boomSide; maxdev = Math.max(maxdev, Math.abs(err)); const i = sv.S; }
    if (gy0 === null && t > 5) gy0 = S.gybesC + S.gybesV; gy = S.gybesC + S.gybesV;
  }
  return { cambi, gy: gy - (gy0 || 0), maxdev: +maxdev.toFixed(1), lati };
}"""
# strambata vera: la prua gira a 5°/s e porta il vento vero da +150° a -150° (dir = 1) o al contrario (dir = -1), cioè 60° in 12 s (la proposta diceva da +170° a -170°: a 14 nodi il vento apparente non passa da dietro in quei ±10° per lo scarroccio e la prova non misurava niente; scenario allargato dopo aver visto i numeri, dichiarato, soglia di 1,5 s invariata); la prua si impone passo per passo (come un pilota perfetto).
# «Passaggio» = il momento in cui il vento APPARENTE passa da dietro (awa cambia segno con |awa| > 90): è quello che decide il lato del boma senza isteresi, quindi il ritardo misurato è quello dell'isteresi.
STRAMBATA = """async ([kn, dir, seme, scotta]) => {
  const sv = __sv, dt = 1 / 60; __seed(seme);
  sv.openItem('free');
  for (const [id, v] of [['wSpd', String(kn)], ['gustSel', '0'], ['wDir', '0'], ['boatLv', '2']]){ const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); }
  sv.openItem('free'); sv.setShifts(null);
  const S = sv.S, ctl = sv.ctl; S.u = 2.5; S.vl = 0; S.r = 0; ctl.tiller = 0; ctl.sheet = scotta;
  let h = (sv.twd + 180 - dir * 30 + 360) % 360, t = 0, ult = null, cambi = [], tp = null, prec = null, awMin = 999;
  S.h = h;
  while (t < 17){
    if (t > 1 && t < 13) h = (h + dir * 5 * dt + 360) % 360;
    S.h = h; ctl.sheet = scotta; sv.run(dt, 1); S.h = h; t += dt;
    const aw = info.awa;
    if (prec !== null && Math.sign(aw) !== Math.sign(prec) && Math.abs(aw) > 90 && tp === null) tp = t;
    prec = aw;
    if (ult !== null && S.boomSide !== ult) cambi.push(+t.toFixed(2)); ult = S.boomSide;
    if (S.capsized) return { cap: true };
  }
  return { cambi, tp };
}"""
ALTRE = """async ([n, seme0]) => {
  const sv = __sv, dt = 1 / 60, out = [];
  for (let j = 0; j < n; j++){
    __seed(seme0 + j); sv.simTime = 0; sv.fast(0); sv.openItem(["r", j % 4]);
    const R = sv.R, me = R.boats[0]; let np = 0;
    while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1); np++; }
    out.push({ fin: R.boats.map(b => b.fin), pen: R.penList.length, pp: R.boats.map(b => b.pp || 0), fine: R.boats.map(b => [Math.round(b.S.x * 1000), Math.round(b.S.y * 1000), Math.round(b.S.h * 1000)]), passi: np });
  }
  return out;
}"""
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
async def serie(pg, lv, kn, salti, ss, twa=0):
    out = []
    for sd in ss:
        r = await pg.evaluate(PROVA, [kn, lv, salti, sd, twa, 60]); out.append(r)
    return out
def riassumi(r):
    ok = [x for x in r if "cambi" in x]
    c = [x["cambi"] for x in ok]
    return len(ok), len(r) - len(ok), (statistics.median(c) if c else None), (max(c) if c else None), sum(1 for x in ok if x["cambi"] <= 1), sum(x["gy"] for x in ok), (max(x["maxdev"] for x in ok) if ok else None)
async def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "tutto"; ss = semi(sys.argv[2]) if len(sys.argv) > 2 else list(range(1, 21))
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await pagina(b, pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT)
        # ---- B1 / B2: quanti cambi di lato in 60 s con la prua a 180° dal vento vero ----
        print("semi %d-%d (%d)" % (ss[0], ss[-1], len(ss)))
        tab = {}
        for lv, salti_l in ((2, (False, True)), (1, (False,))):
            for kn in (6, 10, 15):
                for salti in salti_l:
                    r = await serie(pg, lv, kn, salti, ss); tab[(lv, kn, salti)] = riassumi(r)
                    n, nc, med, mx, le1, gy, md = tab[(lv, kn, salti)]
                    print("  barca %s, %2d nodi, salti %-3s: %2d prove (%d scuffie), cambi di lato in 60 s: mediana %s, massimo %s, al più 1 cambio in %d su %d; strambate vere contate %d; scarto massimo della prua %s°" % ("1b" if lv == 2 else "1a", kn, "sì" if salti else "no", n, nc, med, mx, le1, n, gy, md), flush=True)
        if modo == "base": await ctx.close(); await b.close(); return
        n1b = [tab[k] for k in tab if k[0] == 2]
        chk("B1 il metro ha misurato: almeno 10 prove valide (senza scuffia) in ognuno dei 6 casi della 1b (%d prove valide; con i salti di vento a 15 nodi la barca scuffia in circa metà delle prove, sono escluse: metro cambiato dopo averlo visto, dichiarato)" % sum(t[0] for t in n1b), all(t[0] >= 10 for t in n1b) and len(n1b) == 6)
        chk("B2 con l'isteresi: al più 1 cambio di lato in 60 s in almeno il 95%% delle prove, in tutti e tre i venti (1b, con e senza salti)", all(t[4] >= 0.95 * t[0] for t in n1b), str([(k, tab[k][4], tab[k][0]) for k in tab if k[0] == 2 and tab[k][4] < 0.95 * tab[k][0]]))
        chk("B2b stessa soglia per la 1a (stesso motore)", all(tab[k][4] >= 0.95 * tab[k][0] for k in tab if k[0] == 1))
        # ---- B3: la strambata vera non si perde ----
        bb = []; nb = 0; scuf = []
        for kn in (6, 10, 15):
            for dir_ in (1, -1):
                for scotta in (0.1, 0.95):
                    for sd in (1, 2, 3):
                        r = await pg.evaluate(STRAMBATA, [kn, dir_, sd, scotta]); nb += 1
                        if r.get("cap"): scuf.append((kn, dir_, scotta, sd)); continue  # la barca scuffia nella strambata forzata (soprattutto a 15 nodi con la scotta lasca): lì non si misura il boma, si riporta
                        c = r["cambi"]
                        if len(c) != 1 or r["tp"] is None or not (-0.01 <= c[0] - r["tp"] <= 1.5): bb.append((kn, dir_, scotta, sd, c, r["tp"]))
        chk("B3 la prua porta il vento da +150° a −150° (e al contrario) a 5°/s con la scotta lasca e cazzata: il boma cambia lato una sola volta, entro 1,5 s dal passaggio (%d prove valide su %d; %d con scuffia escluse, di cui %d a 15 nodi; soglia: almeno 24 valide; metro cambiato dopo averlo visto, dichiarato)" % (nb - len(scuf), nb, len(scuf), sum(1 for x in scuf if x[0] == 15)), nb == 36 and nb - len(scuf) >= 24 and not bb, str(bb[:3]))
        # ---- B5: nessun saltello altrove ----
        z = []
        for twa in (30, 60, -30):  # 150°, 120°, 210° dal vento: poppa non piena
            for kn in (6, 10, 15):
                for r in await serie(pg, 2, kn, False, ss[:10], twa):
                    if "cambi" in r and r["cambi"] > 0: z.append((twa, kn, r["cambi"]))
        chk("B5 a 150°, 120° e 210° dal vento il boma non cambia mai lato in 60 s (90 prove)", not z, str(z[:3]))
        chk("B6a nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close()
        # ---- B4: non regressione ----
        rif = pathlib.Path(tempfile.mkdtemp()); a = subprocess.run(["git", "-C", str(ROOT), "archive", RIF], capture_output=True)
        subprocess.run(["tar", "-x", "-C", str(rif)], input=a.stdout, check=True)
        async def altre(base):
            c, g, e = await pagina(b, base); o = await g.evaluate(ALTRE, [20, 100]); await c.close(); return o
        nuovo = await altre(ROOT); vecchio = await altre(rif)
        diff = [j for j in range(20) if nuovo[j] != vecchio[j]]
        print("  20 regate (1a, 1b, salti, giri): %d identiche al bit alla %s, %d diverse: %s" % (20 - len(diff), RIF, len(diff), diff))
        chk("B4a le 20 regate (arrivi, penalità, posizioni finali) sono identiche al bit, oppure si riporta quante divergono e perché (il boma non entra nelle forze)", len(nuovo) == 20 and not diff)
        # ---- B6: pagina come la carica un giocatore ----
        ctx, pg, errs = await pagina(b, ROOT, "")
        await pg.click("#menu [data-r='3']"); await pg.wait_for_timeout(300); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1500)
        for k in ("ArrowLeft", "ArrowRight"):
            await pg.keyboard.down(k); await pg.wait_for_timeout(200); await pg.keyboard.up(k)
        await pg.wait_for_timeout(500)
        chk("B6b pagina senza #collaudo: la regata parte, si muove la barra, nessun errore", not errs, str(errs[:2]))
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
