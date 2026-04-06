import html

import streamlit as st

from modules.carrito import agregar, mostrar_carrito
from modules.cliente import formulario_cliente
from modules.config import (
    INTRO_PLATOS_SEMANA,
    INTRO_POSTRES_ESPECIALIDADES,
    RUTA_ICONO_APP,
    RUTA_ICONO_MINI_CARRITO,
    TELEFONO_ELAFOOD,
    TEXTO_AYUDA_CARRITO,
    URL_SALIR_DESTINO,
)
from modules.imagenes import src_para_html
from modules.estilo import cabecera_portada, estilos_app, expandir_sidebar_streamlit
from modules.menu_semana import DIAS_ORDEN, ETIQUETA_DIA, cargar_menu_semana
from modules.productos import PRODUCTOS
from modules.tarjetas import tarjeta_producto_hoy
from modules.whatsapp import generar_link_whatsapp, generar_mensaje

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
if hasattr(st, "logo"):
    try:
        st.logo(RUTA_ICONO_APP)
    except Exception:
        pass

if "vista_salida" not in st.session_state:
    st.session_state.vista_salida = False

if st.session_state.vista_salida:
    st.markdown(
        "<h1 style='color:#7A1F1F;text-align:center;'>¡Gracias por visitar ElaFood!</h1>",
        unsafe_allow_html=True,
    )
    st.info("Ya puedes **cerrar esta pestaña** del navegador o volver cuando quieras.")
    if URL_SALIR_DESTINO and URL_SALIR_DESTINO.strip():
        st.link_button("Seguir a ElaFood en redes / web →", URL_SALIR_DESTINO.strip())
    if st.button("Volver a la tienda", type="primary"):
        st.session_state.vista_salida = False
        st.rerun()
    st.stop()

if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "mensaje_generado" not in st.session_state:
    st.session_state.mensaje_generado = ""

if "link" not in st.session_state:
    st.session_state.link = ""

if "pedido_generado" not in st.session_state:
    st.session_state.pedido_generado = False

cabecera_portada()

st.info(TEXTO_AYUDA_CARRITO, icon="🛒")

tab1, tab2 = st.tabs(["Platos de la Semana", "Postres y Especialidades"])


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
# Platos de la Semana (Lun–Dom en Chef)
# =========================================================
with tab1:
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
            "El chef puede configurarlos en la página **Chef** (Lunes a Domingo)."
        )
    else:
        for dia in DIAS_ORDEN:
            bloque = data["dias"][dia]
            if not any(bloque.get(k) for k in ("comidas", "postres", "otros")):
                continue

            st.markdown(
                f"<h2 style='color:#7A1F1F;margin-top:1.2rem;'>{ETIQUETA_DIA[dia]}</h2>",
                unsafe_allow_html=True,
            )
            for col_key in ("comidas", "postres", "otros"):
                _render_platos_columna(
                    dia,
                    bloque.get(col_key) or [],
                    titulos_col[col_key],
                )


# =========================================================
# Postres y Especialidades (pestaña Esp. en Chef)
# =========================================================
with tab2:
    st.markdown(INTRO_POSTRES_ESPECIALIDADES)
    st.markdown("---")

    data = cargar_menu_semana()
    esp = data.get("especial") or {"comidas": [], "postres": [], "otros": []}
    titulos_col = {"comidas": "Comidas", "postres": "Postres", "otros": "Otros"}

    alguno_esp = any(esp.get(k) for k in ("comidas", "postres", "otros"))

    if not alguno_esp:
        st.info(
            "Aún no hay platos en **Especial**. "
            "El chef puede cargarlos en **Chef** → pestaña **Esp.**"
        )
    else:
        st.markdown(
            "<h2 style='color:#7A1F1F;'>Especial</h2>",
            unsafe_allow_html=True,
        )
        for col_key in ("comidas", "postres", "otros"):
            _render_platos_columna(
                "especial",
                esp.get(col_key) or [],
                titulos_col[col_key],
            )

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
# SIDEBAR (pedido)
# =========================================================
total = mostrar_carrito()
cliente = formulario_cliente()

st.sidebar.markdown("---")

hay_productos = len(st.session_state.carrito) > 0

if hay_productos and not st.session_state.pedido_generado:
    generar = st.sidebar.button("Generar pedido")
else:
    generar = False

if generar:
    if cliente["nombre"] == "":
        st.sidebar.warning("Por favor ingresa el nombre del cliente.")
    else:
        mensaje = generar_mensaje(st.session_state.carrito, total, cliente)
        st.session_state.mensaje_generado = mensaje
        st.session_state.link = generar_link_whatsapp(TELEFONO_ELAFOOD, mensaje)

        st.session_state.pedido_generado = True
        st.sidebar.success("Pedido generado. Presione Enviar por WS.")

if st.session_state.pedido_generado:
    st.sidebar.markdown(
        f"<a href='{st.session_state.link}' target='_blank' style='padding:12px; background:#25D366; color:white; border-radius:8px; text-decoration:none; display:block; text-align:center;'>📲 Enviar por WhatsApp</a>",
        unsafe_allow_html=True,
    )

if st.sidebar.button("Hacer nuevo pedido"):
    st.session_state.carrito = []
    st.session_state.mensaje_generado = ""
    st.session_state.link = ""
    st.session_state.pedido_generado = False
    st.sidebar.success("Listo. Puedes comenzar un nuevo pedido.")

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Salir", use_container_width=True, help="Cierra el flujo y muestra despedida"):
    st.session_state.vista_salida = True
    st.rerun()
