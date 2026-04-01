import streamlit as st
from modules.menu import mostrar_menu
from modules.productos import obtener_productos
from modules.carrito import inicializar_carrito, agregar, mostrar_carrito
from modules.whatsapp import generar_mensaje, generar_link_whatsapp
from modules.estilos import banner
from modules.tarjetas import tarjeta_producto
from modules.cliente import formulario_cliente
from modules.config import TELEFONO_ELAFOOD

# ---------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------------------------------------
st.set_page_config(page_title="ElaFood", layout="wide")

# Banner superior
banner()

# ---------------------------------------------------------
# INICIALIZACIÓN DE SESSION_STATE
# ---------------------------------------------------------
if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "mensaje_generado" not in st.session_state:
    st.session_state.mensaje_generado = ""

if "link" not in st.session_state:
    st.session_state.link = ""

if "pedido_listo" not in st.session_state:
    st.session_state.pedido_listo = False

if "pedido_generado" not in st.session_state:
    st.session_state.pedido_generado = False

if "pedido_enviado" not in st.session_state:
    st.session_state.pedido_enviado = False

# ---------------------------------------------------------
# MENÚ Y PRODUCTOS
# ---------------------------------------------------------
inicializar_carrito()

categoria = mostrar_menu()
st.subheader(f"Categoría: {categoria}")

for p in obtener_productos(categoria):
    key = f"{categoria}_{p['nombre']}"
    cantidad, agregar_btn = tarjeta_producto(
        p["nombre"],
        p["precio"],
        p["imagen"],
        p.get("descripcion", ""),
        key
    )

    if agregar_btn and cantidad > 0:
        agregar(p["nombre"], cantidad, p["precio"])
        st.success(f"{cantidad} x {p['nombre']} agregado(s) al carrito.")

# ---------------------------------------------------------
# CARRITO Y CLIENTE
# ---------------------------------------------------------
total = mostrar_carrito()
cliente = formulario_cliente()

st.sidebar.markdown("---")

# ---------------------------------------------------------
# BOTÓN: GENERAR PEDIDO
# ---------------------------------------------------------
generar = st.sidebar.button(
    "Generar pedido",
    disabled=st.session_state.pedido_generado
)

if generar:
    if len(st.session_state.carrito) == 0:
        st.sidebar.warning("El carrito está vacío.")
    elif cliente["nombre"] == "":
        st.sidebar.warning("Por favor ingresa el nombre del cliente.")
    else:
        mensaje = generar_mensaje(st.session_state.carrito, total, cliente)
        st.session_state.mensaje_generado = mensaje
        st.session_state.link = generar_link_whatsapp(TELEFONO_ELAFOOD, mensaje)

        st.session_state.pedido_listo = True
        st.session_state.pedido_generado = True
        st.sidebar.success("Pedido generado. Presione enviar por WhatsApp.")

# ---------------------------------------------------------
# ENVIAR POR WHATSAPP (LINK REAL + AUTO-MARCAR ENVÍO)
# ---------------------------------------------------------
if st.session_state.pedido_listo and not st.session_state.pedido_enviado:

    # Enlace real que abre WhatsApp en móviles
    st.sidebar.markdown(
        f"""
        <a href="{st.session_state.link}" target="_blank" id="ws_link" style="
            display: block;
            padding: 12px;
            background-color: #25D366;
            color: white;
            text-align: center;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            font-size: 16px;">
            Enviar por WhatsApp
        </a>
        """,
        unsafe_allow_html=True
    )

    # Botón invisible para marcar que ya se envió
    marcar = st.sidebar.button(" ", key="marcar_envio_btn")

    # Script que presiona automáticamente el botón invisible
    st.components.v1.html(
        """
        <script>
            const link = document.getElementById("ws_link");
            link.addEventListener("click", () => {
                const btn = window.parent.document.querySelector('button[k="marcar_envio_btn"]');
                if (btn) btn.click();
            });
        </script>
        """,
        height=0
    )

    if marcar:
        st.session_state.pedido_enviado = True

# ---------------------------------------------------------
# HACER NUEVO PEDIDO
# ---------------------------------------------------------
if st.session_state.pedido_enviado:
    if st.sidebar.button("Hacer nuevo pedido", key="nuevo_pedido_btn"):
        st.session_state.carrito = []
        st.session_state.mensaje_generado = ""
        st.session_state.link = ""
        st.session_state.pedido_listo = False
        st.session_state.pedido_generado = False
        st.session_state.pedido_enviado = False
        st.sidebar.success("Listo. Puedes comenzar un nuevo pedido.")