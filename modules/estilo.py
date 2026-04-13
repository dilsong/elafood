# -*- coding: utf-8 -*-
# ElaFood - Proyecto de Comida Casera
# Módulo: estilo.py
# Descripción: Contiene funciones para el diseño y estilo de la aplicación.

import streamlit as st
import streamlit.components.v1 as components

from modules.imagenes import obtener_imagen, src_para_html

from modules.config import (
    FONT_SCALE,
    RUTA_IMAGEN_PORTADA,
    URL_QR_COMPARTIR,
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
        /* Tipografía base (ajusta FONT_SCALE en modules/config.py) */
        html {
            font-size: calc(16px * __FONT_SCALE__) !important;
        }
        .stApp, .stApp p, .stApp li, .stApp label {
            font-size: 1rem !important;
        }

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
            background-color: #9D1414 !important;
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
            background-color: #9D1414 !important;
            color: #ffffff !important;
        }
        /* Sidebar: botones a ancho completo y texto centrado (p. ej. Hacer nuevo pedido, Finalizar…) */
        section[data-testid="stSidebar"] [data-testid="stButton"] {
            width: 100% !important;
        }
        section[data-testid="stSidebar"] [data-testid="stButton"] button,
        section[data-testid="stSidebar"] button[kind="secondary"],
        section[data-testid="stSidebar"] button[kind="primary"] {
            width: 100% !important;
            max-width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            text-align: center !important;
            background-color: #9D1414 !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 8px 14px !important;
            font-size: 15px !important;
        }

        /* Enlaces WSP/MSG (markdown en sidebar): mismo look que botones ElaFood; móvil/Safari suelen forzar color de <a> */
        section[data-testid="stSidebar"] a.elafood-channel-btn,
        section[data-testid="stSidebar"] a.elafood-channel-btn:link,
        section[data-testid="stSidebar"] a.elafood-channel-btn:visited,
        section[data-testid="stSidebar"] a.elafood-channel-btn:hover,
        section[data-testid="stSidebar"] a.elafood-channel-btn:active {
            background-color: #9D1414 !important;
            background: #9D1414 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            border: none !important;
            text-decoration: none !important;
            font-weight: 600 !important;
        }
        section[data-testid="stSidebar"] a.elafood-channel-btn:hover {
            background-color: #761d17 !important;
            background: #761d17 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p a.elafood-channel-btn,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] a.elafood-channel-btn {
            background-color: #9D1414 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        /* Aire entre fila WSP/MSG (markdown) y el botón «Ya envié» de Streamlit */
        section[data-testid="stSidebar"] .elafood-channel-row {
            margin-bottom: 1.15rem !important;
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

        /* Pestañas: dos líneas sin recortar texto (altura automática + fuente algo menor) */
        div[data-testid="stTabs"] [role="tablist"] {
            gap: 0.35rem !important;
        }
        .stTabs [data-baseweb="tab"],
        div[data-testid="stTabs"] button[data-baseweb="tab"] {
            font-size: 1.28rem !important;
            font-weight: 600 !important;
            padding: 0.45rem 0.55rem !important;
            min-height: 3.1rem !important;
            height: auto !important;
            min-width: 0 !important;
            flex: 1 1 0 !important;
            color: #9D1414 !important;
            line-height: 1.22 !important;
            white-space: pre-line !important;
            text-align: center !important;
            overflow: visible !important;
            align-items: center !important;
        }
        div[data-testid="stTabs"] [data-baseweb="tab"] p,
        div[data-testid="stTabs"] button[data-baseweb="tab"] p {
            font-size: 1.28rem !important;
            color: #9D1414 !important;
            line-height: 1.22 !important;
            white-space: pre-line !important;
            text-align: center !important;
            overflow: visible !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] p {
            color: #9D1414 !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            background: #E5CDC1 !important;
            border-radius: 8px 8px 0 0 !important;
            border-bottom: 3px solid #9D1414 !important;
        }

        /* Mensajes tipo "info" personalizados (fondo y letras solicitados) */
        .elafood-note {
            background: #E5CDC1 !important;
            color: #9D1414 !important;
            border: 1px solid #E5CDC1 !important;
            border-radius: 10px !important;
            padding: 12px 14px !important;
            margin: 8px 0 12px 0 !important;
            line-height: 1.45 !important;
        }
        .elafood-note strong {
            color: #9D1414 !important;
        }

        /* Links de envío en sidebar */
        .elafood-send-link {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 10px !important;
            padding: 10px 12px !important;
            margin: 6px 0 !important;
            border-radius: 10px !important;
            text-decoration: none !important;
            background: #9D1414 !important;
            color: #fff !important;
            font-weight: 600 !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        .elafood-send-link:hover {
            background: #9D1414 !important;
            color: #fff !important;
        }
        .elafood-send-icon {
            width: 30px !important;
            height: 30px !important;
            border-radius: 999px !important;
            background: #fff !important;
            color: #9D1414 !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 17px !important;
            line-height: 1 !important;
            flex-shrink: 0 !important;
        }
        .elafood-send-icon svg {
            width: 18px !important;
            height: 18px !important;
            fill: #9D1414 !important;
            display: block !important;
        }

        /* Mini logo junto al control del sidebar (arriba izquierda) */
        .elafood-sidebar-badge {
            position: fixed !important;
            top: 0.56rem !important;
            left: 2.55rem !important;
            z-index: 999991 !important;
            width: 26px !important;
            height: 26px !important;
            border-radius: 999px !important;
            overflow: hidden !important;
            border: 2px solid #fff !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
            pointer-events: none !important;
        }
        .elafood-sidebar-badge img {
            width: 100% !important;
            height: 100% !important;
            object-fit: cover !important;
            display: block !important;
        }

        /* En móvil, centrar imagen cuando columnas se apilan */
        section.main [data-testid="stImage"] img {
            display: block !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        /* Aviso al agregar: debajo de la barra (no tapa «» del sidebar) */
        .elafood-flash-carrito {
            position: fixed !important;
            top: 3.85rem !important;
            left: 0.5rem !important;
            right: auto !important;
            z-index: 999990 !important;
            background: #9D1414 !important;
            color: #fff !important;
            padding: 10px 14px !important;
            border-radius: 10px !important;
            font-size: 0.95rem !important;
            box-shadow: 0 4px 14px rgba(0,0,0,0.25) !important;
            max-width: min(92vw, 360px) !important;
            line-height: 1.35 !important;
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
        }
        .elafood-flash-carrito-ico {
            width: 26px !important;
            height: 26px !important;
            object-fit: contain !important;
            flex-shrink: 0 !important;
        }

        @media (max-width: 768px) {
            /* Cantidad en fichas de platos (área principal): táctil cómodo */
            section.main [data-testid="stNumberInput"] button {
                min-height: 30px !important;
                min-width: 30px !important;
            }
        }
        </style>
        """.replace("__FONT_SCALE__", str(FONT_SCALE)),
        unsafe_allow_html=True,
    )


def expandir_sidebar_streamlit():
    """
    Abre el panel lateral si está colapsado (equivalente a pulsar » / ≡).
    Depende del DOM de Streamlit; si falla en una versión, el usuario sigue pudiendo abrir a mano.
    """
    components.html(
        """
        <script>
        const doc = window.parent.document;
        const q = [
            '[data-testid="collapsedControl"]',
            'button[aria-label="Open sidebar"]',
            'button[aria-label="View sidebar"]',
            'button[title="View sidebar"]',
        ];
        for (const s of q) {
            const b = doc.querySelector(s);
            if (b) { b.click(); break; }
        }
        </script>
        """,
        height=0,
        width=0,
    )


def cabecera_portada():
    """
    Imagen principal + redes; debajo van las pestañas (Streamlit) en Home.
    """
    st.image(obtener_imagen(RUTA_IMAGEN_PORTADA), width="stretch")
    qr_src = URL_QR_COMPARTIR
    st.markdown(
        f"""
        <div class="elafood-redes" style="text-align:center;margin:10px 0 6px 0;font-size:18px;">
            <a href="{URL_INSTAGRAM}" target="_blank" rel="noopener noreferrer" style="color:#9D1414;font-weight:600;">Instagram</a>
            &nbsp;|&nbsp;
            <a href="{URL_FACEBOOK}" target="_blank" rel="noopener noreferrer" style="color:#9D1414;font-weight:600;">Facebook</a>
            &nbsp;|&nbsp;
            <a href="{URL_WHATSAPP}" target="_blank" rel="noopener noreferrer" style="color:#9D1414;font-weight:600;">WhatsApp</a>
            &nbsp;|&nbsp;
            <a href="{qr_src}" target="_blank" rel="noopener noreferrer" style="color:#9D1414;font-weight:600;">Compartir QR</a>
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
                background-color: #9D1414;
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
        width="stretch",
        help="Acceso restringido",
    )
