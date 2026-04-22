import re

import streamlit as st
from modules.i18n import tr


def formulario_cliente():
    st.sidebar.markdown(f"### {tr('Datos del cliente', 'Client details')}")

    if "cliente" not in st.session_state:
        st.session_state.cliente = {
            "nombre": "",
            "telefono": "",
            "direccion": "",
            "notas": ""
        }

    st.session_state.cliente["nombre"] = st.sidebar.text_input(
        tr("Nombre", "Name"),
        value=st.session_state.cliente["nombre"]
    )

    def _sync_telefono():
        raw = st.session_state.get("_tel_input", "")
        st.session_state.cliente["telefono"] = re.sub(r"\D+", "", raw or "")

    if "_tel_input" not in st.session_state:
        st.session_state["_tel_input"] = st.session_state.cliente.get("telefono", "")

    st.sidebar.text_input(
        tr("Teléfono", "Phone"),
        key="_tel_input",
        on_change=_sync_telefono,
        help=tr(
            "Solo números. Ej: 7875551234 o 17875551234 (sin espacios ni guiones).",
            "Numbers only. Ex: 7875551234 or 17875551234 (no spaces or hyphens).",
        ),
    )
    _sync_telefono()

    st.session_state.cliente["direccion"] = st.sidebar.text_area(
        tr("Dirección", "Address"),
        value=st.session_state.cliente["direccion"]
    )

    st.session_state.cliente["notas"] = st.sidebar.text_area(
        tr("Notas adicionales", "Additional notes"),
        value=st.session_state.cliente["notas"]
    )

    return st.session_state.cliente