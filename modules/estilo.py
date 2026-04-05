# -*- coding: utf-8 -*-
# ElaFood - Proyecto de Comida Casera
# Módulo: estilo.py
# Descripción: Contiene funciones para el diseño y estilo de la aplicación.

import streamlit as st

def banner():
    # Contenedor principal vino tinto
    st.markdown(
        """
        <div style="
            width: 100%;
            background-color: #7A1F1F;
            padding: 20px;
            border-radius: 10px;
        ">
        """,
        unsafe_allow_html=True
    )

    # Tres columnas: logo | texto | redes + acerca de
    col1, col2, col3 = st.columns([1, 2, 2])

    # ------------------ COL 1: LOGO ------------------
    with col1:
        st.image("Imagenes/Logos/logo.jpg", width=120)

    # ------------------ COL 2: TÍTULO Y ESLOGAN ------------------
    with col2:
        st.markdown(
            """
            <div style="color: #7A1F1F; font-size: 32px; font-weight: bold;">
                ElaFood
            </div>
            <div style="color: #7A1F1F; font-size: 16px; margin-top: -10px;">
                Food made with love
            </div>
            """,
            unsafe_allow_html=True
        )

    # ------------------ COL 3: REDES + ACERCA DE ------------------
    with col3:
        st.markdown(
            """
            <div style="text-align: right; color: #7A1F1F; font-size: 14px;">
                <b>Síguenos:</b><br>
                <a href="https://instagram.com/elafood" target="_blank" style="color:#7A1F1F;">Instagram</a> |
                <a href="https://facebook.com/elafood" target="_blank" style="color:#7A1F1F;">Facebook</a> |
                <a href="https://wa.me/17862361031" target="_blank" style="color:#7A1F1F;">WhatsApp</a>
                <br><br>
                <b>Acerca de:</b><br>
                ElaFood es un proyecto familiar creado con amor para ofrecer comida casera,
                fresca y deliciosa.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Cerrar contenedor
    st.markdown("</div>", unsafe_allow_html=True)

# ESTILO PARA BOTONES PERSONALIZADOS
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color:#7A1F1F !important;
        color:white !important;
        padding:12px 28px !important;
        border:none !important;
        border-radius:8px !important;
        font-size:18px !important;
        cursor:pointer !important;
    }
    div.stButton > button:hover {
        background-color:#5e1717 !important;
        color:white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def boton_vino_tinto(texto, key=None):
    return st.button(
        texto,
        key=key,
        use_container_width=True,
        help="Acceso restringido",
    )

