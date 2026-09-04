from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile, ZIP_DEFLATED
import re

photos = [
    ("Lomas del Valle", "https://lh3.googleusercontent.com/sitesv/AG8ngQWjUvBn6NaBja3_2iLo8pap6gPl7kXxsqub_bdVLdPYEIr37SpcczwDk5ou8UOllV4J9Dx5GHYWtps-ybKqcwOJIVSzprd2GjumnkJupqTFL9McVP9Nig1vcuRHfNbTpnHE82CXImH3R-qXK6WzBfIIr4luajIyiZ55r4Qzio3h1yx5rhkpSXbRrTGN1kk=w16383"),
    ("Los Olivos", "https://lh3.googleusercontent.com/sitesv/AG8ngQV6Xeho6Mtii0Vf76SXtKMv7QkDVegTk2YZXeEOXe61_2sRO0kEU4W3JLq0nRHXXRW71xz084MTnZuXBhPSNH4wkWX4J7cA0gt8RjJinF2Kui7tEpF3pHlcvvSXi0d7OfA2FVxecn5wWGFob1-qWsG7_Srer33nbYgkB0eDpK0G9JukbgWj7XUro4YnaAk=w16383"),
    ("Rancho Escondido", "https://lh3.googleusercontent.com/sitesv/AG8ngQUi1LqdcUlB84PVsckXfDrA0XBlsr9xmztMl_wlMOLxM-iTOhCEMPlCJIITOYfRIkIuTiuRJAzdgWZubY8nChA9o08BvGpPbImD6yMVn_EQzThDgqjrVBULHqwQIkN0WYWq91JzcfQCbPWP5ikVyr1YPIaizH3TqdHKljfNJshNH79-GoGp_hCO8V0zI0Y=w16383"),
    ("Alamar Residencial", "https://lh3.googleusercontent.com/sitesv/AG8ngQUifPx8O9pc6XXyZlHj_Zt1LsOh6yFKHLsgWFVq1aFsFGyc4RV_VLj-JKdhxwdOpHs636NHJDp830LIXPwv2vKGfSzcXOYT5YIV2SbTHXVhxMDdeP_0kE4FneNCfSQbllT6LbT-R5qnhC7WHE2WchlmOdDkoFTaAhYe4NAixvtDft9XshD3ulvQYdLs=w16383"),
    ("Paramo", "https://lh3.googleusercontent.com/sitesv/AG8ngQVnNZQPX_jGc9i4ObnfY2uEJx4WZf-mfqAoC7vfTH8tNrPYVp7gtdVncRsjvUTZ7W7f4dxFbqRU90i-sXFInpqW6o85mCkvCSt5EiHogBu0cjmAPl_Egf7HxHeEM7jOao1b0cUwBwLm8zVq2D5L6Wdb7RJHHg4LJJ7PwQRb6z3F5Yg8uV7MURp49oHT=w16383"),
    ("Andares de Santa Fe", "https://lh3.googleusercontent.com/sitesv/AG8ngQUi60tg91AGVtCMOt-kceskgPmWZm8pjEoNGR6FGSnhBwNbGtOf8ditYCOgt-fqe-B8pUk1nNXJHQsmiOr8fSL_Bo_Vnhb6w02XHpJpfBgX_Q0w-t8pYnmVCEiohUFZ_vXOQawdElPk-T0dQQngn3hyOT3xaOIDe1A7iCVFjAtYoOY6f2lmulOqXm3IRYQ=w16383"),
    ("Sahara", "https://lh3.googleusercontent.com/sitesv/AG8ngQU05eo3WNoDZAatokXAiP63ADlvbZpWs6IAMd9YFnDXgsDoieNIehcxUUbib-tFg2db7R-iIAVzSMjI5sImhkPK4E1nTQtjidi8e5jOjvDecMOLlE3BOH0jIQ5dvTd0BQyyBYqnQJFFyt79H_JGzTsPQ7vV5WqgIkMgI6ml3Ft8qexQ1pG4B7Ct26yoSvQ=w16383"),
    ("Vistas de Puerto Nuevo", "https://lh3.googleusercontent.com/sitesv/AG8ngQWcRlBmAoElEsIzvxzJzjunO54BIcAs3_lrNFALczRysZ3vTyUFQmosm9WP9iGcb_ZRX92Va91tIYpWIKbg0AZd5w4ZC_qTd8X-dLLVtw6BB9cwBGUt7YxvW1EBhLl84T--GShBh-V5ZfyZQZMr02Rea_OJ88rC9aSrBxVBerf4qjbv4uriLlvMB3oZ=w16383"),
    ("Cielo", "https://lh3.googleusercontent.com/sitesv/AG8ngQW8wvDqt9gFmPMXM01hXhSHky74Ha-sXfyG4MFTe79xlE7smU86-JM0LIObFgf8s7SbeR-5T_0H12gFYqiyZh8yrA0fN1C1sP9Eii8uNKX0cV8yGMOmz8kyxYvcJ6qELuIAdebwFpGutcHnKVL6R64mLgcEEI5g8Cezzp-2oP_irDLRc5IIWiYCrwqdQs0=w16383"),
    ("Santorini", "https://lh3.googleusercontent.com/sitesv/AG8ngQXLaftpRhaN9ZkxardOnUKroMJrxB8sLdLneNO-HFV4fAjc2RSFPyOgT0LHAHt3h41UPwLgIWGFrtBCW-c4ttFqdr77MXIPvPx9pd7IPRYBULv3GyTcbJYfYfW01duJ2a0EVVUkYNZUAgwgkEJEnyYnUdaN5vMTVba47wrFR2GjF6H3pgkYQr0sMWtW=w16383"),
    ("Puerto Escondido", "https://lh3.googleusercontent.com/sitesv/AG8ngQXEYysB9nJtWOEV69kx95PXoeaRKwDRh_uZzPkKsG9fFNndhh3UNF6FZSmWpbkYnF2FCpASwFSToqEUBHrpkaIaed4AVQp8Os_u_sduXcF34E4ZS8S0H0vmK58ANLGKkVhfAUpILoJ9hBsk3KG4ygiat_4Q1iTo_gCOarDgcuFIH2ZzJiwLf646oFqa=w16383"),
    ("Costa Dorada Perla", "https://lh3.googleusercontent.com/sitesv/AG8ngQXbhp_u9Sma4Y-jVhL5FenmZsV6DNMBi5Cwa6YGGXPLCXhinPPPdeBtimK8EA6WSIO2plE_7lDm6M58hA6RzObW9gImujBFLlEOMgIyQObeJtieTomhFkG7hcA28-2H3QAQbhwtBaWp_fvYb1pTQS6GYQm7MdRviXbfb7agQMXtJ-rUVFIPTrrxTSrnhZE=w16383"),
    ("Villa Toscana", "https://lh3.googleusercontent.com/sitesv/AG8ngQVB0cQyQDmsuOkv91MIpKWmUkrKpTmppA4qRGitLwFDpTg4Tzcs8n5MoFMwfgaizwxxzxHW97BIwVnap0vrnh1Qagg9Hc0g89zDOAxYa35oFvkci1_NvPv9n8QUBT3p_27vcGKE1blGqkTg772W9j2Fin3nwsmN6tv38s6suVsMQju5Amcflmf8klqkd4M=w16383"),
    ("Otay Campestre", "https://lh3.googleusercontent.com/sitesv/AG8ngQWvqsNIN-SVojeicnKQNYjkYEZbkXdSmYUVyzD_DQgQ9Ya4r020bRgjlxsT9jEE_96BtvdQJmCNOGOJ19WcykIdMOQUogFhDafyKWTB4GhCgzKHLa8VnnuRzcAWrZEln94FACywyLaVkJB5RQOENdOyA_uPOHMtRlF6Q0t9BktpYGdLBxBVQgAfxtc5=w16383"),
]

out = Path("google-site-photos")
out.mkdir(exist_ok=True)
exts = {"image/jpeg":"jpg", "image/png":"png", "image/webp":"webp", "image/gif":"gif"}

for name, url in photos:
    req = Request(url, headers={"User-Agent":"Mozilla/5.0"})
    with urlopen(req, timeout=60) as r:
        data = r.read()
        ctype = (r.headers.get_content_type() or "").lower()
    ext = exts.get(ctype, "img")
    safe = re.sub(r"[^A-Za-z0-9_-]+", "_", name).strip("_")
    path = out / f"{safe}.{ext}"
    path.write_bytes(data)
    print(f"{name}: {ctype} {len(data)} bytes -> {path}")

zip_path = Path("Invierte_Inteligente_TJ_fotos_Google_Site.zip")
with ZipFile(zip_path, "w", ZIP_DEFLATED) as z:
    for p in sorted(out.iterdir()):
        z.write(p, p.name)
print(f"ZIP: {zip_path} ({zip_path.stat().st_size} bytes)")
