from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
changes={
'<div><strong>Invierte Inteligente TJ</strong> · Catálogo actualizado desde inventario</div>':'<div><strong>Invierte Inteligente TJ</strong> · Catálogo de terrenos</div>',
'<p>Catálogo conectado a inventario para mostrar desarrollos, ubicación y lotes con información actualizada.</p>':'<p>Explora desarrollos, ubicaciones y lotes disponibles, y recibe atención directa de un asesor.</p>'
}
for old,new in changes.items():
    if old not in s:
        raise SystemExit(f'Expected visible text not found: {old}')
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
