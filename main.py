import requests
from bs4 import BeautifulSoup
import os
import urllib.robotparser as robotparser

BASE_URL = "https://automatizacion-porcentaje-dinero.onrender.com"

# 1️⃣ Revisar robots.txt
rp = robotparser.RobotFileParser()
rp.set_url(BASE_URL + "/robots.txt")
rp.read()

if not rp.can_fetch("*", BASE_URL):
    print("❌ Scraping no permitido por robots.txt")
    exit()

print("✅ Scraping permitido")

# 2️⃣ Descargar HTML
response = requests.get(BASE_URL)

if response.status_code != 200:
    print("❌ Error al acceder a la página")
    exit()

soup = BeautifulSoup(response.text, "lxml")
print("Título:", soup.title.text)

# 3️⃣ Encontrar CSS
css_links = soup.find_all("link", rel="stylesheet")

css_urls = []
for link in css_links:
    href = link.get("href")
    if href.startswith("http"):
        css_urls.append(href)
    else:
        css_urls.append(BASE_URL + href)

# 4️⃣ Crear carpeta
os.makedirs("css", exist_ok=True)

# 5️⃣ Descargar y guardar CSS
for i, css_url in enumerate(css_urls):
    css_response = requests.get(css_url)

    if css_response.status_code == 200:
        with open(f"css/style_{i}.css", "w", encoding="utf-8") as f:
            f.write(css_response.text)
        print(f"✔ CSS {i} guardado")
    else:
        print(f"⚠️ Error al descargar {css_url}")
