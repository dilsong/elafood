# tarjetas.py: Funciones para mostrar tarjetas de productos en Streamlit

import streamlit as st
from modules.imagenes import obtener_imagen, obtener_imagen_plato, src_para_html


def tarjeta_producto(nombre, precio, imagen, descripcion, key, mostrar_boton=True):
    # Convertir la ruta local a URL
    imagen = obtener_imagen_plato(imagen)

    st.markdown(
        """
        <style>
        .card {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.image(imagen, width=200)

        st.subheader(nombre)
        st.write(descripcion)
        st.write(f"**Precio:** ${precio}")

        if mostrar_boton:
            cantidad = st.number_input(
                "Cantidad",
                min_value=1,
                max_value=20,
                value=1,
                key=f"cantidad_{key}"
            )

            agregar_btn = st.button(
                "Agregar al carrito",
                key=f"btn_{key}"
            )

            return cantidad, agregar_btn

        else:
            return 0, False


def tarjeta_producto_hoy(nombre, precio, imagen, descripcion, key):
    imagen = obtener_imagen_plato(imagen)

    # 3 columnas: imagen | nombre + descripción | precio + cantidad + botón + check
    col1, col2, col3 = st.columns([1, 2, 1])

    # ------------------ COL 1: Imagen ------------------
    with col1:
        st.image(imagen, width=150)

    # ------------------ COL 2: Nombre + Descripción ------------------
    with col2:
        st.markdown(f"<h3 style='color:#7A1F1F;'>{nombre}</h3>", unsafe_allow_html=True)
        st.write(descripcion)

    # ------------------ COL 3: Precio + cantidad + botón + check ------------------
    with col3:
        st.write(f"**Precio:** ${precio}")

        cantidad = st.number_input(
            "Cantidad",
            min_value=1,
            max_value=20,
            value=1,
            key=f"cantidad_hoy_{key}"
        )

        agregar_btn = st.button(
            "Agregar al carrito",
            key=f"btn_hoy_{key}",
            use_container_width=True,
        )

        return cantidad, agregar_btn
    

# Ruta del logo/foto opcional en Panel Chef (mismo archivo en disco o en GitHub raw)
RUTA_LOGO_CHEF_OPCIONAL = "Imagenes/Logos/Logo minimalista Ela.png"


def tarjeta_acerca_chef():
    src_logo = src_para_html(RUTA_LOGO_CHEF_OPCIONAL)

    st.markdown(
        f"""
        <div style="display:flex;justify-content:center;width:100%;margin-bottom:12px;">
            <div style="
                width:150px;
                height:150px;
                border-radius:50%;
                overflow:hidden;
                border:3px solid #7A1F1F;
                flex-shrink:0;
            ">
                <img src="{src_logo}" alt="ElaFood" style="width:100%;height:100%;object-fit:cover;display:block;" />
            </div>
        </div>
        <p style="color:#7A1F1F; font-size:13px; text-align:center; margin-top:8px; margin-bottom:20px;">
            (Foto opcional — Ela prefiere el anonimato)
        </p>

        <p style="font-size:16px; line-height:1.6; color:#333;">
            Nuestra chef prefiere el silencio a los reflectores.
            Cocina como quien reza: en voz baja, con devoción.
            <br><br>
            Aprendió de su madre, entre aromas que no se olvidan,
            y perfeccionó su sazón en cocinas de Ecuador,
            pero su verdadero arte nació en casa,
            alimentando a quienes ama.
            <br><br>
            No negocia con la frescura:
            cada plato se prepara al momento,
            cada postre vive apenas dos días,
            porque la comida —dice ella—
            tiene alma solo cuando es reciente.
            <br><br>
            Sus recetas son familiares, honestas,
            hechas con manos que conocen el cariño.
            Por eso, cuando pruebas su comida,
            no solo comes… te sientes en casa.
        </p>
        """,
        unsafe_allow_html=True,
    )