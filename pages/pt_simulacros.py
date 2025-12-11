import streamlit as st
import pandas as pd
import sections.pt_1_simulacros.sidebar as sidebar
import utils.navegacion

utils.navegacion.generarMenu()

import utils.data
from sections.pt_1_simulacros import st_puntaje_global, st_puntaje_area, st_puntaje_grupo, st_puntaje_año, st_descarga

# Configurar sidebar
#filtros = sidebar.render_sidebar()  # <- todo el sidebar queda encapsulado
filtros = sidebar.render_sidebar()  # <- todo el sidebar queda encapsulado
st.title("Simulacros ICFES")
#st.write(filtros)

# Cargar df al iniciar la aplicación
#st.write(datos_icfes.head())
# mostrar tipos de datos
#st.write(df.dtypes)
# Aplicar filtros
df = utils.data.filtrar_datos(st.session_state.Datos, filtros)
#st.dataframe(df.head(10), use_container_width=True)
#st.dataframe(st.session_state["datos_filtrados"].head(10), use_container_width=True)
# Tabs principales del Dashboard
tabs = [
    "Análisis Puntaje Global",
    "Análisis Por Area",
    "Análisis Por Grupo",
    "Análisis Por Año",
    "Descarga de Datos",
    "Información"
]

# Crear Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tabs)

# Lógica de cada pantalla
with tab1:
    #guardar pantalla actual
    st.session_state.pantalla_actual = "global"
    try:
        st_puntaje_global.puntaje_global(df,filtros)

    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis global: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis global. Por favor, verifica los datos o intenta más tarde.")

with tab2:
    #guardar pantalla actual
    st.session_state.pantalla_actual = "area"
    try:
        st_puntaje_area.puntaje_por_area(df,filtros)
    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis por área: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis por área. Por favor, verifica los datos o intenta más tarde.")

with tab3:
    #guardar pantalla actual
    st.session_state.pantalla_actual = "grupo"
    try:
        st_puntaje_grupo.puntaje_por_grupo(df,filtros)
    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis por grupo: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis por grupo. Por favor, verifica los datos o intenta más tarde.")
with tab4:
    #guardar pantalla actual
    st.session_state.pantalla_actual = "año"
    try:
        st_puntaje_año.puntaje_por_año()
    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis por año: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis por año. Por favor, verifica los datos o intenta más tarde.")

with tab5:
    #guardar pantalla actual
    st.session_state.pantalla_actual = "descarga"
    try:
        st_descarga.descarga()
    except Exception as e:
        st.error(f"Error al cargar la pantalla para descarga: {e}")

with tab6:
    st.session_state.pantalla_actual = "info"
    st.header("Validación de Información ℹ️")

    st.dataframe(df.head(10), use_container_width=True)
    # mostrar columnas disponibles
    st.subheader("Columnas disponibles en el conjunto de datos:")
    st.write(df.columns.tolist())
