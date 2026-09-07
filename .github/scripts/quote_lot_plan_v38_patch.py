from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = 'CATALOGO_V38_QUOTE_LOT_PLAN'
if marker in text:
    print('V38 quote lot plan already installed')
    raise SystemExit(0)

# Make source detail available to the frontend so verified future plan metadata can travel with the lot.
old_select = 'select=id,desarrollo,desarrollo_id,manzana,lote,superficie_m2,disponible,estatus,es_esquina,tiene_talud,lados_talud,entrega_status,descripcion_lote,foto_lote_public_url,urlfoto,foto_lote_url&order=desarrollo.asc,manzana.asc,lote.asc'
new_select = 'select=id,desarrollo,desarrollo_id,manzana,lote,superficie_m2,disponible,estatus,es_esquina,tiene_talud,lados_talud,entrega_status,descripcion_lote,foto_lote_public_url,urlfoto,foto_lote_url,detalle_fuente&order=desarrollo.asc,manzana.asc,lote.asc'
if old_select in text:
    text = text.replace(old_select, new_select, 1)

block = r'''

<!-- CATALOGO_V38_QUOTE_LOT_PLAN -->
<script src="./assets/lot-plans/lot-plan-data.js"></script>
<style id="catalogo-v38-quote-lot-plan-style">
  /* El mapa de Google deja de ser protagonista en la ficha de desarrollo. */
  .premium-location-shell{grid-template-columns:1fr!important}
  .premium-location-shell>.premium-map-panel{display:none!important}

  .quote-lot-location{
    margin:18px 0 22px;border:1px solid rgba(10,74,91,.12);border-radius:24px;
    overflow:hidden;background:#fff;box-shadow:0 15px 38px rgba(13,48,60,.08)
  }
  .quote-lot-location-head{
    display:flex;align-items:flex-start;justify-content:space-between;gap:16px;padding:19px 21px;
    background:linear-gradient(135deg,#f5fbfa,#edf6f6);border-bottom:1px solid rgba(10,74,91,.08)
  }
  .quote-lot-location-head small{
    display:block;margin-bottom:5px;color:#087781;font-size:.67rem;font-weight:950;
    letter-spacing:.14em;text-transform:uppercase
  }
  .quote-lot-location-head h3{margin:0;color:#123944;font-size:1.08rem;line-height:1.25}
  .quote-lot-location-id{
    flex:0 0 auto;padding:8px 11px;border-radius:999px;background:#103d49;color:#fff;
    font-size:.73rem;font-weight:950;white-space:nowrap
  }
  .quote-plan-stage{position:relative;background:#e9eeee;isolation:isolate}
  .quote-plan-stage>img{display:block;width:100%;height:auto;max-height:520px;object-fit:contain;background:#f5f7f7}
  .quote-plan-dim{position:absolute;inset:0;background:rgba(9,27,35,.17);pointer-events:none;z-index:2}
  .quote-plan-highlight{
    position:absolute;z-index:4;border:4px solid #ffc928;background:rgba(255,201,40,.27);
    box-shadow:0 0 0 3px rgba(255,255,255,.92),0 0 0 7px rgba(255,201,40,.50),0 12px 28px rgba(0,0,0,.25);
    border-radius:6px;pointer-events:none;animation:quoteLotPulse 1.9s ease-in-out infinite
  }
  .quote-plan-highlight::after{
    content:"LOTE COTIZADO";position:absolute;left:50%;bottom:calc(100% + 9px);transform:translateX(-50%);
    padding:7px 10px;border-radius:999px;background:#102f3b;color:#fff;white-space:nowrap;
    font-size:.66rem;font-weight:950;letter-spacing:.06em;box-shadow:0 6px 18px rgba(0,0,0,.20)
  }
  .quote-plan-polygon{position:absolute;inset:0;width:100%;height:100%;z-index:4;pointer-events:none;overflow:visible}
  .quote-plan-polygon polygon{
    fill:rgba(255,201,40,.34);stroke:#ffc928;stroke-width:1.1;vector-effect:non-scaling-stroke;
    filter:drop-shadow(0 0 2px #fff) drop-shadow(0 3px 4px rgba(0,0,0,.35));
    animation:quoteLotPolyPulse 1.9s ease-in-out infinite
  }
  .quote-plan-badge{
    position:absolute;z-index:6;left:14px;bottom:14px;padding:10px 13px;border-radius:14px;
    background:rgba(9,37,47,.94);color:#fff;box-shadow:0 8px 24px rgba(0,0,0,.25)
  }
  .quote-plan-badge small{display:block;color:#a9cdd0;font-size:.66rem;font-weight:850;margin-bottom:2px}
  .quote-plan-badge strong{display:block;font-size:.91rem}
  .quote-plan-caption{
    display:flex;gap:14px;align-items:center;justify-content:space-between;padding:15px 18px;
    background:#fff;color:#56676d;font-size:.82rem;line-height:1.45
  }
  .quote-plan-caption strong{color:#183b46}
  .quote-plan-caption span{display:block}

  .quote-lot-location.pending .quote-plan-pending{
    padding:24px 21px;display:grid;grid-template-columns:auto 1fr auto;gap:15px;align-items:center;background:#fff
  }
  .quote-plan-pending-icon{
    width:48px;height:48px;border-radius:16px;display:grid;place-items:center;background:#eef6f5;
    color:#0b6470;font-size:1.2rem;font-weight:950
  }
  .quote-plan-pending-copy strong{display:block;color:#173b46;margin-bottom:4px}
  .quote-plan-pending-copy span{display:block;color:#687980;font-size:.81rem;line-height:1.45}
  .quote-plan-official{
    border:0;border-radius:999px;padding:11px 15px;background:#0b5968;color:#fff;font-weight:900;
    cursor:pointer;white-space:nowrap
  }
  @keyframes quoteLotPulse{0%,100%{filter:brightness(1);transform:scale(1)}50%{filter:brightness(1.13);transform:scale(1.025)}}
  @keyframes quoteLotPolyPulse{0%,100%{opacity:1}50%{opacity:.68}}

  @media(max-width:680px){
    .quote-lot-location{border-radius:19px}
    .quote-lot-location-head{padding:16px;flex-direction:column;gap:10px}
    .quote-lot-location-id{align-self:flex-start}
    .quote-plan-badge{left:10px;bottom:10px}
    .quote-plan-caption{align-items:flex-start;flex-direction:column;gap:6px;padding:13px 15px}
    .quote-lot-location.pending .quote-plan-pending{grid-template-columns:auto 1fr;padding:18px 16px}
    .quote-plan-official{grid-column:1/-1;width:100%}
  }
</style>
<script id="catalogo-v38-quote-lot-plan-script">
(function(){
  const originalRenderQuoteModal=window.renderQuoteModal;
  if(typeof originalRenderQuoteModal!=="function") return;

  function norm(v=""){
    return String(v||"").normalize("NFD").replace(/[\u0300-\u036f]/g,"")
      .toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"");
  }
  function finite(v){const n=Number(v);return Number.isFinite(n)?n:null}
  function lotKey(lot){return `${String(lot?.manzana||"").trim()}|${String(lot?.lote||"").trim()}`}

  function embeddedLotPlan(lot){
    const d=lot?.detalle_fuente;
    if(!d || typeof d!=="object") return null;
    const p=d.plan || d.plano || d.lot_plan || d.ubicacion_plano;
    if(!p || typeof p!=="object") return null;
    const image=String(p.image||p.public_url||p.url||"").trim();
    if(!image)return null;
    if(Array.isArray(p.polygon)&&p.polygon.length>=3){return {image,polygon:p.polygon,source:p.source||"Plano del desarrollo"}}
    const x=finite(p.x),y=finite(p.y),w=finite(p.w),h=finite(p.h);
    if([x,y,w,h].every(v=>v!==null)) return {image,x,y,w,h,source:p.source||"Plano del desarrollo"};
    return null;
  }

  function configuredLotPlan(model,lot){
    const root=window.CATALOG_LOT_PLAN_DATA||{};
    const devs=root.developments||{};
    const candidates=[model?.id,model?.name,...(model?.members||[])].filter(Boolean).map(norm);
    let entry=null;
    for(const key of candidates){
      entry=devs[key]||Object.entries(devs).find(([k])=>norm(k)===key)?.[1];
      if(entry)break;
    }
    if(!entry||!entry.image)return null;
    const exact=entry.lots?.[lotKey(lot)] || entry.lots?.[`${String(lot?.manzana||"").trim()}-${String(lot?.lote||"").trim()}`];
    if(!exact)return null;
    if(Array.isArray(exact.polygon)&&exact.polygon.length>=3){
      return {image:entry.image,polygon:exact.polygon,source:entry.source||"Plano del desarrollo"};
    }
    const x=finite(exact.x),y=finite(exact.y),w=finite(exact.w),h=finite(exact.h);
    if([x,y,w,h].every(v=>v!==null))return {image:entry.image,x,y,w,h,source:entry.source||"Plano del desarrollo"};
    return null;
  }

  function resolveLotPlan(model,lot){return embeddedLotPlan(lot)||configuredLotPlan(model,lot)}

  function safePct(v){const n=Math.max(0,Math.min(100,Number(v)));return Number.isFinite(n)?n:0}
  function polygonPoints(points){
    return points.map(p=>Array.isArray(p)&&p.length>=2?`${safePct(p[0])},${safePct(p[1])}`:null).filter(Boolean).join(" ");
  }

  function planHtml(model,lot){
    const plan=resolveLotPlan(model,lot);
    const mz=esc(lot?.manzana||"—"), lote=esc(lot?.lote||"—");
    const identity=`Mz ${mz} · Lote ${lote}`;
    if(plan){
      let highlight="";
      if(plan.polygon){
        const pts=polygonPoints(plan.polygon);
        if(pts) highlight=`<svg class="quote-plan-polygon" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><polygon points="${pts}"></polygon></svg>`;
      }else{
        highlight=`<div class="quote-plan-highlight" aria-hidden="true" style="left:${safePct(plan.x)}%;top:${safePct(plan.y)}%;width:${safePct(plan.w)}%;height:${safePct(plan.h)}%"></div>`;
      }
      return `<section class="quote-lot-location" aria-label="Ubicación del lote dentro del desarrollo">
        <div class="quote-lot-location-head"><div><small>Ubicación dentro del desarrollo</small><h3>Identifica exactamente el terreno que estás cotizando</h3></div><span class="quote-lot-location-id">${identity}</span></div>
        <div class="quote-plan-stage">
          <img src="${esc(plan.image)}" alt="Plano de ${esc(model.name)} con el lote ${lote} resaltado" loading="lazy">
          <div class="quote-plan-dim"></div>${highlight}
          <div class="quote-plan-badge"><small>Este es el terreno cotizado</small><strong>${identity}</strong></div>
        </div>
        <div class="quote-plan-caption"><div><strong>Lote resaltado en el plano</strong><span>La marca corresponde a la manzana y lote seleccionados en esta cotización.</span></div><span>${esc(plan.source||"Plano del desarrollo")}</span></div>
      </section>`;
    }

    const official=String(window.CATALOG_LOT_PLAN_DATA?.officialInteractiveUrl||"").trim();
    return `<section class="quote-lot-location pending" aria-label="Ubicación del lote dentro del desarrollo">
      <div class="quote-lot-location-head"><div><small>Ubicación dentro del desarrollo</small><h3>${identity}</h3></div><span class="quote-lot-location-id">${identity}</span></div>
      <div class="quote-plan-pending">
        <div class="quote-plan-pending-icon">⌖</div>
        <div class="quote-plan-pending-copy"><strong>Plano exacto pendiente de vincular</strong><span>No colocamos un marcador aproximado: el lote solo se resaltará cuando su posición dentro del plano esté verificada.</span></div>
        ${official?`<button class="quote-plan-official" type="button" onclick="window.open('${esc(official)}','_blank','noopener')">Abrir plano interactivo</button>`:""}
      </div>
    </section>`;
  }

  function injectLotPlan(){
    if(!window.selectedQuote)return;
    const {model,lot}=window.selectedQuote;
    const body=document.querySelector("#quoteContent .quote-body");
    if(!body||body.querySelector(".quote-lot-location"))return;
    const summary=body.querySelector(".quote-summary");
    if(!summary)return;
    summary.insertAdjacentHTML("afterend",planHtml(model,lot));
  }

  window.renderQuoteModal=function(preserve=false){
    originalRenderQuoteModal(preserve);
    injectLotPlan();
  };
})();
</script>
<!-- /CATALOGO_V38_QUOTE_LOT_PLAN -->
'''

if '</body>' not in text:
    raise SystemExit('No </body> found')
text = text.replace('</body>', block + '\n</body>', 1)
path.write_text(text, encoding='utf-8')
print('Installed CATALOGO_V38_QUOTE_LOT_PLAN')
