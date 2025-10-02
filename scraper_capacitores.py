import os
import requests
from serpapi import GoogleSearch
import re

# ¡IMPORTANTE! Pega aquí la API Key que copiaste de SerpApi.
API_KEY = "76d399653c4a352029ec3e3e1661df6da938fe356fb3f3306e6b02c8c51c7d71"

# Lista COMPLETA de descripciones de capacitores.
DESCRIPCIONES = [
    "CAPACITOR 4.5 MFD 450V",
    "CAPACITOR 40MF 450V 4 TERMINALES BLANCO",
    "CAPACITOR 250MFD 250V",
    "CAPACITOR 30+10UF 110 125 VAC",
    "CAPACITOR 10MFD 440V CABLE NEGRO ELEVADOR",
    "CAPACITOR 12 MFD 250VCA P/VENTILADOR",
    "CAPACITOR 12.5 + 5 MFD 370 VCA PARA VENTY CON CABLE",
    "CAPACITOR 12.5 + 6 MFD 370V",
    "CAPACITOR 14 MDF 250V",
    "CAPACITOR 15 + 2.5 MFD 370 VCA",
    "CAPACITOR 15 MFD 250VAC P/CLIMA",
    "CAPACITOR 15 MDF 250V",
    "CAPACITOR 2.5 UF 450V VENTILADOR",
    "CAPACITOR 20 MFD 370-440VCA GRIS",
    "CAPACITOR 25 MFD 370-440 VCA BLANCO",
    "CAPACITOR 25MFD+5MFD 250V 4 TERMINALES BLANCO",
    "CAPACITOR 3.5MF 450V NEGRO",
    "CAPACITOR 3UF 250 VAC DE VENTILADOR",
    "CAPACITOR 3UF 450V P/VENTILADOR",
    "CAPACITOR 30+10-5 MF 440 VCA BOMBA",
    "CAPACITOR 35 + 1.5 MF 440 VCA",
    "CAPACITOR 35 + 2.5 MF 440 VCA",
    "CAPACITOR 35 + 5 MFD 370/440VCA",
    "CAPACITOR 35+6 370VCA",
    "CAPACITOR 350MFD 250V A 440VOLT",
    "CAPACITOR 378-440 110/125",
    "CAPACITOR 4+2.5 MF 370 VCA",
    "CAPACITOR 4.5 MFD 450VCA",
    "CAPACITOR 40 MDF 250VAC",
    "CAPACITOR 40+5 440 VCA",
    "CAPACITOR 40+5=2.5 440 VCA",
    "CAPACITOR 41UF 15MF",
    "CAPACITOR 4.5 UF 250 VCA",
    "CAPACITOR 45 MF 250VAC PLASTICO BLANCO",
    "CAPACITOR 45 MFD + 5 370 A 440",
    "CAPACITOR 45 MF A 250 VCA PARA LAVADORA CON BASE",
    "CAPACITOR 5.5 UF 250 VCA",
    "CAPACITOR 50 MF 250 VCA",
    "CAPACITOR 50 MF 370 VCA/440V",
    "CAPACITOR 50 MFD 250VAC",
    "CAPACITOR 50MFD/250-450VAC",
    "CAPACITOR 50UF 370VCA",
    "CAPACITOR 55 MFD 370 VCA/440",
    "CAPACITOR 60 UF 250 VAC MABE ORIG",
    "CAPACITOR 70 UF 250 VCA",
    "CAPACITOR 72-88 220VAC 50-60HZ",
    "CAPACITOR 8 MF 370 VCA",
    "CAPACITOR 8 MFD 440 VCA",
    "CAPACITOR CON CABLE DE 5+5 250 VCA",
    "CAPACITOR DE 1.5 MF 450V",
    "CAPACITOR DE 1.8 MF 450V",
    "CAPACITOR DE 10 MF 250 VCA",
    "CAPACITOR DE 10 MFD 370 VCA",
    "CAPACITOR DE 15 A 250VAC",
    "CAPACITOR DE 15 MF RECTANGULAR",
    "CAPACITOR DE 150MF 250VAC",
    "CAPACITOR DE 16MFD 250V 4 TERMINALES BLANCO",
    "CAPACITOR DE 2 + 1 440 VCA",
    "CAPACITOR DE 25 MFD A 440VOLT",
    "CAPACITOR DE 2+2 UF P/4 V 440 VAC",
    "CAPACITOR DE 30+5 440V",
    "CAPACITOR DE 35 MF 250V",
    "CAPACITOR DE 350-400 125 VAC",
    "CAPACITOR DE 35+5 MF A 440 VAC",
    "CAPACITOR DE 4 MF 450V PARA VENTILADOR",
    "CAPACITOR DE 4.5 MF 450V",
    "CAPACITOR DE 45-6 MF A 250 VAC",
    "CAPACITOR DE 4MFD 250V",
    "CAPACITOR DE 4MFD 440 50/60",
    "CAPACITOR DE 5+5 UF 370 VCA",
    "CAPACITOR DE 50+5UF 370/440 VAC CLIMA",
    "CAPACITOR DE 50+5UF A 440VAC",
    "CAPACITOR DE 5MF 440V 50/60",
    "CAPACITOR DE 6.5 MFD 450V",
    "CAPACITOR DE 60 UF A 440VAC",
    "CAPACITOR DE 60+5 MF 370 VCA",
    "CAPACITOR DE 6MFD 440-50/60 TERMINAL",
    "CAPACITOR DE 7.5UF 370V",
    "CAPACITOR DE 70+5 440V",
    "CAPACITOR DE 7MFD 370-50-60",
    "CAPACITOR DE 8 MF 450V",
    "CAPACITOR DE BOMBA 40-48",
    "CAPACITOR DE DOBLE 15 UF A 250VAC",
    "CAPACITOR DE LAVADORA 35+18 250 VAC",
    "CAPACITOR DE CLIMA 40 MF 250VCA-450 VAC",
    "CAPACITOR DE CLIMA 45 MF 370-440-VAC-VCA",
    "CAPACITOR DE LAVADORA 60-20MFD-4TERMINALES",
    "CAPACITOR DE VENTILADOR 2MFD + 6MFD A 250VAC",
    "CAPACITOR DE W 4 MF+5MF A 250 V 50/60",
    "CAPACITOR DE W 21 6UF+5P 20 8UF A 250V AC",
    "CAPACITOR DUAL 50-5 MFD 370V",
    "CAPACITOR MFD 5+5+5 VOL 440",
    "CAPACITOR PARA ARRANQUE DE 53-64UF A 180VAC",
    "CAPACITOR PARA BOMBA 108-130 110V",
    "CAPACITOR PARA BOMBA 124-149 110V",
    "CAPACITOR PARA BOMBA 161-193 110V CHICO",
    "CAPACITOR PARA BOMBA 216-259",
    "CAPACITOR PARA BOMBA 21-25 250",
    "CAPACITOR PARA BOMBA 270-324",
    "CAPACITOR PARA BOMBA 400-480 UF 110-125VCA",
    "CAPACITOR PARA BOMBA 500-600 UF 110-125VAC",
    "CAPACITOR PARA BOMBA 590-708 UF 110-125VAC",
    "CAPACITOR PARA BOMBA 700-800 UF 110-125VAC",
    "CAPACITOR PARA BOMBA 88-108 110V",
    "CAPACITOR PARA BOMBA DE AGUA 270-324 MDF 110 VCA",
    "CAPACITOR PARA CLIMA 30 + 5 370VAC",
    "CAPACITOR PARA CLIMA 30-4 MF 440VOLT",
    "CAPACITOR PARA CLIMA DE 30UF 370V",
    "CAPACITOR PARA CLIMA DE 5 UF 450V B",
    "CAPACITOR PARA HIDROLAVADORA 30 UF A 400VAC",
    "CAPACITOR PARA LAVADORA 35+18 250 VAC",
    "CAPACITOR PARA LAVADORA 45+14 A 250V",
    "CAPACITOR PARA LAVADORA 60-20 MFD",
    "CAPACITOR PARA LAVADORA 70 MDF 250 VCA",
    "CAPACITOR PARA LAVADORA SAMSUM 3.5 MDF",
    "CAPACITOR PARA MICROONDAS 0.91",
    "CAPACITOR PARA MOTOR 7.5 440",
    "CAPACITOR PARA REFRIGERADOR UMP 250 VAC",
    "CAPACITOR PARA RELEVADOR UMP 250 VAC",
    "CAPACITOR PARA VENTILADOR 1.5 MFD A 450V",
    "CAPACITOR PARA VENTILADOR 2MFD 250V",
    "CAPACITOR PARA VENTILADOR 6 MF 250V",
    "CAPACITOR PARA CLIMA 8 MFD A 370 VCA",
    "CAPACITOR PARA CLIMA 8 MFD 370 VCA"
]

