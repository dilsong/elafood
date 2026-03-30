import streamlit as st
from modules.menu import mostrar_menu
from modules.productos import obtener_productos
from modules.carrito import inicializar_carrito, agregar, mostrar_carrito
from modules.estilos import banner

st.set_page_config(page_title="ElaFood", layout="wide")

# Banner
banner()

# Inicializar carrito
inicializar_carrito()

# Mostrar menú
categoria = mostrar_menu()

st.subheader(f"Categoría: {categoria}")

# Mostrar productos de la categoría
for p in obtener_productos(categoria):
    cantidad = st.number_input(
        f"{p['nombre']} - ${p['precio']}",
        min_value=0,
        max_value=10,
        step=1,
        key=f"{categoria}_{p['nombre']}"
    )

    if cantidad > 0:
        agregar(p["nombre"], cantidad, p["precio"])

# Mostrar carrito
total = mostrar_carrito()