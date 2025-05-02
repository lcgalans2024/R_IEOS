import streamlit as st
import pandas as pd

def descarga():
    st.header("Descarga de Datos 📥")

    # Verifica si los datos están en session_state
    if "datos_filtrados" not in st.session_state:
        st.warning("No se han cargado datos aún.")
        return

    # Cargar los datos
    df = st.session_state["datos"]

    # Botón para descargar el DataFrame como CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name='datos.csv',
        mime='text/csv',
        help="Descargar los datos filtrados como archivo CSV."
    )
    # Botón para descargar el DataFrame como Excel

    excel = df.to_excel(index=False).encode('utf-8')
    st.download_button(
        label="Descargar Excel",
        data=excel,
        file_name='datos.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        help="Descargar los datos filtrados como archivo Excel."
    )