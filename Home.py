import html
import json
import re

import streamlit as st
import streamlit.components.v1 as components

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
    TEXTO_AYUDA_CARRITO,
    URL_FACEBOOK,
    URL_INSTAGRAM,
    URL_QR_COMPARTIR,
    URL_WHATSAPP,
)
from modules.imagenes import src_para_html
from modules.pedidos_csv import registrar_pedido_csv
from modules.estilo import cabecera_portada, estilos_app, expandir_sidebar_streamlit
from modules.menu_semana import DIAS_ORDEN, ETIQUETA_DIA, cargar_menu_semana
from modules.productos import PRODUCTOS
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


def _abrir_url_mensajeria(url: str) -> None:
    """
    Abre wa.me / sms: en el mismo ciclo que el clic del botón (importante en móvil).
    Usa <a> programático + window.open + fallback a location (iframes de Streamlit).
    """
    if not url:
        return
    u = json.dumps(url)
    components.html(
        f"""
<script>
(function () {{
  var u = {u};
  function go() {{
    try {{
      var a = document.createElement("a");
      a.href = u;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.style.display = "none";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }} catch (e0) {{}}
    try {{
      var w = window.open(u, "_blank", "noopener,noreferrer");
      if (w) return;
    }} catch (e1) {{}}
    try {{
      if (window.top && window.top !== window) {{
        window.top.location.href = u;
        return;
      }}
    }} catch (e2) {{}}
    try {{
      if (window.parent && window.parent !== window) {{
        window.parent.location.href = u;
        return;
      }}
    }} catch (e3) {{}}
    try {{ window.location.href = u; }} catch (e4) {{}}
  }}
  go();
  setTimeout(go, 50);
  setTimeout(go, 200);
}})();
</script>
        """,
        height=48,
        width=1,
    )


TEXTOS = {
    "ES": {
        "tabs": ["Postres y\nEspecialidades", "Platos de\nla Semana"],
        "salir_titulo": "¡Gracias por visitar ElaFood!",
        "salir_msg": "Ya puedes cerrar esta pestaña del navegador o volver cuando quieras.",
        "volver": "Volver a la tienda",
        "generar": "Generar pedido",
        "confirmar": "Confirmar envío",
        "nuevo": "Hacer nuevo pedido",
        "salir": "🚪 Salir",
        "pedido_ok": (
            "Pedido listo. Elige WhatsApp o mensaje de texto; se guarda el pedido y se abre la app."
        ),
        "nombre_req": "Por favor ingresa el nombre del cliente.",
        "nuevo_ok": "Listo. Puedes comenzar un nuevo pedido.",
        "idioma": "Idioma / Language",
        "wsp": "WSP",
        "msg": "MSG",
        "gracias": "Gracias por preferirnos",
        "envio_siguiente": (
            "Tu pedido ya está guardado. Para que también llegue por WhatsApp o SMS al restaurante, "
            "toca el botón y envía el mensaje que se abre."
        ),
        "abrir_wsp": "Abrir WhatsApp",
        "abrir_sms": "Abrir SMS",
        "onb_title": "Instala ElaFood en tu teléfono",
        "onb_body": "Para acceso rápido, usa 'Añadir a pantalla de inicio' da click a los ... abajo a la derecha.",
        "onb_ios": "iPhone (Safari): Compartir → Ver mas -> Agregar a Inicio. -> Reemplaza Streamlit por ElaFood",
        "onb_android": "Android (Chrome): menú ⋮ → Añadir a pantalla de inicio.",
        "intro_postres": INTRO_POSTRES_ESPECIALIDADES,
        "intro_platos": INTRO_PLATOS_SEMANA,
        "esp_vacio": "Aún no hay platos en Especial. El chef puede cargarlos en Quienes Somos! → pestaña Esp.",
        "semana_vacio": "Aún no hay platos publicados para estos días. El chef puede configurarlos en Quienes Somos! (Lunes a Domingo).",
    },
    "EN": {
        "tabs": ["Desserts &\nSpecialties", "Weekly\nDishes"],
        "salir_titulo": "Thanks for visiting ElaFood!",
        "salir_msg": "You can close this browser tab now or come back anytime.",
        "volver": "Back to store",
        "generar": "Generate order",
        "confirmar": "Confirm send",
        "nuevo": "Start new order",
        "salir": "🚪 Exit",
        "pedido_ok": (
            "Order ready. Choose WhatsApp or text message; the order is saved and the app opens."
        ),
        "nombre_req": "Please enter customer name.",
        "nuevo_ok": "Done. You can start a new order.",
        "idioma": "Idioma / Language",
        "wsp": "WSP",
        "msg": "MSG",
        "gracias": "Thank you for choosing us",
        "envio_siguiente": (
            "Your order is saved. To also send it via WhatsApp or SMS, tap the button and send the message."
        ),
        "abrir_wsp": "Open WhatsApp",
        "abrir_sms": "Open SMS",
        "onb_title": "Install ElaFood on your phone",
        "onb_body": "For quick access, use 'Add to Home screen' from your browser menu.",
        "onb_ios": "iPhone (Safari): Share → Add to Home Screen.",
        "onb_android": "Android (Chrome): menu ⋮ → Add to Home screen.",
        "intro_postres": "Available by pre-order only. Every order is prepared in advance to ensure freshness and quality.",
        "intro_platos": "A different menu every week, with a special dish for each day. Receive ready-to-heat lunches and save time without giving up homemade flavor.",
        "esp_vacio": "There are no dishes in Special yet. The chef can load them in Who We Are! → Sp. tab.",
        "semana_vacio": "No dishes are published for these days yet. The chef can configure them in Who We Are! (Monday to Sunday).",
    },
}


