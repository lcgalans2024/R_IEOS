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