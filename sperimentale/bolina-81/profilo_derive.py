# Voce 81 (25 nov 2026): confronto col numero di compenso per vento (F123; testo estratto con pdftotext -layout in us/f.txt, non nel repo).
import re
rows=[]
for l in open('us/f.txt'):
    m=re.match(r'^(.{3,45}?)\s+Centerboard\s+(\S+)\s+(.*)$',l.rstrip())
    if not m: continue
    v=re.findall(r'[\(\[]?[\d.]+[\)\]]?',m.group(3))
    v=[float(x.strip('()[]')) for x in v]
    # posizioni: con 5 valori DPN + 4 
    if len(v)==5: rows.append((m.group(1).strip(),v[1:]))
L=dict(rows)['Laser (Int.)'] ; print('Laser',L)
game=[1.16,1.125,1.035]   # stima: Bft 0-1, 2-3, 4 (vedi testo)
out=[]
for n,v in rows:
    r=[a/b for a,b in zip(v[:3],L[:3])]; r4=v[3]/L[3]
    d=sum((a-b)**2 for a,b in zip(r,game))**.5
    out.append((d,n,[round(100*(x-1),1) for x in r+[r4]]))
out.sort()
print('piu simili al profilo del gioco (in % di tempo in piu della barca di riferimento: Bft 0-1, 2-3, 4, 5+)')
for d,n,r in out[:14]: print(f'{d:.3f} {n:32s} {r}')
for n in ('Sunfish (Int.)','Force 5','Finn (Int.)','OK Dinghy (Int.)','Butterfly','Banshee','Laser (Int.)','420 (Int. or Club)','Snipe (Int.)'):
    for d,m,r in out:
        if m==n: print('  ',n,r,round(d,3))
print('--- classi con 4 valori per vento:',len(rows))
dd=sorted(((v[1]/L[1]-v[2]/L[2])*100,n) for n,v in rows)
print('calo fra Bft 2-3 e Bft 4 rispetto alla barca di riferimento, punti: >=10:',sum(x>=10 for x,_ in dd),' >=8:',sum(x>=8 for x,_ in dd),' >=5:',sum(x>=5 for x,_ in dd),'mediana',round(dd[len(dd)//2][0],1)); print('i piu ripidi',[(n,round(x,1)) for x,n in dd[::-1][:8]])
game=[1.16,1.125,1.015]
print('con 1.015 a Bft 4:',[(n,r) for d,n,r in sorted((sum((a-b)**2 for a,b in zip([x/y for x,y in zip(v[:3],L[:3])],game))**.5,n,[round(100*(a/b-1),1) for a,b in zip(v,L)]) for n,v in rows)[:6]])
