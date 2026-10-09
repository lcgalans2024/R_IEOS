import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards

""" Función para crear el dataframe de frecuencias relativas de los niveles de desempeño por área."""
def crear_dataframe_frecuencias(df):
    df_frecuencias = pd.DataFrame({'Niveles': ['1', '2', '3', '4']})
    # Calcular la frecuencia realativa de estudiantes por nivel de desempeño
    df_frecuencias['Frecuencia'] = df['Nivel_LC'].value_counts().reindex(df_frecuencias['Niveles']).fillna(0).values
    df_frecuencias['Lectura Crítica'] = (df_frecuencias['Frecuencia'] / df_frecuencias['Frecuencia'].sum() * 100).round(2)
    df_frecuencias['Frecuencia'] = df['Nivel_M'].value_counts().reindex(df_frecuencias['Niveles']).fillna(0).values
    df_frecuencias['Matemáticas'] = (df_frecuencias['Frecuencia'] / df_frecuencias['Frecuencia'].sum() * 100).round(2)
    df_frecuencias['Frecuencia'] = df['Nivel_CN'].value_counts().reindex(df_frecuencias['Niveles']).fillna(0).values
    df_frecuencias['Ciencias Naturales'] = (df_frecuencias['Frecuencia'] / df_frecuencias['Frecuencia'].sum() * 100).round(2)
    df_frecuencias['Frecuencia'] = df['Nivel_SC'].value_counts().reindex(df_frecuencias['Niveles']).fillna(0).values
    df_frecuencias['Sociales y Ciudadanas'] = (df_frecuencias['Frecuencia'] / df_frecuencias['Frecuencia'].sum() * 100).round(2)
    df_frecuencias['Frecuencia'] = df['Nivel_ingles_numerico'].value_counts().reindex(df_frecuencias['Niveles']).fillna(0).values
    df_frecuencias['Inglés'] = (df_frecuencias['Frecuencia'] / df_frecuencias['Frecuencia'].sum() * 100).round(2)
    df_frecuencias = df_frecuencias.drop(columns=['Frecuencia'])
    return df_frecuencias

"""Agrupamos por niveles de desempeño, hacemos merge en un dataframe con los porcentajes de estudiantes en cada nivel por área."""

def niveles_desempeño_areas(df,año=None):
    #filtramos el año si es necesario
    if año:
        df = df[df.AÑO == año]
    
    df_niveles = crear_dataframe_frecuencias(df)
    
    #df1 =df[df.AÑO == año].groupby(['Grupo'])[['Matemáticas','Lectura crítica', 'Ciencias naturales', 'Sociales y ciudadanas','Inglés']].mean().reset_index().round(0)
    df1 = df_niveles.melt(id_vars=['Niveles'], var_name="Área", value_name="Promedio")
    fig = px.bar(df1,
             x="Área",
             y="Promedio",
             color = 'Niveles',
             barmode= 'relative',
             text_auto=True,
             category_orders={'Niveles': ['1', '2', '3', '4']},  # <- Orden definido
             color_discrete_map={
                    '1': 'red',
                    '2': 'orange',
                    '3': 'yellow',
                    '4': 'green',
                    'PA1': 'red',
                    'A1': 'orange',
                    'A2': 'yellow',
                    'B1': 'green',
                    'B+': 'green'
                }
             )
    # Actualizar el diseño para etiquetas y título
    fig.update_layout(
            xaxis_title= "Áreas",
            yaxis_title="Porcentaje de Estudiantes (%)",
            title="Comparativo niveles de desempeño por área",
            width=800,     # ancho del gráfico en píxeles
            height=500,    # alto del gráfico en píxeles
            bargap=0.3,  # Reduce la separación entre las barras (ajústalo según tu preferencia)
            xaxis=dict(
                tickangle=-45  # Aquí rotas las etiquetas del eje X
            )
        )
    # Bloquear cambios de escala en ambos ejes
    fig.update_xaxes(fixedrange=True)         
    fig.update_yaxes(fixedrange=True)         
    
    # Mostrar el gráfico
    st.plotly_chart(fig)

