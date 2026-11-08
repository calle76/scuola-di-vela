# Perché gli avversari non fanno i giri di penalità (osservazione 99, docs/PROPOSTA-GIRI-AVVERSARI-GRUPPO.md). Non è un collaudo: misura e basta.
# Regata dei giri (indice 3), pilota per il giocatore. Per ogni avversario con un debito di giri e non ancora in giro, ogni secondo: che cosa lo blocca secondo la regola
# di oggi (giroAI in js/regate.js: prima del via o prima di passare la linea, ocs, una barca entro GIRO_AI_VIA = 4 lunghezze, entro 25 m da una boa o dall'arrivo)
# e quanto è vicina la barca più vicina. All'arrivo: con quanti giri ancora da fare.
# Uso: python tests/misura_giri_avversari_liberi.py PRIMO_SEME ULTIMO_SEME      (BROWSER=firefox per l'altro browser; RADICE=cartella per un altro codice)
import asyncio, collections, json, os, pathlib, statistics, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent)
SEME = (pathlib.Path(__file__).resolve().parent / "esplora.py").read_text().split('SEME = """')[1].split('"""')[0]
CORSA = """([seme, liv]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", 3]); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const R = sv.R, dt = 1 / 60, L = 4.2, av = R.boats.filter(b => !b.me), sec = [], debiti = [];
  let n = 0; const d0 = new Map(av.map(b => [b, 0]));
  while (R.t < 900 && av.some(b => b.fin === null && !b.dnf)){
    sv.pilota(dt); sv.run(dt, 1);
    for (const b of av){ const g = b.gDebt || 0; if (g > d0.get(b)) debiti.push({ nome: b.name, t: +R.t.toFixed(1), prima: R.t < 0 }); d0.set(b, g); }
    if (n++ % 60) continue;
    for (const b of av){
      if (!(b.gDebt > 0) || b.fin !== null || b.dnf || b.gCum != null) continue;
      let dMin = 1e9; for (const o of R.boats) if (o !== b && o.fin === null && !o.dnf && !o.S.capsized) dMin = Math.min(dMin, Math.hypot(o.S.x - b.S.x, o.S.y - b.S.y));
      let boa = false; for (const m of R.marks) if (Math.hypot(m.x - b.S.x, m.y - b.S.y) < 25) boa = true;
      if (b.leg === R.marks.length + 1 && Math.abs(toWF(b.S.x, b.S.y)[1]) < 25) boa = true;
      const motivo = R.t < 0 ? "prima del via" : b.leg < 1 ? "non ancora partita" : b.ocs ? "partenza da rifare" : dMin < 4 * L ? "barca entro 4 lunghezze" : boa ? "vicino a boa o arrivo" : "libera (sta per cominciare)";
      sec.push({ nome: b.name, t: +R.t.toFixed(0), motivo, d: +(dMin / L).toFixed(2), leg: b.leg });
    }
  }
  const arrivi = av.map(b => ({ nome: b.name, fin: b.fin, mancanti: (R.penList.find(p => p.startsWith("La " + b.name + ", giri di penalità non fatti")) || "").match(/\\((\\d+)\\)/)?.[1] | 0 }));
  return { sec, debiti, arrivi, tuContatti: R.penList.filter(p => p.startsWith("Tu, contatto")).length, contatti: Object.keys(R.contacts || {}).length,
           giriDove: R.penList.filter(p => / penalità scontata/.test(p) && !p.startsWith("Tu")).length, dsq: av.filter(b => b.dsq).length };
}"""
async def main():
    a, z = int(sys.argv[1]), int(sys.argv[2]); tutti = []
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for liv in ("principianti", "esperti"):
            for seme in range(a, z + 1):
                pg = await br.new_page(); await pg.add_init_script(SEME); await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(150)
                r = await pg.evaluate(CORSA, [seme, liv]); await pg.close(); r["liv"] = liv; r["seme"] = seme; tutti.append(r)
        await br.close()
    n = len(tutti); sec = [s for r in tutti for s in r["sec"]]; deb = [d for r in tutti for d in r["debiti"]]
    print(f"regate {n} ({a}-{z}, principianti ed esperti) | debiti presi dagli avversari {len(deb)}, di cui prima del via {sum(d['prima'] for d in deb)}")
    if not sec: print("ATTENZIONE: nessun secondo con un debito: la misura non vale"); return
    c = collections.Counter(s["motivo"] for s in sec)
    print(f"secondi di avversari con un debito e non in giro: {len(sec)}")
    for k, v in c.most_common(): print(f"  {k}: {v} ({100 * v / len(sec):.0f}%)")
    dopo = [s for s in sec if s["motivo"] in ("barca entro 4 lunghezze", "vicino a boa o arrivo", "libera (sta per cominciare)")]
    if dopo:
        print(f"dopo la partenza ({len(dopo)} s): barca più vicina, mediana {statistics.median(s['d'] for s in dopo):.1f} lunghezze; " + ", ".join(f"almeno {k} L: {100 * sum(s['d'] >= k for s in dopo) / len(dopo):.0f}%" for k in (1.5, 2, 3, 4)))
    print(f"colpe degli avversari (debiti) {len(deb)} | contatti con colpa del giocatore {sum(r['tuContatti'] for r in tutti)} | penalità scontate dagli avversari {sum(r['giriDove'] for r in tutti)} | avversari squalificati {sum(r['dsq'] for r in tutti)}")
    arr = [x for r in tutti for x in r["arrivi"] if x["fin"] is not None]; manc = [x for x in arr if x["mancanti"]]
    print(f"avversari arrivati {len(arr)}, con giri non fatti {len(manc)} ({100 * len(manc) / max(len(arr), 1):.0f}%), giri mancanti in tutto {sum(x['mancanti'] for x in manc)}")
    attese = []   # secondi dal debito al primo istante «libera» secondo soglie diverse, per avversario e debito (solo dopo la partenza)
    for r in tutti:
        for nome in {s["nome"] for s in r["sec"]}:
            ss = [s for s in r["sec"] if s["nome"] == nome and s["leg"] >= 1]
            if ss: attese.append(ss)
    att = sorted(sum(1 for s in ss if s["motivo"] != "prima del via") for ss in attese)   # secondi di attesa dopo il via, per avversario con un debito
    if att: print(f"attesa dopo il via prima di cominciare i giri (per avversario con debito): mediana {statistics.median(att):.0f} s, 75% sotto {att[int(0.75 * len(att))]} s, massimo {att[-1]} s")
    for k in (4, 3, 2, 1.5):
        trovate = sum(1 for ss in attese if any(s["d"] >= k for s in ss))
        print(f"  avversari con debito dopo la partenza che hanno avuto almeno un secondo con nessuno entro {k} L: {trovate} su {len(attese)}")
asyncio.run(main())
