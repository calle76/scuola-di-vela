# Regole di precedenza dell'1b (1.0.40, docs/PROPOSTA-REGOLE-PRECEDENZA-1B.md): chi deve cedere, per le regole 10, 11, 12 e 13 di F15.
# Casi scritti a mano dal testo del regolamento (non letti dal gioco): coppie di barche messe nella regata dei salti di vento (1b), senza salti di
# vento; per ognuna la barca che deve cedere e la regola. Più i confini: dietro/affiancate per pochi centimetri, virata finita da poco.
# L'1a (regata 0) deve dare le due regole di sempre (10; stesse mure col più sopravento): casi in fondo. Il metro non dipende dal gioco:
# la geometria (davanti, a sinistra) è calcolata qui con le formule dei casi. Il controllo deve aver visto casi di tutte le regole.
# Uso: python collaudo_regole.py
import asyncio, math, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()

# stato: A in (0,0); la prua di A è twd + 45 (mure a sinistra) o twd - 45 (mure a dritta); B a (avanti, lato) rispetto alla prua di A (lato > 0 = a destra di A)
# cd = "p"/"s": mure di A e di B (se diverse, B ha la prua opposta); virA, virB: barche in virata
CASO = """([race, twdRel, tackA, tackB, avanti, lato, virA, virB]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", race]); sv.setShifts && sv.setShifts(null);
  const R = sv.R, A = R.boats[1], B = R.boats[2], twd = sv.twd;
  const prua = t => t === "p" ? twd + 45 : twd - 45;          // p: vento da sinistra, mure a sinistra
  A.S.h = prua(tackA); B.S.h = prua(tackB); A.S.x = 0; A.S.y = 0;
  const h = A.S.h * Math.PI / 180, fx = Math.sin(h), fy = -Math.cos(h), rx = Math.cos(h), ry = Math.sin(h);
  B.S.x = avanti * fx + lato * rx; B.S.y = avanti * fy + lato * ry;
  A.virando = !!virA; B.virando = !!virB;
  const c = sv.chiCede(A, B); return { cede: c.cede === A ? "A" : "B", regola: c.regola }; }"""

# nome, mure A, mure B, avanti, lato, virA, virB, cede atteso, regola attesa
CASI = [
    # regola 10: mure opposte, cede quella a sinistra, comunque stiano le barche
    ("10 a sinistra A, B a dritta", "p", "s", 15, 8, 0, 0, "A", 10),
    ("10 a dritta A, B a sinistra", "s", "p", 15, -8, 0, 0, "B", 10),
    ("10 B davanti a sinistra, A a dritta", "s", "p", 12, 12, 0, 0, "B", 10),
    ("10 B dietro a dritta, A a sinistra", "p", "s", -12, 5, 0, 0, "A", 10),
    ("10 vicine (6 m)", "p", "s", 3, 5, 0, 0, "A", 10),
    ("10 lontane (30 m)", "s", "p", 25, 18, 0, 0, "B", 10),
    # regola 11: stesse mure, affiancate, cede la sopravento. Mure a sinistra: il vento arriva da sinistra, sopravento = lato sinistro
    ("11 mure a sinistra, B a sinistra di A (sopravento)", "p", "p", 0, -3, 0, 0, "B", 11),
    ("11 mure a sinistra, B a destra di A (sottovento)", "p", "p", 0, 3, 0, 0, "A", 11),
    ("11 mure a dritta, B a destra di A (sopravento)", "s", "s", 0, 3, 0, 0, "B", 11),
    ("11 mure a dritta, B a sinistra di A (sottovento)", "s", "s", 0, -3, 0, 0, "A", 11),
    ("11 confine: B avanti 4,0 m, affiancate di 0,2 m, B a sinistra", "p", "p", 4.0, -3, 0, 0, "B", 11),
    ("11 confine: B indietro 4,0 m, affiancate di 0,2 m, B a destra", "p", "p", -4.0, 3, 0, 0, "A", 11),
    # regola 12: stesse mure, non affiancate, cede quella dietro (anche se è la sottovento)
    ("12 B davanti in fila, mure a sinistra", "p", "p", 8, 0, 0, 0, "A", 12),
    ("12 B dietro in fila, mure a sinistra", "p", "p", -8, 0, 0, 0, "B", 12),
    ("12 B davanti e sopravento (il caso che prima era sbagliato)", "p", "p", 8, -2, 0, 0, "A", 12),
    ("12 B dietro e sopravento", "p", "p", -8, -2, 0, 0, "B", 12),
    ("12 confine: B davanti 4,4 m (dietro per 0,2 m)", "p", "p", 4.4, -3, 0, 0, "A", 12),
    ("12 mure a dritta, B davanti e sottovento", "s", "s", 7, -2, 0, 0, "A", 12),
    # regola 13: chi vira cede, le regole 10, 11 e 12 non valgono
    ("13 A in virata, B mure opposte (con le 10 cederebbe B)", "p", "s", 15, 8, 1, 0, "A", 13),
    ("13 A in virata, B affiancata sopravento (con le 11 cederebbe B)", "p", "p", 0, -3, 1, 0, "A", 13),
    ("13 B in virata, A dietro non affiancata (con le 12 cederebbe A)", "p", "p", 8, 0, 0, 1, "B", 13),
    ("13 B in virata, mure opposte (con le 10 cederebbe A)", "p", "s", 12, 6, 0, 1, "B", 13),
    ("13 entrambe in virata, B a sinistra di A: cede B", "p", "p", 0, -3, 1, 1, "B", 13),
    ("13 entrambe in virata, B a destra di A: cede A", "p", "p", 0, 3, 1, 1, "A", 13),
]
# l'1a: stesse due regole di sempre (10; stesse mure: cede la più sopravento, cioè la y minore del vento)
CASI_1A = [
    ("1a mure opposte: cede quella a sinistra", "p", "s", 15, 8, 0, 0, "A", 10),
    ("1a stesse mure in fila, B davanti (più sopravento): cede B, come sempre", "p", "p", 8, 0, 0, 0, "B", 11),
    ("1a stesse mure in fila, B dietro (più sottovento): cede A, come sempre", "p", "p", -8, 0, 0, 0, "A", 11),
]

