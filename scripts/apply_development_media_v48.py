from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Supabase is canonical for development media when active rows exist.
old = 'const media=localMedia.length ? localMedia : (syncedMedia.length ? syncedMedia : siteMedia);'
new = 'const media=syncedMedia.length ? syncedMedia : (localMedia.length ? localMedia : siteMedia);'
if old in s:
    s = s.replace(old, new, 1)

# Show all active development images in the development detail/gallery.
s = s.replace('const gallery=m.media.slice(0,5).map', 'const gallery=(Array.isArray(m.media)?m.media:[]).map')
s = s.replace('.filter(x=>x?.public_url && x.public_url!==cover)\n      .slice(0,6);', '.filter(x=>x?.public_url && x.public_url!==cover);')

# Development photos are ONLY for development cards/cover/gallery.
new_get_lot_photo = '''function getLotPhoto(lot,model){
  const direct=lot.foto_lote_public_url || lot.foto_lote_url || lot.urlfoto;
  if(direct) return {url:direct,type:"lote"};
  const lm=(Array.isArray(model?.lotMedia)?model.lotMedia:[]).find(x=>canon(x.manzana)===canon(lot.manzana)&&canon(x.lote)===canon(lot.lote)&&x.public_url);
  if(lm?.public_url) return {url:lm.public_url,type:"lote"};
  // Las imágenes del desarrollo quedan separadas de lotes, precotización y cotización.
  return {url:"",type:"none"};
}'''
pattern = r'function getLotPhoto\(lot,model\)\{.*?\n\}\n(?=function )'
s2, n = re.subn(pattern, new_get_lot_photo + '\n', s, count=1, flags=re.S)
if n != 1:
    raise RuntimeError('No se pudo reemplazar getLotPhoto de forma segura')
s = s2

# Remove previous development-image override blocks to avoid conflicting rules.
for name in [
    'CATALOGO_V48_DEVELOPMENT_MEDIA_CONTAIN',
    'CATALOGO_V49_NO_CROP_DEVELOPMENT_IMAGES',
    'CATALOGO_V50_ADAPTIVE_DEVELOPMENT_IMAGES'
]:
    s = re.sub(
        rf'\n?<!-- {name} -->.*?<!-- /{name} -->\n?',
        '\n',
        s,
        flags=re.S
    )

