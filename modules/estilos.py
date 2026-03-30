# modules/estilos.py
import base64
import streamlit as st

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def banner():
    logo_base64 = image_to_base64("Imagenes/Logos/logo.jpg")

    st.markdown(
        f"""
        <div style="
            background-color:#8B1E1E;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            color: white;
            margin-bottom: 30px;
        ">
            <img src="data:image/jpg;base64,{logo_base64}" width="120" style="margin-bottom:15px;">
            <h1 style="margin-bottom:5px;">ElaFood</h1>
            <h3 style="font-weight:300; margin-top:0;">Food made with love</h3>
        </div>
        """,
        unsafe_allow_html=True
    )