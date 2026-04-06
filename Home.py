import streamlit as st

from modules.carrito import agregar, mostrar_carrito
from modules.cliente import formulario_cliente
from modules.config import RUTA_ICONO_APP, TELEFONO_ELAFOOD, URL_SALIR_DESTINO
from modules.estilo import cabecera_portada, estilos_app
from modules.menu import mostrar_filtro_categoria_semana
from modules.menu_semana import DIAS_ORDEN, ETIQUETA_DIA, cargar_menu_semana
from modules.productos import PRODUCTOS
from modules.tarjetas import tarjeta_producto, tarjeta_producto_hoy
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

filtro_columna = mostrar_filtro_categoria_semana()

tab1, tab2 = st.tabs(["Esta Semana!", "Menú"])


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
            st.toast(
                f"Listo: {cantidad}× {p['nombre']} en el carrito",
                icon="✅",
            )


# =========================================================
# ESTA SEMANA
# =========================================================
with tab1:
    data = cargar_menu_semana()
    titulos = {"comidas": "Comidas", "postres": "Postres", "otros": "Otros"}

    alguno_en_filtro = any(
        (data["dias"][d].get(filtro_columna) or []) for d in DIAS_ORDEN
    )
    alguno_en_semana = any(
        any(data["dias"][d].get(k) for k in ("comidas", "postres", "otros"))
        for d in DIAS_ORDEN
    )

    if not alguno_en_semana:
        st.info(
            "Aún no hay platos publicados para esta semana. "
            "El chef puede configurarlos en la página **Chef**."
        )
    elif not alguno_en_filtro:
        st.info(
            f"No hay **{titulos[filtro_columna]}** publicados en ningún día. "
            "Elige otra categoría en el menú lateral o pide al chef que complete esa columna."
        )
    else:
        for dia in DIAS_ORDEN:
            bloque = data["dias"][dia]
            pids = bloque.get(filtro_columna) or []
            if not pids:
                continue

            st.markdown(
                f"<h2 style='color:#7A1F1F;margin-top:1.2rem;'>{ETIQUETA_DIA[dia]}</h2>",
                unsafe_allow_html=True,
            )
            _render_platos_columna(dia, pids, titulos[filtro_columna])


# =========================================================
# MENÚ (catálogo)
# =========================================================
with tab2:
    st.subheader("Todos los platos de ElaFood")

    for pid, p in PRODUCTOS.items():
        key = f"catalogo_{p['nombre']}"
        tarjeta_producto(
            p["nombre"],
            p["precio"],
            p["imagen"],
            p.get("descripcion", ""),
            key,
            mostrar_boton=False,
        )


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
