// Confronta l'uscita di un collaudo della fisica con quella salvata in git, carattere per carattere (dal «test dei test»,
// docs/PROPOSTA-TEST-DEI-TEST.md). Uso: node confronta.js polare.js   (riferimento: polare.txt nella stessa cartella)
//      node confronta.js polare.js --rigenera   riscrive il riferimento (solo dopo aver deciso che il cambio è voluto, dicendolo)
// Esce con 1 se l'uscita è diversa o se il riferimento manca; stampa le righe diverse.
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const nome = process.argv[2];
if (!nome) { console.error("uso: node confronta.js polare.js [--rigenera]"); process.exit(2); }
const qui = __dirname, rif = path.join(qui, nome.replace(/\.js$/, ".txt"));
const ora = execFileSync(process.execPath, [path.join(qui, nome)], { cwd: qui, encoding: "utf8" });
if (process.argv.includes("--rigenera")) { fs.writeFileSync(rif, ora); console.log("riferimento riscritto:", rif); process.exit(0); }
if (!fs.existsSync(rif)) { console.log("FALLITO: manca il riferimento", rif); process.exit(1); }
const prima = fs.readFileSync(rif, "utf8");
process.stdout.write(ora);
if (ora === prima) { console.log(`ESITO: OK, identico al riferimento (${prima.split("\n").length - 1} righe)`); process.exit(0); }
const a = prima.split("\n"), b = ora.split("\n");
for (let i = 0; i < Math.max(a.length, b.length); i++)
  if (a[i] !== b[i]) console.log(`riga ${i + 1}\n  prima: ${a[i] ?? "(manca)"}\n  ora:   ${b[i] ?? "(manca)"}`);
console.log("ESITO: FALLITO, uscita diversa dal riferimento");
process.exit(1);
