# Semaforo di precedenza sullo scafo (1.0.40, docs/PROPOSTA-REGOLE-PRECEDENZA-1B.md).
# Parte 1, coerenza: regate dei salti di vento (1b) col pilota, semi 1-8, principianti ed esperti, passi di 1/60 s, semaforo attivo. Per ogni contatto
#   del giocatore il colore che il semaforo aveva un passo prima deve essere quello della penalità assegnata: rosso se la penalità è andata al
#   giocatore, verde se è andata all'altra. 0 contraddizioni (non contano i contatti in cui al passo prima la geometria dietro/affiancate era a meno
#   di 5 cm dal confine: nel passo la regola può cambiare; si riportano a parte, soglia aggiunta il 23 ottobre dopo aver visto un caso a 1,2 cm); il controllo deve aver visto contatti e semafori (n > 0), e si riporta quanti contatti
#   del giocatore erano senza semaforo visibile.
# Parte 2, impostazione: con il semaforo spento l'immagine del mare non cambia quando c'è un colore (rosso o verde) e cambia quando è acceso.
#   Spento di default; l'1a (regata 0) non lo ha mai (R.sem sempre nullo).
# Uso: python collaudo_semaforo.py
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""

# conta gli alone del semaforo disegnati (tratto largo e trasparente nei due colori): in ogni immagine con il semaforo ce ne deve essere uno solo, quello del giocatore
# (nella 1.0.40 il colore finiva anche sugli avversari, perché passano dalla stessa funzione di disegno)
HALO = """(() => { const st = CanvasRenderingContext2D.prototype.stroke; window.__halo = 0;
  CanvasRenderingContext2D.prototype.stroke = function(...a){ if (Math.abs(this.globalAlpha - 0.3) < 1e-3 && (Math.abs(this.lineWidth - 0.5) < 1e-3 || Math.abs(this.lineWidth - 0.36) < 1e-3) && (this.strokeStyle === "#e0553a" || this.strokeStyle === "#3fbf6b")) window.__halo++; return st.apply(this, a); }; })();"""

CORSA = """([race, seme, liv, acceso]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", race]); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const cb = document.getElementById("showSem"); cb.checked = acceso; cb.dispatchEvent(new Event("change"));
  const R = sv.R, me = R.boats[0], dt = 1 / 60, c = document.getElementById("c");
  const out = { contatti: 0, visibili: 0, sbagliati: 0, alConfine: 0, senza: 0, rossi: 0, verdi: 0, secondi: 0, nonNullo: 0, img: null }, visti = new Set();
  let prevSem = null, prevNome = null, prevPen = 0, pos = null;
  const margine = (i, j) => { const A = pos[i], B = pos[j], m = [];   // distanza (m) dal confine «dietro / affiancate» al passo prima: quanto manca perché la regola cambi
    for (const [X, Y] of [[A, B], [B, A]]){ const h = Y.h * Math.PI / 180, fx = Math.sin(h), fy = -Math.cos(h), pr = p => p[0] * fx + p[1] * fy;
      m.push(Math.abs(Math.max(...sv.hullWorld(X).map(pr)) - Math.min(...sv.hullWorld(Y).map(pr)))); } return +Math.min(...m).toFixed(3); };
  const foto = () => { sv.draw(0); return c.toDataURL().length + ":" + c.toDataURL().slice(-300); };
  const passo = () => {
    for (const key of Object.keys(R.contacts)){ const id = key + ":" + R.contacts[key]; if (visti.has(id)) continue; visti.add(id);
      const [i, j] = key.split("-").map(Number); if (i !== 0 && j !== 0) continue;
      out.contatti++; const colpa = (me.pen || 0) + (me.pp || 0) > prevPen;   // la penalità è andata al giocatore?
      if (prevSem === null){ out.senza++; continue; }
      out.visibili++; if ((prevSem === "rosso") !== colpa){ const mg = margine(i, j); if (mg > 0.05) out.sbagliati++; else out.alConfine++; (out.dett = out.dett || []).push({ t: +R.t.toFixed(1), key, prevSem, colpa, vicina: prevNome, altra: R.boats[i === 0 ? j : i].name, lastRule: R.lastRule, margineDalConfine: mg }); } }
    if (R.sem){ out.nonNullo++; if (R.sem === "rosso") out.rossi++; else out.verdi++; }
    prevSem = R.sem; prevNome = R.semNome || null; prevPen = (me.pen || 0) + (me.pp || 0);
  };
  let n = 0;
  while (me.fin === null && !me.dnf && R.t < 900){ pos = R.boats.map(b => ({ x: b.S.x, y: b.S.y, h: b.S.h })); sv.pilota(dt); sv.run(dt, 1); passo(); n++;
    if (acceso && !out.img && R.sem){   // immagine con il colore, poi con l'impostazione spenta (stesso istante) e con il colore tolto
      window.__halo = 0; const con = foto(); const alone = window.__halo; cb.checked = false; cb.dispatchEvent(new Event("change")); const spento = foto();
      const col = R.sem; R.sem = null; const senza = foto(); R.sem = col; cb.checked = true; cb.dispatchEvent(new Event("change"));
      out.img = { colore: col, diverse: con !== spento, spentoUguale: spento === senza, alone, barcheVicine: R.boats.filter(b => b !== me && Math.hypot(b.S.x - me.S.x, b.S.y - me.S.y) < 12).length }; } }
  out.secondi = +(n / 60).toFixed(0); out.lv2 = R.lv2; return out; }"""

