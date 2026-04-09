# tarjetas.py: Funciones para mostrar tarjetas de productos en Streamlit

import streamlit as st
from modules.imagenes import obtener_imagen, obtener_imagen_plato, src_para_html
from modules.i18n import get_lang, tr


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
        st.write(f"**{tr('Precio', 'Price')}:** ${precio}")

        if mostrar_boton:
            cantidad = st.number_input(
                tr("Cantidad", "Quantity"),
                min_value=1,
                max_value=99,
                value=1,
                key=f"cantidad_{key}"
            )

            agregar_btn = st.button(
                tr("Agregar al carrito", "Add to cart"),
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
        st.markdown(f"<h3 style='color:#91241D;'>{nombre}</h3>", unsafe_allow_html=True)
        st.write(descripcion)

    # ------------------ COL 3: Precio + cantidad + botón + check ------------------
    with col3:
        st.write(f"**{tr('Precio', 'Price')}:** ${precio}")

        cantidad = st.number_input(
            tr("Cantidad", "Quantity"),
            min_value=1,
            max_value=99,
            value=1,
            key=f"cantidad_hoy_{key}"
        )

        agregar_btn = st.button(
            tr("Agregar al carrito", "Add to cart"),
            key=f"btn_hoy_{key}",
            width="stretch",
        )

        return cantidad, agregar_btn
    

# Ruta del logo/foto opcional en Panel Chef (usa logo principal para mejor nitidez).
RUTA_LOGO_CHEF_OPCIONAL = "Imagenes/Logos/logo.jpg"


def tarjeta_acerca_chef():
    src_logo = src_para_html(RUTA_LOGO_CHEF_OPCIONAL)
    en = get_lang() == "EN"

    st.markdown(
        f"""
        <style>
            .elafood-qs-text {{
                font-size: 16px;
                line-height: 1.6;
                color: #333;
                margin: 0 0 12px 0;
            }}
            @media (prefers-color-scheme: dark) {{
                .elafood-qs-text {{
                    color: #fff !important;
                }}
            }}
        </style>
        <div style="display:flex;justify-content:center;width:100%;margin-bottom:12px;">
            <div style="
                width:150px;
                height:150px;
                border-radius:50%;
                overflow:hidden;
                border:3px solid #91241D;
                flex-shrink:0;
            ">
                <img src="{src_logo}" alt="ElaFood" style="width:100%;height:100%;object-fit:cover;display:block;" />
            </div>
        </div>        

        <p class="elafood-qs-text">
            {"We are a family business born from the love of homemade desserts and meals. Every dish, dessert, and detail is prepared with dedication, care, and that homemade flavor that feels like family." if en else "Somos un negocio familiar nacido del amor por los postres y la comida hecha en casa. Cada plato, postre y detalle lo preparamos con dedicación, cariño y ese sabor casero que hace sentir como en familia."}
        </p>
        <p class="elafood-qs-text">
            {"Our vision is to help you enjoy fresh, healthy, and balanced meals, especially with our weekly lunches, designed to make your day easier without giving up great flavor." if en else "Nuestra visión es ayudarte a disfrutar de comidas frescas, sanas y balanceadas, especialmente con nuestros almuerzos semanales, pensados para facilitar tu día sin renunciar al buen sabor."}
        </p>
        <p class="elafood-qs-text">
            {"We are also developing a healthy menu with macro and protein information, ideal for those who want a more conscious diet aligned with their goals." if en else "Además, estamos desarrollando un menú saludable con información de macros y proteína, ideal para quienes desean llevar una alimentación más consciente y adaptada a sus objetivos."}
        </p>
        <p class="elafood-qs-text">
            {"And for dessert lovers, we create irresistible homemade sweets full of <strong>flavor</strong>, <strong>love</strong>, and that special touch that only <strong>homemade food can offer</strong>." if en else "Y para los amantes del dulce, creamos postres caseros irresistibles, llenos de <strong>sabor</strong>, <strong>amor</strong> y ese toque especial que solo lo <strong>hecho en casa puede ofrecer</strong>."}
        </p>
        <p class="elafood-qs-text" style="margin:0;">
            {"To bring every home fresh and delicious homemade food prepared with love, offering balanced options for everyday life and desserts that brighten any moment." if en else "Llevar a cada hogar comida casera, fresca y deliciosa, preparada con amor, ofreciendo opciones balanceadas para el día a día y postres que alegren cualquier momento."}
        </p>
        """,
        unsafe_allow_html=True,
    )