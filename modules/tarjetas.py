import streamlit as st
from PIL import Image

def tarjeta_producto(nombre, precio, imagen, descripcion, key):
    
    st.markdown(
        """
        <div style="
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            background-color: #ffffff;
        ">
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 2])

    # Imagen
    with col1:
        try:
            img = Image.open(imagen)
            st.image(img, width=180)
        except:
            st.write("Imagen no disponible")

    # Texto + cantidad + botón
    with col2:
        st.write(f"### {nombre}")
        st.write(f"**Precio:** ${precio}")
        st.write(descripcion if descripcion else "")

        cantidad = st.number_input(
            "Cantidad",
            min_value=0,
            max_value=10,
            step=1,
            key=f"cantidad_{key}"
        )

        agregar_btn = st.button(
            "Agregar al carrito",
            key=f"btn_{key}"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    return cantidad, agregar_btn