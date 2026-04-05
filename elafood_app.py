import streamlit as st

# ------------------ TUS MÓDULOS EXISTENTES ------------------
from modules.menu import mostrar_menu
from modules.carrito import inicializar_carrito, agregar, mostrar_carrito
from modules.whatsapp import generar_mensaje, generar_link_whatsapp
from modules.estilo import banner
from modules.tarjetas import tarjeta_producto, tarjeta_producto_hoy
from modules.cliente import formulario_cliente
from modules.config import TELEFONO_ELAFOOD
from modules.imagenes import ruta_imagen
from modules.productos import PRODUCTOS

import os

# ------------------ NUEVO MÓDULO DEL CHEF ------------------
from modules.chef_module import (
    cargar_config_menu,
    productos_por_categoria
)



# ---------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------------------------------------
st.set_page_config(page_title="ElaFood", layout="wide")

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

    # Luego recargamos el menú del Chef (si cambió, aquí se actualiza)
    st.session_state._reload_key = os.urandom(4)

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
                    ruta_imagen(p["imagen"]),
                    p.get("descripcion", ""),
                    key
                )

                if agregar_btn and cantidad > 0:
                    agregar(p["nombre"], cantidad, p["precio"])
                    #st.success(f"{cantidad} x {p['nombre']} agregado(s) al carrito.")

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
            ruta_imagen(p["imagen"]),
            p.get("descripcion", ""),
            key,
            mostrar_boton=False  # Solo mostrar, no agregar al carrito
        )