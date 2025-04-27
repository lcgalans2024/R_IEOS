import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards

def puntaje_por_area(datos1, datos2):
    st.header("Análisis por Área 🧮")
    
    # Validar si 'datos' tiene registros
    if datos1.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return
    
    if datos2.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return
    # cargar los datos
    df = datos2.groupby(['SIMULACRO'])[["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().round(2).reset_index()

    # Validar si hay datos
    if df.empty:
        st.warning("⚠️ No se tienen datos aún para este grado en el año seleccionado.")
    else:

        # derretir datos_agrupados por columnas de areas
        df_derretidos = df.melt(id_vars=['SIMULACRO'], var_name="Área", value_name="Promedio")
        # Crear gráfico de barras
        fig = px.bar(df_derretidos,
                     x ="Área",
                     y="Promedio",
                     color="SIMULACRO",
                     barmode= "group",#['stack', 'group', 'overlay', 'relative'],
                     text_auto=True
                     )
        
        # Actualizar el diseño para etiquetas y título
        fig.update_layout(
            xaxis_title="Áreas",
            yaxis_title="Puntaje promedio",
            title="Distribución de puntajes por área",
        )

        # Mostrar el gráfico
        st.plotly_chart(fig)

        col1, col2, col3 = st.columns(3)

        with col1:
            # seleccionar el area
            area_seleccionada = st.selectbox("Seleccione un área:", df.columns[1:], key="area_seleccionada")

        # Filtrar los datos según el área y el simulacro seleccionados
        datos_filtrados = datos2[datos2.AÑO == '2024'][['SIMULACRO','Grupo',area_seleccionada]].copy()

        st.dataframe(datos_filtrados, use_container_width=True)

        # Validar si hay datos filtrados
        if datos_filtrados.empty:
            st.warning("⚠️ No se tienen datos aún para este grado en el año seleccionado.")
        else:
            # Crear gráfico de barras
            fig = px.bar(datos_filtrados,
                         x="Grupo",
                         y=area_seleccionada,
                         color="SIMULACRO",
                         barmode='group',
                         text_auto=True
                         )

            # Actualizar el diseño para etiquetas y título
            fig.update_layout(
                xaxis_title="Grupo",
                yaxis_title="Puntaje promedio",
                title=f"Distribución de puntaje en {area_seleccionada} por grupo"
            )

            # Mostrar el gráfico
            st.plotly_chart(fig)

        with col2:
            # Seleccionar el simulacro
            simulacro_seleccionado = st.selectbox("Seleccione un simulacro:", df["SIMULACRO"].unique(), key="simulacro_seleccionado")

        # Filtrar los datos según el área y el simulacro seleccionados
        datos_filtrados = datos_filtrados[(datos_filtrados.SIMULACRO == simulacro_seleccionado)].copy()

        st.dataframe(datos_filtrados, use_container_width=True)

    

        