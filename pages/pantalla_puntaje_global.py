import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards

def puntaje_global():
    st.header("Análisis Puntaje Global 📈")

    # Validar si '1, datos2):' tiene registros
    #if datos1.empty:
    #    st.warning("No hay datos disponibles para mostrar.")
    #    return
    
    #if datos2.empty:
    #    st.warning("No hay datos disponibles para mostrar.")
    #    return

    # Mostrar gráfico de barras de distribución de puntajes por grupo
    # Agrupar datos por grupo y calcular promedios de puntajes globales
    datos_agrupados = st.session_state["datos_filtrados"].groupby(['Grupo','SIMULACRO','AÑO'])['Puntaje global'].mean().round(2).reset_index()
    datos_agrupados["Grupo"] = datos_agrupados["Grupo"].astype(str)
    # Validar si hay datos
    if datos_agrupados.empty:
          st.warning("⚠️ No se tienen datos aún para este grado en el año seleccionado.")
    else:
          # Crear gráfico de barras

          fig = px.bar(datos_agrupados,
                       x="Grupo",
                       y="Puntaje global",
                       color = 'SIMULACRO',
                       barmode='group',
                       text_auto=True
                       )

    #     Actualizar el diseño para etiquetas y título
          fig.update_layout(
              xaxis_title="Grupo",
              yaxis_title="Puntaje global",
              title="Distribución de puntajes globales por grupo",
          )

    #     Mostrar el gráfico
          st.plotly_chart(fig)

    # Metricas globales por prueba
    st.subheader("Métricas Globales por Prueba")

    # Definir la columna por la que se desea agrupar
    columna_prueba = "SIMULACRO"

    # Obtener grupos únicos de la columna elegida
    pruebas_unicos = st.session_state["datos_filtrados"][columna_prueba].unique()

    # Crear un selector de grupo con st.selectbox
    prueba_seleccionada = st.selectbox("Seleccione un simulacro o ICFES:", pruebas_unicos)

    # Filtrar los datos según la prueba seleccionada
    datos_filtrados = st.session_state["datos_filtrados"][st.session_state["datos_filtrados"][columna_prueba] == prueba_seleccionada]

    # Validar si hay datos filtrados
    if datos_filtrados.empty:
        st.warning("⚠️ No se tienen datos aún para este grado en el año seleccionado.")
    else:
        minimo = min(datos_filtrados['Puntaje global'])
        maximo = max(datos_filtrados['Puntaje global'])
        media = datos_filtrados['Puntaje global'].mean()
        desviacion = datos_filtrados['Puntaje global'].std()

        # Mostrar tarjetas con las métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Mínimo", value=f"{minimo:.2f}")
        with col2:
            st.metric(label="Máximo", value=f"{maximo:.2f}")
        with col3:
            st.metric(label="Promedio", value=f"{media:.2f}")
        style_metric_cards(border_color="#3A74E7")

        #Ordenar por 'Puntaje global' y seleccionar los top 10
        datos_top_10 = datos_filtrados.sort_values(by='Puntaje global', ascending=False).head(10)
        datos_top_10 = datos_top_10[["Grupo","Nombre alumno","Puntaje global"]].reset_index(drop=True)
        datos_top_10["Grupo"] = datos_top_10["Grupo"].astype(str)
        # Crear gráfico de barras para los top 10
        
        st.dataframe(datos_top_10.reset_index(drop=True), use_container_width=True, hide_index=True)
