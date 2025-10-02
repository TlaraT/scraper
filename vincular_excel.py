import pandas as pd
import os
import re
from unidecode import unidecode

# --- CONFIGURACIÓN ---
NOMBRE_ARCHIVO_EXCEL = "producto.xls"
CARPETA_IMAGENES = "imagenes_convertidas_webp"
COLUMNA_NOMBRES = "nombre"
COLUMNA_IMAGENES = "ruta_imagen"
# ---------------------

def super_normalizar(texto):
    """
    Función de normalización definitiva.
    Convierte a minúsculas, quita acentos y ELIMINA todos los caracteres
    que no sean letras o números para crear una 'huella digital'.
    """
    # 1. Convertir a string, minúsculas y quitar acentos
    texto_limpio = unidecode(str(texto).lower())
    # 2. Eliminar TODO lo que no sea letra o número
    texto_limpio = re.sub(r'[^a-z0-9]', '', texto_limpio)
    return texto_limpio

def vincular_imagenes_a_excel():
    """
    Función principal que lee el Excel, busca las imágenes de forma súper-flexible
    y guarda los cambios, además de un reporte de depuración.
    """
    try:
        print(f"📖 Leyendo el archivo '{NOMBRE_ARCHIVO_EXCEL}'...")
        df = pd.read_excel(NOMBRE_ARCHIVO_EXCEL)
    except Exception as e:
        print(f"🚨 ¡Error crítico al leer el Excel! Verifica el nombre y que no esté dañado. Error: {e}")
        return
    
    if COLUMNA_NOMBRES not in df.columns:
        print(f"🚨 ¡Error! La columna '{COLUMNA_NOMBRES}' no existe en el archivo de Excel.")
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
        df[COLUMNA_IMAGENES] = "No procesado"

    # Lista para guardar los datos de depuración
    datos_debug = []
    encontradas = 0

    print("\n🔄 Procesando filas y buscando coincidencias...")
    for index, row in df.iterrows():
        nombre_producto = row[COLUMNA_NOMBRES]
        resultado = "No se encontró la imagen"
        
        if pd.notna(nombre_producto):
            huella_producto = super_normalizar(nombre_producto)
            
            if huella_producto in mapa_imagenes:
                resultado = mapa_imagenes[huella_producto]
                encontradas += 1
            
            df.loc[index, COLUMNA_IMAGENES] = resultado
            datos_debug.append({
                "Nombre Original (Excel)": nombre_producto,
                "Huella Digital (Buscada)": huella_producto,
                "Resultado": resultado
            })

    # --- Guardar el archivo principal actualizado ---
    nombre_archivo_salida = "catalogo_actualizado_final.xlsx"
    try:
        df.to_excel(nombre_archivo_salida, index=False)
        print("\n" + "="*40)
        print("✨ ¡Proceso principal completado! ✨")
        print(f"✔️ {encontradas} imágenes vinculadas con éxito.")
        print(f"💾 Resultados guardados en: '{nombre_archivo_salida}'")
        print("="*40)
    except Exception as e:
        print(f"🚨 Ocurrió un error al guardar el archivo principal: {e}")

    # --- Guardar el archivo de reporte para depuración ---
    nombre_reporte_debug = "debug_report.xlsx"
    try:
        df_debug = pd.DataFrame(datos_debug)
        df_debug.to_excel(nombre_reporte_debug, index=False)
        print(f"🔍 Se ha creado un reporte de depuración en: '{nombre_reporte_debug}'")
        print("Si faltan imágenes, abre este archivo para ver por qué no coincidieron.")
    except Exception as e:
        print(f"🚨 Ocurrió un error al guardar el reporte de depuración: {e}")


if __name__ == "__main__":
    vincular_imagenes_a_excel()