# Carpeta donde se guardarán las imágenes
DIRECTORIO_SALIDA = "imagenes_capacitores"

if not os.path.exists(DIRECTORIO_SALIDA):
    os.makedirs(DIRECTORIO_SALIDA)

def limpiar_nombre_archivo(nombre):
    """Limpia la descripción para usarla como nombre de archivo."""
    nombre_limpio = re.sub(r'[^\w\.\-]', '_', nombre)
    return nombre_limpio + ".jpg"

def buscar_y_descargar_imagen(descripcion, api_key):
    """Busca con SerpApi y descarga la primera imagen."""
    print(f"🔎 Buscando con API: '{descripcion}'...")
    params = {
        "engine": "google_images",
        "q": descripcion,
        "api_key": api_key
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "images_results" in results and len(results["images_results"]) > 0:
            url_imagen = results["images_results"][0]['original']
        else:
            print(f"❌ No se encontraron resultados en la API para '{descripcion}'.\n")
            return

        print(f"⏬ Descargando imagen desde {url_imagen[:70]}...")
        headers = {"User-Agent": "Mozilla/5.0"}
        img_data = requests.get(url_imagen, headers=headers).content
        
        nombre_archivo = limpiar_nombre_archivo(descripcion)
        ruta_archivo = os.path.join(DIRECTORIO_SALIDA, nombre_archivo)
        
        with open(ruta_archivo, 'wb') as handler:
            handler.write(img_data)
        
        print(f"✅ ¡Guardado! -> {ruta_archivo}\n")

    except Exception as e:
        print(f"🔥 Ocurrió un error inesperado con '{descripcion}': {e}\n")

# --- Iniciar el proceso ---
if __name__ == "__main__":
    if API_KEY == "PEGA_AQUÍ_TU_API_KEY":
        print("🚨 ¡Error! Por favor, edita el script y añade tu API Key de SerpApi.")
    else:
        for desc in DESCRIPCIONES:
            buscar_y_descargar_imagen(desc, API_KEY)
        print("✨ Proceso de scraping completado.")