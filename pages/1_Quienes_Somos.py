import streamlit as st

from modules.chef_module import validar_pin, vista_panel_chef
from modules.config import RUTA_ICONO_APP
from modules.i18n import tr
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

# Logo en sidebar sin usar st.logo (evita warning deprecado interno).
try:
    st.sidebar.image(RUTA_ICONO_APP, width=110)
except Exception:
    pass

st.markdown(
    """
    <h1 style='color:#9D1414; text-align:center; margin-bottom:10px;'>
        """
    + tr("Quienes Somos!", "Who We Are!")
    + """
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
    if boton_vino_tinto(tr("🔐 Entrar al Panel del Chef", "🔐 Enter Chef Panel"), key="btn_acceso"):
        st.session_state.mostrar_pin = True
        st.rerun()
else:
    # Validación de PIN para habilitar la configuración de menú.
    pin_ingresado = st.text_input(tr("Ingrese el PIN del Chef", "Enter Chef PIN"), type="password")
    if pin_ingresado:
        if validar_pin(pin_ingresado):
            st.success(tr("Acceso concedido", "Access granted"))
            vista_panel_chef()
        else:
            st.error(tr("PIN incorrecto", "Wrong PIN"))
