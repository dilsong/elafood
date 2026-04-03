# modules/menu.py
import streamlit as st

def mostrar_menu():
    opciones = {
        "Lunch": "lunch",
        "Comida Rápida": "comida_rapida",
        "Postres": "postres",
        "Otros": "otros"
    }

    seleccion = st.sidebar.radio(
        "Selecciona una categoría",
        list(opciones.keys())
    )

    return opciones[seleccion]   # ← devuelve la clave interna correcta