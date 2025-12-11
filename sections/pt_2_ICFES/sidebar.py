import streamlit as st

def render_sidebar():
    with st.sidebar:
        #st.header("🧭 Sidebar — Pantalla 1")
        # Selector de grado
        grupos = ["1101", "1102", "1103", "1104"]
        grupo = st.selectbox("Grado", grupos, key="p1_grado")
        anio = st.selectbox("Año", ["2025", "2024"], key="p1_anio")
        
        if anio != "2025":
            # -- Select for high sample rate data
            high_fs = st.checkbox('Sin conectar')

        #piar = st.checkbox('Sin PIAR')
    return {"anio": anio, "grado": grupo, "high_fs": high_fs if anio != "2025" else False}#, "piar": piar}