import streamlit as st

def formulario_cliente():
    st.sidebar.markdown("### Datos del cliente")

    if "cliente" not in st.session_state:
        st.session_state.cliente = {
            "nombre": "",
            "telefono": "",
            "direccion": "",
            "notas": ""
        }

    st.session_state.cliente["nombre"] = st.sidebar.text_input(
        "Nombre",
        value=st.session_state.cliente["nombre"]
    )

    st.session_state.cliente["telefono"] = st.sidebar.text_input(
        "Teléfono",
        value=st.session_state.cliente["telefono"]
    )

    st.session_state.cliente["direccion"] = st.sidebar.text_area(
        "Dirección",
        value=st.session_state.cliente["direccion"]
    )

    st.session_state.cliente["notas"] = st.sidebar.text_area(
        "Notas adicionales",
        value=st.session_state.cliente["notas"]
    )

    return st.session_state.cliente