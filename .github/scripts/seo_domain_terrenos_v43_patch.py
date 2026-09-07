from pathlib import Path

OLD = "https://catalogo.invierteinteligentetj.com"
NEW = "https://terrenos.invierteinteligentetj.com"

for name in ["index.html", "robots.txt", "sitemap.xml"]:
    p = Path(name)
    text = p.read_text(encoding="utf-8")
    if OLD not in text:
        raise SystemExit(f"{OLD} no encontrado en {name}")
    text = text.replace(OLD, NEW)
    p.write_text(text, encoding="utf-8")

print("SEO domain corrected to terrenos.invierteinteligentetj.com")
