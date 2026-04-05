import streamlit as st
from modules.chef_module import vista_panel_chef, validar_pin

st.set_page_config(
    page_title="Panel del Chef – ElaFood",
    layout="wide"
)

st.title("Panel del Chef – ElaFood")
st.write("Configura el menú del día, categorías y platos disponibles.")

pin_ingresado = st.text_input("Ingrese el PIN del Chef", type="password")

if pin_ingresado:
    if validar_pin(pin_ingresado):
        st.success("Acceso concedido")
        vista_panel_chef()
    else:
        st.error("PIN incorrecto")