from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Separate active El Fuerte inventory from the sold-out El Fuerte 2 phase.
s = s.replace(
    'members:["El Fuerte","El Fuerte 2","El Fuerte II"], priceNames:["El Fuerte","El Fuerte 2","El Fuerte II"]',
    'members:["El Fuerte"], priceNames:["El Fuerte","El Fuerte II"]'
)

# Add historical developments that are present in inventory with zero available lots.
marker = '// CATALOGO_V36_VENDIDOS'
if marker not in s:
    block = r'''
,
// CATALOGO_V36_VENDIDOS
  {
    id:"alamar-vendido", name:"Alamar", members:["Alamar"], priceNames:["Alamar"], siteImage:"https://vivelabaja.com/images/Desarrollos/760x500-Alamar.jpg", type:"urbano",
    description:"Desarrollo de Tijuana que ya colocó la totalidad de sus lotes registrados.", amenities:["Desarrollo vendido","Tijuana"]
  },
  {
    id:"costa-dorada-elite", name:"Costa Dorada Elite", members:["Costa Dorada Elite"], priceNames:["Costa Dorada Elite"], siteImage:"", type:"costa",
    description:"Etapa costera que ya colocó la totalidad de sus lotes registrados.", amenities:["Desarrollo vendido","Costa"]
  },
  {
    id:"el-fuerte-2-vendido", name:"El Fuerte 2", members:["El Fuerte 2"], priceNames:["El Fuerte 2"], siteImage:"https://vivelabaja.com/images/Desarrollos/760x500-Fuerte.jpg", type:"urbano",
    description:"Etapa urbana de Tijuana que ya colocó la totalidad de sus lotes registrados.", amenities:["Desarrollo vendido","Tijuana"]
  },
  {
    id:"vistas-del-rio-vendido", name:"Vistas del Río", members:["Vistas del Rio","Vistas del Río"], priceNames:["Vistas del Rio","Vistas del Río"], siteImage:"", type:"urbano",
    description:"Desarrollo de Tijuana que ya colocó la totalidad de sus lotes registrados.", amenities:["Desarrollo vendido","Tijuana"]
  }
'''
    needle = '\n];\n\n\nconst APPOINTMENT_ENDPOINT'
    if needle not in s:
        raise SystemExit('No se encontró el cierre del catálogo')
    s = s.replace(needle, block + '\n];\n\n\nconst APPOINTMENT_ENDPOINT', 1)

# Prominent sold-out styling.
css_marker = 'SOLD_OUT_CARDS_V36'
if css_marker not in s:
    css = r'''
<style id="sold-out-cards-v36">
/* SOLD_OUT_CARDS_V36 */
.dev.sold-out-card{grid-column:span 2;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,.14);box-shadow:0 22px 60px rgba(0,0,0,.24)}
.sold-out-card .sold-out-photo{position:relative;min-height:270px}
.sold-out-card .sold-out-photo img{filter:saturate(.72) brightness(.64)}
.sold-out-overlay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:24px;background:linear-gradient(180deg,rgba(4,19,27,.12),rgba(4,19,27,.80))}
.sold-out-stamp{width:min(92%,620px);padding:22px 26px;border:3px solid rgba(255,255,255,.92);border-radius:18px;text-align:center;transform:rotate(-2deg);background:rgba(6,25,34,.74);backdrop-filter:blur(5px);box-shadow:0 10px 30px rgba(0,0,0,.32)}
.sold-out-stamp small{display:block;font-size:12px;letter-spacing:.22em;font-weight:800;text-transform:uppercase;opacity:.9;margin-bottom:6px}
.sold-out-stamp strong{display:block;font-size:clamp(28px,4vw,48px);line-height:.98;letter-spacing:.025em;font-weight:950;text-transform:uppercase}
.sold-out-panel{margin:14px 0 4px;padding:18px 20px;border-radius:16px;background:linear-gradient(135deg,rgba(167,116,33,.16),rgba(12,46,59,.10));border:1px solid rgba(180,138,69,.32)}
.sold-out-panel span{display:block;font-size:12px;font-weight:900;letter-spacing:.18em;text-transform:uppercase;margin-bottom:5px}
.sold-out-panel strong{display:block;font-size:clamp(21px,2.4vw,30px);line-height:1.05;margin-bottom:7px}
.sold-out-panel small{font-size:13px;opacity:.78}
.modal-sold-out{margin:18px 0;padding:24px;border-radius:18px;text-align:center;border:2px solid rgba(180,138,69,.45);background:linear-gradient(135deg,rgba(167,116,33,.18),rgba(8,35,46,.10))}
.modal-sold-out span{display:block;font-size:12px;letter-spacing:.18em;font-weight:900;text-transform:uppercase;margin-bottom:6px}
.modal-sold-out strong{display:block;font-size:clamp(26px,4vw,40px);line-height:1;text-transform:uppercase}
@media(max-width:900px){.dev.sold-out-card{grid-column:span 1}.sold-out-card .sold-out-photo{min-height:230px}.sold-out-stamp{padding:18px}.sold-out-stamp strong{font-size:32px}}
</style>
'''
    if '</head>' not in s:
        raise SystemExit('No se encontró </head>')
    s = s.replace('</head>', css + '\n</head>', 1)

