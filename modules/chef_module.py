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
# -----------------------------
# PIN
# -----------------------------
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


# -----------------------------
# Panel: menú semanal (grilla día × Comidas / Postres / Otros)
# -----------------------------
def vista_panel_chef():
    if "chef_pin_ok" not in st.session_state:
        st.session_state.chef_pin_ok = False

    st.subheader("Menú de la semana")
    st.caption(
        "Por cada día elige qué ofrecerás. **Comidas** agrupa Lunch y Comida rápida. "
        "Sin fechas: la semana es siempre la misma plantilla hasta que la cambies."
    )

    st.markdown("---")

    config = cargar_menu_semana()
    opts_c = ids_opcion_comidas()
    opts_p = ids_opcion_postres()
    opts_o = ids_opcion_otros()

    tab_labels = [ETIQUETA_DIA[d][:3] + "." for d in DIAS_ORDEN]
    tabs = st.tabs(tab_labels)

    for i, dia in enumerate(DIAS_ORDEN):
        with tabs[i]:
            st.markdown(f"### {ETIQUETA_DIA[dia]}")
            bloque = config["dias"][dia]

            bloque["comidas"] = st.multiselect(
                "Comidas",
                options=opts_c,
                default=[x for x in bloque["comidas"] if x in opts_c],
                format_func=nombre_producto,
                key=f"chef_ms_{dia}_comidas",
            )
            bloque["postres"] = st.multiselect(
                "Postres",
                options=opts_p,
                default=[x for x in bloque["postres"] if x in opts_p],
                format_func=nombre_producto,
                key=f"chef_ms_{dia}_postres",
            )
            bloque["otros"] = st.multiselect(
                "Otros",
                options=opts_o,
                default=[x for x in bloque["otros"] if x in opts_o],
                format_func=nombre_producto,
                key=f"chef_ms_{dia}_otros",
            )

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
            st.success("Plantilla reiniciada.")
            st.rerun()
