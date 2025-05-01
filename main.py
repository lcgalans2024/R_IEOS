import streamlit as st
import sidebar
from pages import pantalla_puntaje_global, pt_por_area, pt_por_grupo, pt_por_año, pantalla_olimpiadas

# Configuracion general
st.set_page_config(page_title="Dashboard Institucional", layout="wide")

st.title("ANÁLISIS RESULTADOS INSTITUCIONALES")
st.subheader("⚠️ Este es un espacio en construcción ⚠️")

# Configurar sidebar y cargar datos
sidebar.sidebar_config()

# Tabs principales del Dashboard
tabs = [
    "Análisis Puntaje Global",
    "Análisis Por Area",
    "Análisis Por Grupo",
    "Análisis Por Año",
    "Olimpiadas Institucionales",
]

# Crear Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs)

# Lógica de cada pantalla
with tab1:
    try:
        pantalla_puntaje_global.puntaje_global()

    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis global: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis global. Por favor, verifica los datos o intenta más tarde.")

        # Opción para volver a cargar la página
        #if st.button("Recargar"):
         #   st.experimental_rerun()
with tab2:
    try:
        pt_por_area.puntaje_por_area()
    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis por área: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis por área. Por favor, verifica los datos o intenta más tarde.")

with tab3:
    try:
        pt_por_grupo.puntaje_por_grupo()
    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis por grupo: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis por grupo. Por favor, verifica los datos o intenta más tarde.")
with tab4:
    try:
        pt_por_año.puntaje_por_año()
    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis por año: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis por año. Por favor, verifica los datos o intenta más tarde.")
with tab5:
    try:
        pantalla_olimpiadas.puntaje_olimpiadas()
    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis de olimpiadas: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis de olimpiadas. Por favor, verifica los datos o intenta más tarde.")
        # Si la función puntaje_olimpiadas no existe, comentar la línea siguiente
