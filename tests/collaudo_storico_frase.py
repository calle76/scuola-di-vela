# La frase del Coach dallo storico dei rivali (1.3.38, voce 74 passo 2 a, docs/PROPOSTA-STORICO-RIVALI.md «Passo 2, fermata 1»). Soglie scritte nella proposta prima del codice.
#   R7  la frase dice il vero: compare se e solo se un rivale in acqua ha, nello storico RICALCOLATO QUI (dal registro tor.ris per i casi naturali, dai numeri messi a mano per quelli
#       costruiti), almeno 2 regate con contatto per colpa sua; nome, barca e numero giusti (il più alto; a parità il primo nell'ordine delle barche). 0 sbagliate,
#       almeno 100 casi con la frase e almeno 100 senza; stampa quanti naturali e quanti costruiti
#   R7b una sola per regata, fra -151 e -149 s con la preparazione da 3 minuti; al primo istante (-60 s) con quella da 1 minuto. Dichiarato prima di misurare: un ritardo dovuto a un commento
#       forzato appena passato (penalità prima del via) si conta a parte e non è un errore
#   R7c col Coach spento 0 frasi su 20 regate (con lo storico che la farebbe comparire)
#   R3  la regata non cambia: 20 regate a semi fissi, guidate dal pilota, identiche al bit con lo storico che dà la frase e con lo storico vuoto (solo Chromium: in Firefox la stessa versione
#       contro se stessa non è identica al bit, vedi collaudo_storico_rivali R3; lì solo riportato)
#   R5  la frase col nome più lungo dei rivali sta nel riquadro del Coach, dentro il mare a 1360x650
#   R6  come un giocatore: pagina senza #collaudo, storico con 2 regate «colpa sua»: la frase compare, 0 errori
# 22 nov, dopo il primo giro in Chromium (soglie invariate): le regate costruite si fermano a -100 s invece di -140 (la frase ritardata da un commento forzato usciva dopo), R6 aspetta il conto alla rovescia.
# Uso: python tests/collaudo_storico_frase.py   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib, random, re
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
COLORI = ["rossa", "verde", "blu", "viola", "grigia"]
bad = []; n_casi = 0
def chk(ok, m):
    global n_casi; n_casi += 1
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
def attesa(nomi, cs):
    """la frase attesa, calcolo nostro: cs = regate «colpa sua» per nome"""
    m, v = -1, 0
    for n, nome in enumerate(nomi):
        c = cs.get(nome, 0)
        if c >= 2 and c > v: m, v = n, c
    return None if m < 0 else f"{nomi[m]}, barca {COLORI[m]}: in {v} regate ti ha toccato con colpa sua. Tieni d'occhio la sua barca."
# una regata del torneo: clic su «Corri», (facoltativo) storico messo a mano subito dopo, poi pilota fino all'arrivo oppure fino a fin_t e ritiro; legge le frasi dello storico nel registro del Coach
CORRI = """async ([sto, fin_t, coach]) => { const sv = __sv, dt = 1 / 60; sv.opt.coachReg = coach; document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], T = sv.tor, nomi = T.av.map(a => a.nome);
  if (sto) nomi.forEach((n, k) => { progress.rivali = progress.rivali || {}; progress.rivali[n] = { ...(progress.rivali[n] || {}), st: { n: 9, dav: 0, die: 0, pDav: 0, pDie: 0, fuori: 0, cont: 9, cS: sto[k], cT: 0 } }; });
  const t0 = R.t;
  if (fin_t !== null){ while (R.t < fin_t){ sv.pilota(dt); sv.run(dt, 1); } window.confirm = () => true; document.getElementById("rRet").click(); sv.run(dt, 1); }
  else while (me.fin === null && !me.dnf && R.t < 1500){ sv.pilota(dt); sv.run(dt, 1); }
  const L = (R.cr ? R.cr.log : []).filter(c => /ti ha toccato con colpa sua/.test(c.testo)), t1 = L.length ? L[0].t : 0, forz = (R.cr ? R.cr.log : []).filter(c => c.t < t1 && c.t > t1 - 31 && !/ti ha toccato/.test(c.testo)).length;
  const firma = R.boats.map(b => [b.fin, b.pp || 0, !!b.dnf, !!b.dsq, b.me ? R.need || 0 : 0, Math.round(b.S.x * 100), Math.round(b.S.y * 100)].join(',')).join('|');
  document.getElementById("rTor").click(); return { nomi, frasi: L.map(c => c.testo), tempi: L.map(c => c.t), t0, forz, firma, ris: JSON.parse(JSON.stringify(sv.tor ? sv.tor.ris : [])) }; }"""
async def pagina(b, url=BASE + "#collaudo", seme=True):
    ctx = await b.new_context(viewport={"width": 1360, "height": 650})
    if seme: await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(url); await pg.wait_for_timeout(300); return ctx, pg, errs
