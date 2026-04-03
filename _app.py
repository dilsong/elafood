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
# MOSTRAR BOTÓN GENERAR PEDIDO SOLO SI HAY PRODUCTOS
# ---------------------------------------------------------
hay_productos = len(st.session_state.carrito) > 0

if hay_productos and not st.session_state.pedido_generado:
    generar = st.sidebar.button("Generar pedido")
else:
    generar = False

# ---------------------------------------------------------
# GENERAR PEDIDO
# ---------------------------------------------------------
if generar:
    if cliente["nombre"] == "":
        st.sidebar.warning("Por favor ingresa el nombre del cliente.")
    else:
        mensaje = generar_mensaje(st.session_state.carrito, total, cliente)
        st.session_state.mensaje_generado = mensaje
        st.session_state.link = generar_link_whatsapp(TELEFONO_ELAFOOD, mensaje)

        st.session_state.pedido_generado = True
        st.sidebar.success("Pedido generado. Presione Enviar por WS.")

# ---------------------------------------------------------
# ENVIAR POR WS (BOTÓN REAL QUE ABRE WHATSAPP + REINICIA)
# ---------------------------------------------------------
if st.session_state.pedido_generado:
    if st.sidebar.button("Enviar por WS", key="enviar_ws_btn"):

        # ABRIR WHATSAPP DIRECTO SIN RECARGAR LA APP
        js = f"window.open('{st.session_state.link}', '_blank').focus();"
        st.components.v1.html(f"<script>{js}</script>", height=0)

        # REINICIAR LA APLICACIÓN AUTOMÁTICAMENTE
        st.session_state.carrito = []
        st.session_state.mensaje_generado = ""
        st.session_state.link = ""
        st.session_state.pedido_generado = False
        st.session_state.pedido_listo = False
        st.session_state.pedido_enviado = False

        st.sidebar.success("Listo. Puedes comenzar un nuevo pedido.")