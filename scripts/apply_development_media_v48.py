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

marker = '<!-- CATALOGO_V48_DEVELOPMENT_MEDIA_CONTAIN -->'
if marker not in s:
    patch = r'''
<!-- CATALOGO_V48_DEVELOPMENT_MEDIA_CONTAIN -->
<style id="catalogo-v48-development-media-contain-style">
  #devGrid .dev-photo{
    height:300px!important;
    display:grid!important;
    place-items:center!important;
    padding:12px!important;
    background:linear-gradient(145deg,#eef3f2,#e3eceb)!important;
    overflow:hidden!important;
  }
  #devGrid .dev-photo>img{
    width:100%!important;
    height:100%!important;
    object-fit:contain!important;
    object-position:center!important;
    transform:none!important;
    border-radius:15px!important;
    background:#e8efee!important;
  }

  #devModal .modal-hero,
  #devModal .premium-hero-media{
    min-height:360px!important;
    height:clamp(360px,50vw,560px)!important;
    display:grid!important;
    place-items:center!important;
    padding:16px!important;
    background:linear-gradient(145deg,#edf3f2,#dfe9e8)!important;
    overflow:hidden!important;
  }
  #devModal .modal-hero>img,
  #devModal .premium-hero-media>img{
    width:100%!important;
    height:100%!important;
    object-fit:contain!important;
    object-position:center!important;
    transform:none!important;
    background:#e7eeee!important;
    border-radius:18px!important;
  }

  #devModal .premium-gallery-shell .gallery,
  #devModal .gallery{
    display:grid!important;
    grid-template-columns:repeat(auto-fit,minmax(250px,1fr))!important;
    grid-auto-rows:auto!important;
    gap:14px!important;
    align-items:stretch!important;
  }
  #devModal .premium-gallery-shell .gallery img,
  #devModal .gallery img{
    width:100%!important;
    height:auto!important;
    min-height:220px!important;
    max-height:440px!important;
    aspect-ratio:16/10!important;
    object-fit:contain!important;
    object-position:center!important;
    transform:none!important;
    padding:8px!important;
    border-radius:17px!important;
    background:#e9efee!important;
    border:1px solid rgba(16,58,69,.08)!important;
  }
  #devModal .gallery img:first-child{grid-row:auto!important}

  #devGrid .dev-photo img[src*="#campestre-clean"],
  #devModal .modal-hero img[src*="#campestre-clean"],
  #devModal .premium-hero-media img[src*="#campestre-clean"],
  #devModal .gallery img[src*="#campestre-clean"]{
    object-fit:contain!important;
    object-position:center!important;
    transform:none!important;
  }

  @media(max-width:680px){
    #devGrid .dev-photo{height:240px!important;padding:8px!important}
    #devModal .modal-hero,#devModal .premium-hero-media{min-height:260px!important;height:340px!important;padding:10px!important}
    #devModal .premium-gallery-shell .gallery,#devModal .gallery{grid-template-columns:1fr!important}
    #devModal .premium-gallery-shell .gallery img,#devModal .gallery img{min-height:200px!important;max-height:360px!important}
  }
</style>
<!-- /CATALOGO_V48_DEVELOPMENT_MEDIA_CONTAIN -->
'''
    s = s.replace('</body>', patch + '\n</body>', 1)

p.write_text(s, encoding='utf-8')

wp = Path('worker.js')
ws = wp.read_text(encoding='utf-8')
stamp = '// DEPLOY_REFRESH_DEVELOPMENT_MEDIA_V48_2026_10_07\n'
if not ws.startswith(stamp):
    wp.write_text(stamp + ws, encoding='utf-8')

print('V48 applied')
