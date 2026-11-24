# Simulazione di soli rivali per docs/PROPOSTA-RIVALI-CHE-CRESCONO.md (24 nov 2026): 300 mondi da 30 stagioni per riga, seme fisso, nessuna barca in acqua (ordine sorteggiato col modello del gioco, peso e^(0,2*forza)).
# F = quanto pesa il numero nella forza: non misurato, provati 2, 4 e 8. Uso: python3 tests/simula_crescita_rivali.py
import random, math, statistics as st
# solo rivali, niente giocatore: 10 zonali e 10 nazionali, 4 tappe a stagione, ordine sorteggiato col modello del gioco (peso e^(0.2*forza)), forza = doti (-2..2) + F*c/100
def stagione(g, c, tr, F):
    pt={i:0 for i in g}; vit={i:0 for i in g}
    for _ in range(4):
        r=list(g); pos=1
        while r:
            w=[math.exp(0.2*(tr[i]+F*c[i]/100)) for i in r]; i=random.choices(r,w)[0]; r.remove(i); pt[i]+=pos
            if pos==1: vit[i]+=1
            pos+=1
    return sorted(g,key=lambda i:(pt[i],random.random())), vit
def mondo(regola,F,S=30):
    mix=lambda m:(random.sample(m,10))
    Z=list(range(10)); N=list(range(10,20)); tr={}
    for g,m in ((Z,[1,1,1,0,0,0,0,-1,-1,-1]),(N,[1]*4+[0]*4+[-1]*2)):
        a,b=mix(m),mix(m)
        for k,i in enumerate(g): tr[i]=a[k]+b[k]
    c={i:random.uniform(10,30) if i<10 else random.uniform(45,70) for i in range(20)}
    tetto={i:random.uniform(50,100) for i in range(20)} if regola=="tetto personale" else {i:100 for i in range(20)}
    if regola=="tetto personale":
        for i in range(10,20): tetto[i]=random.uniform(75,100)
    camp={}; fasce={}
    for s in range(1,S+1):
        oz,vz=stagione(Z,c,tr,F); on,vn=stagione(N,c,tr,F); camp[on[0]]=camp.get(on[0],0)+1
        for g,v in ((Z,vz),(N,vn)):
            for i in g:
                if regola=="chi vince cresce": c[i]=min(100,c[i]+8*v[i])
                else:
                    q=max(0,1-c[i]/tetto[i]); c[i]+=4*(4*q*q*1.0)/1.0*0.6+3*v[i]*q   # regate (rallenta) + vittorie di tappa
        up=oz[0]; dn=on[-1]; Z.remove(up); N.remove(dn); Z.append(dn); N.append(up)
        if s in (1,3,5,10,20,30): fasce[s]=(sum(x>=90 for x in c.values()),round(st.mean(c[i] for i in Z)),round(st.mean(c[i] for i in N)),round(max(c.values())-min(c.values())))
    return max(camp.values())/S, len(camp), fasce
for F in (2,4,8):
    for regola in ("chi vince cresce","quattro regole, tetto 100","tetto personale"):
        random.seed(11); R=[mondo("chi vince cresce" if regola.startswith("chi") else regola,F) for _ in range(300)]
        m=lambda k,j:round(st.mean(r[2][k][j] for r in R),1)
        print(f"F={F} {regola:26s} titoli al più vincente {100*st.mean(r[0] for r in R):4.0f}%  campioni diversi {st.mean(r[1] for r in R):4.1f}  rivali >=90 alle stagioni 5,10,30: {m(5,0)},{m(10,0)},{m(30,0)}  media zon/naz st.5 {m(5,1)}/{m(5,2)}  st.30 {m(30,1)}/{m(30,2)}  distanza max-min st.30 {m(30,3)}")
