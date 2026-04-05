import streamlit as st

# ------------------ TUS MÓDULOS EXISTENTES ------------------
from modules.menu import mostrar_menu
from modules.carrito import agregar, mostrar_carrito
from modules.whatsapp import generar_mensaje, generar_link_whatsapp
from modules.estilo import banner, estilos_app
from modules.tarjetas import tarjeta_producto, tarjeta_producto_hoy
from modules.cliente import formulario_cliente
from modules.config import TELEFONO_ELAFOOD, URL_SALIR_DESTINO, RUTA_ICONO_APP
from modules.productos import PRODUCTOS

# ------------------ NUEVO MÓDULO DEL CHEF ------------------
from modules.chef_module import (
    cargar_config_menu,
    productos_por_categoria
)

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
    unsafe_allow_html=True
)
if hasattr(st, "logo"):
    try:
        st.logo(RUTA_ICONO_APP)
    except Exception:
        pass
# ---------------------------------------------------------
# FIN: CONFIGURACIÓN INICIAL
# ---------------------------------------------------------

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

# Banner superior
banner()

# ---------------------------------------------------------
# PESTAÑAS
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["Hoy en ElaFood", "Los platos de ElaFood"])


# =========================================================
# ===============   HOY EN EL ALAFOOD  ====================
# =========================================================
with tab1:

    # INICIALIZACIÓN DE SESSION_STATE
    if "carrito" not in st.session_state:
        st.session_state.carrito = []

    if "mensaje_generado" not in st.session_state:
        st.session_state.mensaje_generado = ""

    if "link" not in st.session_state:
        st.session_state.link = ""

    if "pedido_generado" not in st.session_state:
        st.session_state.pedido_generado = False

    # MENÚ DEL DÍA CONFIGURADO POR EL CHEF
    # Primero obtenemos la categoría seleccionada
    categoria = mostrar_menu()

    config = cargar_config_menu()
    categorias_activas = config["categorias"]
    platos_activados = config["platos"]
    productos_cat = productos_por_categoria()

    NOMBRES_BONITOS = {
            "lunch": "Lunch",
            "comida_rapida": "Comida Rápida",
            "postres": "Postres",
            "otros": "Otros"
    }

    st.markdown(
    f"<h2 style='color:#7A1F1F;'>Categoría: {NOMBRES_BONITOS.get(categoria, categoria)}</h2>",
    unsafe_allow_html=True
)

    # Si la categoría NO está activa → no mostrar nada
    if not categorias_activas.get(categoria, False):
        st.warning("Esta categoría no está disponible hoy.")
    else:
        ids_activos = set(platos_activados.get(categoria, []))

        if len(ids_activos) == 0:
            st.info("No hay platos disponibles en esta categoría hoy.")
        else:
            for pid in ids_activos:
                if pid not in PRODUCTOS:
                    st.error(f"El producto '{pid}' no existe en PRODUCTOS.")
                    continue

                p = PRODUCTOS[pid]

                key = f"{categoria}_{p['nombre']}"
                cantidad, agregar_btn = tarjeta_producto_hoy(
                    p["nombre"],
                    p["precio"],
                    p["imagen"],
                    p.get("descripcion", ""),
                    key
                )

                if agregar_btn and cantidad > 0:
                    agregar(p["nombre"], cantidad, p["precio"])
                    st.toast(
                        f"Listo: {cantidad}× {p['nombre']} en el carrito",
                        icon="✅",
                    )

    # CARRITO Y CLIENTE
    total = mostrar_carrito()
    cliente = formulario_cliente()

    st.sidebar.markdown("---")

    # BOTÓN GENERAR PEDIDO
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
            unsafe_allow_html=True
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


# =========================================================
# ===============   LOS PLATOS DE ELAFOOD  ================
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
            mostrar_boton=False  # Solo mostrar, no agregar al carrito
        )