# -*- coding: utf-8 -*-
# ElaFood - Proyecto de Comida Casera
# Módulo: estilo.py
# Descripción: Contiene funciones para el diseño y estilo de la aplicación.

import streamlit as st

from modules.imagenes import obtener_imagen


def estilos_app():
    """
    Debe llamarse justo después de st.set_page_config (nunca en import del módulo).

    Incluye: layout móvil, botones (selectores compatibles con Streamlit 1.5x),
    banner apilado en pantallas estrechas, controles del carrito más táctiles.
    """
    st.markdown(
        """
        <style>
        /* Contenedor principal */
        .block-container {
            padding-left: max(1rem, env(safe-area-inset-left)) !important;
            padding-right: max(1rem, env(safe-area-inset-right)) !important;
            padding-top: 0.75rem;
            padding-bottom: 1.5rem;
        }

        /*
         * Botones Streamlit 1.53+: el tema y el DOM ya no coinciden con "div.stButton > button".
         * Cubrimos varios data-testid y atributo kind.
         */
        .stApp [data-testid="stButton"] button,
        .stApp [data-testid="baseButton-secondary"],
        .stApp [data-testid="baseButton-primary"],
        .stApp button[kind="secondary"],
        .stApp button[kind="primary"] {
            background-color: #7A1F1F !important;
            color: #ffffff !important;
            padding: 12px 28px !important;
            border: none !important;
            border-radius: 8px !important;
            font-size: 18px !important;
            cursor: pointer !important;
            box-shadow: none !important;
        }
        .stApp [data-testid="stButton"] button:hover,
        .stApp [data-testid="baseButton-secondary"]:hover,
        .stApp [data-testid="baseButton-primary"]:hover,
        .stApp button[kind="secondary"]:hover,
        .stApp button[kind="primary"]:hover {
            background-color: #5e1717 !important;
            color: #ffffff !important;
        }
        /* Sidebar: mismos botones */
        section[data-testid="stSidebar"] [data-testid="stButton"] button,
        section[data-testid="stSidebar"] button[kind="secondary"],
        section[data-testid="stSidebar"] button[kind="primary"] {
            background-color: #7A1F1F !important;
            color: #ffffff !important;
            border: none !important;
        }

        @media (max-width: 768px) {
            /* number_input (cantidad en platos) */
            [data-testid="stNumberInput"] button {
                min-height: 44px !important;
                min-width: 44px !important;
                font-size: 1.1rem !important;
            }
            /* Carrito en sidebar: botones ➕ ➖ (mismo stButton) */
            section[data-testid="stSidebar"] [data-testid="stButton"] button {
                min-height: 44px !important;
                min-width: 44px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
        unsafe_allow_html=True,
    )

    # Tres columnas: logo | texto | redes + acerca de
    col1, col2, col3 = st.columns([1, 2, 2])

    # ------------------ COL 1: LOGO ------------------
    with col1:
        st.image(obtener_imagen("Imagenes/Logos/logo.jpg"), width=120)

    # ------------------ COL 2: TÍTULO Y ESLOGAN ------------------
    with col2:
        st.markdown(
            """
            <div style="color: #FFFFFF; font-size: 32px; font-weight: bold;">
                ElaFood
            </div>
            <div style="color: #F5E6E6; font-size: 16px; margin-top: -10px;">
                Food made with love
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ------------------ COL 3: REDES + ACERCA DE ------------------
    with col3:
        st.markdown(
            """
            <div style="text-align: right; color: #F5E6E6; font-size: 14px;">
                <b>Síguenos:</b><br>
                <a href="https://instagram.com/elafood" target="_blank" style="color:#FFFFFF;">Instagram</a> |
                <a href="https://facebook.com/elafood" target="_blank" style="color:#FFFFFF;">Facebook</a> |
                <a href="https://wa.me/17862361031" target="_blank" style="color:#FFFFFF;">WhatsApp</a>
                <br><br>
                <b>Acerca de:</b><br>
                ElaFood es un proyecto familiar creado con amor para ofrecer comida casera,
                fresca y deliciosa.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Cerrar contenedor
    st.markdown("</div>", unsafe_allow_html=True)


def boton_vino_tinto(texto, key=None):
    return st.button(
        texto,
        key=key,
        use_container_width=True,
        help="Acceso restringido",
    )