""" Creamos función para crear el grafico de que compare las áreas por año.
Los parámetros de entrada son el dataframe y la variable de agrupación, con la que se calculan los promedios de las áreas.
"""
def comparativo_areas(df, variable=None):
    st.header("Puntaje Áreas 📈")

    df1 = df.groupby([variable])[['Matemáticas','Lectura crítica', 'Ciencias naturales', 'Sociales y ciudadanas','Inglés']].mean().reset_index().round(0)
    df1 = df1.melt(id_vars=[variable], var_name="Área", value_name="Promedio")
    fig = px.bar(df1,
             x="Área",
             y="Promedio",
             color = variable,
             barmode='group',
             text_auto=True
             
             )
    # Actualizar el diseño para etiquetas y título
    fig.update_layout(
            xaxis_title= "Áreas",
            yaxis_title="Promedio",
            title="Comparativo puntajes áreas por año",
            width=800,     # ancho del gráfico en píxeles
            height=500,    # alto del gráfico en píxeles
            bargap=0.3,  # Reduce la separación entre las barras (ajústalo según tu preferencia)
            xaxis=dict(
                tickangle=-45  # Aquí rotas las etiquetas del eje X
            )
        )
    # Bloquear cambios de escala en ambos ejes
    fig.update_xaxes(fixedrange=True)         
    fig.update_yaxes(fixedrange=True)         
    
    # Mostrar el gráfico
    st.plotly_chart(fig)

    """ Grafico de barras de puntajes por grupo en cada área.
    Filtra los datos para el año 2025 y agrupa por grupo, calculando el promedio de cada área.
    Luego, utiliza Plotly Express para crear un gráfico de barras agrupadas."""
def comparativo_areas_grupo(df, año=None):
    st.header("Puntaje Áreas por Grupo 📊")

    df1 =df[df.AÑO == año].groupby(['Grupo'])[['Matemáticas','Lectura crítica', 'Ciencias naturales', 'Sociales y ciudadanas','Inglés']].mean().reset_index().round(0)
    df1 = df1.melt(id_vars=['Grupo'], var_name="Área", value_name="Promedio")

    fig = px.bar(df1,
             x="Área",
             y="Promedio",
             color = 'Grupo',
             barmode='group',
             text_auto=True
             
             )
    # Actualizar el diseño para etiquetas y título
    fig.update_layout(
            xaxis_title= "Áreas",
            yaxis_title="Promedio",
            title=f"Comparativo puntajes áreas por grupo en {año}",
            width=800,     # ancho del gráfico en píxeles
            height=500,    # alto del gráfico en píxeles
            bargap=0.3,  # Reduce la separación entre las barras (ajústalo según tu preferencia)
            xaxis=dict(
                tickangle=-45  # Aquí rotas las etiquetas del eje X
            )
        )
    # Bloquear cambios de escala en ambos ejes
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    
    # Mostrar el gráfico
    st.plotly_chart(fig)

""" Función para calcular las metricas de desempeño por área y mostrarlas en tarjetas."""
def mostrar_metricas_area(df, area,año=None):
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

""" Función para obtener los mejores y peores puntajes por área."""
def mejores_peores_puntajes_area(df, area, año=None):
    if año:
        df = df[df.AÑO == año]
    # Mejores y peores puntajes por área
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
                Mejores y peores puntajes en
                <span style='color:#1f77b4'>{area}</span> 
                del año 
                <span style='color:#d62728'>{año}</span>
            </span>
        </div>
        """,
        unsafe_allow_html=True
        )
    col1, col2 = st.columns(2)
    
    datos3 = df[["Grupo","Nombre alumno", area]].copy()
    with col1:
        # Mejores 10 puntajes
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
        st.dataframe(datos3.sort_values(by=area, ascending=False).head(10).reset_index(drop=True), use_container_width=True, hide_index=True)
    
    with col2:
        # Ultimos 10 puntajes
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
        st.dataframe(datos3.sort_values(by=area, ascending=False).tail(10).reset_index(drop=True), use_container_width=True, hide_index=True)