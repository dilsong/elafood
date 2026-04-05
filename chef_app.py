import streamlit as st
from modules.chef_module import vista_panel_chef


def cargar_pin() -> str:
    return st.secrets.get("PIN_CHEF", "").strip()

def validar_pin(pin_ingresado: str) -> bool:
    pin_real = cargar_pin()
    return pin_real != "" and pin_ingresado == pin_real

st.set_page_config(page_title="Panel del Chef – ElaFood", layout="wide")

st.title("Panel del Chef – ElaFood")
st.write("Configura el menú del día, categorías y platos disponibles.")

vista_panel_chef()