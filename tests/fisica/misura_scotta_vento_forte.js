// Misura della voce 73 (docs/PROPOSTA-BARCA-73.md §3, 22 nov 2026): virata e bolina con 14-20 nodi, scotta della regola (boma = apparente − 17°) e regola con lasca sullo sbandamento
// (quella della scotta automatica di js/gioco.js: +1,5° di boma per grado oltre 12°). Barra sola freccia (35°) o Maiusc (45°). Solo misura. Uso: node misura_scotta_vento_forte.js [trace]
const M = require("./motore.js");
const { step, norm180, BOAT, RUD2_SICURA } = M;
const DT=0.01,K=1.6,KN=1.943844,D2R=Math.PI/180, clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const rule=(awa,extra=0)=>clamp((Math.max(BOAT.minBoom,Math.abs(awa)-17+extra)-BOAT.minBoom)/(BOAT.maxBoom-BOAT.minBoom),0,1);
function run(kn, bar, sheetMode, log){
  const E={twd:0,tws:kn/KN}, S={x:0,y:0,h:-45,u:2,vl:0,r:0,lv:2,heel:0}; let info={awa:45}, til=0;
  const sh=()=> sheetMode==="regola"?rule(info.awa): sheetMode==="sicura"? rule(info.awa, 1.5*Math.max(0,Math.abs(S.heel)-12)) : sheetMode;
  const tieni=h=>{const e=norm180(h-S.h); til+=clamp(clamp(-e/25,-RUD2_SICURA,RUD2_SICURA)-til,-K*DT,K*DT);};
  let cap=false, gesto=true, t=0, out=[];
  for(let i=0;i<4000;i++){tieni(-45); info=step(S,{sheet:sh(),tiller:til},E,DT); if(Math.abs(S.heel)>60){cap=true;}}
  const u0=S.u, y0=S.y; let umin=u0, done=null;
  for(let i=0;i<3000;i++){ t=i*DT;
    if(gesto && norm180(S.h)>30) gesto=false;
    if(gesto){ til+=clamp(-bar-til,-K*DT,K*DT);} else tieni(45);
    info=step(S,{sheet:sh(),tiller:til},E,DT); if(Math.abs(S.heel)>60) cap=true;
    umin=Math.min(umin,S.u); if(done===null && Math.abs(norm180(45-S.h))<5) done=t;
    if(log && i%25==0) out.push(`${t.toFixed(2)} h=${norm180(S.h).toFixed(0)} u=${(S.u*KN).toFixed(2)} heel=${S.heel.toFixed(0)} hike=${S.hike.toFixed(2)} r=${S.r.toFixed(1)} awa=${info.awa.toFixed(0)} drive=${info.drive.toFixed(0)} til=${til.toFixed(2)} stall=${S.stall}`);
  }
  return {kn,u0:u0*KN,umin:umin*KN,done,cap,pre:cap, out};
}
const mode=process.argv[2];
if(mode==="trace"){ const r=run(18,RUD2_SICURA,"regola",true); console.log(r.out.slice(0,40).join("\n")); console.log(r); }
else for(const kn of [14,16,18,20]) for(const sm of ["regola","sicura"]) for(const bar of [RUD2_SICURA,1]){ const r=run(kn,bar,sm,false); console.log(kn,sm,bar===1?"45°":"35°", "u0",r.u0.toFixed(2),"min",r.umin.toFixed(2),"fatta in",r.done,"scuffia",r.cap); }
