from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='CATALOGO_V39_OFFICIAL_LOT_SVG'
if marker in s:
    print('V39 official lot SVG already installed')
    raise SystemExit(0)

block=r'''

<!-- CATALOGO_V39_OFFICIAL_LOT_SVG -->
<style id="catalogo-v39-official-lot-svg-style">
  .quote-official-plan-stage{
    position:relative;height:500px;overflow:hidden;background:#e9efef;border-top:1px solid rgba(14,61,74,.07);
    border-bottom:1px solid rgba(14,61,74,.07)
  }
  .quote-official-plan-stage svg{display:block;width:100%;height:100%;background:#f2f5f5}
  .quote-official-plan-stage .quote-svg-other-lot{opacity:.30!important;transition:opacity .2s ease}
  .quote-official-plan-stage .quote-svg-target{
    opacity:1!important;fill:#ffd538!important;stroke:#d8232a!important;stroke-width:10px!important;
    vector-effect:non-scaling-stroke;filter:drop-shadow(0 0 5px #fff) drop-shadow(0 0 9px #ffd538) drop-shadow(0 3px 5px rgba(0,0,0,.40));
    animation:quoteSvgTargetPulse 1.55s ease-in-out infinite
  }
  .quote-official-plan-stage .quote-svg-pin-ring{
    fill:none;stroke:#d8232a;stroke-width:8;vector-effect:non-scaling-stroke;pointer-events:none;
    filter:drop-shadow(0 0 4px #fff);animation:quoteSvgRingPulse 1.55s ease-out infinite
  }
  .quote-official-plan-label{
    position:absolute;left:14px;bottom:14px;z-index:8;max-width:calc(100% - 28px);padding:10px 14px;
    border-radius:14px;background:rgba(10,40,50,.94);color:#fff;box-shadow:0 8px 25px rgba(0,0,0,.26)
  }
  .quote-official-plan-label small{display:block;color:#a9d0d1;font-size:.65rem;font-weight:900;margin-bottom:3px;text-transform:uppercase;letter-spacing:.08em}
  .quote-official-plan-label strong{display:block;font-size:.94rem}
  .quote-plan-tools{
    display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:12px 16px;background:#fff;border-top:1px solid rgba(14,61,74,.06)
  }
  .quote-plan-tools button,.quote-plan-tools a{
    appearance:none;border:1px solid rgba(11,89,104,.15);border-radius:999px;padding:9px 13px;background:#f6f9f9;
    color:#284b55;font-size:.75rem;font-weight:900;cursor:pointer;text-decoration:none
  }
  .quote-plan-tools button.active{background:#0b5968;color:#fff;border-color:#0b5968}
  .quote-plan-tools .quote-plan-source{margin-left:auto;color:#75868b;font-size:.70rem;font-weight:800}
  .quote-plan-loading{padding:25px 20px;text-align:center;color:#61747a;background:#fff}
  .quote-plan-loading strong{display:block;color:#173b46;margin-bottom:5px}
  @keyframes quoteSvgTargetPulse{0%,100%{filter:drop-shadow(0 0 4px #fff) drop-shadow(0 0 7px #ffd538) drop-shadow(0 3px 5px rgba(0,0,0,.35))}50%{filter:drop-shadow(0 0 6px #fff) drop-shadow(0 0 15px #ffbd18) drop-shadow(0 4px 7px rgba(0,0,0,.45))}}
  @keyframes quoteSvgRingPulse{0%{opacity:.95;stroke-width:9}100%{opacity:.18;stroke-width:22}}
  @media(max-width:680px){
    .quote-official-plan-stage{height:360px}
    .quote-official-plan-label{left:9px;bottom:9px;max-width:calc(100% - 18px);padding:9px 11px}
    .quote-plan-tools{padding:10px 12px}
    .quote-plan-tools button,.quote-plan-tools a{flex:1 1 auto;text-align:center}
    .quote-plan-tools .quote-plan-source{width:100%;margin-left:0;text-align:center}
  }
</style>
<script id="catalogo-v39-official-lot-svg-script">
(function(){
  const PLAN_ENDPOINT="https://cisiancuphdkybkddwmq.supabase.co/functions/v1/vive-plano-publico";
  const previousRender=window.renderQuoteModal;
  if(typeof previousRender!=="function")return;
  const svgCache=new Map();
  let hydrateToken=0;

  function token(v){
    const s=String(v??"").trim();
    if(/^0*\d+$/.test(s))return String(Number(s));
    return s.replace(/\s+/g,"").toUpperCase();
  }
  function targetSuffix(lot){return `M${token(lot?.manzana)}-L${token(lot?.lote)}`.toUpperCase()}
  function escAttr(s=""){return String(s).replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[m]))}
  function unique(arr){return [...new Set(arr.filter(Boolean).map(x=>String(x).trim()).filter(Boolean))]}

  async function fetchOfficialSvg(model){
    const names=unique([model?.name,...(model?.members||[])]);
    let lastErr=null;
    for(const name of names){
      const key=name.toLowerCase();
      if(svgCache.has(key))return {text:svgCache.get(key),source:name};
      try{
        const r=await fetch(`${PLAN_ENDPOINT}?dev=${encodeURIComponent(name)}`,{headers:{Accept:"image/svg+xml"}});
        if(!r.ok){lastErr=new Error(`Plano ${r.status}`);continue}
        const text=await r.text();
        if(!/^\s*<svg\b/i.test(text)){lastErr=new Error("Plano inválido");continue}
        svgCache.set(key,text);
        return {text,source:r.headers.get("X-Vive-Plan-Source")||name};
      }catch(err){lastErr=err}
    }
    throw lastErr||new Error("Plano no disponible");
  }

  function cleanSvg(doc){
    doc.querySelectorAll("script,foreignObject").forEach(n=>n.remove());
    doc.querySelectorAll("*").forEach(el=>{
      [...el.attributes].forEach(a=>{if(/^on/i.test(a.name))el.removeAttribute(a.name)});
    });
    const svg=doc.documentElement;
    svg.removeAttribute("width");svg.removeAttribute("height");
    svg.setAttribute("preserveAspectRatio","xMidYMid meet");
    svg.setAttribute("role","img");
    return svg;
  }

  function exactElement(svg,lot){
    const suffix=targetSuffix(lot);
    return [...svg.querySelectorAll("[id]")].find(el=>String(el.id||"").trim().toUpperCase().endsWith(suffix))||null;
  }

  function viewBoxOf(svg){
    const raw=(svg.getAttribute("viewBox")||"").trim().split(/[ ,]+/).map(Number);
    if(raw.length===4&&raw.every(Number.isFinite))return {x:raw[0],y:raw[1],w:raw[2],h:raw[3],raw:raw.join(" ")};
    return null;
  }

  function clamp(v,min,max){return Math.max(min,Math.min(max,v))}
  function zoomBox(original,b){
    if(!original||!b)return original?.raw||"";
    const w=Math.min(original.w,Math.max(b.width*10,original.w*.19));
    const h=Math.min(original.h,Math.max(b.height*12,original.h*.22));
    const cx=b.x+b.width/2,cy=b.y+b.height/2;
    const x=clamp(cx-w/2,original.x,original.x+original.w-w);
    const y=clamp(cy-h/2,original.y,original.y+original.h-h);
    return `${x} ${y} ${w} ${h}`;
  }

  function addRing(svg,target,b){
    if(!b||!svg)return;
    const ns="http://www.w3.org/2000/svg";
    const ring=document.createElementNS(ns,"ellipse");
    ring.setAttribute("class","quote-svg-pin-ring");
    ring.setAttribute("cx",String(b.x+b.width/2));
    ring.setAttribute("cy",String(b.y+b.height/2));
    ring.setAttribute("rx",String(Math.max(b.width*.85,25)));
    ring.setAttribute("ry",String(Math.max(b.height*.85,25)));
    target.parentNode?.appendChild(ring);
  }

  function installTools(section,svg,original,local,model,lot,source){
    const tools=document.createElement("div");tools.className="quote-plan-tools";
    const localBtn=document.createElement("button");localBtn.type="button";localBtn.className="active";localBtn.textContent="Ver lote resaltado";
    const fullBtn=document.createElement("button");fullBtn.type="button";fullBtn.textContent="Ver plano completo";
    const external=document.createElement("a");external.href="https://gcmaps.grupoconcordia.info/";external.target="_blank";external.rel="noopener noreferrer";external.textContent="Plano interactivo ↗";
    const src=document.createElement("span");src.className="quote-plan-source";src.textContent=`Plano: ${source}`;
    localBtn.onclick=()=>{svg.setAttribute("viewBox",local);localBtn.classList.add("active");fullBtn.classList.remove("active")};
    fullBtn.onclick=()=>{svg.setAttribute("viewBox",original.raw);fullBtn.classList.add("active");localBtn.classList.remove("active")};
    tools.append(localBtn,fullBtn,external,src);section.appendChild(tools);
  }

  async function hydrateOfficialPlan(){
    const myToken=++hydrateToken;
    if(typeof selectedQuote==="undefined"||!selectedQuote)return;
    const {model,lot}=selectedQuote;
    const section=document.querySelector("#quoteContent .quote-lot-location");
    if(!section)return;
    const pending=section.querySelector(".quote-plan-pending");
    if(pending)pending.innerHTML='<div class="quote-plan-loading" style="grid-column:1/-1"><strong>Cargando plano del desarrollo…</strong><span>Localizando el lote seleccionado.</span></div>';
    try{
      const result=await fetchOfficialSvg(model);
      if(myToken!==hydrateToken||typeof selectedQuote==="undefined"||selectedQuote?.lot?.id!==lot?.id)return;
      const doc=new DOMParser().parseFromString(result.text,"image/svg+xml");
      if(!doc||doc.querySelector("parsererror"))throw new Error("No se pudo leer el plano");
      const svg=cleanSvg(doc);
      const target=exactElement(svg,lot);
      if(!target)throw new Error("Lote no identificado en el plano");
      target.classList.add("quote-svg-target");
      svg.querySelectorAll('[id*="-L"],[id*="-l"]').forEach(el=>{if(el!==target)el.classList.add("quote-svg-other-lot")});

      const original=viewBoxOf(svg);
      section.classList.remove("pending");
      section.innerHTML=`<div class="quote-lot-location-head"><div><small>Ubicación dentro del desarrollo</small><h3>Terreno localizado en el plano real</h3></div><span class="quote-lot-location-id">Mz ${escAttr(lot.manzana||"—")} · Lote ${escAttr(lot.lote||"—")}</span></div>`;
      const stage=document.createElement("div");stage.className="quote-official-plan-stage";
      stage.appendChild(svg);section.appendChild(stage);
      svg.setAttribute("aria-label",`Plano de ${model.name}, manzana ${lot.manzana}, lote ${lot.lote} resaltado`);

      await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
      let b=null;try{b=target.getBBox()}catch(_e){}
      const local=zoomBox(original,b);
      if(local)svg.setAttribute("viewBox",local);
      addRing(svg,target,b);
      const label=document.createElement("div");label.className="quote-official-plan-label";
      label.innerHTML=`<small>Este es el terreno cotizado</small><strong>Mz ${escAttr(lot.manzana||"—")} · Lote ${escAttr(lot.lote||"—")}</strong>`;
      stage.appendChild(label);
      if(original&&local)installTools(section,svg,original,local,model,lot,result.source);
      const cap=document.createElement("div");cap.className="quote-plan-caption";
      cap.innerHTML='<div><strong>Lote resaltado directamente sobre el plano del desarrollo</strong><span>Puedes ampliar la zona del lote o consultar el plano completo para identificar calles y ubicación dentro del desarrollo.</span></div>';
      section.appendChild(cap);
    }catch(err){
      if(myToken!==hydrateToken)return;
      const pendingNow=section.querySelector(".quote-plan-pending");
      if(pendingNow)pendingNow.innerHTML=`<div class="quote-plan-pending-icon">⌖</div><div class="quote-plan-pending-copy"><strong>Ubicación en plano no disponible para este lote</strong><span>Para evitar confusiones no mostramos una posición aproximada.</span></div><button class="quote-plan-official" type="button" onclick="window.open('https://gcmaps.grupoconcordia.info/','_blank','noopener')">Abrir plano interactivo</button>`;
    }
  }

  window.renderQuoteModal=function(preserve=false){previousRender(preserve);hydrateOfficialPlan()};
})();
</script>
<!-- /CATALOGO_V39_OFFICIAL_LOT_SVG -->
'''

if '</body>' not in s: raise SystemExit('No </body> found')
s=s.replace('</body>',block+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Installed CATALOGO_V39_OFFICIAL_LOT_SVG')
