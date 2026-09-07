from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# El dato de talud no es suficientemente consistente en la fuente pública.
# Se conserva internamente en inventario, pero se retira de toda presentación pública.
patterns=[
'        <div class="qitem"><small>Talud</small><strong>${esc(talud)}</strong></div>\n',
'            <div class="lot-feature"><small>Talud</small><strong>${esc(talud)}</strong></div>\n',
'            <div><small>Talud</small><strong>${esc(talud)}</strong></div>\n',
'          <div><small>Talud</small><b>${esc(talud)}</b></div>\n',
]
for pat in patterns:
    s=s.replace(pat,'')

old='''      <div class="df-group"><span class="df-label">Tipo de terreno</span><div class="df-seg">
        ${[["all","Todos"],["flat","Plano"],["talud","Talud"],["corner","Esquina"]].map(([v,l])=>`<button type="button" class="df-btn ${f.terrain===v?"active":""}" onclick="setDevelopmentFilter('terrain','${v}',true)">${l}</button>`).join("")}
      </div></div>'''
new='''      <div class="df-group"><span class="df-label">Tipo de lote</span><div class="df-seg">
        ${[["all","Todos"],["corner","Esquina"]].map(([v,l])=>`<button type="button" class="df-btn ${f.terrain===v?"active":""}" onclick="setDevelopmentFilter('terrain','${v}',true)">${l}</button>`).join("")}
      </div></div>'''
s=s.replace(old,new)

# Si una URL antigua llega con flat/talud, neutralizarla para no aplicar un filtro engañoso.
s=s.replace('''function developmentLotMatches(model,lot){
  const f=developmentFilters,area=Number(lot.superficie_m2)||0;
  if(f.terrain==="flat" && lot.tiene_talud!==false)return false;
  if(f.terrain==="talud" && lot.tiene_talud!==true)return false;
  if(f.terrain==="corner" && lot.es_esquina!==true)return false;''','''function developmentLotMatches(model,lot){
  const f=developmentFilters,area=Number(lot.superficie_m2)||0;
  if(f.terrain==="corner" && lot.es_esquina!==true)return false;''')

p.write_text(s,encoding='utf-8')

assert '<small>Talud</small>' not in s
assert '["talud","Talud"]' not in s
assert '["flat","Plano"]' not in s
print('V45 OK: talud/plano retirados de la presentación pública; esquina conservada.')
