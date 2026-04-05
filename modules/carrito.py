import hashlib

import streamlit as st

from modules.imagenes import obtener_imagen


def inicializar_carrito():
    if "carrito" not in st.session_state:
        st.session_state.carrito = []


def agregar(producto, cantidad, precio):
    for item in st.session_state.carrito:
        if item["producto"] == producto:
            item["cantidad"] += cantidad
            return

    st.session_state.carrito.append(
        {
            "producto": producto,
            "cantidad": cantidad,
            "precio": precio,
        }
    )


def vaciar_carrito():
    st.session_state.carrito = []


def _clave_cantidad_carrito(nombre_producto: str) -> str:
    h = hashlib.md5(nombre_producto.encode("utf-8")).hexdigest()[:16]
    return f"elafood_cart_qty_{h}"


def _sync_cantidad_linea(nombre_producto: str, state_key: str):
    def _fn():
        val = int(st.session_state[state_key])
        for it in st.session_state.carrito:
            if it["producto"] == nombre_producto:
                it["cantidad"] = val
                return

    return _fn


def mostrar_carrito():
    # Solo icono: dos columnas + CSS global del sidebar hacían que el texto “Carrito” se saliera del panel en móvil.
    carrito_icono = obtener_imagen("Imagenes/Logos/carrito.jpeg")
    st.sidebar.image(carrito_icono, width=40)

    total = 0

    if len(st.session_state.carrito) == 0:
        st.sidebar.write("Tu carrito está vacío.")
        return 0

    for item in st.session_state.carrito:
        producto = item["producto"]
        cantidad = item["cantidad"]
        precio = item["precio"]
        subtotal = precio * cantidad

        st.sidebar.write(f"**{producto}** — ${subtotal}")

        sk = _clave_cantidad_carrito(producto)
        if st.session_state.get(sk) != cantidad:
            st.session_state[sk] = cantidad

        st.sidebar.number_input(
            "Uds.",
            min_value=1,
            max_value=99,
            key=sk,
            on_change=_sync_cantidad_linea(producto, sk),
            label_visibility="collapsed",
        )

        total += subtotal

    st.sidebar.markdown(f"### Total: ${total}")

    if st.sidebar.button("Vaciar carrito"):
        vaciar_carrito()
        st.rerun()

    return total
