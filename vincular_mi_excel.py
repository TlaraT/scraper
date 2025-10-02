import pandas as pd
import os
import re
from unidecode import unidecode

# --- CONFIGURACIÓN ---
# 1. Escribe el nombre EXACTO de tu archivo de Excel.
NOMBRE_ARCHIVO_EXCEL = "producto.xls" # <--- ¡CAMBIA ESTO!

# 2. Escribe el nombre de la carpeta donde están tus imágenes .webp.
CARPETA_IMAGENES = "imagenes_convertidas_webp"

# 3. Escribe el nombre de la columna que tiene los nombres de los productos.
COLUMNA_NOMBRES = "nombre" # <--- ¡CAMBIA ESTO SI TU COLUMNA SE LLAMA DIFERENTE!

# 4. Nombre de la nueva columna que se creará con las imágenes.
COLUMNA_IMAGENES = "ruta_imagen"
# ---------------------

def super_normalizar(texto):
    """Normaliza un texto para la comparación: minúsculas, sin acentos y solo letras/números."""
    texto_limpio = unidecode(str(texto).lower())
    texto_limpio = re.sub(r'[^a-z0-9]', '', texto_limpio)
    return texto_limpio

def vincular_imagenes_a_excel():
    """Lee el Excel del usuario, añade la columna de imágenes respetando el orden y guarda un nuevo archivo."""
    try:
        print(f"📖 Leyendo tu archivo de Excel: '{NOMBRE_ARCHIVO_EXCEL}'...")
        df = pd.read_excel(NOMBRE_ARCHIVO_EXCEL)
    except FileNotFoundError:
        print(f"🚨 ¡Error! No se encontró el archivo Excel '{NOMBRE_ARCHIVO_EXCEL}'. Asegúrate de que el nombre es correcto.")
        return
    except Exception as e:
        print(f"🚨 ¡Error crítico al leer el Excel! Verifica que no esté dañado. Error: {e}")
        return

    if COLUMNA_NOMBRES not in df.columns:
        print(f"🚨 ¡Error! La columna de nombres '{COLUMNA_NOMBRES}' no existe en tu Excel.")
        print(f"   Columnas disponibles: {list(df.columns)}")
        return

    mapa_imagenes = {}
    print(f"🖼️  Creando mapa de imágenes desde la carpeta '{CARPETA_IMAGENES}'...")
    try:
        for nombre_archivo in os.listdir(CARPETA_IMAGENES):
            if nombre_archivo.lower().endswith('.webp'):
                nombre_base = os.path.splitext(nombre_archivo)[0]
                huella_digital = super_normalizar(nombre_base)
                mapa_imagenes[huella_digital] = nombre_archivo
    except FileNotFoundError:
        print(f"🚨 ¡Error! No se encontró la carpeta de imágenes '{CARPETA_IMAGENES}'.")
        return

    print(f"🗺️  Mapa creado con {len(mapa_imagenes)} imágenes.")

    if COLUMNA_IMAGENES not in df.columns:
        df[COLUMNA_IMAGENES] = "" # Crea la columna vacía
    
    print(f"\n🔄 Procesando {len(df)} filas de tu Excel (esto puede tardar un momento)...")
    
    # Esta es la parte clave: aplicamos la búsqueda a la columna de nombres.
    # El orden se mantiene intacto.
    def encontrar_imagen(nombre_producto):
        if pd.notna(nombre_producto):
            huella_producto = super_normalizar(nombre_producto)
            return mapa_imagenes.get(huella_producto, "No se encontró la imagen")
        return ""

    df[COLUMNA_IMAGENES] = df[COLUMNA_NOMBRES].apply(encontrar_imagen)
    
    # --- Guardar el archivo final ---
    nombre_archivo_salida = "MiCatalogo_CON_IMAGENES.xlsx"
    try:
        df.to_excel(nombre_archivo_salida, index=False)
        encontradas = (df[COLUMNA_IMAGENES] != "No se encontró la imagen").sum()
        
        print("\n" + "="*40)
        print("✨ ¡Proceso completado! ✨")
        print(f"✔️ Se vincularon {encontradas} imágenes.")
        print(f"💾 Se ha creado un NUEVO archivo llamado '{nombre_archivo_salida}'")
        print("   Este archivo es una copia de tu original, con la nueva columna de imágenes.")
        print("   ¡El orden de tus filas y precios está intacto!")
        print("="*40)
    except Exception as e:
        print(f"🚨 Ocurrió un error al guardar el archivo: {e}")

if __name__ == "__main__":
    vincular_imagenes_a_excel()