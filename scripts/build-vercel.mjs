/**
 * Copie uniquement les fichiers servis sur le web vers dist/ (déploiement Vercel).
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");
const DIST = path.join(ROOT, "dist");

function rmrf(p) {
  fs.rmSync(p, { recursive: true, force: true });
}

function copyDir(src, dest) {
  fs.cpSync(src, dest, { recursive: true });
}

rmrf(DIST);
fs.mkdirSync(DIST, { recursive: true });

const topFiles = [
  "index.html",
  "neowake.html",
  "artikel-uebersicht.html",
  "impressum.html",
  "datenschutz.html",
  "affiliate-disclosure.html",
  "styles.css",
  "favicon.svg",
  "robots.txt",
  "sitemap.xml",
  "sitemap-pages.xml",
  "sitemap-articles.xml",
];

for (const f of topFiles) {
  const s = path.join(ROOT, f);
  if (fs.existsSync(s)) {
    fs.copyFileSync(s, path.join(DIST, f));
  }
}

for (const dir of ["artikel", "quiz", "blog", "images"]) {
  const s = path.join(ROOT, dir);
  if (fs.existsSync(s) && fs.statSync(s).isDirectory()) {
    copyDir(s, path.join(DIST, dir));
  }
}

console.log("build-vercel: OK → dist/");
