const CACHE_NAME='invierte-inteligente-offline-v1';
const APP_SHELL=['/','/index.html','/favicon.png'];

self.addEventListener('install',event=>{
  event.waitUntil((async()=>{
    const cache=await caches.open(CACHE_NAME);
    await Promise.all(APP_SHELL.map(async url=>{
      try{await cache.add(new Request(url,{cache:'reload'}));}catch(_){ }
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate',event=>{
  event.waitUntil((async()=>{
    const keys=await caches.keys();
    await Promise.all(keys.filter(k=>k!==CACHE_NAME).map(k=>caches.delete(k)));
    await self.clients.claim();
  })());
});

function normalizedRequest(request){
  const url=new URL(request.url);
  if(url.origin!==self.location.origin) return request;
  if(request.mode==='navigate'){
    return new Request('/index.html',{method:'GET',headers:request.headers,mode:'same-origin',credentials:'same-origin',redirect:'follow'});
  }
  url.search='';
  return new Request(url.toString(),{method:'GET',headers:request.headers,mode:request.mode==='navigate'?'same-origin':request.mode,credentials:request.credentials,redirect:'follow'});
}

self.addEventListener('fetch',event=>{
  const req=event.request;
  if(req.method!=='GET') return;
  const url=new URL(req.url);
  if(url.origin!==self.location.origin) return;

  if(req.mode==='navigate'){
    event.respondWith((async()=>{
      const cache=await caches.open(CACHE_NAME);
      try{
        const fresh=await fetch(req);
        if(fresh && fresh.ok) cache.put('/index.html',fresh.clone());
        return fresh;
      }catch(_){
        return (await cache.match('/index.html')) || (await cache.match('/')) || Response.error();
      }
    })());
    return;
  }

  event.respondWith((async()=>{
    const cache=await caches.open(CACHE_NAME);
    const key=normalizedRequest(req);
    const cached=await cache.match(key);
    const network=fetch(req).then(res=>{
      if(res && res.ok && (url.protocol==='https:'||url.protocol==='http:')) cache.put(key,res.clone());
      return res;
    }).catch(()=>null);
    return cached || (await network) || Response.error();
  })());
});
