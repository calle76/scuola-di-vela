// Scuola di vela, base.js — Strumenti comuni a tutto il gioco: $, KN, canvas, clamp, rotte e andature.
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/PROPOSTA-DIVISIONE-CODICE.md.
  const $ = id => document.getElementById(id);
  const KN = 1.943844;
  const canvas = $("c"), ctx = canvas.getContext("2d");
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const sgn = v => v < 0 ? -1 : 1;
  const deg3 = d => String(Math.round(norm360(d)) % 360).padStart(3, "0") + "°";
  const CARD = ["nord","nord-est","est","sud-est","sud","sud-ovest","ovest","nord-ovest"];
  const cardName = d => CARD[Math.round(norm360(d) / 45) % 8];
  const card = d => ["N","NE","E","SE","S","SO","O","NO"][Math.round(norm360(d) / 45) % 8];
  const ANDATURE = [[40,"Angolo morto"],[55,"Bolina stretta"],[75,"Bolina larga"],[105,"Traverso"],[135,"Lasco"],[165,"Gran lasco"],[181,"Poppa"]];
  const andName = twa => ANDATURE.find(a => twa < a[0])[1];

