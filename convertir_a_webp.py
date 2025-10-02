import os
from PIL import Image

# --- CONFIGURACIÓN ---
# 1. Nombre de la carpeta que contiene tus imágenes originales (JPG, PNG, etc.)
CARPETA_ENTRADA = "imagenes_capacitores"

# 2. Nombre de la carpeta donde se guardarán las nuevas imágenes .webp
CARPETA_SALIDA = "imagenes_convertidas_webp"

# 3. Calidad de la compresión WebP (0-100). 80 es un buen balance.
CALIDAD_WEBP = 80
# ---------------------

def convertir_imagenes():
    """
    Busca todas las imágenes en la carpeta de entrada, las convierte a .webp
    y las guarda en la carpeta de salida.
    """
    # Crear la carpeta de salida si no existe
    if not os.path.exists(CARPETA_SALIDA):
        os.makedirs(CARPETA_SALIDA)
        print(f"📁 Carpeta de salida creada: '{CARPETA_SALIDA}'")

    # Obtener la lista de archivos en la carpeta de entrada
    try:
        archivos = os.listdir(CARPETA_ENTRADA)
    except FileNotFoundError:
        print(f"🚨 ¡Error! No se encontró la carpeta de entrada '{CARPETA_ENTRADA}'.")
        print("Asegúrate de que el nombre de la carpeta sea correcto y esté al mismo nivel que el script.")
        return

    total_imagenes = 0
    convertidas_exito = 0

    for nombre_archivo in archivos:
        # Comprobar si el archivo es una imagen común
        if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            total_imagenes += 1
            ruta_entrada = os.path.join(CARPETA_ENTRADA, nombre_archivo)
            
            # Crear el nuevo nombre de archivo con la extensión .webp
            nombre_base = os.path.splitext(nombre_archivo)[0]
            ruta_salida = os.path.join(CARPETA_SALIDA, f"{nombre_base}.webp")

            try:
                # Abrir la imagen original
                with Image.open(ruta_entrada) as img:
                    print(f"🔄 Convirtiendo: {nombre_archivo}...")
                    
                    # Convertir a RGB si tiene transparencia (para compatibilidad con compresión con pérdidas)
                    if img.mode in ('RGBA', 'LA'):
                        img = img.convert('RGB')
                        
                    # Guardar la imagen en formato WebP
                    img.save(ruta_salida, 'webp', quality=CALIDAD_WEBP)
                    convertidas_exito += 1

            except Exception as e:
                print(f"❌ Error al convertir {nombre_archivo}: {e}")
    
    print("\n" + "="*30)
    print("✨ ¡Proceso completado! ✨")
    print(f"Imágenes encontradas: {total_imagenes}")
    print(f"Imágenes convertidas con éxito: {convertidas_exito}")
    print(f"Resultados guardados en la carpeta: '{CARPETA_SALIDA}'")
    print("="*30)

# --- Iniciar el proceso ---
if __name__ == "__main__":
    convertir_imagenes()