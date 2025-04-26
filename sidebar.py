import streamlit as st
import pandas as pd
import numpy as np

def sidebar_config():
    st.sidebar.header("Filtros del Dashboard")

    # Estilos de botones en HTML + CSS
    st.markdown(
        """
        <style>
        div.stButton > button.reset-filtros {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 18px;
            border-radius: 8px;
            font-size: 14px;
            margin: 4px;
            cursor: pointer;
        }
        div.stButton > button.reset-todo {
            background-color: #f44336;
            color: white;
            border: none;
            padding: 8px 18px;
            border-radius: 8px;
            font-size: 14px;
            margin: 4px;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Dos columnas para los botones
    col1, col2 = st.sidebar.columns(2)

    with col1:
        reset_filtros = st.button("🧹 Reset Filtros", key="reset_filtros", help="Limpiar grado y año")
    with col2:
        reset_todo = st.button("🔄 Reset Todo", key="reset_todo", help="Reiniciar toda la sesión")

    # Lógica de botones
    if reset_filtros:
        st.session_state.grado_seleccionado = None
        st.session_state.año_seleccionado = None
        st.success("Filtros reseteados. Selecciona de nuevo.")
        st.rerun()

    if reset_todo:
        st.session_state.clear()
        st.success("Todo reseteado. Aplicación reiniciada.")
        st.rerun()

    # Inicializar session_state si es necesario
    if "grado_seleccionado" not in st.session_state:
        st.session_state.grado_seleccionado = None
    if "año_seleccionado" not in st.session_state:
        st.session_state.año_seleccionado = None

    #Cargamos los datos
    datos = pd.read_excel("Resultados_Simulacro_ICFES.xlsx")
    datos = datos.dropna()

    # Convertir la columna 'Grado' a string para evitar problemas de tipo
    datos["Grupo"] = datos["Grupo"].astype(str)
    datos["AÑO"] = datos["AÑO"].astype(str)

    for col in datos.select_dtypes(include=np.float64):
        datos[col] = datos[col].round(2)

    # Selector de grado
    grados = ["11", "10"]
    grado_seleccionado = st.sidebar.selectbox("Seleccione el grado:", grados)

    # Selector de año
    años = datos["AÑO"].unique().tolist()
    año_seleccionado = st.sidebar.selectbox("Seleccione el año", años)

    # Filtrar datos según el grado y año seleccionados
    datos_filtrados = datos[(datos['Grupo'].str.startswith(grado_seleccionado)) & (datos["AÑO"] == año_seleccionado)]

    ################################################# METRICAS EXTERNAS #################################################

    # Devolver el dataframe filtrado
    return datos, datos_filtrados#, datos_filtrados, grado_seleccionado, año_seleccionado#, media_nacional, media_depto, media_munpio, media_colegio

