from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
original = s

# Remove share metadata that exposes the Concordia domain.
s = re.sub(r'\n<meta property="og:image" content="https://grupoconcordia\.info/[^"]+">', '', s)
s = re.sub(r'\n<meta property="og:image:alt" content="[^"]+">', '', s)
s = re.sub(r'\n<meta name="twitter:image" content="https://grupoconcordia\.info/[^"]+">', '', s)
s = s.replace('<meta name="twitter:card" content="summary_large_image">', '<meta name="twitter:card" content="summary">')

# Exact label requested by the user.
s = s.replace('Imagen real del desarrollo', 'Imagen del desarrollo')

# Only development media already tied to that development may be used as fallback.
old = 'const developmentPhoto=model.cover || model.siteImage || "";'
if old not in s:
    raise SystemExit('development fallback not found')
s = s.replace(old, 'const developmentPhoto=model.cover || "";', 1)

# Label development fallback inside the development modal lot cards too.
old = '    const photo=getLotPhoto(l,m).url;'
if old not in s:
    raise SystemExit('development lot photo line not found')
s = s.replace(old, '    const photoInfo=getLotPhoto(l,m);\n    const photo=photoInfo.url;', 1)

old = '''      <div class="mlot-photo">${photo?`<img src="${esc(photo)}" alt="Foto del lote ${esc(l.lote||"")}" loading="lazy">`:`<div class="mlot-photo-placeholder"><div><b>📷 Foto del lote</b><span>Espacio reservado para fotografía</span></div></div>`}</div>'''
new = '''      <div class="mlot-photo">${photo?`<img src="${esc(photo)}" alt="${photoInfo.type==="lote"?"Foto del lote":"Imagen del desarrollo"}" loading="lazy"><span class="lot-tag">${photoInfo.type==="lote"?"Foto del lote":"Imagen del desarrollo"}</span>`:`<div class="mlot-photo-placeholder"><div><b>📷 Fotografía por agregar</b><span>Sin fotografía propia ni imagen del desarrollo revisada.</span></div></div>`}</div>'''
if old not in s:
    raise SystemExit('development lot markup not found')
s = s.replace(old, new, 1)

# Offices: keep address/map data, but the only public office name is Vive La Baja.
start = s.find('function cleanOfficeName(name=""){')
end = s.find('\nconst state = {', start)
if start < 0 or end < 0:
    raise SystemExit('office block not found')
office = r'''function stripOfficeText(value=""){
  return String(value||"")
    .replace(/grupo\s+concordia/ig,"")
    .replace(/concordia/ig,"")
    .replace(/\s+/g," ").trim();
}
function renderOffices(){
  const grid=document.getElementById("officeGrid");
  const count=document.getElementById("officeCount");
  if(!grid)return;
  const list=Array.isArray(state.offices)?state.offices:[];
  if(count)count.textContent="Vive La Baja";
  if(!list.length){
    grid.innerHTML=`<div class="office-empty">Vive La Baja · ubicación por confirmar.</div>`;
    return;
  }
  grid.innerHTML=list.map(o=>{
    const ref=stripOfficeText(o.zona||o.direccion||"").replace(/_/g," ");
    const link=o.maps_url||"";
    return `<article class="office-card"><span class="office-label">Vive La Baja</span><h3>Vive La Baja</h3>${ref?`<p>${esc(ref)}</p>`:""}${link?`<a href="${esc(link)}" target="_blank" rel="noopener noreferrer">Abrir en Google Maps <span>↗</span></a>`:`<span class="office-empty">Liga por confirmar</span>`}</article>`;
  }).join("");
}
'''
s = s[:start] + office + s[end:]

# No raw Concordia-domain reference may remain in the public HTML.
if 'grupoconcordia.info' in s.lower():
    raise SystemExit('Concordia domain remains in index.html')
if s == original:
    raise SystemExit('no changes produced')
p.write_text(s, encoding='utf-8')
