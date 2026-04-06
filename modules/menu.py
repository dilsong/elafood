# modules/menu.py
import streamlit as st

# Claves alineadas con menu_semana.json (columnas del chef)
_CLAVES = ("comidas", "postres", "otros")
_ETIQUETAS = ("Comidas", "Postres", "Otros")


def mostrar_filtro_categoria_semana() -> str:
    """
    Radio en el sidebar: Comidas (lunch + comida rápida en el menú semanal), Postres, Otros.
    Devuelve 'comidas' | 'postres' | 'otros'.
    """
    seleccion = st.sidebar.radio(
        "Selecciona una categoría",
        list(_ETIQUETAS),
        key="filtro_categoria_semana",
    )
    return _CLAVES[_ETIQUETAS.index(seleccion)]