async def apri(pg, seme, cd=180):
    await pg.evaluate("([s, cd]) => { __sv.fast(0); __seed(s); __sv.opt.countdown = cd; __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); }", [seme, cd])
def cs_registro(ris_lista, nomi_lista):
    """regate con contatto colpa sua per nome, dal registro (calcolo nostro)"""
    out = {}
    for ris, nomi in zip(ris_lista, nomi_lista):
        for r in ris:
            for i, nome in enumerate(nomi, 1):
                out[nome] = out.get(nome, 0) + ("s" in (r[i].get("c") or ""))
    return out
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        con = senza = sbagliate = 0; nat = {"con": 0, "senza": 0}; cos = {"con": 0, "senza": 0}; fuori_t = []; ritardi = 0; parita = 0; errori = []; dett = []
        def conta(r, att, tipo, cd):
            nonlocal con, senza, sbagliate, ritardi
            got = r["frasi"]
            ok = (att is None and not got) or (att is not None and got == [att])
            if not ok: sbagliate += 1; dett.append((tipo, att, got))
            if att is None: senza += 1; (nat if tipo == "nat" else cos)["senza"] += 1
            else: con += 1; (nat if tipo == "nat" else cos)["con"] += 1
            for t in r["tempi"]:
                lo, hi = (-151, -149) if cd == 180 else (-61, -59)
                if not lo <= t <= hi:
                    if r["forz"]: ritardi += 1
                    else: fuori_t.append((tipo, t, cd))
        # ---- R7 naturali: tornei interi col pilota, due per pagina (lo storico si somma) ----
        for sess in range(5):
            ctx, pg, errs = await pagina(b); ris_l, nomi_l = [], []
            for sd in (sess * 2 + 301, sess * 2 + 302):
                await apri(pg, sd); fin = None
                for k in range(4):
                    r = await pg.evaluate(CORRI, [None, None, True])
                    att = attesa(r["nomi"], cs_registro(ris_l + [r["ris"][:k]], nomi_l + [r["nomi"]]))
                    conta(r, att, "nat", 180); fin = r
                ris_l.append(fin["ris"]); nomi_l.append(fin["nomi"])
            if errs: errori.append(("nat", sess, errs[0]))
            await ctx.close()
        # ---- R7 costruiti: storico messo a mano (metà senza frase, metà con, parità comprese); regata fino a -140 s (o -50 con 1 minuto) e ritiro ----
        rnd = random.Random(74)
        for sess in range(12):   # 22 nov, dopo il secondo giro: con 8 sessioni 80 casi con la frase e 88 senza, sotto i 100 della soglia (invariata): più casi
            ctx, pg, errs = await pagina(b)
            for tn in range(4):
                cd = 60 if (sess in (7, 11) and tn >= 2) else 180
                await apri(pg, 500 + sess * 10 + tn, cd)
                for k in range(4):
                    if rnd.random() < 0.5: sto = [rnd.choice([0, 1]) for _ in range(3)]
                    else:
                        sto = [rnd.choice([0, 1, 2, 3, 4, 5]) for _ in range(3)]
                        if rnd.random() < 0.3: v = rnd.choice([2, 3, 4]); i, j = rnd.sample(range(3), 2); sto[i] = sto[j] = v
                    r = await pg.evaluate(CORRI, [sto, -100 if cd == 180 else -20, True])   # 22 nov, dopo il primo giro: a -140 la frase ritardata da un contatto con colpa a -162 non era ancora uscita (4 casi)
                    att = attesa(r["nomi"], dict(zip(r["nomi"], sto)))
                    vals = [x for x in sto if x >= 2]
                    if vals and vals.count(max(vals)) > 1: parita += 1
                    conta(r, att, "cos", cd)
            if errs: errori.append(("cos", sess, errs[0]))
            await ctx.close()
        chk(sbagliate == 0 and con >= 100 and senza >= 100 and not errori, f"R7 frasi sbagliate {sbagliate} su {con + senza} regate: con la frase {con} (naturali {nat['con']}, costruite {cos['con']}), senza {senza} (naturali {nat['senza']}, costruite {cos['senza']}); parità {parita}; errori {errori[:1]}; esempi {dett[:2]}")
        chk(not fuori_t and con > 0, f"R7b frasi fuori tempo {len(fuori_t)} su {con} {fuori_t[:3]}; ritardate da un commento forzato (contate a parte) {ritardi}")
        # ---- R7c: Coach spento ----
        ctx, pg, errs = await pagina(b); n_off = f_off = 0
        for tn in range(5):
            await apri(pg, 700 + tn)
            for k in range(4):
                r = await pg.evaluate(CORRI, [[3, 0, 2], -100, False]); n_off += 1; f_off += len(r["frasi"])
        chk(n_off == 20 and f_off == 0 and not errs, f"R7c Coach spento: {f_off} frasi su {n_off} regate (storico che la darebbe), errori {errs[:1]}")
        await ctx.close()
        # ---- R3: regate identiche con e senza frase ----
        uguali = tot = 0; con_frase = 0
        for seme in range(801, 806):
            f = []
            for sto in ([3, 0, 2], [0, 0, 0]):
                ctx, pg, errs = await pagina(b); await apri(pg, seme); fr = []
                for k in range(4):
                    r = await pg.evaluate(CORRI, [sto, None, True]); fr.append(r["firma"]); con_frase += bool(r["frasi"]) and sto[0] == 3
                f.append(fr); await ctx.close()
            for x, y in zip(*f): tot += 1; uguali += x == y
        if BR == "chromium": chk(tot == 20 and uguali == 20 and con_frase == 20, f"R3 {uguali} regate su {tot} identiche al bit con e senza frase (la frase è comparsa in {con_frase} su 20)")
        else: print(f"RIPORTATO R3 ({BR}): {uguali} regate su {tot} identiche con e senza frase (frase in {con_frase} su 20); il controllo vale in Chromium", flush=True)
        # ---- R5: il nome più lungo nel riquadro del Coach ----
        ctx, pg, errs = await pagina(b); await apri(pg, 9)
        r5 = await pg.evaluate("""() => { const sv = __sv; sv.opt.coachReg = true; document.getElementById("torGo").click(); const R = sv.R, T = sv.tor;
          const lungo = [...RIVALI_ZONALE, ...RIVALI_NAZIONALE].map(x => x[0]).sort((a, b) => b.length - a.length)[0], vecchio = T.av[1].nome;
          T.av[1].nome = lungo; progress.rivali[lungo] = { st: { n: 99, dav: 0, die: 0, pDav: 0, pDie: 0, fuori: 0, cont: 99, cS: 99, cT: 0 } };
          for (const a of T.av) if (a.nome !== lungo && progress.rivali[a.nome]) progress.rivali[a.nome].st && (progress.rivali[a.nome].st.cS = 0);
          while (R.t < -140) sv.run(1 / 60, 1); sv.draw(0.016);
          const q = R.crRect, testo = R.cr && R.cr.cur ? R.cr.cur.testo : null, ecc = Math.max(document.documentElement.scrollWidth - innerWidth, document.documentElement.scrollHeight - innerHeight, 0); T.av[1].nome = vecchio;
          return { lungo, testo, q, w: W, h: H, ecc }; }""")
        q = r5["q"]
        dentro = bool(q) and q[0] >= 0 and q[1] >= 0 and q[0] + q[2] <= r5["w"] and q[1] + q[3] <= r5["h"] and r5["ecc"] == 0
        chk(dentro and r5["testo"] and r5["lungo"] in r5["testo"] and not errs, f"R5 nome più lungo «{r5['lungo']}»: riquadro {q} dentro il mare {r5['w']}x{r5['h']}: {dentro}; errori {errs[:1]}")
        await ctx.close()
        # ---- R6: come un giocatore ----
        ctx, pg, errs = await pagina(b, url=BASE, seme=False)
        await pg.evaluate("() => { const d = document.querySelector('#livSel [data-v=deriva]'); d && d.click(); }"); await pg.click("#goTor"); await pg.wait_for_timeout(200)
        nome = await pg.evaluate("() => { const T = torBozza; progress.rivali = progress.rivali || {}; progress.rivali[T.av[2].nome] = { st: { n: 4, dav: 1, die: 3, pDav: 1, pDie: 3, fuori: 0, cont: 2, cS: 2, cT: 0 } }; return T.av[2].nome; }")
        await pg.click("#torGo"); await pg.wait_for_timeout(300)
        if await pg.is_visible("#bGo"): await pg.click("#bGo")
        for _ in range(90):   # 22 nov, dopo il primo giro: 35 s fissi non bastavano (la regata era a -159 s); ora si aspetta il conto alla rovescia, al più 90 s
            if await pg.evaluate("() => typeof R !== 'undefined' && !!R && R.t >= -140"): break
            await pg.wait_for_timeout(1000)
        r6 = await pg.evaluate("() => ({ log: R.cr ? R.cr.log.map(c => c.testo) : [], t: R.t })")
        att = f"{nome}, barca blu: in 2 regate ti ha toccato con colpa sua. Tieni d'occhio la sua barca."
        chk(att in r6["log"] and not errs, f"R6 pagina da giocatore (t = {r6['t']:.0f} s): frase {'presente' if att in r6['log'] else 'ASSENTE'}; registro del Coach {r6['log']}; errori {errs[:1]}")
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    raise SystemExit(1 if bad or n_casi == 0 else 0)
asyncio.run(main())
