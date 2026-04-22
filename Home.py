import html
import re

import streamlit as st

from modules.carrito import agregar, mostrar_carrito
from modules.cliente import formulario_cliente
from modules.clientes_csv import registrar_cliente_csv
from modules.config import (
    INTRO_PLATOS_SEMANA,
    INTRO_POSTRES_ESPECIALIDADES,
    RUTA_ICONO_APP,
    RUTA_ICONO_MINI_CARRITO,
    RUTA_LOGO_SALIDA,
    TELEFONO_ELAFOOD,
    URL_FACEBOOK,
    URL_INSTAGRAM,
    URL_QR_COMPARTIR,
    URL_WHATSAPP,
)
from modules.imagenes import src_para_html
from modules.pedidos_csv import registrar_pedido_csv
from modules.estilo import cabecera_portada, estilos_app, expandir_sidebar_streamlit
from modules.menu_semana import DIAS_ORDEN, cargar_menu_semana, etiqueta_dia
from modules.productos import PRODUCTOS, descripcion_ui_producto, nombre_ui_producto
from modules.chef_notify import notificar_chef_pedido
from modules.supabase_store import registrar_pedido_supabase
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


def _solo_digitos_telefono(valor: str) -> str:
    return re.sub(r"\D+", "", valor or "")


def _telefono_valido(digitos: str) -> bool:
    # Acepta 10 dígitos locales o 11–15 con código país (solo dígitos).
    n = len(digitos)
    return n == 10 or (11 <= n <= 15)


def _telefono_coherente_solo_digitos(raw: str, digitos: str) -> bool:
    """True si lo escrito es exactamente el número (solo dígitos), sin letras ni símbolos extraídos."""
    return (raw or "").strip() == digitos


def _enlace_pedido_markdown(
    label: str,
    url: str,
    *,
    primario: bool,
    en_sidebar: bool = False,
) -> None:
    """
    Enlace tipo botón para wa.me / sms:. Evita st.link_button (en Cloud puede dar TypeError
    con sms: o con kwargs según versión). Use en_sidebar=True para el flujo post-Finalizar.
    """
    url = str(url or "").strip()
    if not url:
        return
    safe_url = html.escape(url, quote=True)
    safe_label = html.escape(label, quote=True)
    es_sms = url.lower().startswith("sms:")
    extra = "" if es_sms else ' target="_blank" rel="noopener noreferrer"'
    if primario:
        bg, fg = "#25D366", "#ffffff"
    else:
        bg, fg = "#5c636a", "#ffffff"
    _md = (
        f'<a href="{safe_url}"{extra} '
        f'style="display:block;text-align:center;padding:12px 14px;margin:10px 0 14px 0;'
        f"background:{bg};color:{fg};border-radius:8px;text-decoration:none;"
        f'font-weight:600;">{safe_label}</a>'
    )
    if en_sidebar:
        st.sidebar.markdown(_md, unsafe_allow_html=True)
    else:
        st.markdown(_md, unsafe_allow_html=True)