def t(clave: str) -> str:
    # i18n desactivado temporalmente: se fuerza español por defecto.
    return TEXTOS["ES"].get(clave, clave)

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
st.session_state.lang = "ES"

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
            <a href="{_src_qr}" target="_blank" rel="noopener noreferrer" style="color:#9D1414;font-weight:600;">Compartir QR</a>
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

if "pedido_generado" not in st.session_state:
    st.session_state.pedido_generado = False

if "envio_confirmado" not in st.session_state:
    st.session_state.envio_confirmado = False
if "_flash_gracias" not in st.session_state:
    st.session_state._flash_gracias = False

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
        f"<div>{_html_con_negritas_desde_markdown(TEXTO_AYUDA_CARRITO)}</div>"
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

# Tras confirmar canal: enlaces reales (no iframe) — en móvil abren WhatsApp/SMS de forma fiable.
if st.session_state.envio_confirmado:
    _url_w = (st.session_state.get("link") or "").strip()
    _url_s = (st.session_state.get("link_sms") or "").strip()
    if _url_w or _url_s:
        st.success(t("gracias"))
        st.caption(t("envio_siguiente"))
        _c_w, _c_s = st.columns(2)
        with _c_w:
            if _url_w:
                st.link_button(
                    t("abrir_wsp"),
                    _url_w,
                    use_container_width=True,
                    type="primary",
                    key="hero_open_wsp",
                )
        with _c_s:
            if _url_s:
                st.link_button(
                    t("abrir_sms"),
                    _url_s,
                    use_container_width=True,
                    key="hero_open_sms",
                )
        st.markdown("---")

