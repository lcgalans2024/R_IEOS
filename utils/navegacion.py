import streamlit as st

def generarMenu():
    st.sidebar.title("Navegación")
    with st.sidebar:
        st.page_link("main.py", label="Inicio", icon="🏠")
        st.page_link("pages/pt_icfes.py", label="ICFES", icon= "📊")
        st.page_link("pages/pt_qsqs.py", label="Quiero ser Quiero Saber", icon="📊")