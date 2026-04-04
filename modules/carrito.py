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

        # Botones ➖ cantidad ➕
        col1, col2, col3 = st.sidebar.columns([1, 1, 1])

        with col1:
            menos = st.button("➖", key=f"menos_{producto}")

        with col2:
            st.write(f"{cantidad}")

        with col3:
            mas = st.button("➕", key=f"mas_{producto}")

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