import streamlit as st

def render_sidebar():
    with st.sidebar:
        #st.header("🧭 Sidebar — Pantalla 1")
        # Selector de grado
        grados = ["11", "10"]
        grado = st.selectbox("Grado", grados, key="p1_grado")
        anio = st.selectbox("Año", ["2026", "2025", "2024"], key="p1_anio")
        
        if anio == "2024":
            # -- Select for high sample rate data
            high_fs = st.checkbox('Sin conectar')

        #piar = st.checkbox('Sin PIAR')
    return {"anio": anio, "grado": grado, "high_fs": high_fs if anio == "2024" else False}#, "piar": piar}