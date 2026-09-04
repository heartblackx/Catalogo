from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
original=s

# --- Fotos de desarrollos: sin filtros, degradados, etiquetas ni texto encima ---
s=s.replace('.dev-photo img{width:100%;height:100%;object-fit:cover;transition:.4s ease}',
            '.dev-photo img{width:100%;height:100%;object-fit:cover;filter:none!important;opacity:1!important;mix-blend-mode:normal!important;transition:none}')
s=s.replace('.dev:hover .dev-photo img{transform:scale(1.035)}',
            '.dev:hover .dev-photo img{transform:none}')
s=s.replace('.dev-photo:after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(4,18,25,.78),rgba(4,18,25,.02) 62%)}',
            '.dev-photo:after{display:none}')
s=s.replace('.modal-hero img{width:100%;height:100%;object-fit:cover}',
            '.modal-hero img{width:100%;height:100%;object-fit:cover;filter:none!important;opacity:1!important;mix-blend-mode:normal!important}')
s=s.replace('.modal-hero:after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(5,19,26,.85),transparent 68%)}',
            '.modal-hero:after{display:none}')
s=s.replace('.gallery img{width:100%;height:100%;object-fit:cover;border-radius:15px}',
            '.gallery img{width:100%;height:100%;object-fit:cover;border-radius:15px;filter:none!important;opacity:1!important;mix-blend-mode:normal!important}')

# Cabeceras fuera de las imágenes.
anchor='.dev-body{padding:22px 23px 23px;display:flex;flex-direction:column;flex:1}'
addition='''\n.dev-summary{display:flex;justify-content:space-between;align-items:flex-start;gap:14px;margin-bottom:14px}\n.dev-heading{min-width:0}.dev-type{display:inline-block;color:#0f6f75;text-transform:uppercase;letter-spacing:.11em;font-size:.65rem;font-weight:900}\n.dev-heading h3{margin:5px 0 2px;font-size:1.45rem;letter-spacing:-.025em;line-height:1.05}.dev-zone{margin:0;color:#758188;font-size:.78rem}\n.dev-availability{flex:none;padding:7px 10px;border-radius:999px;background:#e4f4ee;color:#197254;font-size:.67rem;font-weight:900;white-space:nowrap}.dev-availability.off{background:#f3ebe2;color:#7c6551}\n'''
if addition.strip() not in s:
    if anchor not in s: raise SystemExit('dev-body CSS anchor not found')
    s=s.replace(anchor,anchor+addition,1)

modal_anchor='.modal-content{padding:30px}'
modal_add='''\n.modal-heading{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;margin:0 0 22px}.modal-heading small{display:block;color:#0f777c;text-transform:uppercase;letter-spacing:.13em;font-size:.68rem;font-weight:900}.modal-heading h2{margin:6px 0 0;font-size:clamp(2rem,5vw,3.5rem);letter-spacing:-.045em;line-height:.98}.modal-heading .modal-zone{color:#728087;font-size:.86rem;text-align:right}\n'''
if modal_add.strip() not in s:
    if modal_anchor not in s: raise SystemExit('modal-content CSS anchor not found')
    s=s.replace(modal_anchor,modal_anchor+modal_add,1)

# Mobile polish for headings moved outside images.
media_anchor='@media(max-width:680px){\n  .quote-summary{grid-template-columns:1fr 1fr}'
if media_anchor in s and '.modal-heading{display:block}' not in s:
    s=s.replace(media_anchor,'@media(max-width:680px){\n  .modal-heading{display:block}.modal-heading .modal-zone{text-align:left;margin-top:7px}.dev-summary{display:block}.dev-availability{display:inline-flex;margin-top:9px}\n  .quote-summary{grid-template-columns:1fr 1fr}',1)

