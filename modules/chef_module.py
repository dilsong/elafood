# chef_module.py
import os

import streamlit as st

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
        "Comidas",
        options=ids_opcion_comidas(),
        default=[x for x in bloque["comidas"] if x in ids_opcion_comidas()],
        format_func=nombre_producto,
        key=f"chef_ms_{prefijo_keys}_comidas",
    )
    bloque["postres"] = st.multiselect(
        "Postres",
        options=ids_opcion_postres(),
        default=[x for x in bloque["postres"] if x in ids_opcion_postres()],
        format_func=nombre_producto,
        key=f"chef_ms_{prefijo_keys}_postres",
    )
    bloque["otros"] = st.multiselect(
        "Otros",
        options=ids_opcion_otros(),
        default=[x for x in bloque["otros"] if x in ids_opcion_otros()],
        format_func=nombre_producto,
        key=f"chef_ms_{prefijo_keys}_otros",
    )


def vista_panel_chef():
    if "chef_pin_ok" not in st.session_state:
        st.session_state.chef_pin_ok = False

    st.subheader("Menú de la semana")
    st.caption(
        "**Lunes a domingo:** platos que ves en **Platos de la Semana** en la app. "
        "**Esp. (Especial):** lo que ves en **Postres y Especialidades**. "
        "**Comidas** agrupa Lunch y Comida rápida."
    )

    st.markdown("---")

    config = cargar_menu_semana()

    tab_labels = [ETIQUETA_DIA[d][:3] + "." for d in DIAS_ORDEN] + ["Esp."]
    tabs = st.tabs(tab_labels)

    for i, dia in enumerate(DIAS_ORDEN):
        with tabs[i]:
            _editor_dia_o_especial(config, dia, ETIQUETA_DIA[dia], dia)

    with tabs[-1]:
        st.caption("Contenido de la pestaña **Postres y Especialidades** en la página principal.")
        _editor_dia_o_especial(config, "especial", "Especial (Esp.)", "especial")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Guardar menú semanal"):
            guardar_menu_semana(config)
            st.success("Menú semanal guardado.")
    with c2:
        if st.button("Vaciar toda la semana"):
            vacio = menu_semana_por_defecto()
            guardar_menu_semana(vacio)
            for d in DIAS_ORDEN:
                for col in ("comidas", "postres", "otros"):
                    st.session_state.pop(f"chef_ms_{d}_{col}", None)
            for col in ("comidas", "postres", "otros"):
                st.session_state.pop(f"chef_ms_especial_{col}", None)
            st.success("Plantilla reiniciada.")
            st.rerun()
