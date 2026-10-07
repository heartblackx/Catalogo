from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='<!-- CATALOGO_V51_HORIZONTAL_DEVELOPMENT_CARDS -->'
if marker not in s:
    patch=r'''
<!-- CATALOGO_V51_HORIZONTAL_DEVELOPMENT_CARDS -->
<style id="catalogo-v51-horizontal-development-cards-style">
#devGrid{display:grid!important;grid-template-columns:1fr!important;gap:26px!important;align-items:stretch!important}
#devGrid .dev,#devGrid .dev:nth-child(3n+1),#devGrid .dev:nth-child(3n+2){grid-column:1/-1!important;display:grid!important;grid-template-columns:minmax(430px,52%) minmax(0,48%)!important;min-height:390px!important;height:auto!important;overflow:hidden!important;border-radius:28px!important;background:#fffdfa!important;border:1px solid rgba(16,47,57,.08)!important;box-shadow:0 18px 45px rgba(16,42,52,.09)!important;transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease!important}
#devGrid .dev:hover{transform:translateY(-2px)!important;box-shadow:0 26px 60px rgba(16,42,52,.14)!important;border-color:rgba(10,102,116,.18)!important}
#devGrid .dev-photo{position:relative!important;width:100%!important;height:100%!important;min-height:390px!important;display:flex!important;align-items:center!important;justify-content:center!important;overflow:hidden!important;padding:18px!important;background:linear-gradient(145deg,#e6eeed,#f2f5f4)!important;border-radius:28px 0 0 28px!important}
#devGrid .dev-photo>img{display:block!important;width:100%!important;height:100%!important;max-width:100%!important;max-height:100%!important;object-fit:contain!important;object-position:center!important;transform:none!important;transform-origin:center!important;scale:none!important;clip-path:none!important;opacity:1!important;margin:auto!important;border-radius:18px!important;background:#e7eeee!important;filter:none!important}
#devGrid .dev-photo img[src*="#campestre-clean"],#devGrid .dev-photo img{object-fit:contain!important;object-position:center!important;transform:none!important;scale:none!important}
#devGrid .dev-body{display:flex!important;flex-direction:column!important;min-width:0!important;padding:32px 34px 28px!important;background:#fffdfa!important}
#devGrid .dev-summary{display:flex!important;align-items:flex-start!important;justify-content:space-between!important;gap:20px!important}
#devGrid .dev-heading{min-width:0!important}
#devGrid .dev-type{display:block!important;margin-bottom:7px!important;color:#087b84!important;font-size:.68rem!important;font-weight:950!important;letter-spacing:.13em!important;text-transform:uppercase!important}
#devGrid .dev-heading h3{margin:0!important;font-size:clamp(1.35rem,2vw,1.85rem)!important;line-height:1.05!important;letter-spacing:-.035em!important;color:#102d38!important}
#devGrid .dev-zone{margin-top:6px!important;font-size:.78rem!important;color:#77858a!important;text-transform:uppercase!important;letter-spacing:.035em!important}
#devGrid .dev-availability{flex:0 0 auto!important;padding:9px 12px!important;border-radius:999px!important;background:#e3f4ed!important;color:#087557!important;font-size:.72rem!important;font-weight:950!important;white-space:nowrap!important}
#devGrid .dev-desc{margin-top:20px!important;min-height:0!important;color:#52676f!important;line-height:1.65!important;font-size:.98rem!important;display:-webkit-box!important;-webkit-line-clamp:3!important;-webkit-box-orient:vertical!important;overflow:hidden!important}
#devGrid .dev-metrics{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:10px!important;margin-top:22px!important}
#devGrid .metric{padding:13px 14px!important;border-radius:15px!important;background:#f3ede4!important;border:1px solid rgba(29,57,67,.06)!important}
#devGrid .metric small{display:block!important;margin-bottom:5px!important;font-size:.62rem!important;color:#839095!important;text-transform:uppercase!important;letter-spacing:.05em!important;font-weight:850!important}
#devGrid .metric strong{display:block!important;color:#153540!important;font-size:.9rem!important;overflow:hidden!important;text-overflow:ellipsis!important}
#devGrid .dev-actions{display:grid!important;grid-template-columns:minmax(0,1fr) auto!important;gap:10px!important;margin-top:auto!important;padding-top:24px!important}
#devGrid .devbtn{min-height:50px!important;padding:13px 18px!important;border-radius:14px!important;font-size:.95rem!important;background:linear-gradient(135deg,#074555,#0d7180)!important;box-shadow:0 12px 26px rgba(7,69,85,.17)!important}
#devGrid .mapbtn{min-height:50px!important;padding:12px 18px!important;border-radius:14px!important}
#devGrid .sold-out-card{grid-template-columns:minmax(430px,52%) minmax(0,48%)!important}
#devGrid .sold-out-photo{height:100%!important;min-height:390px!important}
@media(max-width:1050px){#devGrid .dev,#devGrid .dev:nth-child(3n+1),#devGrid .dev:nth-child(3n+2){grid-template-columns:minmax(360px,47%) minmax(0,53%)!important;min-height:360px!important}#devGrid .dev-photo{min-height:360px!important;padding:14px!important}#devGrid .dev-body{padding:26px!important}#devGrid .dev-metrics{grid-template-columns:repeat(2,minmax(0,1fr))!important}}
@media(max-width:760px){#devGrid{grid-template-columns:1fr!important;gap:20px!important}#devGrid .dev,#devGrid .dev:nth-child(3n+1),#devGrid .dev:nth-child(3n+2){display:flex!important;flex-direction:column!important;min-height:0!important;border-radius:23px!important}#devGrid .dev-photo{width:100%!important;height:auto!important;min-height:0!important;padding:0!important;border-radius:23px 23px 0 0!important;overflow:hidden!important}#devGrid .dev-photo>img{width:100%!important;height:auto!important;max-height:none!important;object-fit:contain!important;border-radius:0!important}#devGrid .dev-body{padding:20px 18px 18px!important}#devGrid .dev-summary{gap:10px!important}#devGrid .dev-heading h3{font-size:1.35rem!important}#devGrid .dev-availability{font-size:.65rem!important;padding:8px 10px!important}#devGrid .dev-desc{margin-top:14px!important;font-size:.9rem!important;-webkit-line-clamp:3!important}#devGrid .dev-metrics{grid-template-columns:repeat(2,minmax(0,1fr))!important;margin-top:16px!important}#devGrid .dev-actions{grid-template-columns:1fr!important;padding-top:18px!important}#devGrid .mapbtn{width:100%!important}}
@media(max-width:480px){#devGrid .dev-body{padding:18px 15px 16px!important}#devGrid .dev-summary{flex-direction:column!important}#devGrid .dev-availability{align-self:flex-start!important}#devGrid .dev-metrics{grid-template-columns:1fr 1fr!important}}
</style>
<script id="catalogo-v51-horizontal-development-cards-script">
(function(){
  function normalizeDevelopmentImages(){
    document.querySelectorAll('#devGrid .dev-photo img').forEach(img=>{
      img.style.objectFit='contain';
      img.style.objectPosition='center';
      img.style.transform='none';
      img.style.width='100%';
      if(window.innerWidth>760) img.style.height='100%'; else img.style.height='auto';
    });
  }
  const observer=new MutationObserver(normalizeDevelopmentImages);
  function start(){
    const grid=document.getElementById('devGrid');
    if(!grid){setTimeout(start,250);return;}
    normalizeDevelopmentImages();
    observer.observe(grid,{childList:true,subtree:true});
    window.addEventListener('resize',normalizeDevelopmentImages,{passive:true});
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start); else start();
})();
</script>
<!-- /CATALOGO_V51_HORIZONTAL_DEVELOPMENT_CARDS -->
'''
    s=s.replace('</body>',patch+'\n</body>',1)
    p.write_text(s,encoding='utf-8')

w=Path('worker.js')
if w.exists():
    ws=w.read_text(encoding='utf-8')
    stamp='// DEPLOY_REFRESH_HORIZONTAL_DEVELOPMENT_CARDS_V51_2026_10_07\n'
    if not ws.startswith(stamp):
        w.write_text(stamp+ws,encoding='utf-8')
print('V51 applied')
