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
from modules.productos import agregar_producto_custom, migrar_catalogo_a_supabase
from modules.translate_suggest import sugerir_en_desde_es

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

    def _ordenar_por_seleccion_anterior(prev: list, selected: list) -> list:
        # Conserva el orden previo del chef y agrega nuevas selecciones al final.
        selected_set = set(selected or [])
        ordenado = [x for x in (prev or []) if x in selected_set]
        for x in (selected or []):
            if x not in ordenado:
                ordenado.append(x)
        return ordenado

    def _mover_item(lista: list, idx: int, delta: int) -> list:
        j = idx + delta
        if idx < 0 or j < 0 or idx >= len(lista) or j >= len(lista):
            return lista
        nueva = list(lista)
        nueva[idx], nueva[j] = nueva[j], nueva[idx]
        return nueva

    def _selector_con_orden(col_key: str, titulo_col: str, opciones: list):
        actual = [x for x in (bloque.get(col_key) or []) if x in opciones]
        order_key = f"chef_ms_order_{prefijo_keys}_{col_key}"
        if order_key not in st.session_state:
            st.session_state[order_key] = list(actual)

        actual_order = [x for x in st.session_state.get(order_key, []) if x in opciones]
        seleccionado = st.multiselect(
            titulo_col,
            options=opciones,
            default=actual_order,
            format_func=nombre_producto,
            key=f"chef_ms_{prefijo_keys}_{col_key}",
        )
        nuevo_orden = _ordenar_por_seleccion_anterior(actual_order, seleccionado)
        st.session_state[order_key] = nuevo_orden
        bloque[col_key] = list(nuevo_orden)

        if bloque[col_key]:
            st.caption(
                tr(
                    f"Orden en menú ({titulo_col}): usa ↑ y ↓ para reordenar.",
                    f"Menu order ({titulo_col}): use ↑ and ↓ to reorder.",
                )
            )
            for i, pid in enumerate(list(bloque[col_key])):
                c1, c2, c3 = st.columns([8, 1, 1])
                with c1:
                    st.write(f"{i + 1}. {nombre_producto(pid)}")
                with c2:
                    if st.button(
                        "↑",
                        key=f"chef_ord_up_{prefijo_keys}_{col_key}_{pid}_{i}",
                        disabled=(i == 0),
                    ):
                        nueva = _mover_item(bloque[col_key], i, -1)
                        st.session_state[order_key] = list(nueva)
                        bloque[col_key] = list(nueva)
                        st.rerun()
                with c3:
                    if st.button(
                        "↓",
                        key=f"chef_ord_dn_{prefijo_keys}_{col_key}_{pid}_{i}",
                        disabled=(i == len(bloque[col_key]) - 1),
                    ):
                        nueva = _mover_item(bloque[col_key], i, +1)
                        st.session_state[order_key] = list(nueva)
                        bloque[col_key] = list(nueva)
                        st.rerun()

    _selector_con_orden("comidas", tr("Comidas", "Meals"), ids_opcion_comidas())
    _selector_con_orden("postres", tr("Postres", "Desserts"), ids_opcion_postres())
    _selector_con_orden("otros", tr("Otros", "Others"), ids_opcion_otros())


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

    opciones_editor = DIAS_ORDEN + ["especial"]
    if "chef_editor_dia_activo" not in st.session_state:
        st.session_state.chef_editor_dia_activo = DIAS_ORDEN[0]

    dia_activo = st.radio(
        tr("Día a editar", "Day to edit"),
        options=opciones_editor,
        index=opciones_editor.index(st.session_state.chef_editor_dia_activo)
        if st.session_state.chef_editor_dia_activo in opciones_editor
        else 0,
        format_func=lambda d: (
            tr("Esp.", "Sp.") if d == "especial" else ETIQUETA_DIA.get(d, d)
        ),
        horizontal=True,
        key="chef_editor_dia_activo",
    )

    if dia_activo == "especial":
        st.caption(
            tr(
                "Contenido de la pestaña **Postres y Especialidades** en la página principal.",
                "Content shown in **Desserts & Specialties** on Home page.",
            )
        )
        _editor_dia_o_especial(
            config,
            "especial",
            tr("Especial (Esp.)", "Special (Sp.)"),
            "especial",
        )
    else:
        _editor_dia_o_especial(
            config,
            dia_activo,
            ETIQUETA_DIA.get(dia_activo, dia_activo),
            dia_activo,
        )

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
                    st.session_state.pop(f"chef_ms_order_{d}_{col}", None)
                    st.session_state[f"chef_ms_order_{d}_{col}"] = []
            for col in ("comidas", "postres", "otros"):
                st.session_state.pop(f"chef_ms_especial_{col}", None)
                st.session_state[f"chef_ms_especial_{col}"] = []
                st.session_state.pop(f"chef_ms_order_especial_{col}", None)
                st.session_state[f"chef_ms_order_especial_{col}"] = []
            st.success(tr("Plantilla reiniciada.", "Template reset."))
            st.rerun()

    st.markdown("---")
    with st.expander(tr("➕ Agregar producto al catálogo", "➕ Add product to catalog"), expanded=False):
        st.caption(
            tr(
                "Este formulario crea un producto nuevo para que aparezca en las listas del chef y menú del cliente.",
                "This form creates a new product so it appears in chef lists and customer menu.",
            )
        )
        # Aplicar sugerencias EN pendientes antes de instanciar widgets EN.
        if st.session_state.pop("chef_suggest_apply_pending", False):
            _p_nombre = st.session_state.pop("chef_suggest_nombre_en", "")
            _p_desc = st.session_state.pop("chef_suggest_desc_en", "")
            if _p_nombre:
                st.session_state["chef_new_nombre_en"] = _p_nombre
            if _p_desc:
                st.session_state["chef_new_desc_en"] = _p_desc
            st.success("Sugerencia aplicada. Puedes editar los campos EN.")

        c_a, c_b = st.columns(2)
        with c_a:
            nombre_es = st.text_input(tr("Nombre (ES)", "Name (ES)"), key="chef_new_nombre_es")
            descripcion_es = st.text_area(
                tr("Descripción (ES)", "Description (ES)"),
                key="chef_new_desc_es",
                height=90,
            )
            categoria = st.selectbox(
                tr("Categoría", "Category"),
                options=[
                    ("lunch", tr("Lunch", "Lunch")),
                    ("comida_rapida", tr("Comida rápida", "Fast food")),
                    ("postres", tr("Postres", "Desserts")),
                    ("otros", tr("Otros", "Others")),
                ],
                format_func=lambda x: x[1],
                key="chef_new_categoria",
            )[0]
        with c_b:
            nombre_en = st.text_input(tr("Nombre (EN)", "Name (EN)"), key="chef_new_nombre_en")
            descripcion_en = st.text_area(
                tr("Descripción (EN)", "Description (EN)"),
                key="chef_new_desc_en",
                height=90,
            )
            precio = st.number_input(
                tr("Precio", "Price"),
                min_value=0.0,
                step=0.5,
                format="%.2f",
                key="chef_new_precio",
            )
            imagen_nombre = st.text_input(
                tr("Nombre de imagen", "Image name"),
                key="chef_new_imagen",
                placeholder="nuevo.jpg",
            )

        c_s1, c_s2 = st.columns(2)
        with c_s1:
            if st.button("Sugerir EN", key="chef_suggest_en"):
                base_name_es = st.session_state.get("chef_new_nombre_es", "").strip()
                base_desc_es = st.session_state.get("chef_new_desc_es", "").strip()
                sug_name = sugerir_en_desde_es(base_name_es)
                sug_desc = sugerir_en_desde_es(base_desc_es)
                if sug_name or sug_desc:
                    st.session_state["chef_suggest_nombre_en"] = sug_name
                    st.session_state["chef_suggest_desc_en"] = sug_desc
                    st.session_state["chef_suggest_apply_pending"] = True
                else:
                    st.warning("No se pudo generar sugerencia en este momento.")
                st.rerun()
        with c_s2:
            if st.button("Migrar catálogo a Supabase", key="chef_migrate_catalog"):
                ok_n, fail_n, errs = migrar_catalogo_a_supabase(base_only=True)
                if fail_n == 0:
                    st.success(f"Migración completada: {ok_n} productos.")
                else:
                    st.warning(f"Migración parcial: {ok_n} OK, {fail_n} con error.")
                    if errs:
                        st.error("Primer error:\n" + errs[0])
                        with st.expander("Ver errores de migración", expanded=False):
                            st.code("\n".join(errs[:50]))

        if st.button(tr("Guardar producto", "Save product"), key="chef_new_save_producto"):
            base_img = {
                "lunch": "Imagenes/Comidas/Lunch/",
                "comida_rapida": "Imagenes/Comidas/Rapidas/",
                "postres": "Imagenes/Comidas/Postres/",
                "otros": "Imagenes/Comidas/Otros/",
            }
            img_input = (imagen_nombre or "").strip()
            if "/" in img_input or "\\" in img_input:
                imagen = img_input
            else:
                imagen = f"{base_img.get(categoria, 'Imagenes/Comidas/Otros/')}{img_input}"
            ok, nuevo_id, err = agregar_producto_custom(
                nombre_es=nombre_es,
                nombre_en=nombre_en,
                descripcion_es=descripcion_es,
                descripcion_en=descripcion_en,
                precio=precio,
                categoria=categoria,
                imagen=imagen,
            )
            if ok:
                st.success(
                    tr(
                        f"Producto creado correctamente. ID: {nuevo_id}",
                        f"Product created successfully. ID: {nuevo_id}",
                    )
                )
                st.rerun()
            else:
                st.error(
                    tr(
                        f"No se pudo crear el producto ({err}).",
                        f"Could not create product ({err}).",
                    )
                )
