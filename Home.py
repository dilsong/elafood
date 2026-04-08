import html

import streamlit as st

from modules.carrito import agregar, mostrar_carrito
from modules.cliente import formulario_cliente
from modules.config import (
    INTRO_PLATOS_SEMANA,
    INTRO_POSTRES_ESPECIALIDADES,
    RUTA_ICONO_APP,
    RUTA_ICONO_MINI_CARRITO,
    RUTA_LOGO_SALIDA,
    TELEFONO_ELAFOOD,
    TEXTO_AYUDA_CARRITO,
    URL_FACEBOOK,
    URL_INSTAGRAM,
    URL_QR_COMPARTIR,
    URL_WHATSAPP,
)
from modules.imagenes import src_para_html
from modules.estilo import cabecera_portada, estilos_app, expandir_sidebar_streamlit
from modules.menu_semana import DIAS_ORDEN, ETIQUETA_DIA, cargar_menu_semana
from modules.productos import PRODUCTOS
from modules.tarjetas import tarjeta_producto_hoy
from modules.whatsapp import generar_link_sms, generar_link_whatsapp, generar_mensaje

# SVG de iconos para botones de envío (más parecido a los logos del móvil).
WHATSAPP_SVG = (
    "<svg viewBox='0 0 24 24' aria-hidden='true'>"
    "<path d='M19.1 4.9A9.95 9.95 0 0 0 12 2C6.48 2 2 6.48 2 12c0 1.76.46 3.49 1.33 5.01L2 22l5.12-1.3A9.98 9.98 0 0 0 12 22c5.52 0 10-4.48 10-10 0-2.67-1.04-5.18-2.9-7.1zM12 20a7.93 7.93 0 0 1-4.04-1.1l-.29-.17-3.04.77.81-2.96-.19-.31A7.96 7.96 0 0 1 4 12c0-4.41 3.59-8 8-8 2.14 0 4.16.83 5.66 2.34A7.95 7.95 0 0 1 20 12c0 4.41-3.59 8-8 8zm4.39-5.73c-.24-.12-1.42-.7-1.64-.78-.22-.08-.38-.12-.54.12-.16.24-.62.78-.76.94-.14.16-.28.18-.52.06-.24-.12-1-.37-1.91-1.19-.71-.63-1.19-1.41-1.33-1.65-.14-.24-.01-.37.11-.49.11-.11.24-.28.36-.42.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.42-.06-.12-.54-1.3-.74-1.78-.2-.47-.4-.41-.54-.42h-.46c-.16 0-.42.06-.64.3-.22.24-.84.82-.84 2s.86 2.32.98 2.48c.12.16 1.69 2.58 4.1 3.62.57.25 1.02.4 1.37.51.58.18 1.1.16 1.52.1.46-.07 1.42-.58 1.62-1.14.2-.56.2-1.04.14-1.14-.06-.1-.22-.16-.46-.28z'/>"
    "</svg>"
)
SMS_SVG = (
    "<svg viewBox='0 0 24 24' aria-hidden='true'>"
    "<path d='M12 3c-4.97 0-9 3.58-9 8 0 2.2 1 4.2 2.66 5.64L5 21l4.03-2.01c.93.24 1.93.37 2.97.37 4.97 0 9-3.58 9-8s-4.03-8-9-8zm-4 8.5A1.5 1.5 0 1 1 8 8.5a1.5 1.5 0 0 1 0 3zm4 0A1.5 1.5 0 1 1 12 8.5a1.5 1.5 0 0 1 0 3zm4 0A1.5 1.5 0 1 1 16 8.5a1.5 1.5 0 0 1 0 3z'/>"
    "</svg>"
)


def _html_con_negritas_desde_markdown(texto: str) -> str:
    # Convierte pares **...** en <strong>...</strong> para el bloque HTML de ayuda.
    partes = texto.split("**")
    salida = []
    for i, parte in enumerate(partes):
        if i % 2 == 1:
            salida.append(f"<strong>{html.escape(parte)}</strong>")
        else:
            salida.append(html.escape(parte))
    return "".join(salida).replace("\n", "<br>")

# ---------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------------------------------------
st.set_page_config(
    page_title="ElaFood",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon=RUTA_ICONO_APP,
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    },
)
estilos_app()
st.markdown(
    "<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'>",
    unsafe_allow_html=True,
)
# Logo en sidebar sin usar st.logo (evita warning deprecado interno).
try:
    st.sidebar.image(RUTA_ICONO_APP, width=110)
except Exception:
    pass

if "vista_salida" not in st.session_state:
    st.session_state.vista_salida = False

