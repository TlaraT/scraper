import os
import pandas as pd

# --- CONFIGURACIÓN ---
# Nombre de la carpeta donde están tus imágenes .webp.
CARPETA_IMAGENES = "imagenes_convertidas_webp"

# Nombre que tendrá el nuevo archivo de Excel de salida.
NOMBRE_ARCHIVO_SALIDA = "lista_de_imagenes.xlsx"

# Nombre de la columna en el archivo de Excel.
NOMBRE_COLUMNA = "nombre_archivo_imagen"
# ---------------------

def crear_excel_con_nombres_de_archivos():
    """
    Busca todos los archivos en la carpeta de imágenes y los guarda
    en una columna de un nuevo archivo de Excel.
    """
    print(f"📁 Buscando archivos en la carpeta: '{CARPETA_IMAGENES}'...")

    try:
        # Obtener la lista de todos los archivos en el directorio
        lista_de_archivos = os.listdir(CARPETA_IMAGENES)
        
        # Opcional: Filtrar para asegurarse de que solo sean archivos .webp
        imagenes_webp = [archivo for archivo in lista_de_archivos if archivo.lower().endswith('.webp')]
        
        if not imagenes_webp:
            print("❌ No se encontraron archivos .webp en la carpeta.")
            return

        print(f"✔️ Se encontraron {len(imagenes_webp)} imágenes.")

        # Crear un DataFrame de pandas con la lista de nombres
        df = pd.DataFrame({NOMBRE_COLUMNA: imagenes_webp})

        # Guardar el DataFrame en un archivo de Excel
        df.to_excel(NOMBRE_ARCHIVO_SALIDA, index=False)

        print(f"\n✨ ¡Éxito! Se ha creado el archivo '{NOMBRE_ARCHIVO_SALIDA}' con los nombres de las imágenes.")

    except FileNotFoundError:
        print(f"🚨 ¡Error! No se pudo encontrar la carpeta '{CARPETA_IMAGENES}'.")
        print("Asegúrate de que el script esté en la carpeta correcta.")
    except Exception as e:
        print(f"🚨 Ocurrió un error inesperado: {e}")

# --- Iniciar el proceso ---
if __name__ == "__main__":
    crear_excel_con_nombres_de_archivos()