import os

GITHUB_BASE = "https://raw.githubusercontent.com/dilsong/elafood/main/"

def ruta_imagen(ruta_local):
    """
    Convierte rutas locales como:
        Imagenes/Comidas/Otros/refresco.jpg
    en URLs válidas para Streamlit Cloud y móviles.
    """
    if ruta_local.startswith("http"):
        return ruta_local  # Ya es URL

    # Normalizar separadores
    ruta_local = ruta_local.replace("\\", "/")

    # Asegurar que no empiece con "./"
    if ruta_local.startswith("./"):
        ruta_local = ruta_local[2:]

    # Construir URL final
    return GITHUB_BASE + ruta_local