async def main():
    fail = []; casi = 0
    def chk(ok, msg):
        nonlocal casi
        casi += 1
        if not ok: fail.append(msg); print("FALLITO:", msg)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650}); await pg.add_init_script(SEME); await pg.add_init_script(HALO)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_function("window.__sv")
        print("== parte 1: coerenza fra semaforo e penalità (1b)")
        tot = dict(contatti=0, visibili=0, sbagliati=0, alConfine=0, senza=0, rossi=0, verdi=0, nonNullo=0); immagini = []
        for seme in range(1, 9):
            for liv in ("principianti", "esperti"):
                r = await pg.evaluate(CORSA, [2, seme, liv, True])
                for k in tot: tot[k] += r[k]
                if r["img"]: immagini.append(r["img"])
                if r.get("dett"): print("  contraddizione", seme, liv, r["dett"])
        print(f"  16 regate: contatti del giocatore {tot['contatti']}, con semaforo visibile {tot['visibili']}, senza {tot['senza']}, contraddizioni {tot['sbagliati']} (più {tot['alConfine']} con la regola al confine dietro/affiancate a meno di 5 cm al passo prima); passi con semaforo: rosso {tot['rossi']}, verde {tot['verdi']}")
        chk(tot["contatti"] > 0 and tot["visibili"] > 0, "il controllo non ha misurato niente (nessun contatto o nessun semaforo visibile)")
        chk(tot["rossi"] > 0 and tot["verdi"] > 0, "il semaforo non è mai stato visto di tutti e due i colori")
        chk(tot["sbagliati"] == 0, f"{tot['sbagliati']} contatti con il colore diverso dalla penalità")
        print("== parte 2: impostazione")
        print("  immagini controllate:", len(immagini), immagini[:2])
        chk(len(immagini) > 0, "nessuna immagine controllata")
        chk(all(i["alone"] == 1 for i in immagini), f"alone del semaforo disegnato {sorted(set(i['alone'] for i in immagini))} volte per immagine (atteso 1: solo il giocatore)")
        chk(all(i["barcheVicine"] >= 1 for i in immagini), "il controllo non ha avuto avversari vicini")
        chk(all(i["diverse"] for i in immagini), "con il semaforo acceso l'immagine è uguale a quella senza colore")
        chk(all(i["spentoUguale"] for i in immagini), "con il semaforo spento l'immagine cambia per il colore")
        r = await pg.evaluate("() => document.getElementById('showSem').checked"); chk(r is False or r is True, "impostazione mancante")
        await pg.reload(); await pg.wait_for_function("window.__sv")
        spento = await pg.evaluate("() => document.getElementById('showSem').checked"); chk(spento is False, "il semaforo non è spento all'avvio")
        r1a = await pg.evaluate(CORSA, [0, 1, "principianti", True]); chk(r1a["nonNullo"] == 0 and not r1a["lv2"], f"1a: semaforo mai visto: {r1a['nonNullo']} passi")
        chk(not errs, f"errori della pagina: {errs[:3]}")
        await b.close()
    print(f"controlli: {casi}, falliti: {len(fail)}")
    print("ESITO:", "OK" if casi and not fail else "FALLITO"); sys.exit(1 if fail or not casi else 0)
asyncio.run(main())
