import streamlit as st

from modules.chef_module import validar_pin, vista_panel_chef
from modules.config import RUTA_ICONO_APP
from modules.estilo import boton_vino_tinto, estilos_app
from modules.tarjetas import tarjeta_acerca_chef

# Configuración de página para que en sidebar aparezca "Quienes Somos!"
st.set_page_config(
    page_title="Quienes Somos! – ElaFood",
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
    <h1 style='color:#91241D; text-align:center; margin-bottom:10px;'>
        Quienes Somos!
    </h1>
    """,
    unsafe_allow_html=True,
)

# Muestra la tarjeta de presentación del proyecto/equipo.
tarjeta_acerca_chef()

# Estado para mostrar/ocultar acceso del panel del chef.
if "mostrar_pin" not in st.session_state:
    st.session_state.mostrar_pin = False

if not st.session_state.mostrar_pin:
    if boton_vino_tinto("🔐 Entrar al Panel del Chef", key="btn_acceso"):
        st.session_state.mostrar_pin = True
        st.rerun()
else:
    # Validación de PIN para habilitar la configuración de menú.
    pin_ingresado = st.text_input("Ingrese el PIN del Chef", type="password")
    if pin_ingresado:
        if validar_pin(pin_ingresado):
            st.success("Acceso concedido")
            vista_panel_chef()
        else:
            st.error("PIN incorrecto")
