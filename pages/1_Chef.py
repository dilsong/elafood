import streamlit as st
from modules.chef_module import validar_pin, vista_panel_chef
from modules.tarjetas import tarjeta_acerca_chef
from modules.estilo import boton_vino_tinto, estilos_app
from modules.config import RUTA_ICONO_APP

st.set_page_config(
    page_title="Panel del Chef – ElaFood",
    layout="centered",
    page_icon=RUTA_ICONO_APP,
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    },
)
estilos_app()
if hasattr(st, "logo"):
    try:
        st.logo(RUTA_ICONO_APP)
    except Exception:
        pass

st.markdown(
    """
    <h1 style='color:#7A1F1F; text-align:center; margin-bottom:10px;'>
        Panel del Chef – ElaFood
    </h1>
    <p style='text-align:center; color:#444; margin-top:-10px;'>
        Configura el menú de la semana: por día, Comidas, Postres y Otros.
    </p>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# TARJETA ACERCA DEL CHEF
# -----------------------------
tarjeta_acerca_chef()

# -----------------------------
# BOTÓN PARA MOSTRAR PIN
# -----------------------------
if "mostrar_pin" not in st.session_state:
    st.session_state.mostrar_pin = False

if not st.session_state.mostrar_pin:
    if boton_vino_tinto("🔐 Entrar al Panel del Chef", key="btn_acceso"):
        st.session_state.mostrar_pin = True
        st.rerun()

# -----------------------------
# CAMPO PIN
# -----------------------------
else:
    pin_ingresado = st.text_input("Ingrese el PIN del Chef", type="password")

    if pin_ingresado:
        if validar_pin(pin_ingresado):
            st.success("Acceso concedido")
            vista_panel_chef()
        else:
            st.error("PIN incorrecto")