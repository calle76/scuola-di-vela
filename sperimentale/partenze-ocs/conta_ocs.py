# conta le sigle di partenza anticipata nelle tabelle riassuntive Sailwave: per ogni colonna gara (R1, R2, ...) barche partite (non DNC/DNS/vuote) e OCS/UFD/BFD
import sys, re
from html.parser import HTMLParser
class T(HTMLParser):
    def __init__(s): super().__init__(); s.tabs=[]; s.row=None; s.cell=None
    def handle_starttag(s,t,a):
        if t=="table": s.tabs.append([])
        elif t=="tr" and s.tabs: s.row=[]
        elif t in("td","th") and s.row is not None: s.cell=""
    def handle_endtag(s,t):
        if t in("td","th") and s.cell is not None and s.row is not None: s.row.append(s.cell.strip()); s.cell=None
        elif t=="tr" and s.row is not None: s.tabs[-1].append(s.row); s.row=None
    def handle_data(s,d):
        if s.cell is not None: s.cell+=d
COD=("OCS","UFD","BFD"); NON=("DNC","DNS","DNE")
tot_st=tot_o=tot_r=tot_rr=0
for f in sys.argv[1:]:
    p=T(); p.feed(open(f,encoding="utf-8",errors="replace").read())
    st=o=gare=gare_con=0
    for tab in p.tabs:
        if not tab: continue
        h=[c.replace("\xa0"," ").strip() for c in tab[0]]
        if "Total" not in h: continue
        col=[i for i,c in enumerate(h[:h.index("Total")]) if re.search(r"^R\d|Race|\d",c)]
        if len(col)<1 or len(tab)<4: continue
        for i in col:
            cs=[r[i] for r in tab[1:] if i<len(r)]
            if not cs: continue
            s_=sum(1 for c in cs if c and c not in ("-",) and not any(n in c.upper() for n in NON))
            oo=sum(1 for c in cs if any(k in c.upper() for k in COD))
            if s_<3: continue
            st+=s_; o+=oo; gare+=1; gare_con+=oo>0
    tot_st+=st; tot_o+=o; tot_r+=gare; tot_rr+=gare_con
    print(f"{f.split('/')[-1]}: gare {gare}, partenze di barche {st}, OCS/UFD/BFD {o} ({100*o/max(1,st):.1f}%), gare con almeno uno {gare_con}")
print(f"TOTALE: gare {tot_r}, partenze di barche {tot_st}, OCS/UFD/BFD {tot_o} ({100*tot_o/max(1,tot_st):.2f}%), gare con almeno uno {tot_rr} ({100*tot_rr/max(1,tot_r):.0f}%)")
