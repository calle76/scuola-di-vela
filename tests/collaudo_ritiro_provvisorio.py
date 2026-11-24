# Il ritiro provvisorio (1.3.53, voci 41 e 6, docs/PROPOSTA-RITIRO-PROVVISORIO.md): criteri e soglie della proposta, scritti prima del codice.
#  P1 simulazione interrotta apposta (un errore lanciato dentro il ciclo di torChiudi): alla riapertura il ritiro c'è, un solo risultato, niente provv; 4 momenti x 10 tornei = 40 su 40;
#     lo stesso nell'ultima regata (torneo chiuso, 10 su 10) e nell'ultima regata di una tappa di stagione (tappa chiusa, 10 su 10). Controllo del metro: la simulazione è stata davvero interrotta
#  P2 non interrotta: i risultati sono quelli di torChiudi chiamata senza il provvisorio (40 su 40 identici al bit), provv assente
#  P3 (solo con --chiusura) pagina lasciata davvero, regate lunghe: ritiro registrato 20 su 20 (4 momenti x 5 semi). --chiusura --base: solo riportato, per misurare il gioco di prima
#  P4 chi ha già finito e chiude con la simulazione interrotta: il suo risultato resta quello vero, 20 su 20
#  P5 un salvataggio senza provv si apre come prima (10 su 10); provv di una regata già registrata: scartato (10 su 10); il riquadro con la nota non esce a 1360x650; 0 errori
#  P6 (aggiunto col codice: la riga in beforeunload non era nella proposta) chiusura annullata: beforeunload parte, il provvisorio c'è, la regata continua e il risultato è identico a quello
#     senza beforeunload, provv cancellato, 10 su 10; in allenamento beforeunload non scrive niente, 10 su 10
# Uso: python tests/collaudo_ritiro_provvisorio.py   (BROWSER=firefox per Firefox; --chiusura: solo P3)
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(os.environ.get("GIOCO") or pathlib.Path(__file__).resolve().parents[1]) / "index.html").as_uri() + "#collaudo"   # GIOCO=cartella: il gioco di un'altra versione
BR = os.environ.get("BROWSER", "chromium"); CHIUSURA = "--chiusura" in sys.argv; SOLOBASE = "--base" in sys.argv
ATTESA = float(sys.argv[sys.argv.index("--attesa") + 1]) if "--attesa" in sys.argv else 0   # P3: secondi fra la chiusura e la riapertura (24 nov: misurate 0, 3 e 10)
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
MOMENTI = [1, 40, 150, 300]
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    print(("ok      " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)
async def pagina(b, ctx=None, lungo=False):
    ctx = ctx or await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); await pg.add_init_script(SEME)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(BASE); await pg.wait_for_timeout(150)
    await pg.evaluate("v => { __sv.fast(0); __sv.lungo = v; __sv.store = 'scuolaVelaSim.v1'; }", lungo)
    return ctx, pg, errs
# preparazione, corsa e uscita in un solo evaluate. fatte: regate già corse finte; stag: tappa di stagione; come: "rotto" (errore a metà ciclo), "intero", "senza" (torChiudi col ritiro, senza torEsci), "resta"
CORRI = """([seme, sec, fatte, stag, come, finisci]) => { const sv = __sv, dt = 1 / 60; __seed(seme); let S = null;
  if (stag){ S = progress.stagione = stNuova(); }
  const T = tor = progress.torneo = torNuovo(S), n = T.av.length + 1;
  for (let k = 0; k < fatte; k++) T.ris.push(Array.from({ length: n }, (_, i) => ({ fin: 200 + (i * 7 + k * 3) % n, pp: 0 })));
  saveProgress(); __seed(seme * 7 + 1); openItem(["r", "t"]); const R = sv.R, me = R.boats[0];
  if (finisci){ while (me.fin === null && !me.dnf && R.t < 1500){ sv.pilota(dt); sv.run(dt, 1); } if (me.fin === null) return { salta: true }; }
  else for (let k = 0; k < sec * 60; k++){ sv.pilota(dt); sv.run(dt, 1); }
  const prima = { fin: me.fin, t: R.t, resto: R.boats.filter(b => b.fin === null && !b.dnf).length, ris: T.ris.length, n };
  if (come === "resta") return { prima };
  let giri = 0, rotto = false; const vero = updateRace;
  if (come === "rotto") updateRace = d => { if (++giri > 30) throw new Error("INTERROTTA"); vero(d); };
  try { if (come === "senza"){ if (me.fin === null && !me.dnf) me.dnf = me.ret = true; torChiudi(); } else torEsci(); } catch(e){ rotto = e.message === "INTERROTTA"; if (!rotto) throw e; }
  updateRace = vero; const q = JSON.parse(localStorage.getItem(sv.store));
  return { prima, rotto, salvato: q, ris: JSON.stringify(T.ris), fine: JSON.stringify(T.fine || null), riv: JSON.stringify(q.rivali || null) }; }"""