if st.session_state.vista_salida:
    # Vista de despedida: muestra logo centrado + mensajes con colores solicitados.
    _src_logo_salida = html.escape(src_para_html(RUTA_LOGO_SALIDA), quote=True)
    st.markdown(
        "<div style='display:flex;justify-content:center;width:100%;margin:8px 0 8px 0;'>"
        f"<img src='{_src_logo_salida}' alt='ElaFood' style='width:170px;height:auto;display:block;'/>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h1 style='color:#91241D;text-align:center;'>¡Gracias por visitar ElaFood!</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='elafood-note' style='text-align:center;'>"
        "Ya puedes <strong>cerrar esta pestaña</strong> del navegador o volver cuando quieras."
        "</div>",
        unsafe_allow_html=True,
    )
    _src_qr = html.escape(URL_QR_COMPARTIR, quote=True)
    st.markdown(
        f"""
        <div style="text-align:center;margin:8px 0 8px 0;font-size:18px;">
            <a href="{URL_INSTAGRAM}" target="_blank" rel="noopener noreferrer" style="color:#91241D;font-weight:600;">Instagram</a>
            &nbsp;|&nbsp;
            <a href="{URL_FACEBOOK}" target="_blank" rel="noopener noreferrer" style="color:#91241D;font-weight:600;">Facebook</a>
            &nbsp;|&nbsp;
            <a href="{URL_WHATSAPP}" target="_blank" rel="noopener noreferrer" style="color:#91241D;font-weight:600;">WhatsApp</a>
            &nbsp;|&nbsp;
            <a href="{_src_qr}" target="_blank" rel="noopener noreferrer" style="color:#91241D;font-weight:600;">Compartir QR</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Volver a la tienda", type="primary", width="stretch"):
        st.session_state.vista_salida = False
        st.rerun()
    st.stop()

if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "mensaje_generado" not in st.session_state:
    st.session_state.mensaje_generado = ""

if "link" not in st.session_state:
    st.session_state.link = ""

if "link_sms" not in st.session_state:
    st.session_state.link_sms = ""

if "pedido_generado" not in st.session_state:
    st.session_state.pedido_generado = False

if "envio_confirmado" not in st.session_state:
    st.session_state.envio_confirmado = False

if "_flash_nuevo_pedido" not in st.session_state:
    st.session_state._flash_nuevo_pedido = False

cabecera_portada()

# Mini logo junto al control del sidebar (arriba izquierda, al lado de »/≡).
_src_badge = html.escape(src_para_html(RUTA_ICONO_APP), quote=True)
st.markdown(
    f"<div class='elafood-sidebar-badge'><img src='{_src_badge}' alt='Carrito ElaFood' /></div>",
    unsafe_allow_html=True,
)

st.markdown(
    f"<div class='elafood-note'>{_html_con_negritas_desde_markdown(TEXTO_AYUDA_CARRITO)}</div>",
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["Postres y Especialidades", "Platos de la Semana"])


def _render_platos_columna(dia: str, pids: list, titulo: str):
    if not pids:
        return
    st.markdown(f"### {titulo}")
    for pid in pids:
        if pid not in PRODUCTOS:
            st.error(f"Producto '{pid}' no existe en el catálogo.")
            continue
        p = PRODUCTOS[pid]
        key = f"sem_{dia}_{pid}"
        cantidad, agregar_btn = tarjeta_producto_hoy(
            p["nombre"],
            p["precio"],
            p["imagen"],
            p.get("descripcion", ""),
            key,
        )
        if agregar_btn and cantidad > 0:
            agregar(p["nombre"], cantidad, p["precio"], dia=dia)
            st.session_state["_flash_agregado_carrito"] = f"{cantidad}× {p['nombre']}"
            st.session_state["_expand_sidebar_tras_agregar"] = True

# =========================================================
# Postres y Especialidades (pestaña Esp. en Quienes Somos!)
# =========================================================
with tab1:
    st.markdown(INTRO_POSTRES_ESPECIALIDADES)
    st.markdown("---")

    data = cargar_menu_semana()
    esp = data.get("especial") or {"comidas": [], "postres": [], "otros": []}
    titulos_col = {"comidas": "Comidas", "postres": "Postres", "otros": "Otros"}

    alguno_esp = any(esp.get(k) for k in ("comidas", "postres", "otros"))

    if not alguno_esp:
        st.info(
            "Aún no hay platos en **Especial**. "
            "El chef puede cargarlos en **Quienes Somos!** → pestaña **Esp.**"
        )
    else:
        st.markdown(
            "<h2 style='color:#91241D;'>Especial</h2>",
            unsafe_allow_html=True,
        )
        for col_key in ("comidas", "postres", "otros"):
            _render_platos_columna(
                "especial",
                esp.get(col_key) or [],
                titulos_col[col_key],
            )
# =========================================================
# Platos de la Semana (Lun–Dom en Quienes Somos!)
# =========================================================
with tab2:
    st.markdown(INTRO_PLATOS_SEMANA)
    st.markdown("---")

    data = cargar_menu_semana()
    titulos_col = {"comidas": "Comidas", "postres": "Postres", "otros": "Otros"}

    alguno = any(
        any(data["dias"][d].get(k) for k in ("comidas", "postres", "otros"))
        for d in DIAS_ORDEN
    )

    if not alguno:
        st.info(
            "Aún no hay platos publicados para estos días. "
            "El chef puede configurarlos en la página **Quienes Somos!** (Lunes a Domingo)."
        )
    else:
        for dia in DIAS_ORDEN:
            bloque = data["dias"][dia]
            if not any(bloque.get(k) for k in ("comidas", "postres", "otros")):
                continue

            st.markdown(
                f"<h2 style='color:#91241D;margin-top:1.2rem;'>{ETIQUETA_DIA[dia]}</h2>",
                unsafe_allow_html=True,
            )
            for col_key in ("comidas", "postres", "otros"):
                _render_platos_columna(
                    dia,
                    bloque.get(col_key) or [],
                    titulos_col[col_key],
                )
# =========================================================
msg_flash = st.session_state.pop("_flash_agregado_carrito", None)
if msg_flash:
    _src_ico = html.escape(src_para_html(RUTA_ICONO_MINI_CARRITO), quote=True)
    _txt = html.escape(msg_flash)
    st.markdown(
        f'<div class="elafood-flash-carrito">'
        f'<img class="elafood-flash-carrito-ico" src="{_src_ico}" alt="" />'
        f"<span><strong>{_txt}</strong> — ¡Agregado al carrito!</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

if st.session_state.pop("_expand_sidebar_tras_agregar", False):
    expandir_sidebar_streamlit()

# =========================================================
# SIDEBAR (pedido) - flujo: generar -> enviar -> nuevo pedido
# =========================================================
total = mostrar_carrito()
cliente = formulario_cliente()

st.sidebar.markdown("---")

hay_productos = len(st.session_state.carrito) > 0

if not st.session_state.pedido_generado:
    generar = st.sidebar.button("Generar pedido", disabled=not hay_productos)
else:
    generar = False

if generar:
    if cliente["nombre"] == "":
        st.sidebar.warning("Por favor ingresa el nombre del cliente.")
    else:
        # Generar el contenido del pedido para WhatsApp y SMS.
        mensaje = generar_mensaje(st.session_state.carrito, total, cliente)
        st.session_state.mensaje_generado = mensaje
        st.session_state.link = generar_link_whatsapp(TELEFONO_ELAFOOD, mensaje)
        st.session_state.link_sms = generar_link_sms(TELEFONO_ELAFOOD, mensaje)

        st.session_state.pedido_generado = True
        st.session_state.envio_confirmado = False
        st.sidebar.markdown(
            "<div class='elafood-note'>Pedido generado. Elige WhatsApp o Mensaje de Texto.</div>",
            unsafe_allow_html=True,
        )

if st.session_state.pedido_generado and not st.session_state.envio_confirmado:
    c_wsp, c_msg = st.sidebar.columns(2)
    with c_wsp:
        st.markdown(
            (
                f"<a class='elafood-send-link' href='{st.session_state.link}' target='_blank'>"
                f"<span class='elafood-send-icon'>{WHATSAPP_SVG}</span>"
                "<span>WSP</span>"
                "</a>"
            ),
            unsafe_allow_html=True,
        )
    with c_msg:
        st.markdown(
            (
                f"<a class='elafood-send-link' href='{st.session_state.link_sms}' target='_blank'>"
                f"<span class='elafood-send-icon'>{SMS_SVG}</span>"
                "<span>MSG</span>"
                "</a>"
            ),
            unsafe_allow_html=True,
        )

    # Confirmación explícita para habilitar "Hacer nuevo pedido".
    if not st.session_state.envio_confirmado:
        if st.sidebar.button("Confirmar envío", width="stretch"):
            st.session_state.envio_confirmado = True
            st.rerun()

if st.session_state.envio_confirmado:
    if st.sidebar.button("Hacer nuevo pedido"):
        # Reinicia el flujo completo de pedido (mantiene datos del cliente).
        st.session_state.carrito = []
        st.session_state.mensaje_generado = ""
        st.session_state.link = ""
        st.session_state.link_sms = ""
        st.session_state.pedido_generado = False
        st.session_state.envio_confirmado = False
        st.session_state._flash_nuevo_pedido = True
        st.rerun()

if st.session_state.pop("_flash_nuevo_pedido", False):
    st.sidebar.markdown(
        "<div class='elafood-note'>Listo. Puedes comenzar un nuevo pedido.</div>",
        unsafe_allow_html=True,
    )

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Salir", width="stretch", help="Cierra el flujo y muestra despedida"):
    st.session_state.vista_salida = True
    st.rerun()
