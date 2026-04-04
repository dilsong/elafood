import streamlit as st
from PIL import Image
import os


def tarjeta_producto(nombre, precio, imagen, descripcion, key, mostrar_boton=True):
    # Verificar si la imagen existe
    if not os.path.exists(imagen):
        imagen = "Imagenes/Logos/no_image.JPG"   # Imagen por defecto

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
            # Cuando no se muestra botón, devolvemos valores neutros
            return 0, False
        
def tarjeta_producto_hoy(nombre, precio, imagen, descripcion, key):
    # Verificar si la imagen existe
    if not os.path.exists(imagen):
        imagen = "Imagenes/Logos/no_image.JPG"

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

        # Botón + check en la misma fila
        bcol, ccol = st.columns([4, 1])

        with bcol:
            agregar_btn = st.button(
                "Agregar al carrito",
                key=f"btn_hoy_{key}"
            )

        with ccol:
            if agregar_btn:
                st.markdown(
                    "<span style='font-size:24px; color:green;'>✔</span>",
                    unsafe_allow_html=True
                )

        return cantidad, agregar_btn