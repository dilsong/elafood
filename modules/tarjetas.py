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