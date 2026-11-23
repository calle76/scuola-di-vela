# Voce 2 (23 nov 2026): dalle regate lunghe registrate da Ale e Lucio (registrazioni/, gioco 1.3.26 e oltre, «regata N di 3») tempi di bolina di giocatore e rivali,
# secondi passati coperti (eventi coperta/libera) e cambi di mure dei rivali in bolina. Si lancia dalla cartella registrazioni/: python3 -I ../tests/misura_bolina_registrazioni.py
import sys,re,glob,statistics as st
fs=[f for f in sorted(glob.glob('regata-202611*-intera.txt')) if re.search(r'gioco 1\.3\.(2[6-9]|[3-9]\d)',open(f).readline()+open(f).readlines()[1]) and '3 di 3' in open(f).readlines()[1] or (re.search(r'gioco 1\.3\.(2[6-9]|[3-9]\d)',open(f).readlines()[1]) and 'di 3' in open(f).readlines()[1])]
fs=sorted(set(fs))
tot={'gioc':[], 'riv':[]}; cop=[]; vir={'gioc':[], 'riv':[]}
for f in fs:
    L=open(f).read().split('\n'); h=L[1]
    ver=re.search(r'gioco ([\d.]+)',h).group(1)
    giu=re.search(r'avversari=(\w+)',L[3]); giu=giu.group(1) if giu else '?'
    start={}; legs={}; cur={}
    sgn={}; nv={}
    copt={}; copsum={}
    for l in L:
        p=l.split()
        if not p: continue
        if p[0]=='E':
            t=float(p[1])
            if p[2]=='avv_lato': legs.setdefault(p[3],{})[int(p[4])]=t
            elif p[2]=='partito': legs.setdefault('Tu',{})[1]=t
            elif p[2]=='lato': legs.setdefault('Tu',{})[int(p[3])]=t
            elif p[2]=='arrivo': legs.setdefault('Tu',{})['fin']=t
            elif p[2]=='avv_arrivo': legs.setdefault(p[3],{})['fin']=t
            elif p[2]=='coperta': copt[p[3]]=t
            elif p[2]=='libera' and p[3] in copt: copsum[p[3]]=copsum.get(p[3],0)+t-copt.pop(p[3])
        elif p[0]=='B' and len(p)>8:
            n=p[2]; lato=p[8]; s=1 if float(p[7])>0 else -1
            if lato in('1','3'):
                k=(n,lato)
                if k in sgn and sgn[k]!=s and abs(float(p[7]))<90: nv[k]=nv.get(k,0)+1
                sgn[k]=s
    out=[]
    for n,d in legs.items():
        for a,b in ((1,2),(3,4 if 4 in d else 'fin')):
            if a in d and b in d:
                (tot['gioc'] if n=='Tu' else tot['riv']).append(d[b]-d[a])
    print(f, ver, giu, {n:{k:round(v,1) for k,v in d.items()} for n,d in legs.items()}, 'coperta s:',{k:round(v) for k,v in copsum.items()}, 'virate riv bolina:',nv)
print('bolina giocatore: n',len(tot['gioc']),'mediana',round(st.median(tot['gioc']),1) if tot['gioc'] else None)
print('bolina rivali: n',len(tot['riv']),'mediana',round(st.median(tot['riv']),1))