APRI = """() => { torApri(); const d = document.getElementById("torDlg"), q = d.getBoundingClientRect(), T = tor, m = document.querySelector("#torBody .manca"); const r = { ris: T && T.ris, fine: T && T.fine || null, nota: m ? m.textContent : "",
  ecc: [d.scrollHeight - d.clientHeight, d.scrollWidth - d.clientWidth, Math.round(Math.max(0, q.bottom - innerHeight))], salvato: JSON.parse(localStorage.getItem("scuolaVelaSim.v1")) }; d.close(); torApri(); r.due = tor && tor.ris ? tor.ris.length : null; d.close(); return r; }"""
async def rotta(b, *a):
    ctx, pg, errs = await pagina(b); r = await pg.evaluate(CORRI, list(a))
    if r.get("salta"): await ctx.close(); return r, None, errs
    await pg.evaluate("() => { tor = null; R = null; }")   # la pagina muore così: alla sua chiusura (pagehide) non deve rifare il lavoro
    await pg.close(); _, p2, e2 = await pagina(b, ctx); z = await p2.evaluate(APRI); await ctx.close(); return r, z, errs + e2
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        if CHIUSURA:
            ok = 0; note = []
            for m in MOMENTI:
                for s in range(6301, 6306):
                    ctx, pg, errs = await pagina(b, None, True); await pg.evaluate(CORRI, [s, m, 0, False, "resta", False])
                    try: await pg.goto("about:blank")
                    except Exception:
                        try: await pg.evaluate("location.href='about:blank'"); await pg.wait_for_timeout(1500)
                        except Exception: pass
                    await pg.close(); await asyncio.sleep(ATTESA); _, p2, e2 = await pagina(b, ctx, True); z = await p2.evaluate(APRI); await ctx.close()
                    r = z["ris"] or []; bene = len(r) == 1 and r[0][0]["fin"] is None and any(x["fin"] is not None for x in r[0][1:])
                    ok += bene; note.append((m, s, bool(bene), bool(z["nota"])))
            print(f"P3 {BR}, regate lunghe, riapertura dopo {ATTESA:g} s, pagina lasciata: ritiro registrato {ok} su {len(note)}; di cui dal provvisorio {sum(x[3] for x in note)}; persi {[x[:2] for x in note if not x[2]]}", flush=True)
            await b.close(); sys.exit(0 if SOLOBASE or (ok == 20 and len(note) == 20) else 1)
        # ---- P1 ----
        ok = rotti = diff = 0; note = []; ecc = []
        for m in MOMENTI:
            for s in range(6001, 6011):
                r, z, e = await rotta(b, s, m, 0, False, "rotto", False); rotti += r["rotto"]
                q = (z["ris"] or [None])[0]; bene = z["ris"] and len(z["ris"]) == 1 and z["due"] == 1 and q[0]["fin"] is None and sum(x["fin"] is not None for x in q) >= 1 and "provv" not in z["salvato"]["torneo"] and z["nota"] and not e
                ok += bool(bene); ecc.append(max(z["ecc"]))
                if not bene: note.append((m, s, q, z["due"], e[:1]))
                st = (z["salvato"].get("rivali") or {}); diff += sum((v.get("st") or {}).get("n", 0) for v in st.values()) == r["prima"]["n"] - 1
        chk("P1", rotti == 40 and ok == 40, f"P1 interrotta davvero {rotti} su 40, ritiro alla riapertura una volta sola {ok} su 40; note {note[:2]}")
        chk("P1", diff == 40, f"P1 storico dei rivali aggiornato una volta per rivale: {diff} su 40")
        for stag in (False, True):
            ok = rotti = 0; note = []
            for s in range(6101, 6111):
                r, z, e = await rotta(b, s, 40, 3, stag, "rotto", False); rotti += r["rotto"]; q = z["salvato"]; S = q.get("stagione")
                bene = "torneo" not in q and q.get("torneoFatto") and (not stag or (S["tappe"][0].get("ord") and not S["tappe"][0].get("rit") and not S["tappe"][1].get("ord"))) and not e
                ok += bool(bene); note += [] if bene else [(s, q.get("torneoFatto"), S and S["tappe"][0], e[:1])]
            chk("P1", rotti == 10 and ok == 10, f"P1 ultima regata{' di una tappa' if stag else ''}: interrotta {rotti} su 10, chiuso alla riapertura {ok} su 10; note {note[:2]}")
        # ---- P2 ----
        ug = tot = att = 0; note = []
        for m in MOMENTI:
            for s in range(6001, 6011):
                c1, p1, e1 = await pagina(b); r1 = await p1.evaluate(CORRI, [s, m, 0, False, "intero", False]); await c1.close()
                c2, p2, e2 = await pagina(b); r2 = await p2.evaluate(CORRI, [s, m, 0, False, "senza", False]); await c2.close()
                tot += 1; u = r1["ris"] == r2["ris"] and r1["riv"] == r2["riv"] and not e1 and not e2; ug += u; att += "provv" not in r1["salvato"]["torneo"] and len(r1["salvato"]["torneo"]["ris"]) == 1
                if not u: note.append((m, s))
        chk("P2", tot == att == 40 and (ug == 40 or BR == "firefox"), f"P2 risultati identici {ug} su {tot}{' (in Firefox solo riportato)' if BR == 'firefox' else ''}, provv assente {att} su 40; diversi {note[:4]}")
        # ---- P4 ----
        ok = tot = salt = 0; note = []; s = 6400
        while tot < 20 and s < 6440:
            s += 1; r, z, e = await rotta(b, s, 0, 0, False, "rotto", True)
            if r.get("salta") or r["prima"]["resto"] == 0: salt += 1; continue   # tutte arrivate prima del giocatore: niente da interrompere
            tot += 1; q = z["ris"][0][0] if z["ris"] else None; arr = int(r["prima"]["fin"] * 10 + 0.5) / 10
            bene = r["rotto"] and q and abs(q["fin"] - arr) < 0.051 and len(z["ris"]) == 1 and not e; ok += bool(bene); note += [] if bene else [(s, q, arr, e[:1])]
        chk("P4", tot == 20 and ok == 20, f"P4 chi ha finito tiene il suo arrivo: {ok} su {tot} (saltati {salt}); note {note[:2]}")
        # ---- P5 ----
        ok = ok2 = 0
        for s in range(6501, 6511):
            for doppio in (False, True):
                ctx, pg, e1 = await pagina(b)
                pr = await pg.evaluate("""([s, d]) => { __seed(s); const T = progress.torneo = torNuovo(), n = T.av.length + 1, riga = Array.from({ length: n }, (_, i) => ({ fin: 200 + i, pp: 0 }));
                  T.ris.push(riga); if (d) T.provv = { k: 0, r: riga.map(x => ({ fin: null, pp: 0 })) }; saveProgress(); return JSON.stringify(T.ris); }""", [s, doppio])
                await pg.close(); _, p2, e2 = await pagina(b, ctx); z = await p2.evaluate(APRI)
                bene = json.loads(pr) == z["ris"] and z["nota"] == "" and not e1 and not e2 and "provv" not in z["salvato"]["torneo"]
                if doppio: ok2 += bene
                else: ok += bene
                await ctx.close()
        chk("P5", ok == 10 and ok2 == 10, f"P5 salvataggio vecchio aperto uguale {ok} su 10; provvisorio di una regata già registrata scartato {ok2} su 10")
        chk("P5", len(ecc) == 40 and max(ecc) <= 0, f"P5 riquadro con la nota a 1360x650: eccesso massimo {max(ecc)} px su {len(ecc)}")
        # ---- P6 ----
        ok = c = all_ = 0; note = []
        for s in range(6601, 6611):
            f = []
            for annulla in (False, True):
                ctx, pg, e = await pagina(b)
                f.append(await pg.evaluate('''([s, a]) => { const sv = __sv, dt = 1 / 60; __seed(s); tor = progress.torneo = torNuovo(); saveProgress(); __seed(s * 7 + 1); openItem(["r", "t"]); const me = sv.R.boats[0]; let c = null;
                  for (let k = 0; k < 2400; k++){ sv.pilota(dt); sv.run(dt, 1); } if (a){ dispatchEvent(new Event("beforeunload")); c = !!JSON.parse(localStorage.getItem(sv.store)).torneo.provv && !me.dnf; }
                  while (me.fin === null && !me.dnf && sv.R.t < 1500){ sv.pilota(dt); sv.run(dt, 1); } document.getElementById("rTor").click(); const T = JSON.parse(localStorage.getItem(sv.store)).torneo;
                  return { c, ris: JSON.stringify(T.ris), n: T.ris.length, provv: "provv" in T }; }''', [s, annulla])); await ctx.close()
            c += f[1]["c"]; u = (f[0]["ris"] == f[1]["ris"] or BR == "firefox") and f[1]["n"] == 1 and not f[1]["provv"]; ok += u; note += [] if u else [(s, f)]
            ctx, pg, e = await pagina(b); all_ += await pg.evaluate('''s => { __seed(s); progress.torneo = torNuovo(); saveProgress(); const z = localStorage.getItem(__sv.store); allen = allNuovo(); openItem(["r", "a"]); __sv.run(1 / 60, 60); dispatchEvent(new Event("beforeunload")); return __sv.R.all && z === localStorage.getItem(__sv.store); }''', s); await ctx.close()
        chk("P6", c == ok == 10, f"P6 chiusura annullata: provvisorio scritto {c} su 10, risultato vero e provv cancellato {ok} su 10; note {note[:1]}")
        chk("P6", all_ == 10, f"P6 in allenamento beforeunload non scrive: {all_} su 10")
        await b.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("P1", "P2", "P4", "P5", "P6")): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
