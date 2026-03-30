# modules/carrito.py
import streamlit as st

def inicializar_carrito():
    if "carrito" not in st.session_state:
        st.session_state.carrito = []

def agregar(producto, cantidad, precio):
    st.session_state.carrito.append({
        "producto": producto,
        "cantidad": cantidad,
        "precio": precio
    })

def mostrar_carrito():
    st.sidebar.markdown("### 🛒 Carrito")
    total = 0

    for item in st.session_state.carrito:
        st.sidebar.write(
            f"{item['cantidad']} x {item['producto']} - ${item['precio'] * item['cantidad']}"
        )
        total += item["precio"] * item["cantidad"]

    st.sidebar.markdown(f"### Total: ${total}")
    return total