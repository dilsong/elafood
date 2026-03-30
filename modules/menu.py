# modules/menu.py
import streamlit as st

def mostrar_menu():
    return st.sidebar.radio(
        "Selecciona una categoría",
        ["Lunch", "Comida Rápida", "Postres", "Otros"]
    )