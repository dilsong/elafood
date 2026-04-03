import json
import os
from datetime import date
import streamlit as st
from modules.productos import PRODUCTOS

CONFIG_FILE = "data/config_menu.json"
PIN_FILE = "data/chef_pin.secret"


# -----------------------------
# PIN
# -----------------------------
def cargar_pin() -> str:
    if not os.path.exists(PIN_FILE):
        return ""
    with open(PIN_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


def validar_pin(pin_ingresado: str) -> bool:
    pin_real = cargar_pin()
    return pin_real != "" and pin_ingresado == pin_real


# -----------------------------
# CONFIG MENU (con autocorrección)
# -----------------------------
def config_menu_por_defecto() -> dict:
    return {
        "fecha_menu": str(date.today()),
        "categorias": {
            "lunch": False,
            "comida_rapida": False,
            "postres": False,
            "otros": False,
        },
        "platos": {
            "lunch": [],
            "comida_rapida": [],
            "postres": [],
            "otros": [],
        },
    }


def cargar_config_menu() -> dict:
    # Si el archivo no existe o está vacío → crear uno nuevo
    if not os.path.exists(CONFIG_FILE) or os.path.getsize(CONFIG_FILE) == 0:
        config = config_menu_por_defecto()
        guardar_config_menu(config)
        return config

    # Intentar cargar el JSON
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except (json.JSONDecodeError, ValueError):
        # Si está corrupto → regenerarlo
        config = config_menu_por_defecto()
        guardar_config_menu(config)
        return config


def guardar_config_menu(config: dict) -> None:
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def reiniciar_menu() -> dict:
    config = config_menu_por_defecto()
    guardar_config_menu(config)
    return config


# -----------------------------
# Productos por categoría
# -----------------------------
def productos_por_categoria() -> dict:
    cat_map = {"lunch": [], "comida_rapida": [], "postres": [], "otros": []}
    for pid, data in PRODUCTOS.items():
        cat = data["categoria"]
        if cat in cat_map:
            cat_map[cat].append((pid, data["nombre"]))
    return cat_map


# -----------------------------
# Vista del Panel del Chef
# -----------------------------
def vista_panel_chef():
    if "chef_pin_ok" not in st.session_state:
        st.session_state.chef_pin_ok = False

    st.subheader("Acerca del Chef")

    st.markdown(
        """
Nuestra chef prefiere el silencio a los reflectores.  
Cocina como quien reza: en voz baja, con devoción.

Aprendió de su madre, entre aromas que no se olvidan,  
y perfeccionó su sazón en cocinas de Ecuador,  
pero su verdadero arte nació en casa,  
alimentando a quienes ama.

No negocia con la frescura:  
cada plato se prepara al momento,  
cada postre vive apenas dos días,  
porque la comida —dice ella—  
tiene alma solo cuando es reciente.

Sus recetas son familiares, honestas,  
hechas con manos que conocen el cariño.  
Por eso, cuando pruebas su comida,  
no solo comes… te sientes en casa.
        """
    )

    with st.expander("Acceso al Panel del Chef (PIN)"):
        pin_ingresado = st.text_input("PIN del chef", type="password")
        if st.button("Entrar"):
            if validar_pin(pin_ingresado):
                st.session_state.chef_pin_ok = True
                st.success("Acceso concedido.")
            else:
                st.session_state.chef_pin_ok = False
                st.error("PIN incorrecto.")

    if not st.session_state.chef_pin_ok:
        st.info("Introduce el PIN para configurar el menú del día.")
        return

    st.markdown("---")
    st.subheader("Configuración del menú del día")

    config = cargar_config_menu()

    # Fecha
    fecha_actual = date.fromisoformat(config["fecha_menu"])
    nueva_fecha = st.date_input("Fecha del menú", value=fecha_actual)
    config["fecha_menu"] = str(nueva_fecha)

    st.markdown("### Categorías disponibles")
    categorias = config["categorias"]

    col1, col2 = st.columns(2)
    with col1:
        categorias["lunch"] = st.checkbox("Lunch", value=categorias["lunch"])
        categorias["postres"] = st.checkbox("Postres", value=categorias["postres"])
    with col2:
        categorias["comida_rapida"] = st.checkbox("Comida rápida", value=categorias["comida_rapida"])
        categorias["otros"] = st.checkbox("Otros", value=categorias["otros"])

    st.markdown("### Platos del día")
    platos_config = config["platos"]
    cat_prod = productos_por_categoria()

    for cat_key, cat_label in [
        ("lunch", "Lunch"),
        ("comida_rapida", "Comida rápida"),
        ("postres", "Postres"),
        ("otros", "Otros"),
    ]:
        if not categorias[cat_key]:
            continue

        st.markdown(f"**{cat_label}**")
        seleccionados = set(platos_config[cat_key])
        nuevos = []

        for pid, nombre in cat_prod[cat_key]:
            marcado = pid in seleccionados
            marcado = st.checkbox(nombre, value=marcado, key=f"{cat_key}_{pid}")
            if marcado:
                nuevos.append(pid)

        platos_config[cat_key] = nuevos

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if st.button("Guardar menú del día"):
            guardar_config_menu(config)
            st.success("Menú del día actualizado correctamente.")
    with col_g2:
        if st.button("Reiniciar menú"):
            reiniciar_menu()
            st.success("Menú reiniciado.")