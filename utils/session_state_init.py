import streamlit as st
import utils.data
from funciones import asignar_nivel_desempeno

def inicializar_session_state():
    if 'Datos' not in st.session_state:
        st.session_state.Datos = utils.data.cargar_datos()
        st.session_state.Datos = asignar_nivel_desempeno(st.session_state.Datos)
        

    if 'datos_icfes' not in st.session_state:
        # filtramos datos del ICFES
        st.session_state.datos_icfes = st.session_state.Datos[st.session_state.Datos.SIMULACRO == "ICFES"]

    if "datos_qsqs" not in st.session_state:
        st.session_state["datos_qsqs"] = utils.data.cargar_datos_qsqs()

    if "datos_historicos" not in st.session_state:
        st.session_state["datos_historicos"] = utils.data.cargar_datos_historicos()
