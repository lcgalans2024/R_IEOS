import streamlit as st
from utils.session_state_init import inicializar_session_state
from funciones import BartChartRace

# Inicialización robusta de session_state
inicializar_session_state()

import sidebar
from pages import pantalla_puntaje_global, pt_por_area, pt_por_grupo, pt_por_año, pantalla_olimpiadas, pt_descarga, pt_qsqs

# Configuracion general
st.set_page_config(page_title="Dashboard Institucional", layout="wide")

st.title("ANÁLISIS RESULTADOS INSTITUCIONALES")
#st.subheader("⚠️ Este es un espacio en construcción ⚠️")

BartChartRace(st.session_state.datos_historicos)

################# Revisar lo almacenado en session_state #######################
#st.write(st.session_state)
#st.dataframe(st.session_state.datos_icfes)
################################################################################
#df = st.session_state.datos_icfes.copy()

#st.dataframe(df.groupby(['AÑO'])['Puntaje global'].mean().round(2).reset_index())
# Configurar sidebar y cargar datos
sidebar.sidebar_config()

## Tabs principales del Dashboard
#tabs = [
#    "Análisis Puntaje Global",
#    "Análisis Por Area",
#    "Análisis Por Grupo",
#    "Análisis Por Año",
#    #"Olimpiadas Institucionales",
#    "Quiero Ser Quiero Saber",
#    "Descarga de Datos"
#]
#
## Crear Tabs
#tab1, tab2, tab3, tab4, tab6, tab7 = st.tabs(tabs)
#
## Lógica de cada pantalla
#with tab1:
#    #guardar pantalla actual
#    st.session_state.pantalla_actual = "global"
#    try:
#        pantalla_puntaje_global.puntaje_global()
#
#    except Exception as e:
#        st.error(f"Error al cargar la pantalla de análisis global: {e}")
#
#        # Mostrar mensaje de error y sugerencia
#        st.error("No se pudo cargar el análisis global. Por favor, verifica los datos o intenta más tarde.")
#
#        # Opción para volver a cargar la página
#        #if st.button("Recargar"):
#         #   st.experimental_rerun()
#with tab2:
#    #guardar pantalla actual
#    st.session_state.pantalla_actual = "area"
#    try:
#        pt_por_area.puntaje_por_area()
#    except Exception as e:
#        st.error(f"Error al cargar la pantalla de análisis por área: {e}")
#
#        # Mostrar mensaje de error y sugerencia
#        st.error("No se pudo cargar el análisis por área. Por favor, verifica los datos o intenta más tarde.")
#
#with tab3:
#    #guardar pantalla actual
#    st.session_state.pantalla_actual = "grupo"
#    try:
#        pt_por_grupo.puntaje_por_grupo()
#    except Exception as e:
#        st.error(f"Error al cargar la pantalla de análisis por grupo: {e}")
#
#        # Mostrar mensaje de error y sugerencia
#        st.error("No se pudo cargar el análisis por grupo. Por favor, verifica los datos o intenta más tarde.")
#with tab4:
#    #guardar pantalla actual
#    st.session_state.pantalla_actual = "año"
#    try:
#        pt_por_año.puntaje_por_año()
#    except Exception as e:
#        st.error(f"Error al cargar la pantalla de análisis por año: {e}")
#
#        # Mostrar mensaje de error y sugerencia
#        st.error("No se pudo cargar el análisis por año. Por favor, verifica los datos o intenta más tarde.")
##with tab5:
##    try:
##        pantalla_olimpiadas.puntaje_olimpiadas()
##    except Exception as e:
##        st.error(f"Error al cargar la pantalla de análisis de olimpiadas: {e}")
##
##        # Mostrar mensaje de error y sugerencia
##        st.error("No se pudo cargar el análisis de olimpiadas. Por favor, verifica los datos o intenta más tarde.")
##        # Si la función puntaje_olimpiadas no existe, comentar la línea siguiente
#with tab6:
#    #guardar pantalla actual
#    st.session_state.pantalla_actual = "qsqs"
#    try:
#        pt_qsqs.puntaje_qsqs()
#    except Exception as e:
#        st.error(f"Error al cargar la pantalla de análisis de Quiero Ser Quiero Saber: {e}")
#
#        # Mostrar mensaje de error y sugerencia
#        st.error("No se pudo cargar el análisis de Quiero Ser Quiero Saber. Por favor, verifica los datos o intenta más tarde.")
#
#with tab7:
#    #guardar pantalla actual
#    st.session_state.pantalla_actual = "descarga"
#    try:
#        pt_descarga.descarga()
#    except Exception as e:
#        st.error(f"Error al cargar la pantalla para descarga: {e}")


