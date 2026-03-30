import streamlit as st

def inicializar_carrito():
    if "carrito" not in st.session_state:
        st.session_state.carrito = []

def agregar(producto, cantidad, precio):
    # Si ya existe el producto, sumar cantidades
    for item in st.session_state.carrito:
        if item["producto"] == producto:
            item["cantidad"] += cantidad
            return
    
    # Si no existe, agregarlo
    st.session_state.carrito.append({
        "producto": producto,
        "cantidad": cantidad,
        "precio": precio
    })

def vaciar_carrito():
    st.session_state.carrito = []

def mostrar_carrito():
    st.sidebar.markdown("### 🛒 Carrito")
    total = 0

    for item in st.session_state.carrito:
        subtotal = item["precio"] * item["cantidad"]
        st.sidebar.write(f"{item['cantidad']} x {item['producto']} - ${subtotal}")
        total += subtotal

    st.sidebar.markdown(f"### Total: ${total}")

    if st.sidebar.button("Vaciar carrito"):
        vaciar_carrito()
        st.rerun()

    return total