patch = r'''
<!-- CATALOGO_V50_ADAPTIVE_DEVELOPMENT_IMAGES -->
<style id="catalogo-v50-adaptive-development-images-style">
  /* ============================================================
     PORTADAS DE DESARROLLO
     Regla principal: la fotografía SIEMPRE se muestra completa.
     El contenedor crece cuando la proporción de la foto lo necesita.
     ============================================================ */
  #devGrid .dev-photo{
    position:relative!important;
    width:100%!important;
    height:auto!important;
    min-height:300px!important;
    max-height:none!important;
    display:flex!important;
    align-items:center!important;
    justify-content:center!important;
    overflow:hidden!important;
    padding:0!important;
    background:linear-gradient(145deg,#edf3f2,#e3eceb)!important;
  }

  #devGrid .dev-photo>img{
    display:block!important;
    width:100%!important;
    height:auto!important;
    min-height:0!important;
    max-height:520px!important;
    object-fit:contain!important;
    object-position:center center!important;
    transform:none!important;
    scale:none!important;
    clip-path:none!important;
    margin:0 auto!important;
    padding:0!important;
    border-radius:0!important;
    background:#e8efee!important;
  }

  /* La imagen decide el alto visual. Estas clases solo agregan aire
     cuando una foto tiene proporciones menos panorámicas. */
  #devGrid .dev-photo.media-wide{min-height:300px!important}
  #devGrid .dev-photo.media-standard{min-height:350px!important}
  #devGrid .dev-photo.media-tall{min-height:430px!important}

  /* ============================================================
     PORTADA INTERNA DEL DESARROLLO
     Grande, completa y sin recortar.
     ============================================================ */
  #devModal .modal-hero,
  #devModal .premium-hero-media{
    position:relative!important;
    width:100%!important;
    height:auto!important;
    min-height:420px!important;
    max-height:none!important;
    display:flex!important;
    align-items:center!important;
    justify-content:center!important;
    overflow:hidden!important;
    padding:0!important;
    background:linear-gradient(145deg,#edf3f2,#dfe9e8)!important;
  }

  #devModal .modal-hero>img,
  #devModal .premium-hero-media>img{
    display:block!important;
    width:100%!important;
    height:auto!important;
    min-height:0!important;
    max-height:680px!important;
    object-fit:contain!important;
    object-position:center center!important;
    transform:none!important;
    scale:none!important;
    clip-path:none!important;
    margin:0 auto!important;
    padding:0!important;
    border-radius:0!important;
    background:#e7eeee!important;
  }

  /* ============================================================
     GALERÍA DEL DESARROLLO
     Todas las imágenes completas y respetando su proporción real.
     ============================================================ */
  #devModal .premium-gallery-shell .gallery,
  #devModal .gallery{
    display:grid!important;
    grid-template-columns:repeat(auto-fit,minmax(300px,1fr))!important;
    grid-auto-rows:auto!important;
    gap:16px!important;
    align-items:start!important;
  }

  #devModal .premium-gallery-shell .gallery img,
  #devModal .gallery img{
    display:block!important;
    width:100%!important;
    height:auto!important;
    min-height:0!important;
    max-height:520px!important;
    aspect-ratio:auto!important;
    object-fit:contain!important;
    object-position:center center!important;
    transform:none!important;
    scale:none!important;
    clip-path:none!important;
    margin:0 auto!important;
    padding:0!important;
    border-radius:16px!important;
    background:#e9efee!important;
    border:1px solid rgba(16,58,69,.08)!important;
  }
  #devModal .gallery img:first-child{grid-row:auto!important}

  /* Anular cualquier ajuste histórico por URL/hash o reglas anteriores. */
  #devGrid .dev-photo img,
  #devModal .modal-hero img,
  #devModal .premium-hero-media img,
  #devModal .gallery img{
    transform:none!important;
    transform-origin:center center!important;
    object-position:center center!important;
  }

  @media(min-width:1200px){
    #devGrid .dev-photo.media-standard{min-height:380px!important}
    #devGrid .dev-photo.media-tall{min-height:460px!important}
  }

  @media(max-width:900px){
    #devGrid .dev-photo{min-height:270px!important}
    #devGrid .dev-photo.media-standard{min-height:300px!important}
    #devGrid .dev-photo.media-tall{min-height:360px!important}
    #devModal .modal-hero,
    #devModal .premium-hero-media{min-height:320px!important}
  }

  @media(max-width:680px){
    #devGrid .dev-photo,
    #devGrid .dev-photo.media-wide,
    #devGrid .dev-photo.media-standard,
    #devGrid .dev-photo.media-tall{
      min-height:220px!important;
    }
    #devGrid .dev-photo>img{max-height:420px!important}
    #devModal .modal-hero,
    #devModal .premium-hero-media{min-height:260px!important}
    #devModal .modal-hero>img,
    #devModal .premium-hero-media>img{max-height:520px!important}
    #devModal .premium-gallery-shell .gallery,
    #devModal .gallery{grid-template-columns:1fr!important}
    #devModal .premium-gallery-shell .gallery img,
    #devModal .gallery img{max-height:460px!important}
  }
</style>
<script id="catalogo-v50-adaptive-development-images-script">
(function(){
  function classify(img){
    const box=img.closest('.dev-photo');
    if(!box || !img.naturalWidth || !img.naturalHeight)return;
    const ratio=img.naturalWidth/img.naturalHeight;
    box.classList.remove('media-wide','media-standard','media-tall');
    if(ratio>=1.7)box.classList.add('media-wide');
    else if(ratio>=1.15)box.classList.add('media-standard');
    else box.classList.add('media-tall');
  }

  function scan(scope=document){
    scope.querySelectorAll('#devGrid .dev-photo>img').forEach(img=>{
      if(img.complete)classify(img);
      if(img.dataset.v50RatioBound==='1')return;
      img.dataset.v50RatioBound='1';
      img.addEventListener('load',()=>classify(img),{passive:true});
    });
  }

  const observer=new MutationObserver(()=>scan(document));
  observer.observe(document.documentElement,{childList:true,subtree:true});
  document.addEventListener('DOMContentLoaded',()=>scan(document));
  window.addEventListener('load',()=>scan(document));
  setTimeout(()=>scan(document),500);
})();
</script>
<!-- /CATALOGO_V50_ADAPTIVE_DEVELOPMENT_IMAGES -->
'''

s = s.replace('</body>', patch + '\n</body>', 1)
p.write_text(s, encoding='utf-8')

wp = Path('worker.js')
ws = wp.read_text(encoding='utf-8')
stamp = '// DEPLOY_REFRESH_DEVELOPMENT_IMAGES_V50_2026_10_07\n'
if not ws.startswith(stamp):
    wp.write_text(stamp + ws, encoding='utf-8')

print('V50 applied')
