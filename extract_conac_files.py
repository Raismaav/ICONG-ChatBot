from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup
import os
import hashlib

def calcular_hash_pagina(contenido):
    return hashlib.sha256(contenido.encode("utf-8")).hexdigest()

url = "https://www.conac.gob.mx/es/CONAC/Normatividad_Vigente"
carpeta_destino = "context_files"
hash_file = "generated/ultimo_hash.txt"

response = requests.get(url)

if response.status_code == 200:
    contenido_html = response.text
    hash_actual = calcular_hash_pagina(contenido_html)
    fecha_actual = datetime.now(timezone.utc).isoformat()

    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            lineas = f.readlines()
            hash_guardado = lineas[0].strip()
            fecha_guardada = lineas[1].strip()

        fecha_guardada_dt = datetime.strptime(fecha_guardada[:-6], "%Y-%m-%dT%H:%M:%S.%f")

        if (datetime.now() - fecha_guardada_dt).days < 1:
            print("Los documentos ya fueron actualizados recientemente. No se realizarán nuevas descargas.")
            exit()

        if hash_guardado == hash_actual:
            print("La página no ha cambiado. No se realizarán descargas.")
            exit()
    else:
        print("No se encontró hash anterior, se procederá a la descarga.")

    with open(hash_file, "w") as f:
        f.write(f"{hash_actual}\n")
        f.write(fecha_actual)

    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a")

    for link in links:
        href = link.get("href")
        if href and href.endswith(".pdf"):

            if not href.startswith("https://www.conac.gob.mx/"):
                pdf_url = "https://www.conac.gob.mx/" + href.lstrip('/')
            else:
                pdf_url = href

            pdf_response = requests.get(pdf_url)
            if pdf_response.status_code == 200:
                pdf_name = os.path.join(carpeta_destino, os.path.basename(pdf_url))
                with open(pdf_name, "wb") as f:
                    f.write(pdf_response.content)
                print(f"Descargando: {pdf_name}")
            else:
                print(f"Error al descargar: {pdf_url}")
print("Proceso de descarga finalizado.")