import streamlit as st

def puntaje_por_grupo(datos1, datos2):
    st.header("Análisis por Grupo 👥")
    
    # Validar si 'datos' tiene registros
    if datos1.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return
    
    if datos2.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return

    st.dataframe(datos1)
    st.dataframe(datos2)