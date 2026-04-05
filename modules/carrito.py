import streamlit as st
from modules.imagenes import obtener_imagen


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
    #st.sidebar.image("Imagenes/Logos/carrito.jpeg", width=40)
    col1, col2 = st.sidebar.columns([1, 3])

    with col1:
        carrito_icono = obtener_imagen("Imagenes/Logos/carrito.jpeg")
        st.image(carrito_icono, width=60)
    with col2:
        st.markdown(
            "<div style='margin-top: 18px; font-size: 18px; font-weight: bold;'>Carrito</div>",
            unsafe_allow_html=True
        )
    #st.sidebar.markdown("### Carrito")
    total = 0

    # Si el carrito está vacío
    if len(st.session_state.carrito) == 0:
        st.sidebar.write("Tu carrito está vacío.")
        return 0

    # Mostrar cada producto con botones + y -
    for item in st.session_state.carrito:
        producto = item["producto"]
        cantidad = item["cantidad"]
        precio = item["precio"]
        subtotal = precio * cantidad

        # Fila del producto
        st.sidebar.write(f"**{producto}** - ${subtotal}")

        # Una fila: − | cantidad | +  (texto ASCII para buen contraste con fondo vino)
        c_menos, c_num, c_mas = st.sidebar.columns([2, 2, 2])

        with c_menos:
            menos = st.button("−", key=f"menos_{producto}", use_container_width=True)

        with c_num:
            st.markdown(
                f"<div style='text-align:center;font-weight:700;font-size:1.1rem;padding:0.35rem 0;'>{cantidad}</div>",
                unsafe_allow_html=True,
            )

        with c_mas:
            mas = st.button("+", key=f"mas_{producto}", use_container_width=True)

        # Lógica de sumar
        if mas:
            item["cantidad"] += 1
            st.rerun()

        # Lógica de restar
        if menos:
            if item["cantidad"] > 1:
                item["cantidad"] -= 1
            else:
                st.session_state.carrito.remove(item)
            st.rerun()

        total += subtotal

    st.sidebar.markdown(f"### Total: ${total}")

    if st.sidebar.button("Vaciar carrito"):
        vaciar_carrito()
        st.rerun()

    return total