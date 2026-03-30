import streamlit as st
from modules.menu import mostrar_menu
from modules.productos import obtener_productos
from modules.carrito import inicializar_carrito, agregar, mostrar_carrito
from modules.whatsapp import generar_mensaje, generar_link_whatsapp
from modules.estilos import banner
from modules.tarjetas import tarjeta_producto

from modules.config import TELEFONO_ELAFOOD



st.set_page_config(page_title="ElaFood", layout="wide")

# Banner
banner()

# Inicializar carrito
inicializar_carrito()

# Mostrar menú
categoria = mostrar_menu()

#st.subheader(f"Categoría: {categoria}")

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

st.markdown("---")
st.subheader("Enviar pedido")

if st.sidebar.button("Generar pedido"):
    if len(st.session_state.carrito) == 0:
        st.sidebar.warning("El carrito está vacío.")
    else:
        mensaje = generar_mensaje(st.session_state.carrito, total)
        link = generar_link_whatsapp(TELEFONO_ELAFOOD, mensaje)
        st.sidebar.success("Pedido generado.")
        st.sidebar.markdown(f"[Enviar por WhatsApp]({link})")
