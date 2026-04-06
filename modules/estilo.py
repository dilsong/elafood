# -*- coding: utf-8 -*-
# ElaFood - Proyecto de Comida Casera
# Módulo: estilo.py
# Descripción: Contiene funciones para el diseño y estilo de la aplicación.

import streamlit as st

from modules.imagenes import obtener_imagen, src_para_html

from modules.config import (
    RUTA_IMAGEN_PORTADA,
    URL_FACEBOOK,
    URL_INSTAGRAM,
    URL_WHATSAPP,
)


def estilos_app():
    """
    Debe llamarse justo después de st.set_page_config (nunca en import del módulo).

    Incluye: layout móvil, botones (Streamlit 1.5x), carrito compacto en sidebar.
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
        /* Sidebar: botones (Generar pedido, Salir, Vaciar…) — compactos, sin forzar alturas grandes */
        section[data-testid="stSidebar"] [data-testid="stButton"] button,
        section[data-testid="stSidebar"] button[kind="secondary"],
        section[data-testid="stSidebar"] button[kind="primary"] {
            background-color: #7A1F1F !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 8px 14px !important;
            font-size: 15px !important;
        }

        /* Carrito: number_input delgado; no inflar el sidebar */
        section[data-testid="stSidebar"] [data-testid="stNumberInput"] {
            margin-top: 0 !important;
            margin-bottom: 0.35rem !important;
        }
        section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
            min-height: 28px !important;
            min-width: 28px !important;
            max-height: 32px !important;
            padding: 0 6px !important;
            font-size: 0.9rem !important;
        }
        section[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
            font-size: 0.95rem !important;
            padding: 4px 6px !important;
        }

        /* Quita el adorno gráfico de Streamlit arriba a la derecha (no el menú completo). */
        [data-testid="stDecoration"] {
            display: none !important;
        }

        /* Pestañas principales (Esta Semana! / Menú) */
        .stTabs [data-baseweb="tab"] {
            font-size: 1.2rem !important;
            font-weight: 600 !important;
        }
        div[data-testid="stTabs"] button[data-baseweb="tab"] {
            font-size: 1.2rem !important;
            font-weight: 600 !important;
        }

        @media (max-width: 768px) {
            /* Cantidad en fichas de platos (área principal): táctil cómodo */
            section.main [data-testid="stNumberInput"] button {
                min-height: 30px !important;
                min-width: 30px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def cabecera_portada():
    """
    Imagen principal + redes; debajo van las pestañas (Streamlit) en Home.
    """
    st.image(obtener_imagen(RUTA_IMAGEN_PORTADA), use_container_width=True)
    st.markdown(
        f"""
        <div class="elafood-redes" style="text-align:center;margin:10px 0 6px 0;font-size:18px;">
            <a href="{URL_INSTAGRAM}" target="_blank" rel="noopener noreferrer" style="color:#7A1F1F;font-weight:600;">Instagram</a>
            &nbsp;|&nbsp;
            <a href="{URL_FACEBOOK}" target="_blank" rel="noopener noreferrer" style="color:#7A1F1F;font-weight:600;">Facebook</a>
            &nbsp;|&nbsp;
            <a href="{URL_WHATSAPP}" target="_blank" rel="noopener noreferrer" style="color:#7A1F1F;font-weight:600;">WhatsApp</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def banner():
    """
    Un solo bloque HTML: en Streamlit, st.columns NO quedan dentro del <div> de un
    st.markdown anterior, así que el fondo vino no cubría logo ni enlaces. Aquí todo va junto.
    """
    logo_src = src_para_html("Imagenes/Logos/IMG_5894.jpg")

    st.markdown(
        f"""
        <style>
            .elafood-banner {{
                width: 100%;
                background-color: #7A1F1F;
                padding: 18px 16px;
                border-radius: 10px;
                box-sizing: border-box;
            }}
            .elafood-banner-inner {{
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: space-between;
                gap: 16px 24px;
                max-width: 1100px;
                margin: 0 auto;
            }}
            .elafood-banner-logo img {{
                display: block;
                width: 120px;
                height: 120px;
                object-fit: cover;
                border-radius: 50%;
                border: 3px solid rgba(255,255,255,0.35);
            }}
            .elafood-banner-title {{
                color: #FFFFFF;
                font-size: clamp(1.5rem, 4vw, 2rem);
                font-weight: 700;
                line-height: 1.2;
                margin: 0;
            }}
            .elafood-banner-tagline {{
                color: #FFF8F0;
                font-size: clamp(0.9rem, 2.5vw, 1rem);
                margin: 4px 0 0 0;
                opacity: 0.95;
            }}
            .elafood-banner-mid {{
                flex: 1 1 200px;
                min-width: 160px;
            }}
            .elafood-banner-social {{
                flex: 1 1 240px;
                text-align: right;
                color: #FFF8F0;
                font-size: 14px;
                line-height: 1.5;
            }}
            .elafood-banner-social a {{
                color: #FFFFFF !important;
                font-weight: 600;
                text-decoration: underline;
                text-underline-offset: 2px;
            }}
            .elafood-banner-social a:hover {{
                color: #FFD6D6 !important;
            }}
            .elafood-banner-social strong {{
                color: #FFFFFF;
            }}
            @media (max-width: 768px) {{
                .elafood-banner-inner {{
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                }}
                .elafood-banner-social {{
                    text-align: center;
                }}
            }}
        </style>
        <div class="elafood-banner">
            <div class="elafood-banner-inner">
                <div class="elafood-banner-logo">
                    <img src="{logo_src}" alt="ElaFood" />
                </div>
                <div class="elafood-banner-mid">
                    <p class="elafood-banner-title">ElaFood</p>
                    <p class="elafood-banner-tagline">Food made with love</p>
                </div>
                <div class="elafood-banner-social">
                    <strong>Síguenos:</strong><br />
                    <a href="https://instagram.com/elafood" target="_blank" rel="noopener noreferrer">Instagram</a>
                    &nbsp;|&nbsp;
                    <a href="https://facebook.com/elafood" target="_blank" rel="noopener noreferrer">Facebook</a>
                    &nbsp;|&nbsp;
                    <a href="https://wa.me/17862361031" target="_blank" rel="noopener noreferrer">WhatsApp</a>
                    <br /><br />
                    <strong>Acerca de:</strong><br />
                    ElaFood es un proyecto familiar creado con amor para ofrecer comida casera,
                    fresca y deliciosa.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def boton_vino_tinto(texto, key=None):
    return st.button(
        texto,
        key=key,
        use_container_width=True,
        help="Acceso restringido",
    )
