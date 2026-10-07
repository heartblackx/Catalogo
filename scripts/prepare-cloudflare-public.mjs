import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const out = path.join(root, 'public');

fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });

const rootFiles = ['index.html', 'favicon.png', 'robots.txt', 'sitemap.xml'];
for (const name of rootFiles) {
  const src = path.join(root, name);
  if (fs.existsSync(src)) fs.copyFileSync(src, path.join(out, name));
}

// Copiar únicamente directorios que forman parte del sitio público.
const publicDirs = ['assets', 'admin-trafico', 'tijuana', 'rosarito', 'ensenada'];
for (const name of publicDirs) {
  const src = path.join(root, name);
  if (!fs.existsSync(src)) continue;
  const stat = fs.statSync(src);
  if (!stat.isDirectory()) continue;
  fs.cpSync(src, path.join(out, name), { recursive: true });
}

// Garantía: nunca copiar metadata del repositorio ni archivos de build.
for (const forbidden of ['.git', '.github', 'scripts', 'node_modules']) {
  const bad = path.join(out, forbidden);
  if (fs.existsSync(bad)) fs.rmSync(bad, { recursive: true, force: true });
}

console.log('Cloudflare public bundle preparado en', out);
console.log('Archivos raíz:', fs.readdirSync(out).join(', '));
