B=/tmp/claude-1000/check
for s in polare polare_tabella raffiche_e_virate raffiche_portanti retromarcia angolo_morto bolina scarroccio1b orziera1b costo_manovre virata1b virate2 timone2 boma2 finestra misura_scotta_vento_forte studio_barca; do
  for v in 158 160 161; do cd $B/f$v; timeout 600 node $s.js > $B/out_${s}_$v.txt 2>&1; echo "$s $v uscita $?" >> $B/fatto.txt; done
done
echo FINE >> $B/fatto.txt
