from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '<!-- SEO_CITY_ROUTE_V44 -->'
if marker in s:
    print('SEO_CITY_ROUTE_V44 already present')
    raise SystemExit(0)

block = r'''
<!-- SEO_CITY_ROUTE_V44 -->
<script>
(()=>{
  const params=new URLSearchParams(location.search);
  const city=(params.get('ciudad')||'').trim();
  const development=(params.get('desarrollo')||'').trim();
  if(!city && !development) return;
  const norm=s=>(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim().toLowerCase();
  const fire=(el,type)=>el.dispatchEvent(new Event(type,{bubbles:true}));

  function selectExact(target){
    const t=norm(target);
    for(const sel of document.querySelectorAll('select')){
      const opt=[...sel.options].find(o=>norm(o.textContent)===t || norm(o.value)===t);
      if(opt){sel.value=opt.value;fire(sel,'change');return true;}
    }
    return false;
  }
  function clickExact(target){
    const t=norm(target);
    const scopes=[...document.querySelectorAll('.development-filters,.searchbar,[class*="filter"],[id*="filter"]')];
    for(const scope of scopes){
      const hit=[...scope.querySelectorAll('button,a,[role="button"],label')].find(el=>norm(el.textContent)===t);
      if(hit){hit.click();return true;}
    }
    return false;
  }
  function searchDevelopment(target){
    const metaRx=/buscar|desarrollo|terreno/;
    for(const inp of document.querySelectorAll('input[type="search"],input[type="text"]')){
      const meta=norm((inp.placeholder||'')+' '+(inp.getAttribute('aria-label')||'')+' '+(inp.name||'')+' '+(inp.id||''));
      if(metaRx.test(meta)){inp.value=target;fire(inp,'input');fire(inp,'change');return true;}
    }
    return false;
  }

  let tries=0;
  const timer=setInterval(()=>{
    tries++;
    let cityDone=!city;
    let devDone=!development;
    if(city && !cityDone) cityDone=selectExact(city)||clickExact(city);
    if(development && !devDone) devDone=selectExact(development)||clickExact(development)||searchDevelopment(development);
    if((cityDone&&devDone)||tries>=18){
      clearInterval(timer);
      const anchor=document.getElementById('desarrollos')||document.getElementById('lotes');
      if(anchor) setTimeout(()=>anchor.scrollIntoView({behavior:'smooth',block:'start'}),250);
    }
  },450);
})();
</script>
<!-- /SEO_CITY_ROUTE_V44 -->
'''

if '</body>' not in s:
    raise SystemExit('Missing </body>')
s = s.replace('</body>', block + '\n</body>')
p.write_text(s, encoding='utf-8')
print('SEO_CITY_ROUTE_V44 inserted')
