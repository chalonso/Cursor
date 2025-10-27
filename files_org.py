#Automatización - "Organización de archivos"

from pathlib import Path
import shutil

CATEGORIAS = {
    "Imágenes": [".jpg", ".jpeg", ".png", ".gif"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".avi", ".mov"],
    "Otros": []
}

def organizar_archivos(carpeta):
    carpeta = Path(carpeta)

    # Recorre todos los archivos
    for archivo in carpeta.iterdir():
        if archivo.is_file():  # solo archivos
            extension = archivo.suffix.lower()
            categoria = None

            for nombre_cat, extensiones in CATEGORIAS.items():
                if extension in extensiones:
                    categoria = nombre_cat
                    break

            if not categoria:
                categoria = "Otros"

            carpeta_destino = carpeta / categoria

            # Asegurar que la carpeta destino sea realmente una carpeta
            if not carpeta_destino.exists():
                carpeta_destino.mkdir(exist_ok=True)

            # Evitar sobreescribir archivos con el mismo nombre
            destino_final = carpeta_destino / archivo.name
            if destino_final.exists():
                print(f"⚠️ Ya existe {destino_final.name}, se omitirá.")
                continue

            shutil.move(str(archivo), str(destino_final))
            print(f"✅ {archivo.name} movido a {categoria}")


#-----Programa principal
if __name__ == "__main__":
    carpeta = input("Ingresa la ruta de la carpeta que deseas organizar: ").strip()
    organizar_archivos(carpeta)