TEXTOS = {
    "ES": {
        "tabs": ["Postres y\nEspecialidades", "Platos de\nla Semana"],
        "salir_titulo": "¡Gracias por visitar ElaFood!",
        "salir_msg": "Ya puedes cerrar esta pestaña del navegador o volver cuando quieras.",
        "volver": "Volver a la tienda",
        "generar": "Generar pedido",
        "finalizar_pedido": "Finalizar pedido",
        "guardando_pedido": "Guardando tu pedido…",
        "instrucciones_pedido": (
            "Gracias por Preferirnos."
        ),
        "ayuda_carrito": (
            "Mira en el **Carrito** **»** arriba a la izquierda para abrir el **menú lateral**: "
            "allí verás tu **Pedido**; agrega productos, tus datos, elige **→ WSP** o **→ SMS** "
            "y pulsa **Finalizar pedido**."
        ),
        "canal_pedido_titulo": "Escoge una opción para enviar tu solicitud del pedido!",
        "opt_wsp": "→ WSP (WhatsApp)",
        "opt_msg": "→ SMS (Texto)",
        "confirmar": "Confirmar envío",
        "nuevo": "Hacer nuevo pedido",
        "salir": "🚪 Salir",
        "nombre_req": "Por favor ingresa el nombre del cliente.",
        "nuevo_ok": "Listo. Puedes comenzar un nuevo pedido.",
        "idioma": "Idioma / Language",
        "wsp": "WSP",
        "msg": "MSG",
        "gracias": "Gracias por preferirnos",
        "envio_siguiente": (
            "Tu pedido ya está guardado. Toca el botón de abajo para abrir la app con el mensaje listo; "
            "luego envíalo al restaurante."
        ),
        "abrir_wsp": "Abrir WSP",
        "abrir_sms": "Abrir SMS",
        "onb_title": "Instala ElaFood en tu teléfono",
        "onb_body": "Para acceso rápido, usa 'Añadir a pantalla de inicio' da click a los ... abajo a la derecha.",
        "onb_ios": "iPhone (Safari): Compartir → Ver mas -> Agregar a Inicio. -> Reemplaza Streamlit por ElaFood",
        "onb_android": "Android (Chrome): menú ⋮ → Añadir a pantalla de inicio.",
        "intro_postres": INTRO_POSTRES_ESPECIALIDADES,
        "intro_platos": INTRO_PLATOS_SEMANA,
        "col_comidas": "Comidas",
        "col_postres": "Postres",
        "col_otros": "Otros",
        "especial_titulo": "Especial",
        "esp_vacio": "Aún no hay platos en Especial. El chef puede cargarlos en Quienes Somos! → pestaña Esp.",
        "semana_vacio": "Aún no hay platos publicados para estos días. El chef puede configurarlos en Quienes Somos! (Lunes a Domingo).",
        "producto_no_existe": "Producto '{pid}' no existe en el catálogo.",
        "agregado_carrito": "¡Agregado al carrito!",
        "warn_producto_requerido": "Agrega al menos **un producto** al carrito.",
        "warn_nombre_telefono": "Debes ingresar **Nombre** y **Teléfono**.",
        "warn_nombre": "Debes ingresar el **Nombre**.",
        "warn_telefono": "Debes ingresar el **Teléfono**.",
        "warn_telefono_solo_numeros": "El **Teléfono** solo números (sin letras). Ej.: 7875551234 o 17875551234.",
        "warn_telefono_longitud": "El **Teléfono** debe tener 10 dígitos o entre 11 y 15 con código país.",
        "warn_link_no_generado": "No se pudo generar el enlace. Vuelve con **Hacer nuevo pedido** e inténtalo de nuevo.",
        "salir_help": "Cierra el flujo y muestra despedida",
        "social_qr": "Compartir QR",
    },
    "EN": {
        "tabs": ["Desserts &\nSpecialties", "Weekly\nDishes"],
        "salir_titulo": "Thanks for visiting ElaFood!",
        "salir_msg": "You can close this browser tab now or come back anytime.",
        "volver": "Back to store",
        "generar": "Generate order",
        "finalizar_pedido": "Complete order",
        "guardando_pedido": "Saving your order…",
        "instrucciones_pedido": "Add items, fill in your details, and choose one delivery channel below.",
        "ayuda_carrito": (
            "Check **Cart** **»** at the top-left to open the **side menu**: "
            "there you can review your **Order**, add your details, choose **→ WSP** or **→ SMS**, "
            "and tap **Complete order**."
        ),
        "canal_pedido_titulo": "How will you send the order to the restaurant?",
        "opt_wsp": "→ WSP (WhatsApp)",
        "opt_msg": "→ SMS",
        "confirmar": "Confirm send",
        "nuevo": "Start new order",
        "salir": "🚪 Exit",
        "nombre_req": "Please enter customer name.",
        "nuevo_ok": "Done. You can start a new order.",
        "idioma": "Idioma / Language",
        "wsp": "WSP",
        "msg": "MSG",
        "gracias": "Thank you for choosing us",
        "envio_siguiente": (
            "Your order is saved. Tap the button below to open the app with the message ready, then send it."
        ),
        "abrir_wsp": "Open WSP",
        "abrir_sms": "Open SMS",
        "onb_title": "Install ElaFood on your phone",
        "onb_body": "For quick access, use 'Add to Home screen' from your browser menu.",
        "onb_ios": "iPhone (Safari): Share → Add to Home Screen.",
        "onb_android": "Android (Chrome): menu ⋮ → Add to Home screen.",
        "intro_postres": "Available by pre-order only. Every order is prepared in advance to ensure freshness and quality.",
        "intro_platos": "A different menu every week, with a special dish for each day. Receive ready-to-heat lunches and save time without giving up homemade flavor.",
        "col_comidas": "Meals",
        "col_postres": "Desserts",
        "col_otros": "Others",
        "especial_titulo": "Special",
        "esp_vacio": "There are no dishes in Special yet. The chef can load them in Who We Are! → Sp. tab.",
        "semana_vacio": "No dishes are published for these days yet. The chef can configure them in Who We Are! (Monday to Sunday).",
        "producto_no_existe": "Product '{pid}' does not exist in the catalog.",
        "agregado_carrito": "Added to cart!",
        "warn_producto_requerido": "Add at least **one product** to the cart.",
        "warn_nombre_telefono": "Please enter **Name** and **Phone**.",
        "warn_nombre": "Please enter **Name**.",
        "warn_telefono": "Please enter **Phone**.",
        "warn_telefono_solo_numeros": "The **Phone** must contain only numbers. Ex.: 7875551234 or 17875551234.",
        "warn_telefono_longitud": "The **Phone** must have 10 digits or between 11 and 15 with country code.",
        "warn_link_no_generado": "Could not generate the link. Use **Start new order** and try again.",
        "salir_help": "Close flow and show farewell",
        "social_qr": "Share QR",
    },
}


