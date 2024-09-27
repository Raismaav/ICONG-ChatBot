import os
import json

def crear_diccionario(carpeta_destino):
    diccionario_archivos = {}
    if not os.path.exists(carpeta_destino):
        print(f"La carpeta '{carpeta_destino}' no existe.")
        return diccionario_archivos
    for archivo in os.listdir(carpeta_destino):
        if archivo.endswith(".pdf"):
            if archivo not in diccionario_archivos:
                diccionario_archivos[archivo] = ""
    return diccionario_archivos

def guardar_diccionario(diccionario_archivos, carpeta_salida = "generated" ,archivo_salida="diccionario_archivos.json"):
    os.makedirs(carpeta_salida, exist_ok = True)
    ruta_completa = os.path.join(carpeta_salida, archivo_salida)
    with open(ruta_completa, "w") as f:
        json.dump(diccionario_archivos, f, indent = 4)

carpeta_destino = "context_files"
diccionario_archivos = crear_diccionario(carpeta_destino)

if diccionario_archivos:
    guardar_diccionario(diccionario_archivos)
    print("Diccionario de archivos PDF creado y guardado.")
else:
    print("No se encontraron archivos PDF en la carpeta.")
