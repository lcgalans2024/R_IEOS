import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards
#from funciones import

def comparativo_grupos():
    st.header("Análisis de resultados por grupo")

def mostrar_metricas_grupo(df, area,año=None):
    if año:
        df = df[df.AÑO == año]
    # Calcular métricas
    minimo = df[area].min()
    maximo = df[area].max()
    promedio = df[area].mean()
    mediana = df[area].median()
    desviacion = df[area].std()

    # Crear tarjetas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=f"Promedio área {area}", value=f"{promedio:.0f}")
    with col2:
        st.metric(label=f"Puntaje máximo {area}", value=f"{maximo:.0f}")
    with col3:
        st.metric(label=f"Puntaje mínimo {area}", value=f"{minimo:.0f}")
    #with col4:
    #    st.metric(label="Mediana", value=mediana)
    #with col5:
    #    st.metric(label="Desviación Estándar", value=desviacion)
    style_metric_cards(border_color="#3A74E7")

def mostrar_puntaje_areas(df,año=None):
    df1 = df[['Matemáticas','Lectura crítica', 'Ciencias naturales', 'Sociales y ciudadanas','Inglés']].mean().reset_index().round(0)
    df1.columns = ['Área', 'Promedio']
    fig = px.bar(df1,
         x="Área",
         y="Promedio",
         color = 'Área',
         #barmode='group',
         text_auto=True
         
         )
    # Actualizar el diseño para etiquetas y título
    fig.update_layout(
            xaxis_title= "Áreas",
            yaxis_title="Promedio",
            title=f"Comparativo puntajes áreas año {año}",
            width=800,     # ancho del gráfico en píxeles
            height=500,    # alto del gráfico en píxeles
            bargap=0.3,  # Reduce la separación entre las barras (ajústalo según tu preferencia)
            xaxis=dict(
                tickangle=-45  # Aquí rotas las etiquetas del eje X
            )
        )
    # Mostrar el gráfico
    st.plotly_chart(fig)
# Mejores y peres puntajes por grupo
def top_tail(df, grupo_seleccionado, area):
    st.markdown(
        f"""
        <div style='
            background-color:#f0f8ff; 
            padding:15px;
            border-radius:10px;
            border: 1px solid #d0d0d0;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            text-align:center
            '>
            <span style='font-size:22px; font-weight:600'>
                Mejores y peores puntajes en la prueba 
                <span style='color:#1f77b4'>ICFE</span> 
                para el área de 
                <span style='color:#d62728'>{area}</span>
                del grupo
                <span style='color:#2ca02c'>{grupo_seleccionado}</span>
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)
    # filtrar datos2 por grupo seleccionado, area seleccionada y simulacro seleccionado
    with col1:
        # seleccionar el grupo
        #grupo_seleccionado = st.selectbox("Seleccione un grupo:", datos_filtrados_simulacro["Grupo"].unique(), key="grupo_seleccionado")
        #st.subheader("Mejores 10 puntajes")
        st.markdown(
            f"""
            <div style='
                    text-align:center
                    '>
                <span style='font-size:22px; font-weight:600'>
                    Mejores 10 puntajes
                </span>
            </div>
            """,
        unsafe_allow_html=True
    )
        # Ordenar por puntaje de area seleccionada y mostrar top 10
        st.dataframe(df[["Nombre alumno", area]].sort_values(by=area, ascending=False).head(10).reset_index(drop=True), use_container_width=True, hide_index=True)
    
    with col2:
        #st.subheader("Ultimos 10 puntajes")
        st.markdown(
            f"""
            <div style='
                    text-align:center
                    '>
                <span style='font-size:22px; font-weight:600'>
                    Peores 10 puntajes
                </span>
            </div>
            """,
        unsafe_allow_html=True
    )
        # Ordenar por puntaje de area seleccionada y mostrar top 10
        st.dataframe(df[["Nombre alumno", area]].sort_values(by=area, ascending=False).tail(10).reset_index(drop=True), use_container_width=True, hide_index=True)