def t(clave: str) -> str:
    lang = st.session_state.get("lang", "ES")
    if lang not in TEXTOS:
        lang = "ES"
    return TEXTOS[lang].get(clave, clave)

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
if "lang" not in st.session_state:
    st.session_state.lang = "ES"

_lang_opt = st.sidebar.selectbox(
    t("idioma"),
    options=["ES", "EN"],
    index=0 if st.session_state.lang == "ES" else 1,
    key="elafood_lang_selector",
)
if _lang_opt != st.session_state.lang:
    st.session_state.lang = _lang_opt
    st.rerun()

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
        f"<h1 style='color:#9D1414;text-align:center;'>{t('salir_titulo')}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='elafood-note' style='text-align:center;'>"
        f"{t('salir_msg')}"
        "</div>",
        unsafe_allow_html=True,
    )
    _src_qr = html.escape(URL_QR_COMPARTIR, quote=True)
    st.markdown(
        f"""
        <div style="text-align:center;margin:8px 0 8px 0;font-size:18px;">
            <a href="{URL_INSTAGRAM}" target="_blank" rel="noopener noreferrer" style="color:#9D1414;font-weight:600;">Instagram</a>
            &nbsp;|&nbsp;
            <a href="{URL_FACEBOOK}" target="_blank" rel="noopener noreferrer" style="color:#9D1414;font-weight:600;">Facebook</a>
            &nbsp;|&nbsp;
            <a href="{URL_WHATSAPP}" target="_blank" rel="noopener noreferrer" style="color:#9D1414;font-weight:600;">WhatsApp</a>
            &nbsp;|&nbsp;
            <a href="{_src_qr}" target="_blank" rel="noopener noreferrer" style="color:#9D1414;font-weight:600;">{t("social_qr")}</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(t("volver"), type="primary", width="stretch"):
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
    (
        f"<div class='elafood-note' style='display:flex;align-items:flex-start;gap:10px;'>"
        f"<img src='{_src_badge}' alt='Carrito ElaFood' "
        "style='width:22px;height:22px;border-radius:999px;flex-shrink:0;margin-top:2px;'/>"
        f"<div>{_html_con_negritas_desde_markdown(t('ayuda_carrito'))}</div>"
        "</div>"
    ),
    unsafe_allow_html=True,
)

# Onboarding cuando entra desde QR (?src=qr) o en primer ingreso.
_src_qr_param = str(st.query_params.get("src", "")).lower()
if _src_qr_param == "qr" and not st.session_state.get("_onb_seen"):
    st.markdown(
        (
            f"<div class='elafood-note'><strong>{t('onb_title')}</strong><br>"
            f"{t('onb_body')}<br>"
            f"• {t('onb_ios')}<br>"
            f"• {t('onb_android')}</div>"
        ),
        unsafe_allow_html=True,
    )
    st.session_state["_onb_seen"] = True

tab1, tab2 = st.tabs(t("tabs"))


def _render_platos_columna(dia: str, pids: list, titulo: str):
    if not pids:
        return
    st.markdown(f"### {titulo}")
    for pid in pids:
        if pid not in PRODUCTOS:
            st.error(t("producto_no_existe").format(pid=pid))
            continue
        p = PRODUCTOS[pid]
        nombre_ui = nombre_ui_producto(p)
        desc_ui = descripcion_ui_producto(p)
        key = f"sem_{dia}_{pid}"
        cantidad, agregar_btn = tarjeta_producto_hoy(
            nombre_ui,
            p["precio"],
            p["imagen"],
            desc_ui,
            key,
        )
        if agregar_btn and cantidad > 0:
            agregar(nombre_ui, cantidad, p["precio"], dia=dia)
            st.session_state["_flash_agregado_carrito"] = f"{cantidad}× {nombre_ui}"
            st.session_state["_expand_sidebar_tras_agregar"] = True

# =========================================================
# Postres y Especialidades (pestaña Esp. en Quienes Somos!)
# =========================================================
with tab1:
    st.markdown(
        f"<div style='font-size:18px;line-height:1.55;'>{html.escape(t('intro_postres'))}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    data = cargar_menu_semana()
    esp = data.get("especial") or {"comidas": [], "postres": [], "otros": []}
    titulos_col = {
        "comidas": t("col_comidas"),
        "postres": t("col_postres"),
        "otros": t("col_otros"),
    }

    alguno_esp = any(esp.get(k) for k in ("comidas", "postres", "otros"))

    if not alguno_esp:
        st.info(t("esp_vacio"))
    else:
        st.markdown(
            f"<h2 style='color:#9D1414;'>{t('especial_titulo')}</h2>",
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
    st.markdown(
        f"<div style='font-size:18px;line-height:1.55;'>{html.escape(t('intro_platos'))}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    data = cargar_menu_semana()
    titulos_col = {
        "comidas": t("col_comidas"),
        "postres": t("col_postres"),
        "otros": t("col_otros"),
    }

    alguno = any(
        any(data["dias"][d].get(k) for k in ("comidas", "postres", "otros"))
        for d in DIAS_ORDEN
    )

    if not alguno:
        st.info(t("semana_vacio"))
    else:
        for dia in DIAS_ORDEN:
            bloque = data["dias"][dia]
            if not any(bloque.get(k) for k in ("comidas", "postres", "otros")):
                continue

            st.markdown(
                f"<h2 style='color:#9D1414;margin-top:1.2rem;'>{etiqueta_dia(dia)}</h2>",
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
        f"<span><strong>{_txt}</strong> — {t('agregado_carrito')}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

if st.session_state.pop("_expand_sidebar_tras_agregar", False):
    expandir_sidebar_streamlit()

# =========================================================
# SIDEBAR (pedido): canal (radio) + Finalizar -> Supabase; gracias + un enlace al canal (sin auto-abrir)
# =========================================================
total = mostrar_carrito()
cliente = formulario_cliente()
# Valor tal cual en el campo (puede incluir letras; exigimos que coincida con solo dígitos para generar/enviar).
raw_tel = (st.session_state.get("_tel_input") or "").strip()
tel_digits = _solo_digitos_telefono(raw_tel)
st.session_state.cliente["telefono"] = tel_digits
cliente["telefono"] = tel_digits
tel_coherente = _telefono_coherente_solo_digitos(raw_tel, tel_digits)
telefono_ok = tel_coherente and _telefono_valido(tel_digits)

hay_productos = len(st.session_state.carrito) > 0

if not st.session_state.envio_confirmado:
    st.sidebar.markdown(
        f"<div class='elafood-note'>{html.escape(t('instrucciones_pedido'))}</div>",
        unsafe_allow_html=True,
    )
    # Solo una opción a la vez (radio mutuamente excluyente).
    _canal_elegido = st.sidebar.radio(
        t("canal_pedido_titulo"),
        options=["WSP", "MSG"],
        format_func=lambda c: t("opt_wsp") if c == "WSP" else t("opt_msg"),
        horizontal=True,
        key="elafood_canal_pedido",
    )
    if st.sidebar.button(
        t("finalizar_pedido"),
        key="btn_finalizar_pedido",
        type="primary",
        use_container_width=True,
        disabled=not hay_productos,
    ):
        nombre_ok = bool((cliente.get("nombre") or "").strip())
        if not hay_productos:
            st.sidebar.warning(t("warn_producto_requerido"))
        elif not nombre_ok and not telefono_ok:
            st.sidebar.warning(t("warn_nombre_telefono"))
        elif not nombre_ok:
            st.sidebar.warning(t("warn_nombre"))
        elif not tel_digits:
            st.sidebar.warning(t("warn_telefono"))
        elif not tel_coherente:
            st.sidebar.warning(t("warn_telefono_solo_numeros"))
        elif not telefono_ok:
            st.sidebar.warning(t("warn_telefono_longitud"))
        else:
            # Spinner nativo de Streamlit (texto + círculo); no interfiere con Supabase/CSV/notificación.
            with st.spinner(t("guardando_pedido")):
                mensaje = generar_mensaje(st.session_state.carrito, total, cliente)
                st.session_state.mensaje_generado = mensaje
                st.session_state.link = generar_link_whatsapp(TELEFONO_ELAFOOD, mensaje)
                st.session_state.link_sms = generar_link_sms(TELEFONO_ELAFOOD, mensaje)
                canal = (_canal_elegido or "WSP").strip().upper()
                if canal not in {"WSP", "MSG"}:
                    canal = "WSP"
                registrar_cliente_csv(cliente, canal)
                ok_db, _err_db = registrar_pedido_supabase(st.session_state.carrito, cliente, canal)
                if not ok_db:
                    registrar_pedido_csv(st.session_state.carrito, cliente, canal)
                notificar_chef_pedido(st.session_state.mensaje_generado, canal)
                st.session_state["_canal_final"] = canal
                st.session_state.envio_confirmado = True
            st.rerun()

if st.session_state.envio_confirmado:
    st.sidebar.markdown(
        f"<div class='elafood-note'>{t('gracias')}</div>",
        unsafe_allow_html=True,
    )
    st.sidebar.caption(t("envio_siguiente"))
    _canal_f = (st.session_state.get("_canal_final") or "WSP").strip().upper()
    _sw = (st.session_state.get("link") or "").strip()
    _ss = (st.session_state.get("link_sms") or "").strip()
    _url_fb = _sw if _canal_f == "WSP" else _ss
    _lbl = t("abrir_wsp") if _canal_f == "WSP" else t("abrir_sms")
    if _url_fb:
        _enlace_pedido_markdown(
            _lbl,
            _url_fb,
            primario=(_canal_f == "WSP"),
            en_sidebar=True,
        )
    else:
        st.sidebar.warning(t("warn_link_no_generado"))
    if st.sidebar.button(
        t("nuevo"),
        key="elafood_btn_nuevo_pedido",
        use_container_width=True,
    ):
        st.session_state.carrito = []
        st.session_state.mensaje_generado = ""
        st.session_state.link = ""
        st.session_state.link_sms = ""
        st.session_state.envio_confirmado = False
        st.session_state.pop("_canal_final", None)
        st.session_state.elafood_canal_pedido = "WSP"
        st.session_state._flash_nuevo_pedido = True
        st.rerun()

if st.session_state.pop("_flash_nuevo_pedido", False):
    st.sidebar.markdown(
        f"<div class='elafood-note'>{t('nuevo_ok')}</div>",
        unsafe_allow_html=True,
    )

st.sidebar.markdown("---")
if st.sidebar.button(t("salir"), width="stretch", help=t("salir_help")):
    st.session_state.vista_salida = True
    st.rerun()
