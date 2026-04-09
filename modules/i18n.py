import streamlit as st


def get_lang() -> str:
    lang = st.session_state.get("lang", "ES")
    return "EN" if lang == "EN" else "ES"


def tr(es: str, en: str) -> str:
    return en if get_lang() == "EN" else es