tab1, tab2 = st.tabs(t("tabs"))


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
    st.markdown(
        f"<div style='font-size:18px;line-height:1.55;'>{html.escape(t('intro_postres'))}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    data = cargar_menu_semana()
    esp = data.get("especial") or {"comidas": [], "postres": [], "otros": []}
    titulos_col = {"comidas": "Comidas", "postres": "Postres", "otros": "Otros"}

    alguno_esp = any(esp.get(k) for k in ("comidas", "postres", "otros"))

    if not alguno_esp:
        st.info(t("esp_vacio"))
    else:
        st.markdown(
            "<h2 style='color:#9D1414;'>Especial</h2>",
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
    titulos_col = {"comidas": "Comidas", "postres": "Postres", "otros": "Otros"}

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
                f"<h2 style='color:#9D1414;margin-top:1.2rem;'>{ETIQUETA_DIA[dia]}</h2>",
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
# SIDEBAR (pedido): generar -> WSP o MSG (guarda en datos + abre app) -> gracias / nuevo
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

if not st.session_state.pedido_generado:
    generar = st.sidebar.button(t("generar"), disabled=not hay_productos)
else:
    generar = False

if generar:
    nombre_ok = bool((cliente.get("nombre") or "").strip())
    if not nombre_ok or not telefono_ok:
        if not nombre_ok and not telefono_ok:
            st.sidebar.warning("Debes ingresar **Nombre** y **Teléfono** para generar el pedido.")
        elif not nombre_ok:
            st.sidebar.warning("Debes ingresar el **Nombre** para generar el pedido.")
        elif not tel_digits:
            st.sidebar.warning("Debes ingresar el **Teléfono** para generar el pedido.")
        elif not tel_coherente:
            st.sidebar.warning(
                "El **Teléfono** debe contener **solo números** (sin letras ni símbolos). "
                "Ej.: 7875551234 o 17875551234."
            )
        else:
            st.sidebar.warning(
                "El **Teléfono** debe tener **10 dígitos** (local) o **entre 11 y 15** (con código país)."
            )
    else:
        # Generar el contenido del pedido para WhatsApp y SMS.
        mensaje = generar_mensaje(st.session_state.carrito, total, cliente)
        st.session_state.mensaje_generado = mensaje
        st.session_state.link = generar_link_whatsapp(TELEFONO_ELAFOOD, mensaje)
        st.session_state.link_sms = generar_link_sms(TELEFONO_ELAFOOD, mensaje)

        st.session_state.pedido_generado = True
        st.session_state.envio_confirmado = False

if st.session_state.pedido_generado and not st.session_state.envio_confirmado:
    st.sidebar.markdown(
        f"<div class='elafood-note'>{t('pedido_ok')}</div>",
        unsafe_allow_html=True,
    )
    # Botones directos del sidebar (ancho completo): en móvil/Cloud enganchan mejor que columnas.
    if st.sidebar.button(
        f"{t('wsp')} — WhatsApp",
        key="btn_send_wsp",
        type="primary",
        use_container_width=True,
    ):
        if not telefono_ok:
            if not tel_digits:
                st.sidebar.warning("Debes ingresar el **Teléfono**.")
            elif not tel_coherente:
                st.sidebar.warning(
                    "El **Teléfono** solo números (sin letras). Ej.: 7875551234 o 17875551234."
                )
            else:
                st.sidebar.warning(
                    "El **Teléfono** debe tener 10 dígitos o entre 11 y 15 con código país."
                )
        else:
            registrar_cliente_csv(cliente, "WSP")
            ok_db, _err_db = registrar_pedido_supabase(st.session_state.carrito, cliente, "WSP")
            if not ok_db:
                registrar_pedido_csv(st.session_state.carrito, cliente, "WSP")
            notificar_chef_pedido(st.session_state.mensaje_generado, "WSP")
            st.session_state.envio_confirmado = True
            st.session_state._flash_gracias = True
            # Mismo ciclo que el clic: el móvil suele bloquear window.open tras st.rerun().
            _abrir_url_mensajeria(st.session_state.link)
            st.rerun()
    if st.sidebar.button(
        f"{t('msg')} — SMS",
        key="btn_send_msg",
        type="primary",
        use_container_width=True,
    ):
        if not telefono_ok:
            if not tel_digits:
                st.sidebar.warning("Debes ingresar el **Teléfono**.")
            elif not tel_coherente:
                st.sidebar.warning(
                    "El **Teléfono** solo números (sin letras). Ej.: 7875551234 o 17875551234."
                )
            else:
                st.sidebar.warning(
                    "El **Teléfono** debe tener 10 dígitos o entre 11 y 15 con código país."
                )
        else:
            registrar_cliente_csv(cliente, "MSG")
            ok_db, _err_db = registrar_pedido_supabase(st.session_state.carrito, cliente, "MSG")
            if not ok_db:
                registrar_pedido_csv(st.session_state.carrito, cliente, "MSG")
            notificar_chef_pedido(st.session_state.mensaje_generado, "MSG")
            st.session_state.envio_confirmado = True
            st.session_state._flash_gracias = True
            _abrir_url_mensajeria(st.session_state.link_sms)
            st.rerun()

if st.session_state.envio_confirmado:
    if st.session_state.pop("_flash_gracias", False):
        st.sidebar.markdown(
            f"<div class='elafood-note'>{t('gracias')}</div>",
            unsafe_allow_html=True,
        )
    _sw = (st.session_state.get("link") or "").strip()
    _ss = (st.session_state.get("link_sms") or "").strip()
    if _sw or _ss:
        st.sidebar.caption(t("envio_siguiente"))
        _s1, _s2 = st.sidebar.columns(2)
        with _s1:
            if _sw:
                st.link_button(t("abrir_wsp"), _sw, use_container_width=True, key="side_open_wsp")
        with _s2:
            if _ss:
                st.link_button(t("abrir_sms"), _ss, use_container_width=True, key="side_open_sms")
    if st.sidebar.button(t("nuevo")):
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
        f"<div class='elafood-note'>{t('nuevo_ok')}</div>",
        unsafe_allow_html=True,
    )

st.sidebar.markdown("---")
if st.sidebar.button(t("salir"), width="stretch", help="Cierra el flujo y muestra despedida"):
    st.session_state.vista_salida = True
    st.rerun()
