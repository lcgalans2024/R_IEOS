import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards

def puntaje_global(df, filtros):
    st.header("Análisis Puntaje Global 📈")

    # Mostrar gráfico de barras de distribución de puntajes por grupo
    # Agrupar datos por grupo y calcular promedios de puntajes globales
    datos_agrupados = df.groupby(['Grupo','SIMULACRO','AÑO'])['Puntaje global'].mean().round(0).reset_index()
    #datos_agrupados["Grupo"] = datos_agrupados["Grupo"].astype(str)
    #st.dataframe(datos_agrupados.reset_index(drop=True), use_container_width=True, hide_index=True)
    
    # Validar si hay datos
    if datos_agrupados.empty:
          st.warning("⚠️ No se tienen datos aún para este grado en el año seleccionado.")
    else:
          # Crear grafico de barras puntaje global por SIMULACRO
          fig = px.bar(df.groupby(['SIMULACRO'])['Puntaje global'].mean().round(0).reset_index(),
                       x="SIMULACRO",
                       y="Puntaje global",
                       color = 'SIMULACRO',
                       #barmode='group',
                       text_auto=True,
                 category_orders={'SIMULACRO': ['S1', 'S2', 'S3', 'ED1', 'ICFES']},  # <- Orden definido
                 color_discrete_map={
                        'S1': '#83c9ff',
                        'S2': '#39c9ff',
                        'ED1': 'teal',
                        'S3': 'pink',
                        'ICFES': "#1466c3"
                    }

                       )

          #Actualizar el diseño para etiquetas y título
          fig.update_layout(
              xaxis_title="Grupo",
              yaxis_title="Puntaje global",
              title=f"Promedio de puntajes globales por prueba para el grado {filtros['grado']} en el año {filtros['anio']}",
          )

          #Mostrar el gráfico
          st.plotly_chart(fig)

          # Crear gráfico de barras puntaje global por grupo
          # remplazar en Grupo el tercero digito por "_" para los grupos
    datos_agrupados_1 = datos_agrupados.copy()
    datos_agrupados_1["Grupo"] = datos_agrupados_1["Grupo"].astype(str).apply(lambda x: x[:2] + "_" + x[3:] if len(x) > 2 else x)
    # Validar si hay datos
    if datos_agrupados_1.empty:
            st.warning("⚠️ No se tienen datos aún para este año seleccionado.")
    else:
          fig = px.bar(datos_agrupados_1,
                       x="Grupo",
                       y="Puntaje global",
                       color = 'SIMULACRO',
                       barmode='group',
                       text_auto=True,
                 category_orders={'SIMULACRO': ['S1', 'S2', 'S3', 'ED1', 'ICFES']},  # <- Orden definido
                 color_discrete_map={
                        'S1': '#83c9ff',
                        'S2': '#39c9ff',
                        'ED1': 'teal',
                        'S3': 'pink',
                        'ICFES': "#1466c3"
                    }

                       )

          #Actualizar el diseño para etiquetas y título
          fig.update_layout(
              xaxis_title="Grupo",
              yaxis_title="Puntaje global",
              title="Distribución de puntajes globales por grupo en las diferentes pruebas",
          )

          #Mostrar el gráfico
          st.plotly_chart(fig)

    # Metricas globales por prueba
    st.subheader("Métricas Globales por Prueba")

    # Definir la columna por la que se desea agrupar
    columna_prueba = "SIMULACRO"

    # Obtener grupos únicos de la columna elegida
    pruebas_unicos = datos_agrupados[columna_prueba].unique()

    # Crear un selector de grupo con st.selectbox
    prueba_seleccionada = st.selectbox("Seleccione un simulacro o ICFES:", pruebas_unicos)

    # Filtrar los datos según la prueba seleccionada
    datos_filtrados = datos_agrupados[datos_agrupados[columna_prueba] == prueba_seleccionada]

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
            st.metric(label="Mínimo", value=f"{minimo:.0f}")
        with col2:
            st.metric(label="Máximo", value=f"{maximo:.0f}")
        with col3:
            st.metric(label="Promedio", value=f"{media:.0f}")
        style_metric_cards(border_color="#3A74E7")

        #Ordenar por 'Puntaje global' y seleccionar los top 10
        datos_top_10 = df.sort_values(by='Puntaje global', ascending=False).head(10)
        datos_top_10 = datos_top_10[["Grupo","Nombre alumno","Puntaje global"]].reset_index(drop=True)
        datos_top_10["Grupo"] = datos_top_10["Grupo"].astype(str)
        # Crear gráfico de barras para los top 10
        
        st.dataframe(datos_top_10.reset_index(drop=True), use_container_width=True, hide_index=True)