# Main development grid card.
old = '    const mapDisabled=!mapUrlForModel(m);\n    return `'
section_start = s.find('function renderDevelopments')
section_end = s.find('function getLotPhoto')
render_section = s[section_start:section_end] if section_start >= 0 and section_end > section_start else ''
if old in s and 'sold-out-card' not in render_section:
    new = '''    const mapDisabled=!mapUrlForModel(m);\n    if(m.soldOut){\n      return `\n      <article class="dev sold-out-card" data-id="${m.id}">\n        <div class="dev-photo sold-out-photo">${cover}<div class="sold-out-overlay"><div class="sold-out-stamp"><small>Desarrollo concluido</small><strong>VENDIDO COMPLETAMENTE</strong></div></div></div>\n        <div class="dev-body">\n          <div class="dev-summary">\n            <div class="dev-heading"><span class="dev-type">${esc(typeLabel)}</span><h3>${esc(m.name)}</h3><p class="dev-zone">${esc(zone)}</p></div>\n            <span class="dev-availability off">100% vendido</span>\n          </div>\n          <div class="sold-out-panel"><span>Historial de ventas</span><strong>VENDIDO COMPLETAMENTE</strong><small>Todos los lotes registrados de este desarrollo ya fueron colocados.</small></div>\n          <div class="dev-actions">\n            <button class="devbtn" onclick="openDevelopment('${m.id}')">Ver desarrollo →</button>\n            <button class="mapbtn" ${mapDisabled?"disabled":""} onclick="${mapDisabled?"":"openMap('"+m.id+"')"}">📍 Ubicación</button>\n          </div>\n        </div>\n      </article>`;\n    }\n    return `'''
    s = s.replace(old, new, 1)

# Keep sold-out cards after developments with live availability.
filter_anchor = '  state.lotsShown=12;\n  renderDevelopments(state.filtered);'
if filter_anchor in s and 'state.filtered.sort((a,b)=>Number(a.soldOut)-Number(b.soldOut));' not in s:
    s = s.replace(
        filter_anchor,
        '  state.filtered.sort((a,b)=>Number(a.soldOut)-Number(b.soldOut));\n\n  state.lotsShown=12;\n  renderDevelopments(state.filtered);',
        1
    )

# Modal language for sold-out developments.
stats_old = '<div class="modal-stat"><small>Lotes disponibles</small><strong>${m.available.length || "Consultar"}</strong></div>'
stats_new = '<div class="modal-stat"><small>Lotes disponibles</small><strong>${m.soldOut?"Vendido":(m.available.length || "Consultar")}</strong></div>'
s = s.replace(stats_old, stats_new, 1)

modal_anchor = '      <div class="modal-stats">'
open_start = s.find('function openDevelopment')
open_end = s.find('function closeModal')
open_section = s[open_start:open_end] if open_start >= 0 and open_end > open_start else ''
if modal_anchor in s and 'modal-sold-out' not in open_section:
    s = s.replace(
        modal_anchor,
        '      ${m.soldOut?`<div class="modal-sold-out"><span>Desarrollo concluido</span><strong>VENDIDO COMPLETAMENTE</strong><p>Todos los lotes registrados de este desarrollo ya fueron colocados.</p></div>`:""}\n      <div class="modal-stats">',
        1
    )

empty_old = '    if(!list.length){wrap.innerHTML=`<div class="state">No hay lotes que coincidan con estos filtros. Prueba ampliar mensualidad, enganche, plazo o superficie.</div>`;return;}'
empty_new = '    if(!list.length){wrap.innerHTML=`<div class="state">${m.soldOut?"VENDIDO COMPLETAMENTE · Todos los lotes registrados de este desarrollo ya fueron colocados.":"No hay lotes que coincidan con estos filtros. Prueba ampliar mensualidad, enganche, plazo o superficie."}</div>`;return;}'
s = s.replace(empty_old, empty_new, 1)

# Fail fast if the important pieces did not land.
required = [
    'CATALOGO_V36_VENDIDOS',
    'id:"vistas-del-rio-vendido"',
    'id:"costa-dorada-elite"',
    'VENDIDO COMPLETAMENTE',
    'state.filtered.sort((a,b)=>Number(a.soldOut)-Number(b.soldOut));'
]
missing = [x for x in required if x not in s]
if missing:
    raise SystemExit('Faltan marcadores: ' + ', '.join(missing))

p.write_text(s, encoding='utf-8')
