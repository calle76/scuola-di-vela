# Collaudo delle scritte sopra le barche (1.2.34, docs/PROPOSTA-ETICHETTE-BARCHE.md, criteri E2-E3), con la misura di misura_etichette.py.
#   E2: sulle 20 regate fisse, al massimo 187 disegni con una scritta piena sopra lo scafo di un'altra barca (il 10% dei 1870 della 1.2.33), 0 sopra il tuo
#   E3: nessuna scritta cambia posto due volte in meno di 1 s; il metro misura: almeno un cambio di posto e almeno 50 000 disegni
# Uso: python tests/collaudo_etichette.py   (BROWSER=firefox per Firefox). Lungo: circa 10 minuti
import asyncio, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from misura_etichette import main
r = asyncio.run(main()); falli = []
if r["regate"] != 20 or r["disegni"] < 50000: falli.append(f"misura non valida: {r['regate']} regate, {r['disegni']} disegni")
if r["copre"] > 187: falli.append(f"E2: {r['copre']} disegni con una scritta piena sopra uno scafo (soglia 187)")
if r["copreMe"] > 0: falli.append(f"E2: {r['copreMe']} disegni con una scritta piena sopra la tua barca (soglia 0)")
if r["cambi"] == 0: falli.append("E3 non misurato: nessun cambio di posto")
if r["salti"] > 0: falli.append(f"E3: {r['salti']} cambi di posto a meno di 1 s dal precedente")
if r["errori"]: falli.append(f"errori della pagina: {r['errori'][:3]}")
print("ESITO: " + ("OK" if not falli else "FALLITO"))
for f in falli: print("  ", f)
sys.exit(1 if falli else 0)
