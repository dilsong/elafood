# chef_module.py
import os

import streamlit as st
from modules.i18n import tr

from modules.menu_semana import (
    DIAS_ORDEN,
    ETIQUETA_DIA,
    cargar_menu_semana,
    guardar_menu_semana,
    ids_opcion_comidas,
    ids_opcion_otros,
    ids_opcion_postres,
    menu_semana_por_defecto,
    nombre_producto,
)

PIN_FILE = "data/chef_pin.secret"


def cargar_pin() -> str:
    try:
        pin_cloud = st.secrets.get("PIN_CHEF", "").strip()
        if pin_cloud:
            return pin_cloud
    except Exception:
        pass

    if os.path.exists(PIN_FILE):
        with open(PIN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()

    return ""


def validar_pin(pin_ingresado: str) -> bool:
    pin_real = cargar_pin()
    return pin_real != "" and pin_ingresado == pin_real


def _editor_dia_o_especial(
    config: dict,
    clave: str,
    titulo: str,
    prefijo_keys: str,
):
    st.markdown(f"### {titulo}")
    if clave == "especial":
        bloque = config["especial"]
    else:
        bloque = config["dias"][clave]

    bloque["comidas"] = st.multiselect(
        tr("Comidas", "Meals"),
        options=ids_opcion_comidas(),
        default=[x for x in bloque["comidas"] if x in ids_opcion_comidas()],
        format_func=nombre_producto,
        key=f"chef_ms_{prefijo_keys}_comidas",
    )
    bloque["postres"] = st.multiselect(
        tr("Postres", "Desserts"),
        options=ids_opcion_postres(),
        default=[x for x in bloque["postres"] if x in ids_opcion_postres()],
        format_func=nombre_producto,
        key=f"chef_ms_{prefijo_keys}_postres",
    )
    bloque["otros"] = st.multiselect(
        tr("Otros", "Others"),
        options=ids_opcion_otros(),
        default=[x for x in bloque["otros"] if x in ids_opcion_otros()],
        format_func=nombre_producto,
        key=f"chef_ms_{prefijo_keys}_otros",
    )


def vista_panel_chef():
    if "chef_pin_ok" not in st.session_state:
        st.session_state.chef_pin_ok = False

    st.subheader(tr("Menú de la semana", "Weekly menu"))
    st.caption(
        tr(
            "**Lunes a domingo:** platos que ves en **Platos de la Semana** en la app. "
            "**Esp. (Especial):** lo que ves en **Postres y Especialidades**. "
            "**Comidas** agrupa Lunch y Comida rápida.",
            "**Monday to Sunday:** dishes shown in **Weekly Dishes**. "
            "**Sp. (Special):** shown in **Desserts & Specialties**. "
            "**Meals** groups Lunch and Fast Food.",
        )
    )

    st.markdown("---")

    config = cargar_menu_semana()

    tab_labels = [ETIQUETA_DIA[d][:3] + "." for d in DIAS_ORDEN] + [tr("Esp.", "Sp.")]
    tabs = st.tabs(tab_labels)

    for i, dia in enumerate(DIAS_ORDEN):
        with tabs[i]:
            _editor_dia_o_especial(config, dia, ETIQUETA_DIA[dia], dia)

    with tabs[-1]:
        st.caption(tr("Contenido de la pestaña **Postres y Especialidades** en la página principal.", "Content shown in **Desserts & Specialties** on Home page."))
        _editor_dia_o_especial(config, "especial", tr("Especial (Esp.)", "Special (Sp.)"), "especial")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button(tr("Guardar menú semanal", "Save weekly menu")):
            guardar_menu_semana(config)
            st.success(tr("Menú semanal guardado.", "Weekly menu saved."))
    with c2:
        if st.button(tr("Vaciar toda la semana", "Clear full week")):
            vacio = menu_semana_por_defecto()
            guardar_menu_semana(vacio)
            # Refuerza el reinicio visual y del estado de widgets.
            config["dias"] = vacio["dias"]
            config["especial"] = vacio["especial"]
            for d in DIAS_ORDEN:
                for col in ("comidas", "postres", "otros"):
                    st.session_state.pop(f"chef_ms_{d}_{col}", None)
                    st.session_state[f"chef_ms_{d}_{col}"] = []
            for col in ("comidas", "postres", "otros"):
                st.session_state.pop(f"chef_ms_especial_{col}", None)
                st.session_state[f"chef_ms_especial_{col}"] = []
            st.success(tr("Plantilla reiniciada.", "Template reset."))
            st.rerun()
