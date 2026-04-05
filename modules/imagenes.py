import base64
import mimetypes
import os
import urllib.parse

# Raíz del proyecto (carpeta que contiene /modules)
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GITHUB_BASE = "https://raw.githubusercontent.com/dilsong/elafood/main/"

# Imagen por defecto cuando falta foto o ruta vacía (misma ruta en GitHub y en disco local)
RUTA_NO_IMAGEN = "Imagenes/Logos/no_image.jpg"


def _ruta_absoluta(ruta_local: str) -> str:
    ruta_local = ruta_local.replace("\\", "/").strip()
    if ruta_local.startswith("./"):
        ruta_local = ruta_local[2:]
    return os.path.normpath(os.path.join(_BASE_DIR, *ruta_local.split("/")))


def ruta_imagen(ruta_local: str) -> str:
    """
    Convierte una ruta de proyecto a URL raw de GitHub (codificada para espacios
    y caracteres especiales en nombres de archivo).
    """
    if ruta_local.startswith("http"):
        return ruta_local

    ruta_local = ruta_local.replace("\\", "/").strip()
    if ruta_local.startswith("./"):
        ruta_local = ruta_local[2:]

    partes = [p for p in ruta_local.split("/") if p]
    codificada = "/".join(urllib.parse.quote(p, safe="") for p in partes)
    return GITHUB_BASE + codificada


def _archivo_a_data_uri(ruta_abs: str) -> str:
    mime, _ = mimetypes.guess_type(ruta_abs)
    if not mime:
        ext = os.path.splitext(ruta_abs)[1].lower()
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}.get(
            ext, "image/jpeg"
        )
    with open(ruta_abs, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def obtener_imagen_plato(ruta_catalogo: str | None) -> str:
    """
    Imagen para platos del menú/catálogo.

    Si la foto del plato **no está en tu disco**, pero sí tienes `no_image.jpg`,
    se usa esa imagen por defecto (evita URL del plato en GitHub que devuelve 404).

    Si no hay archivos locales (p. ej. Streamlit Cloud), se usa la URL del plato en GitHub.
    """
    if not ruta_catalogo or not str(ruta_catalogo).strip():
        return obtener_imagen(RUTA_NO_IMAGEN)
    ruta = str(ruta_catalogo).strip()
    if ruta.startswith("http"):
        return ruta

    abs_plato = _ruta_absoluta(ruta)
    if os.path.isfile(abs_plato):
        return abs_plato

    abs_no = _ruta_absoluta(RUTA_NO_IMAGEN)
    if os.path.isfile(abs_no):
        return abs_no

    return ruta_imagen(ruta)


def obtener_imagen(ruta_local: str | None) -> str:
    """
    Para st.image: devuelve ruta absoluta local si el archivo existe; si no, URL en GitHub.
    Así en tu PC ves siempre el archivo real; en la nube, la URL.
    """
    if not ruta_local or not str(ruta_local).strip():
        ruta_local = RUTA_NO_IMAGEN
    else:
        ruta_local = str(ruta_local).strip()

    if ruta_local.startswith("http"):
        return ruta_local

    abs_path = _ruta_absoluta(ruta_local)
    if os.path.isfile(abs_path):
        return abs_path

    return ruta_imagen(ruta_local)


def src_para_html(ruta_local: str | None) -> str:
    """
    Para <img src=""> o url() en CSS: el navegador no puede abrir rutas tipo E:\\...
    Si hay archivo local, usa data URI; si no, la misma URL pública que st.image usaría en la nube.
    """
    if not ruta_local or not str(ruta_local).strip():
        ruta_local = RUTA_NO_IMAGEN
    else:
        ruta_local = str(ruta_local).strip()

    if ruta_local.startswith("http"):
        return ruta_local

    abs_path = _ruta_absoluta(ruta_local)
    if os.path.isfile(abs_path):
        return _archivo_a_data_uri(abs_path)

    return ruta_imagen(ruta_local)
