import streamlit as st
import pandas as pd
import numpy as np
from utils.navegacion import generarMenu
import load_data

def sidebar_config():
    # Generar menú de navegación
    generarMenu()

    # Cargar datos
    #load_data.cargar_datos()
    # Título del sidebar
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
    datos = pd.read_excel("Resultados_Simulacro_ICFES.xlsx").dropna()

    # eliminar registo por documento, AÑO y SIMULACRO
    documentos_a_ignorar = ["1035976977","nn_1001"]
    datos = datos[~((datos["DOCUMENTO"].isin(documentos_a_ignorar)) & (datos["AÑO"] == 2025) & (datos["SIMULACRO"] == "S1"))]

    #dim = datos.shape
    #st.sidebar.markdown(f"**Total de registros:** {dim[0]}")
    #st.dataframe(datos, use_container_width=True)

    # Convertir la columna 'Grupo' y 'Año' a string para evitar problemas de tipo
    datos["Grupo"] = datos["Grupo"].astype(str)
    datos["AÑO"] = datos["AÑO"].astype(str)
    datos["ND_LC"] = datos["ND_LC"].astype(str)
    datos["ND_M"] = datos["ND_M"].astype(str)
    datos["ND_CN"] = datos["ND_CN"].astype(str)

    for col in datos.select_dtypes(include=np.float64):
        datos[col] = datos[col].round(2)

    st.session_state["datos"] = datos.copy()

    # Selector de grado
    grados = ["11", "10"]
    st.session_state["grado_seleccionado"] = st.sidebar.selectbox("Seleccione el grado:", grados)
    grado_seleccionado = st.session_state["grado_seleccionado"]

    # Selector de año
    años = datos["AÑO"].unique().tolist()
    st.session_state["año_seleccionado"] = st.sidebar.selectbox("Seleccione el año", años, index=1)
    año_seleccionado = st.session_state["año_seleccionado"]

    if año_seleccionado not in datos[datos.AÑO != "2024"]["AÑO"].unique():
        # -- Select for high sample rate data
        high_fs = st.sidebar.checkbox('Sin conectar')
        if high_fs:
            datos = datos[datos['Grupo'].isin(['1101','1102','1103','1104'])].copy()

    # inicializar filtro PIAR
    #if "piar" not in st.session_state:
    #    st.session_state["piar"] = False

    #piar = st.sidebar.checkbox('Sin PIAR')
    #st.session_state["piar"] = piar
    #if piar:
    datos = datos[~(datos['Inglés'] == 0)].copy()

    # Filtrar datos según el grado y año seleccionados
    st.session_state["datos_filtrados"] = datos[(datos['Grupo'].str.startswith(grado_seleccionado)) & (datos["AÑO"] == año_seleccionado)]

    ################################################# Datos QSQS #################################################

    # Selector de area
    #area = st.sidebar.selectbox("Seleccione el grado:", st.session_state["datos_qsqs"]['Área'].unique().tolist())
    #st.session_state["area_seleccionada"] = area
    # selector de grupo
    #grupos = st.sidebar.multiselect(
    #    "Seleccione el grupo:",
    #    st.session_state["datos_qsqs"]['GRUPO'].unique().tolist(),
    #    default=st.session_state["datos_qsqs"]['GRUPO'].unique().tolist()
    #)
    #st.session_state["grupos_seleccionados"] = grupos
    
        
    

    