# --- Tarjetas de desarrollo: la foto contiene SOLO la foto ---
start=s.find('function renderDevelopments(models){')
end=s.find('\nfunction getLotPhoto(lot,model){',start)
if start<0 or end<0: raise SystemExit('renderDevelopments block not found')
new_render=r'''function renderDevelopments(models){
  const grid=document.getElementById("devGrid");
  if(!models.length){
    grid.innerHTML=`<div class="state">No encontramos desarrollos con esos filtros.</div>`;
    return;
  }
  grid.innerHTML=models.map(m=>{
    const zone=m.zones[0] || m.loc?.zona || "Zona por confirmar";
    const typeLabel=m.type==="costa"?"Costa":m.type==="campestre"?"Campestre":"Urbano";
    const availability=m.available.length
      ? `${m.available.length} lotes disponibles`
      : (m.lots.length ? "Disponibilidad por confirmar" : "Información por confirmar");
    const cover=m.cover
      ? `<img src="${esc(m.cover)}" alt="${esc(m.name)}" loading="lazy" onerror="devImageFallback(this)">`
      : `<div class="dev-photo-fallback"><strong>Imagen no disponible</strong></div>`;
    const mapDisabled=!m.loc?.maps_url;
    return `
      <article class="dev" data-id="${m.id}">
        <div class="dev-photo">${cover}</div>
        <div class="dev-body">
          <div class="dev-summary">
            <div class="dev-heading"><span class="dev-type">${esc(typeLabel)}</span><h3>${esc(m.name)}</h3><p class="dev-zone">${esc(zone)}</p></div>
            <span class="dev-availability ${m.available.length?"":"off"}">${esc(availability)}</span>
          </div>
          <p class="dev-desc">${esc(m.description)}</p>
          <div class="chips">${m.amenities.slice(0,4).map(a=>`<span class="chip">${esc(a)}</span>`).join("")}</div>
          <div class="dev-metrics">
            <div class="metric"><small>Disponibles</small><strong>${m.available.length || "Consultar"}</strong></div>
            <div class="metric"><small>Desde</small><strong>${m.minArea?m2(m.minArea):"Consultar"}</strong></div>
            <div class="metric"><small>Enganche desde</small><strong>${m.minDownPct?`${money(m.minDownPct)}%`:"Consultar"}</strong></div>
          </div>
          <div class="dev-actions">
            <button class="devbtn" onclick="openDevelopment('${m.id}')">Ver desarrollo →</button>
            <button class="mapbtn" ${mapDisabled?"disabled":""} onclick="${mapDisabled?"":"openMap('"+m.id+"')"}">📍 Ubicación</button>
          </div>
        </div>
      </article>`;
  }).join("");
}
'''
s=s[:start]+new_render+s[end:]

# --- Modal del desarrollo: foto limpia, título y zona debajo ---
start=s.find('function openDevelopment(id){')
end=s.find('\nfunction closeModal(){',start)
if start<0 or end<0: raise SystemExit('openDevelopment block not found')
new_modal=r'''function openDevelopment(id){
  const m=state.models.find(x=>x.id===id);
  if(!m) return;
  state.current=m;
  if(typeof lastFocusedElement!=="undefined") lastFocusedElement=document.activeElement;
  developmentFilters={currency:"USD",downPct:0,term:0,monthlyMin:"",monthlyMax:"",terrain:"all",areaMin:"",areaMax:"",search:""};
  const zone=m.zones[0] || m.loc?.zona || "Zona por confirmar";
  const address=m.loc?.direccion || "Consulta la ubicación desde el botón de mapa.";
  const cover=m.cover || "";
  const typeLabel=m.type==="costa"?"Costa":m.type==="campestre"?"Campestre":"Urbano";
  const gallery=m.media.slice(0,5).map(x=>`<img src="${esc(x.public_url)}" alt="${esc(m.name)}" loading="lazy" onerror="devImageFallback(this)">`).join("");
  document.getElementById("modalBody").innerHTML=`
    <div class="modal-hero">${cover?`<img src="${esc(cover)}" alt="${esc(m.name)}" onerror="devImageFallback(this)">`:`<div class="dev-photo-fallback"><strong>Imagen no disponible</strong></div>`}</div>
    <div class="modal-content">
      <div class="modal-heading">
        <div><small>${esc(typeLabel)}</small><h2 id="developmentTitle">${esc(m.name)}</h2></div>
        <div class="modal-zone">${esc(zone)}</div>
      </div>
      <div class="modal-top">
        <div class="info-panel"><h3>Sobre el desarrollo</h3><p>${esc(m.description)}</p><div class="amenities">${m.amenities.map(a=>`<span class="amenity">✓ ${esc(a)}</span>`).join("")}</div></div>
        <div class="location-panel"><h3>Ubicación</h3><p><strong>${esc(zone)}</strong><br>${esc(address)}</p>${m.loc?.maps_url?`<button class="devbtn" style="width:100%;margin-top:10px" onclick="openMap('${m.id}')">Abrir en Maps →</button>`:"<p><small>Ubicación por confirmar.</small></p>"}</div>
      </div>
      <div class="modal-stats">
        <div class="modal-stat"><small>Lotes disponibles</small><strong>${m.available.length || "Consultar"}</strong></div>
        <div class="modal-stat"><small>Superficie desde</small><strong>${m.minArea?m2(m.minArea):"Consultar"}</strong></div>
        <div class="modal-stat"><small>Superficie hasta</small><strong>${m.maxArea?m2(m.maxArea):"Consultar"}</strong></div>
        <div class="modal-stat"><small>Enganche desde</small><strong>${m.minDownPct?`${money(m.minDownPct)}%`:"Consultar"}</strong></div>
      </div>
      ${gallery?`<div class="gallery">${gallery}</div>`:""}
      <div id="developmentFilters" class="development-filters"></div>
      <div class="modal-lots-head"><h3>Lotes disponibles</h3><span id="developmentLotCount">${m.available.length?`${m.available.length} disponibles`:"Disponibilidad por confirmar"}</span></div>
      <div class="modal-lots" id="developmentLots"></div>
    </div>`;
  renderDevelopmentToolbar();
  renderDevelopmentLots();
  const modal=document.getElementById("devModal");
  modal.classList.add("open");modal.setAttribute("aria-hidden","false");document.body.style.overflow="hidden";
  document.getElementById("modalCard")?.focus();
  history.replaceState(null,"",`#${m.id}`);
}
'''
s=s[:start]+new_modal+s[end:]

