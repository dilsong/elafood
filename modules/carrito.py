import hashlib

import streamlit as st

from modules.menu_semana import etiqueta_dia
from modules.productos import es_comida_lunch_o_rapida_por_nombre


def inicializar_carrito():
    if "carrito" not in st.session_state:
        st.session_state.carrito = []


def agregar(producto: str, cantidad: int, precio: float, dia: str | None = None):
    """dia: clave lunes..domingo desde menú semanal; None si viene del catálogo."""
    for item in st.session_state.carrito:
        if item["producto"] == producto and item.get("dia") == dia:
            item["cantidad"] += cantidad
            return

    st.session_state.carrito.append(
        {
            "producto": producto,
            "cantidad": cantidad,
            "precio": precio,
            "dia": dia,
        }
    )


def vaciar_carrito():
    st.session_state.carrito = []


def _clave_cantidad_carrito(nombre_producto: str, dia) -> str:
    raw = f"{nombre_producto}|{dia if dia is not None else ''}"
    h = hashlib.md5(raw.encode("utf-8")).hexdigest()[:16]
    return f"elafood_cart_qty_{h}"


def _sync_cantidad_linea(nombre_producto: str, dia, state_key: str):
    def _fn():
        val = int(st.session_state[state_key])
        for it in st.session_state.carrito:
            if it["producto"] == nombre_producto and it.get("dia") == dia:
                it["cantidad"] = val
                return

    return _fn


def _etiqueta_linea_carrito(producto: str, dia) -> str:
    if dia and es_comida_lunch_o_rapida_por_nombre(producto):
        return f"{etiqueta_dia(dia)} — {producto}"
    return producto


def mostrar_carrito():
    st.sidebar.markdown(
        "<div style='font-size:17px;font-weight:700;color:#7A1F1F;margin-bottom:6px;'>Carrito</div>",
        unsafe_allow_html=True,
    )

    total = 0

    if len(st.session_state.carrito) == 0:
        st.sidebar.write("Tu carrito está vacío.")
        return 0

    for item in st.session_state.carrito:
        producto = item["producto"]
        cantidad = item["cantidad"]
        precio = item["precio"]
        dia = item.get("dia")
        subtotal = precio * cantidad

        etiqueta = _etiqueta_linea_carrito(producto, dia)
        st.sidebar.write(f"**{etiqueta}** — ${subtotal}")

        sk = _clave_cantidad_carrito(producto, dia)
        if st.session_state.get(sk) != cantidad:
            st.session_state[sk] = cantidad

        st.sidebar.number_input(
            "Uds.",
            min_value=1,
            max_value=99,
            key=sk,
            on_change=_sync_cantidad_linea(producto, dia, sk),
            label_visibility="collapsed",
        )

        total += subtotal

    st.sidebar.markdown(f"### Total: ${total}")

    if st.sidebar.button("Vaciar carrito"):
        vaciar_carrito()
        st.rerun()

    return total
