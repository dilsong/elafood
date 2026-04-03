import streamlit as st
from modules.chef_module import vista_panel_chef

st.set_page_config(page_title="Panel del Chef – ElaFood", layout="wide")

st.title("Panel del Chef – ElaFood")
st.write("Configura el menú del día, categorías y platos disponibles.")

vista_panel_chef()