# --- Copia pública: quitar lenguaje de backend, sincronización, bases e inventario en vivo ---
replacements={
'✓ Inventario conectado':'✓ Opciones disponibles',
'Ingresa cuánto puedes dar de enganche y te mostraremos lotes reales del inventario.':'Ingresa cuánto puedes dar de enganche y te mostraremos opciones que se ajusten a tu presupuesto.',
'En Invierte Inteligente TJ te ayudamos a comparar opciones con información clara, revisar disponibilidad real y conectar directamente con un asesor para cotizar el terreno que mejor se ajuste a tu presupuesto.':'En Invierte Inteligente TJ te ayudamos a comparar opciones con información clara, consultar disponibilidad y conectar directamente con un asesor para cotizar el terreno que mejor se ajuste a tu presupuesto.',
'Consulta amenidades y disponibilidad en un solo lugar. Para evitar espacios vacíos, las imágenes de los desarrollos se cargan desde la galería sincronizada en Supabase.':'Consulta amenidades, ubicación y disponibilidad de los desarrollos en un solo lugar.',
'Cargando desarrollos desde el inventario…':'Cargando desarrollos…',
'<div class="kicker">Inventario en vivo</div>':'<div class="kicker">Terrenos disponibles</div>',
'Consultando inventario…':'Consultando disponibilidad…',
'Consulta disponibilidad, compara opciones y agenda una cita. La información comercial se muestra desde la base vigente y un asesor confirma los detalles de tu operación.':'Consulta disponibilidad, compara opciones y agenda una cita. Un asesor puede ayudarte a resolver dudas y confirmar las condiciones de tu operación.',
'<article><span class="trust-icon">↻</span><strong>Inventario actualizado</strong><p>Los lotes y su disponibilidad se consultan desde el inventario conectado al catálogo.</p></article>':'<article><span class="trust-icon">↻</span><strong>Opciones disponibles</strong><p>Consulta los terrenos disponibles y compara sus características antes de cotizar.</p></article>',
'<article><span class="trust-icon">✓</span><strong>Seguimiento personal</strong><p>Las citas se asignan a un asesor para continuar el proceso y confirmar condiciones.</p></article>':'<article><span class="trust-icon">✓</span><strong>Seguimiento personal</strong><p>Un asesor puede acompañarte para resolver dudas y confirmar las condiciones de tu terreno.</p></article>',
'Cargando ubicaciones…':'Ubicaciones',
'Consultando oficinas registradas…':'Cargando oficinas…',
'Usaremos ese monto para comparar únicamente contra lotes con una regla comercial válida.':'Usaremos ese monto para mostrarte opciones que se ajusten a tu presupuesto.',
'Resultados calculados con superficie del lote y la tabla comercial vigente. Se muestran primero los que aprovechan mejor tu presupuesto.':'Te mostramos primero las opciones que mejor se ajustan a tu presupuesto.',
'Estas son las opciones más cercanas por encima de tu monto. No alteramos precios ni porcentajes para forzar una coincidencia.':'Estas son las opciones disponibles más cercanas por encima de tu monto.',
'No hay opciones calculables en esta zona':'No hay opciones disponibles en esta zona',
'Los cálculos usan precios comerciales vigentes':'Ajusta los filtros para comparar opciones',
'Proyecto residencial consolidado. El catálogo original lo presenta como un desarrollo sin disponibilidad, por lo que el estado visible se valida contra el inventario actual.':'Proyecto residencial consolidado para quienes buscan una opción patrimonial en una zona urbana con buena conectividad.',
'No fue posible consultar Supabase desde esta vista.':'No fue posible cargar los desarrollos en este momento.',
'El diseño está listo; al publicarlo en tu sitio volverá a intentar cargar el inventario automáticamente.':'Intenta nuevamente en unos momentos.',
'Inventario no disponible en esta vista previa.':'No fue posible cargar los lotes en este momento.',
'No se pudo conectar al inventario':'Disponibilidad no disponible por el momento'
}
for a,b in replacements.items():
    s=s.replace(a,b)

# En el estado de las tarjetas no mostrar lenguaje interno.
s=s.replace('"Inventario pendiente"','"Disponibilidad por confirmar"')

# Limpieza final de textos públicos conocidos relacionados con infraestructura.
# No tocamos nombres de tablas/funciones internas porque no son visibles al cliente.
visible_forbidden=[
    'galería sincronizada en Supabase',
    'No fue posible consultar Supabase desde esta vista',
    'Inventario en vivo',
    'Inventario conectado',
    'Inventario actualizado',
    'base vigente'
]
for phrase in visible_forbidden:
    if phrase in s:
        raise SystemExit(f'visible technical phrase remains: {phrase}')

if s==original:
    raise SystemExit('No changes produced')
p.write_text(s,encoding='utf-8')
