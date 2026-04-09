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

    st.session_state.cliente["telefono"] = st.sidebar.text_input(
        tr("Teléfono", "Phone"),
        value=st.session_state.cliente["telefono"]
    )

    st.session_state.cliente["direccion"] = st.sidebar.text_area(
        tr("Dirección", "Address"),
        value=st.session_state.cliente["direccion"]
    )

    st.session_state.cliente["notas"] = st.sidebar.text_area(
        tr("Notas adicionales", "Additional notes"),
        value=st.session_state.cliente["notas"]
    )

    return st.session_state.cliente