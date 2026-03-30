import streamlit as st
from modules.menu import mostrar_menu
from modules.productos import obtener_productos
from modules.carrito import inicializar_carrito, agregar, mostrar_carrito
from modules.whatsapp import generar_mensaje, generar_link_whatsapp
from modules.estilos import banner
from modules.tarjetas import tarjeta_producto
from modules.cliente import formulario_cliente

from modules.config import TELEFONO_ELAFOOD

st.set_page_config(page_title="ElaFood", layout="wide")

# Banner
banner()

if "pedido_generado" not in st.session_state:
    st.session_state.pedido_generado = False

if "pedido_enviado" not in st.session_state:
    st.session_state.pedido_enviado = False

# Inicializar carrito
inicializar_carrito()

# Mostrar menú
categoria = mostrar_menu()

# Mostrar productos de la categoría
st.subheader(f"Categoría: {categoria}")

for p in obtener_productos(categoria):
    key = f"{categoria}_{p['nombre']}"
    cantidad, agregar_btn = tarjeta_producto(
    p["nombre"],
    p["precio"],
    p["imagen"],
    p.get("descripcion", ""),
    key)

    if agregar_btn and cantidad > 0:
        agregar(p["nombre"], cantidad, p["precio"])
        st.success(f"{cantidad} x {p['nombre']} agregado(s) al carrito.")


# Mostrar carrito
total = mostrar_carrito()
# Formulario del cliente
cliente = formulario_cliente()

st.sidebar.markdown("---")

# Botón principal
generar = st.sidebar.button("Generar pedido", disabled=st.session_state.pedido_generado)

# Cuando presionan "Generar pedido"
if generar:
    if len(st.session_state.carrito) == 0:
        st.sidebar.warning("El carrito está vacío.")
    elif cliente["nombre"] == "":
        st.sidebar.warning("Por favor ingresa el nombre del cliente.")
    else:
        st.session_state.pedido_generado = True
        mensaje = generar_mensaje(st.session_state.carrito, total, cliente)
        st.session_state.link = generar_link_whatsapp(TELEFONO_ELAFOOD, mensaje)

# Si el pedido ya fue generado, mostrar elementos
if st.session_state.pedido_generado:

    st.sidebar.success("Pedido generado")

    st.sidebar.markdown("")

    # Botón real para detectar clic
    enviar = st.sidebar.button("Enviar pedido por WhatsApp")

    if enviar:
        st.session_state.pedido_enviado = True
        st.sidebar.markdown(
            f"""
            <a href="{st.session_state.link}" target="_blank" style="
                display: inline-block;
                padding: 10px 15px;
                background-color: #25D366;
                color: white;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
            ">
                Abrir WhatsApp
            </a>
            """,
            unsafe_allow_html=True
        )

# Si ya se envió el pedido, mostrar mensajes finales
if st.session_state.pedido_enviado:
    st.sidebar.info("Por favor espere nuestra confirmación para que pueda efectuar el pago.")
    st.sidebar.warning("Si desea hacer un nuevo pedido presione Vaciar Carrito.")