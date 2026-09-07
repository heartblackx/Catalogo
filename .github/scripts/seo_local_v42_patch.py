from pathlib import Path

p = Path('index.html')
t = p.read_text(encoding='utf-8')

if 'CATALOGO_SEO_LOCAL_V42' in t:
    print('SEO V42 already applied')
    raise SystemExit(0)

old_desc = '<meta name="description" content="Explora terrenos disponibles en Baja California, compara enganche, mensualidad, plazo y ubicación, y recibe atención directa de un asesor de Invierte Inteligente TJ.">'
new_desc = '<meta name="description" content="Terrenos en Tijuana, Rosarito y Ensenada. Consulta lotes disponibles, precios, enganche, mensualidades, ubicación y agenda una visita sin compromiso con Invierte Inteligente TJ.">'
if old_desc not in t:
    raise SystemExit('No se encontró la meta description esperada')
t = t.replace(old_desc, new_desc, 1)

old_title = '<title>Invierte Inteligente TJ | Catálogo de Terrenos</title>'
new_title = '<title>Terrenos en Tijuana, Rosarito y Ensenada | Invierte Inteligente TJ</title>'
if old_title not in t:
    raise SystemExit('No se encontró el title esperado')
t = t.replace(old_title, new_title, 1)

anchor = '<meta name="theme-color" content="#0b3040">'
insert = '''<meta name="theme-color" content="#0b3040">\n<!-- CATALOGO_SEO_LOCAL_V42 -->\n<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">\n<meta name="googlebot" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">\n<meta name="geo.region" content="MX-BCN">\n<meta name="geo.placename" content="Baja California">\n<!-- /CATALOGO_SEO_LOCAL_V42 -->'''
if anchor not in t:
    raise SystemExit('No se encontró theme-color')
t = t.replace(anchor, insert, 1)

old_og = '<meta property="og:title" content="Terrenos disponibles | Invierte Inteligente TJ">'
new_og = '<meta property="og:title" content="Terrenos en Tijuana, Rosarito y Ensenada | Invierte Inteligente TJ">'
t = t.replace(old_og, new_og, 1)

old_tw = '<meta name="twitter:title" content="Terrenos disponibles | Invierte Inteligente TJ">'
new_tw = '<meta name="twitter:title" content="Terrenos en Tijuana, Rosarito y Ensenada | Invierte Inteligente TJ">'
t = t.replace(old_tw, new_tw, 1)

p.write_text(t, encoding='utf-8')
print('SEO local V42 aplicado')
