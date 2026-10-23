# Virate degli avversari nella «Regata nei salti di vento» (livello 2), docs/archivio/PROPOSTA-VIRATE-AVVERSARI.md, criterio V5 (1.0.31).
# Pagina con #collaudo, passi di 1/60 s, Math.random a seme fisso, giocatore guidato da __sv.pilota. Per ogni avversario, dopo il via
# sul lato di bolina (leg 1) e ad almeno 25 m dalla boa, una virata è il passaggio della prua da una mura all'altra (twa rispetto al vento locale di quel momento,
# letto da step()); la si segue fino a 12 s o alla virata seguente e se ne prende la prua massima dal vento. Conta come «oltre»
# se supera la bolina di quell'avversario (ai.up) di più di 15°. Scartata se intanto si arriva a 15 m dalla boa (giro di boa).
# Misura in più (aggiunta dopo aver visto i semi 1-2, dichiarato): la prua quando la rotazione si ferma per la prima volta
# (|r| sotto 2°/s, o verso invertito, con la prua già oltre 20° dal vento): separa la prua che va oltre da una manovra voluta dopo.
# Uso con un'altra cartella del gioco (per esempio il motore di prima): GIOCO=/percorso/index.html Semi 1-20 da guardare, 21-60 di conferma, principianti ed esperti.
# Uso: collaudo_virate2.py [primo ultimo]   Esce con 1 se nella conferma più del 5% delle virate va oltre, o se non ne misura nessuna.
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
import os
BASE = pathlib.Path(os.environ.get("GIOCO", ROOT / "index.html")).as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
REGATA = """([liv, seme]) => { const sv = __sv; sv.fast(0); sv.openItem(['r', 2]); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById('aiLevel'); sel.value = liv; sel.dispatchEvent(new Event('change'));
  const R = sv.R, ai = R.boats.filter(b => b.ai), st = new Map(), out = []; let scartate = 0;
  const chiudi = (b, s) => { out.push([s.pk, b.ai.up, s.ferma ?? s.pk]); st.delete(b); };
  while (R.t < 900 && !R.boats.every(b => b.fin !== null)){ sv.pilota(1 / 60); sv.run(1 / 60, 1);
    for (const b of ai){ if (!b.info || R.t < 0 || b.fin !== null || b.S.capsized) continue;
      const a = b.info.twa, s = st.get(b), dm = Math.hypot(b.S.x - R.mark.x, b.S.y - R.mark.y);
      if (s && (b.leg !== 1 || dm < 15)){ st.delete(b); scartate++; }
      else if (s){ if (Math.sign(a) !== s.lato && Math.abs(a) < 90) chiudi(b, s); else { s.pk = Math.max(s.pk, Math.abs(a)); if (s.ferma === undefined && Math.abs(a) > 20 && (Math.abs(b.S.r) < 2 || Math.sign(b.S.r) !== s.verso)) s.ferma = Math.abs(a); if (R.t - s.t0 > 12) chiudi(b, s); } }
      if (b.lato !== undefined && Math.sign(a) !== b.lato && Math.abs(a) < 30 && !st.has(b) && b.leg === 1 && dm >= 25) st.set(b, { lato: Math.sign(a), t0: R.t, pk: Math.abs(a), verso: Math.sign(b.S.r) });
      b.lato = Math.sign(a); } }
  for (const [b, s] of st) out.push([s.pk, b.ai.up, s.ferma ?? s.pk]);
  return { v: out, t: R.t, fin: R.boats.map(b => b.fin), scartate }; }"""

async def main():
    a = sys.argv[1:]; primo, ultimo = (int(a[0]), int(a[1])) if len(a) == 2 else (1, 60)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650})
        await pg.add_init_script(SEME)
        errori = []; pg.on("pageerror", lambda e: errori.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
        gruppi = {"guardati (semi 1-20)": [], "conferma (semi 21-60)": []}; arrivi = n = 0
        for seme in range(primo, ultimo + 1):
            for liv in ("principianti", "esperti"):
                r = await pg.evaluate(REGATA, [liv, seme]); n += 1; arrivi += all(f is not None for f in r["fin"])
                gruppi["guardati (semi 1-20)" if seme <= 20 else "conferma (semi 21-60)"] += r["v"]
                oltre = [round(pk) for pk, up, _ in r["v"] if pk > up + 15]
                print(f"  seme {seme} {liv}: {len(r['v'])} virate ({r['scartate']} scartate al giro di boa), oltre la bolina + 15°: {len(oltre)} {oltre}, durata {r['t']:.0f} s", flush=True)
        esito = True
        for nome, v in gruppi.items():
            if not v: continue
            oltre = sum(pk > up + 15 for pk, up, _ in v); pks = sorted(pk - up for pk, up, _ in v)
            fe = sorted(f - up for _, up, f in v); fo = sum(f > up + 15 for _, up, f in v)
            print(f"{nome}: {len(v)} virate misurate, oltre la bolina + 15°: {oltre} ({100 * oltre / len(v):.1f}%), "
                  f"prua massima meno bolina: mediana {pks[len(pks) // 2]:.1f}°, 95° percentile {pks[int(len(pks) * 0.95)]:.1f}°, massimo {pks[-1]:.1f}°")
            print(f"   prua quando la rotazione si ferma, meno bolina: oltre + 15° {fo} ({100 * fo / len(v):.1f}%), mediana {fe[len(fe) // 2]:.1f}°, "
                  f"95° percentile {fe[int(len(fe) * 0.95)]:.1f}°, massimo {fe[-1]:.1f}°")
            if nome.startswith("conferma"): esito = oltre <= 0.05 * len(v)
        misurate = sum(len(v) for v in gruppi.values())
        print(f"regate con tutte le barche arrivate: {arrivi} su {n}; errori della pagina: {errori[:2]}")
        ok = esito and misurate > 0 and not errori
        print("ESITO: " + ("OK" if ok else "FALLITO")); await b.close(); sys.exit(0 if ok else 1)

asyncio.run(main())
