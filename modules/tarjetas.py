# tarjetas.py: Funciones para mostrar tarjetas de productos en Streamlit

import streamlit as st
from PIL import Image
from modules.imagenes import obtener_imagen


def tarjeta_producto(nombre, precio, imagen, descripcion, key, mostrar_boton=True):
    # Convertir la ruta local a URL
    imagen = obtener_imagen(imagen)

    # Fallback también convertido a URL
    if "no_image" in imagen.lower():
        imagen = obtener_imagen("Imagenes/Logos/no_image.jpg")

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
    # Convertir la ruta local a URL SIEMPRE
    imagen = obtener_imagen(imagen)

    # Fallback también convertido a URL
    if "no_image" in imagen.lower():
        imagen = obtener_imagen("Imagenes/Logos/no_image.jpg")

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
    

def tarjeta_acerca_chef():
    st.markdown(
        """
        <!-- FOTO OPCIONAL -->
        <div style="text-align:center; margin-bottom:20px;">
            <div style="
                width:150px;
                height:150px;
                border-radius:50%;
                border:3px solid #7A1F1F;
                background-image: url('Imagenes/Logos/Logo minimalista Ela.png');
                background-size:cover;
                background-position:center;
            ">            
            </div>
            <p style="color:#7A1F1F; font-size:13px; margin-top:8px;">
                (Foto opcional — Ela prefiere el anonimato)
            </p>
        </div>

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
        unsafe_allow_html=True
    )