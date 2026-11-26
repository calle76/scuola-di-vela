// Voce 84, §16: virata di K con 18 nodi uscendo più larghi e lascando poco la scotta (tecnica descritta da Semb, F137, e Taylor, F130).
const d="/home/callle/scuola-di-vela/sperimentale/barca-84/", C=require(d+"candidato.json");
let src=require("fs").readFileSync(d+"virate_semb.js","utf8").split("\nconst MIS")[0];
src=src.replace("Math.max(lasca, sheetFor(info.awa))","Math.min(1, sheetFor(info.awa) + lasca)");
const virata=new Function("require",src.replace(/require\("\.\//g,'require("'+d)+"\nreturn virata;")(require);
for (const [g,tg,l,tl] of [[0,0,0,0],[0,0,.1,3],[0,0,.2,3],[10,3,.1,3],[10,3,.2,4],[15,4,.15,4],[15,4,.3,4]]){ const r=virata(C[3].P,18,45,g,tg,l,tl);
 console.log(`K 18 nodi, +${g}° per ${tg} s, scotta +${l} per ${tl} s: uscita ${(r.uout/r.uin*100).toFixed(0)}%, media ${(r.umean/r.uin*100).toFixed(0)}%, minimo ${(r.umin/r.uin*100).toFixed(0)}%, 80% dopo ${r.t80===null?"mai":r.t80.toFixed(1)+" s"}`); }
