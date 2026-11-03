# Il codice del gioco dalla 1.0.3: index.html più i file di js/, caricati in ordine dai tag <script src> della pagina.
# testo(): tutto il codice come un testo unico, nell'ordine di caricamento (per leggere costanti con un'espressione regolare).
# copia(cartella, sostituzioni): copia della pagina (index.html, js/ e fonts/) in una cartella, con sostituzioni [(vecchio, nuovo)];
#   ogni «vecchio» deve comparire una volta sola in tutto il codice, altrimenti errore. Torna il percorso del nuovo index.html.
# Funziona anche con una pagina di prima della 1.0.3 (un file unico, senza js/).
import pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent

def file_del_gioco(pagina=ROOT / "index.html"):
    pagina = pathlib.Path(pagina); html = pagina.read_text(encoding="utf-8")
    return [pagina] + [pagina.parent / s for s in re.findall(r'<script src="([^"]+)"></script>', html)]

def testo(pagina=ROOT / "index.html"):
    return "\n".join(f.read_text(encoding="utf-8") for f in file_del_gioco(pagina))

def copia(cartella, sostituzioni=(), pagina=ROOT / "index.html"):
    cartella = pathlib.Path(cartella); cartella.mkdir(parents=True, exist_ok=True)
    pagina = pathlib.Path(pagina); testi = {}
    for f in file_del_gioco(pagina):
        rel = f.relative_to(pagina.parent); testi[rel] = f.read_text(encoding="utf-8")
    for vecchio, nuovo in sostituzioni:
        dove = [r for r, t in testi.items() if vecchio in t]; n = sum(testi[r].count(vecchio) for r in dove)
        if n != 1: raise RuntimeError(f"«{vecchio[:60]}» compare {n} volte nel codice del gioco (ne serve una)")
        testi[dove[0]] = testi[dove[0]].replace(vecchio, nuovo)
    for rel, t in testi.items():
        (cartella / rel).parent.mkdir(parents=True, exist_ok=True); (cartella / rel).write_text(t, encoding="utf-8")
    if (pagina.parent / "fonts").is_dir(): shutil.copytree(pagina.parent / "fonts", cartella / "fonts", dirs_exist_ok=True)   # 1.0.5: i caratteri stanno nel progetto
    return cartella / pagina.name

# 1.2.4 (menu nuovo): script da dare a una pagina prima del caricamento perché nasconda le 14 lezioni nuove (indici 6-19) e ridisegni il menu.
# Lo usano i collaudi che misurano i meccanismi sulle 6 lezioni di prima (esame da 20, carriera); il gioco vero le mostra tutte.
NASCONDI_NUOVE = """window.addEventListener("DOMContentLoaded", () => { if (typeof LESSONS === "undefined") return;
  LESSONS.forEach((L, i) => { if (i >= 6) L.nascosta = true; }); if (mode === "menu") showMenu(); });"""
