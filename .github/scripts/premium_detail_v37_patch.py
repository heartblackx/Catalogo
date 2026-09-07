from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")
marker = "CATALOGO_V37_DETAIL_PREMIUM"

if marker in html:
    print("Premium detail patch already present")
    raise SystemExit(0)

patch = r'''
<!-- CATALOGO_V37_DETAIL_PREMIUM -->
<style id="catalogo-v37-premium-detail">
  .premium-description{
    margin-top:20px;padding:22px 24px;border:1px solid rgba(12,66,82,.10);
    border-radius:24px;background:linear-gradient(145deg,#ffffff,#f7fbfb);
    box-shadow:0 14px 38px rgba(13,49,62,.07)
  }
  .premium-description .premium-eyebrow,.premium-spec-panel .premium-eyebrow,.premium-map-head .premium-eyebrow{
    display:block;margin-bottom:7px;font-size:.68rem;font-weight:900;letter-spacing:.17em;
    text-transform:uppercase;color:#0a7a83
  }
  .premium-description h3,.premium-spec-panel h3,.premium-map-head h3{margin:0;color:#102f3b}
  .premium-description p{margin:10px 0 0;color:#53666d;line-height:1.75}
  .premium-description .amenities{margin-top:16px}

  .premium-location-shell{
    display:grid;grid-template-columns:minmax(0,1.2fr) minmax(330px,.8fr);
    gap:18px;margin-top:20px;align-items:stretch
  }
  .premium-map-panel,.premium-spec-panel{
    overflow:hidden;border:1px solid rgba(12,66,82,.11);border-radius:26px;background:#fff;
    box-shadow:0 18px 45px rgba(11,47,62,.09)
  }
  .premium-map-head{
    display:flex;justify-content:space-between;gap:18px;align-items:center;padding:19px 22px;
    border-bottom:1px solid rgba(12,66,82,.08);background:linear-gradient(135deg,#fbfdfd,#f1f8f8)
  }
  .premium-map-status{
    flex:0 0 auto;padding:7px 11px;border-radius:999px;background:#e6f5f2;color:#08685f;
    font-size:.72rem;font-weight:900;letter-spacing:.03em
  }
  .premium-map-status.pending{background:#f4efe2;color:#80682b}
  .premium-map-frame{min-height:360px;background:linear-gradient(145deg,#eaf1f1,#dce8e9);position:relative}
  .premium-map-frame iframe{display:block;width:100%;height:360px;border:0}
  .premium-map-empty{
    min-height:360px;display:grid;place-items:center;padding:34px;text-align:center;color:#53666d
  }
  .premium-map-empty div{max-width:390px}
  .premium-map-empty b{display:block;margin-bottom:8px;color:#173b48;font-size:1.05rem}
  .premium-map-footer{
    display:flex;gap:16px;align-items:center;justify-content:space-between;padding:17px 20px;background:#fff
  }
  .premium-map-address{min-width:0;color:#52646b;font-size:.86rem;line-height:1.45}
  .premium-map-address strong{display:block;color:#173a46;margin-bottom:2px}
  .premium-map-button{
    flex:0 0 auto;border:0;border-radius:999px;padding:11px 15px;background:#0b5968;color:#fff;
    font-weight:900;cursor:pointer;box-shadow:0 8px 22px rgba(11,89,104,.18)
  }

  .premium-spec-panel{padding:23px}
  .premium-spec-panel h3{font-size:1.22rem;margin-bottom:17px}
  .premium-spec-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .premium-spec{
    min-height:86px;padding:14px;border-radius:17px;background:#f5f9f9;border:1px solid rgba(12,66,82,.07)
  }
  .premium-spec small{display:block;margin-bottom:7px;color:#74848a;font-weight:800;font-size:.72rem}
  .premium-spec strong{display:block;color:#153945;font-size:.96rem;line-height:1.28}
  .premium-spec.wide{grid-column:1/-1;min-height:auto}
  .premium-location-note{
    margin-top:13px;padding:14px 15px;border-radius:16px;background:#102f3b;color:#eaf4f4;
    font-size:.82rem;line-height:1.5
  }
  .premium-location-note small{display:block;color:#9fc1c3;margin-bottom:4px;font-weight:800}

  .premium-gallery-shell{margin-top:25px}
  .premium-section-head{display:flex;align-items:end;justify-content:space-between;gap:14px;margin-bottom:12px}
  .premium-section-head small{display:block;color:#0a7a83;font-weight:900;text-transform:uppercase;letter-spacing:.14em;font-size:.67rem}
  .premium-section-head h3{margin:5px 0 0;color:#123743;font-size:1.18rem}
  .premium-section-head span{color:#718188;font-size:.8rem}
  .premium-gallery-shell .gallery{margin-top:0}

  .premium-lot-separator{height:1px;background:linear-gradient(90deg,transparent,rgba(12,66,82,.16),transparent);margin:26px 0 2px}

  .mobile-quick-nav{display:none}

  @media(max-width:900px){
    .premium-location-shell{grid-template-columns:1fr}
    .premium-map-frame,.premium-map-empty{min-height:315px}
    .premium-map-frame iframe{height:315px}
  }
  @media(max-width:1020px){
    .mobile-quick-nav{
      display:flex;position:sticky;top:70px;z-index:85;gap:7px;overflow-x:auto;padding:8px 14px;
      background:rgba(247,250,249,.96);backdrop-filter:blur(14px);border-bottom:1px solid rgba(12,66,82,.08);
      scrollbar-width:none
    }
    .mobile-quick-nav::-webkit-scrollbar{display:none}
    .mobile-quick-nav a{
      flex:0 0 auto;padding:9px 13px;border-radius:999px;background:#fff;border:1px solid rgba(12,66,82,.10);
      color:#294b55;font-size:.76rem;font-weight:900;box-shadow:0 4px 12px rgba(15,45,58,.04)
    }
    .mobile-quick-nav a.primary{background:#0b5968;color:#fff;border-color:#0b5968}
  }
  @media(max-width:620px){
    .premium-description{padding:18px;border-radius:20px}
    .premium-location-shell{gap:13px}
    .premium-map-panel,.premium-spec-panel{border-radius:20px}
    .premium-map-head{padding:16px;align-items:flex-start}
    .premium-map-frame,.premium-map-empty{min-height:270px}
    .premium-map-frame iframe{height:270px}
    .premium-map-footer{align-items:flex-start;flex-direction:column;padding:15px 16px}
    .premium-map-button{width:100%}
    .premium-spec-panel{padding:18px}
    .premium-spec-grid{gap:8px}
    .premium-spec{padding:12px;min-height:80px}
    .premium-section-head{align-items:flex-start;flex-direction:column}
  }
</style>
<script id="catalogo-v37-premium-detail-script">
(function(){
  function premiumCoords(m){
    const lat=Number(m?.loc?.latitud), lng=Number(m?.loc?.longitud);
    if(Number.isFinite(lat)&&Number.isFinite(lng)&&Math.abs(lat)<=90&&Math.abs(lng)<=180){
      return {lat,lng};
    }
    let url=String(m?.loc?.maps_url||"");
    try{url=decodeURIComponent(url)}catch(_e){}
    const patterns=[
      /@(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)/,
      /[?&](?:query|q)=(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)/i,
      /!3d(-?\d+(?:\.\d+)?).*?!4d(-?\d+(?:\.\d+)?)/
    ];
    for(const pattern of patterns){
      const hit=url.match(pattern);
      if(hit){
        const a=Number(hit[1]), b=Number(hit[2]);
        if(Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a)<=90&&Math.abs(b)<=180) return {lat:a,lng:b};
      }
    }
    return null;
  }

  function premiumEmbedUrl(m){
    const coords=premiumCoords(m);
    if(coords) return `https://www.google.com/maps?q=${coords.lat},${coords.lng}&z=15&output=embed`;
    const storedAddress=String(m?.loc?.direccion||"").trim();
    if(storedAddress) return `https://www.google.com/maps?q=${encodeURIComponent(storedAddress)}&z=15&output=embed`;
    return "";
  }

  window.premiumEmbedUrl=premiumEmbedUrl;

  openDevelopment=function(id){
    const m=state.models.find(x=>x.id===id);
    if(!m) return;
    state.current=m;
    if(typeof lastFocusedElement!=="undefined") lastFocusedElement=document.activeElement;
    developmentFilters={currency:"USD",downPct:0,term:0,monthlyMin:"",monthlyMax:"",terrain:"all",areaMin:"",areaMax:"",search:""};

    const zone=m.zones[0] || m.loc?.zona || "Zona por confirmar";
    const storedAddress=String(m.loc?.direccion||"").trim();
    const address=storedAddress || "Ubicación por confirmar";
    const cover=m.cover || "";
    const typeLabel=m.type==="costa"?"Costa":m.type==="campestre"?"Campestre":"Urbano";
    const amenities=Array.isArray(m.amenities)?m.amenities:[];
    const galleryRows=(Array.isArray(m.media)?m.media:[])
      .filter(x=>x?.public_url && x.public_url!==cover)
      .slice(0,6);
    const gallery=galleryRows.map(x=>`<img src="${esc(x.public_url)}" alt="${esc(m.name)}" loading="lazy" onerror="devImageFallback(this)">`).join("");
    const mapUrl=mapUrlForModel(m);
    const mapEmbed=premiumEmbedUrl(m);
    const minPrice=modelFinancedPrice(m);
    const availability=m.soldOut?"Vendido":(m.available.length?`${m.available.length} disponibles`:"Por confirmar");
    const areaLabel=m.minArea&&m.maxArea
      ? (Number(m.minArea)===Number(m.maxArea)?m2(m.minArea):`${m2(m.minArea)} – ${m2(m.maxArea)}`)
      : (m.minArea?`Desde ${m2(m.minArea)}`:(m.maxArea?`Hasta ${m2(m.maxArea)}`:"Consultar"));
    const downLabel=m.minDownPct?`${money(m.minDownPct)}%`:"Consultar";
    const priceLabel=minPrice?`Desde $${money(minPrice)} USD/m²`:"Consultar";

    document.getElementById("modalBody").innerHTML=`
      <div class="modal-hero">${cover?`<img src="${esc(cover)}" alt="${esc(m.name)}" onerror="devImageFallback(this)">`:`<div class="dev-photo-fallback"><strong>Imagen no disponible</strong></div>`}</div>
      <div class="modal-content">
        <div class="modal-heading">
          <div><small>${esc(typeLabel)}</small><h2 id="developmentTitle">${esc(m.name)}</h2></div>
          <div class="modal-zone">${esc(zone)}</div>
        </div>

        <section class="premium-description">
          <span class="premium-eyebrow">Conoce el desarrollo</span>
          <h3>Información general</h3>
          <p>${esc(m.description||"Información del desarrollo disponible con nuestros asesores.")}</p>
          ${amenities.length?`<div class="amenities">${amenities.map(a=>`<span class="amenity">✓ ${esc(a)}</span>`).join("")}</div>`:""}
        </section>

        ${m.soldOut?`<div class="modal-sold-out"><span>Desarrollo concluido</span><strong>VENDIDO COMPLETAMENTE</strong><p>Todos los lotes registrados de este desarrollo ya fueron colocados.</p></div>`:""}

        <section class="premium-location-shell" aria-label="Ubicación y especificaciones del desarrollo">
          <div class="premium-map-panel">
            <div class="premium-map-head">
              <div><span class="premium-eyebrow">Ubicación real</span><h3>Mapa del desarrollo</h3></div>
              <span class="premium-map-status ${mapEmbed?"":"pending"}">${mapEmbed?"Mapa disponible":"Por confirmar"}</span>
            </div>
            ${mapEmbed
              ? `<div class="premium-map-frame"><iframe src="${esc(mapEmbed)}" title="Mapa de ${esc(m.name)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>`
              : `<div class="premium-map-empty"><div><b>Ubicación pendiente de coordenadas</b><span>No mostramos un mapa aproximado para evitar señalar un punto incorrecto.</span></div></div>`}
            <div class="premium-map-footer">
              <div class="premium-map-address"><strong>${esc(zone)}</strong><span>${esc(address)}</span></div>
              ${mapUrl?`<button class="premium-map-button" type="button" onclick="openMap('${m.id}')">Abrir en Google Maps ↗</button>`:""}
            </div>
          </div>

          <aside class="premium-spec-panel">
            <span class="premium-eyebrow">Especificaciones</span>
            <h3>Datos clave del terreno</h3>
            <div class="premium-spec-grid">
              <div class="premium-spec"><small>Tipo</small><strong>${esc(typeLabel)}</strong></div>
              <div class="premium-spec"><small>Zona</small><strong>${esc(zone)}</strong></div>
              <div class="premium-spec"><small>Disponibilidad</small><strong>${esc(availability)}</strong></div>
              <div class="premium-spec"><small>Superficie</small><strong>${esc(areaLabel)}</strong></div>
              <div class="premium-spec"><small>Precio por m²</small><strong>${esc(priceLabel)}</strong></div>
              <div class="premium-spec"><small>Enganche desde</small><strong>${esc(downLabel)}</strong></div>
            </div>
            <div class="premium-location-note"><small>Ubicación</small>${esc(storedAddress||zone)}</div>
          </aside>
        </section>

        ${gallery?`<section class="premium-gallery-shell"><div class="premium-section-head"><div><small>Galería</small><h3>Fotografías del desarrollo</h3></div><span>${galleryRows.length} ${galleryRows.length===1?"imagen":"imágenes"}</span></div><div class="gallery">${gallery}</div></section>`:""}

        <div class="premium-lot-separator"></div>
        <div id="developmentFilters" class="development-filters"></div>
        <div class="modal-lots-head"><h3>Lotes disponibles</h3><span id="developmentLotCount">${m.available.length?`${m.available.length} disponibles`:"Disponibilidad por confirmar"}</span></div>
        <div class="modal-lots" id="developmentLots"></div>
      </div>`;

    renderDevelopmentToolbar();
    renderDevelopmentLots();
    const modal=document.getElementById("devModal");
    modal.classList.add("open");
    modal.setAttribute("aria-hidden","false");
    document.body.style.overflow="hidden";
    document.getElementById("modalCard")?.focus();
    history.replaceState(null,"",`#${m.id}`);
  };

  function installMobileQuickNav(){
    if(document.getElementById("mobileQuickNav")) return;
    const header=document.querySelector(".navwrap");
    if(!header) return;
    const nav=document.createElement("nav");
    nav.id="mobileQuickNav";
    nav.className="mobile-quick-nav";
    nav.setAttribute("aria-label","Accesos rápidos");
    nav.innerHTML='<a href="#desarrollos">Desarrollos</a><a href="#lotes">Lotes</a><a href="#cotiza">Cotizar</a><a class="primary" href="#asesores">Asesor</a>';
    header.insertAdjacentElement("afterend",nav);
  }

  installMobileQuickNav();
})();
</script>
<!-- /CATALOGO_V37_DETAIL_PREMIUM -->
'''

if "</body>" not in html:
    raise SystemExit("Could not find </body> in index.html")

html = html.replace("</body>", patch + "\n</body>", 1)
path.write_text(html, encoding="utf-8")
print("Applied CATALOGO_V37_DETAIL_PREMIUM")