# virate: la prua attraversa il vento, resta «in virata» finché non è a 42° dal vento o dopo 10 s
VIRATA = """() => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", 2]); sv.setShifts && sv.setShifts(null);
  const R = sv.R, A = R.boats[1], twd = sv.twd, out = {}; R.t = 30;
  const passo = h => { A.S.h = twd + h; A.S.u = 3; for (let i = 0; i < 3; i++) sv.run(1 / 60, 1); return !!A.virando; };
  passo(-20); out.primaDelVento = !!A.virando;                  // a sinistra del vento: non vira
  out.attraversa = passo(15);                                  // passa la prua al vento: in virata
  out.a41 = passo(41);                                         // 41° dal vento: ancora in virata
  out.a43 = passo(43);                                         // 43°: finita
  passo(-30); out.seIncrocia2 = passo(30);                       // di nuovo attraverso: in virata
  passo(-30); passo(30); for (let i = 0; i < 660; i++){ A.S.h = twd + 30; sv.run(1 / 60, 1); }   // incrocia il vento e resta a 30° per 11 s: la virata scade (10 s)
  out.scade = !!A.virando;
  return out; }"""

async def main():
    fail = []; casi = 0; regole = set()
    def chk(ok, msg):
        nonlocal casi
        casi += 1
        if not ok: fail.append(msg); print("FALLITO:", msg)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_function("window.__sv")
        print("== 1b: regole 10, 11, 12, 13")
        for nome, ta, tb, av, la, va, vb, cede, reg in CASI:
            r = await pg.evaluate(CASO, [2, 0, ta, tb, av, la, va, vb])
            ok = r["cede"] == cede and r["regola"] == reg; regole.add(reg)
            print(f"  {'ok ' if ok else 'NO '} {nome:70s} cede {r['cede']} (regola {r['regola']}), atteso {cede} ({reg})")
            chk(ok, f"1b, {nome}: cede {r['cede']} regola {r['regola']}, atteso {cede} regola {reg}")
        print("== 1b: virata (regola 13): inizio e fine")
        v = await pg.evaluate(VIRATA)
        for k, atteso in (("primaDelVento", False), ("attraversa", True), ("a41", True), ("a43", False), ("seIncrocia2", True), ("scade", False)):
            print(f"  {k}: {v[k]} (atteso {atteso})"); chk(v[k] == atteso, f"virata, {k}: {v[k]}, atteso {atteso}")
        print("== 1a: le due regole di sempre")
        for nome, ta, tb, av, la, va, vb, cede, reg in CASI_1A:
            r = await pg.evaluate(CASO, [0, 0, ta, tb, av, la, va, vb])
            print(f"  {'ok ' if r['cede'] == cede and r['regola'] == reg else 'NO '} {nome:70s} cede {r['cede']} (regola {r['regola']}), atteso {cede} ({reg})")
            chk(r["cede"] == cede and r["regola"] == reg, f"1a, {nome}: cede {r['cede']} regola {r['regola']}, atteso {cede} regola {reg}")
        chk(regole == {10, 11, 12, 13}, f"il controllo non ha visto tutte le regole: {sorted(regole)}")
        chk(not errs, f"errori della pagina: {errs[:3]}")
        await b.close()
    print(f"controlli: {casi}, falliti: {len(fail)}")
    print("ESITO:", "OK" if casi and not fail else "FALLITO"); sys.exit(1 if fail or not casi else 0)
asyncio.run(main())
