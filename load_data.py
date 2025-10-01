import pandas as pd
import streamlit as st
import numpy as np

def cargar_datos():
    # Cargar datos de Puntaje Global
    #try:
    #    datos_global = pd.read_excel("Resultados_Puntaje_Global.xlsx", sheet_name="G5")
    #    st.session_state["datos_global"] = datos_global.copy()
    #except Exception as e:
    #    st.error(f"Error al cargar los datos de Puntaje Global: {e}")

    # Cargar datos de Quiero Ser Quiero Saber
    try:
        datos_qsqs = pd.read_excel("Resultados_QSQS.xlsx", sheet_name="G5")
        st.session_state["datos_qsqs"] = datos_qsqs.copy()
    except Exception as e:
        st.error(f"Error al cargar los datos de Quiero Ser Quiero Saber: {e}")

    # Cargar datos de Olimpiadas
    #try:
    #    datos_olimpiadas = pd.read_excel("Resultados_Olimpiadas.xlsx", sheet_name="G5")
    #    st.session_state["datos_olimpiadas"] = datos_olimpiadas.copy()
    #except Exception as e:
    #    st.error(f"Error al cargar los datos de Olimpiadas: {e}")


# Agrupar por afirmación
def agrupar_por_afirmacion(df):
    correctas_afirmacion = df.groupby(['Área', 'Competencia', 'Afirmaciones'])['CORRECTA'].sum().reset_index()
    total_por_afirmacion = df.groupby(['Área', 'Competencia', 'Afirmaciones'])['CORRECTA'].count().reset_index()
    correctas_afirmacion = correctas_afirmacion.merge(total_por_afirmacion, on=['Área', 'Competencia', 'Afirmaciones'])
    correctas_afirmacion.rename(columns={'CORRECTA_x': 'ACIERTOS', 'CORRECTA_y': 'TOTAL'}, inplace=True)
    correctas_afirmacion['% ACIERTOS'] = (correctas_afirmacion['ACIERTOS'] / correctas_afirmacion['TOTAL'] * 100).round(2)
    return correctas_afirmacion