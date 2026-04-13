# -*- coding: utf-8 -*-
"""Rutas de archivos CSV: en Streamlit Cloud el repo suele ser de solo lectura; se usa /tmp como respaldo."""
import os
import tempfile


def ruta_csv_escribible(rel_desde_raiz: str, nombre_en_tmp: str) -> str:
    """
    Intenta `rel_desde_raiz` bajo la raíz del proyecto (p. ej. data/pedidos_privados.csv).
    Si no se puede crear/escribir (Cloud), usa tempfile con `nombre_en_tmp`.
    """
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.normpath(os.path.join(raiz, rel_desde_raiz.replace("/", os.sep)))
    d = os.path.dirname(p)
    try:
        os.makedirs(d, exist_ok=True)
        with open(p, "a", encoding="utf-8"):
            pass
        return p
    except OSError:
        return os.path.join(tempfile.gettempdir(), nombre_en_tmp)
