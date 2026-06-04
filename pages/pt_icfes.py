import streamlit as st
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards

from funciones import asignar_nivel_desempeno

import sections.pt_2_ICFES.sidebar as sidebar

import utils.navegacion 
import utils.data

utils.navegacion.generarMenu()
import utils.data
from sections.pt_2_ICFES import st_general, st_areas, st_grupos, st_municipal#, st_descarga

# Configurar sidebar
filtros = sidebar.render_sidebar()  # <- todo el sidebar queda encapsulado
st.title("ICFES")

# Cargar datos del ICFES al iniciar la aplicación
datos_icfes = utils.data.cargar_datos_icfes()

# Aplicar filtros
#datos_icfes = utils.data.filtrar_datos(datos_icfes, filtros)

# eliminar espacios en AÑO
datos_icfes["AÑO"] = datos_icfes["AÑO"].astype(str).apply(lambda x: str(x).strip())

#st.dataframe(datos_icfes, use_container_width=True, hide_index=True)

# Tabs principales del Dashboard
tabs = [
    "Puntaje Global ICFES",
    "Puntajes Áreas",
    "Puntajes Grupos",
    "Puntajes Entidad Territorial",
    "Descarga de Datos"
]

# Crear Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs)
# Lógica de cada pantalla
with tab1:
    #guardar pantalla actual
    st.session_state.pantalla_actual = "global"
    try:
        st_general.puntaje_global(datos_icfes, filtros, variable="Puntaje global")

        # Puntaje global por grupo
        st_general.puntaje_por_grupo(datos_icfes, filtros, variable="Puntaje global")
        
    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis global: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis global. Por favor, verifica los datos o intenta más tarde.")

with tab2:
    #guardar pantalla actual
    st.session_state.pantalla_actual = "area"
    try:
        asignar_nivel_desempeno(datos_icfes)

        st_areas.comparativo_areas(datos_icfes, variable="AÑO")

        # Definimos dos columnas
        col1, col2 = st.columns(2)
        with col1:
            # Selector de año para gráfico por grupo
            año_seleccionado = st.selectbox("Selecciona el año:", options=datos_icfes["AÑO"].unique(), key="select_año_area", index=1)
        with col2:
            st.write(" ")
        
        st_areas.comparativo_areas_grupo(datos_icfes, año=año_seleccionado)

        st_areas.niveles_desempeño_areas(datos_icfes, año=año_seleccionado)

        # Mostrar métricas de desempeño por área
        # crear selector de área
        area = st.selectbox("Selecciona el área para ver métricas:", options=["Lectura crítica", "Matemáticas", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"])

        st_areas.mostrar_metricas_area(datos_icfes, area=area, año=año_seleccionado)

        # Mejores y peores puntajes por área
        st_areas.mejores_peores_puntajes_area(datos_icfes, area=area, año=año_seleccionado)

    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis por área: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis por área. Por favor, verifica los datos o intenta más tarde.")

with tab3:
    #guardar pantalla actual
    st.session_state.pantalla_actual = "grupo"
    try:
        st_grupos.comparativo_grupos()

        # Definimos dos columnas
        col1, col2 = st.columns(2)
        with col1:
            # Selector de año para gráfico por grupo
            año_seleccionado = st.selectbox("Selecciona el año:", options=datos_icfes["AÑO"].unique(), key="select_año_grupo", index=1)
        with col2:
            grupo_seleccionado = st.selectbox("Selecciona el grupo:", options=datos_icfes[datos_icfes["AÑO"]==año_seleccionado]["Grupo"].unique(), key="select_grupo", index=0)

        df = datos_icfes[(datos_icfes["AÑO"]==año_seleccionado) & (datos_icfes["Grupo"]== grupo_seleccionado)]

        st_grupos.mostrar_metricas_grupo(df,'Puntaje global')

        st_grupos.mostrar_puntaje_areas(df, año_seleccionado)

        st_areas.niveles_desempeño_areas(df)

        area_seleccionado = st.selectbox("Selecciona el area:", options=["Lectura crítica", "Matemáticas", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"], key="select_area", index=0)

        st_grupos.top_tail(df, grupo_seleccionado, area_seleccionado)
    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis por área: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis por área. Por favor, verifica los datos o intenta más tarde.")

with tab4:
    #guardar pantalla actual
    st.session_state.pantalla_actual = "ET"
    try:
        st_municipal.ranking()

        df = st.session_state.datos_historicos.copy()
        df.rename(columns={'Promedio':'Puntaje'},inplace=True)
        
        #st.dataframe(df)

        # Definimos dos columnas
        col1, col2, col3 = st.columns(3)
        with col1:
            # Selector de año para gráfico por grupo
            año_seleccionado = st.selectbox("Selecciona el periodo:", options=sorted(df["Periodo"].unique(), reverse=True), index=1)
        with col2:
            area_seleccionada = st.selectbox("Selecciona el área:", options=df["Area"].unique(), index=0)
        with col3:
            sector_seleccionado = st.multiselect("Selecciona el sector:",
                                                 df["Sector"].unique().tolist(),
                                                 default=df["Sector"].unique().tolist()
        )
        #st.dataframe(st.session_state.datos_historicos)
        df_general = df[(df['Periodo'] == año_seleccionado)
                & (df['Area'] == area_seleccionada)
                & (df['Sector'].isin(sector_seleccionado))
                ].copy()
        df_general['Puntaje'] = pd.to_numeric(df_general['Puntaje'], errors='coerce')

        # Sort by Puntaje descending
        df_general = df_general.sort_values('Puntaje', ascending=True)

        # Asignar un color único a cada colegio
        unique_colegios = df_general['Colegio'].unique()
        palette = px.colors.qualitative.Plotly  # Puedes probar 'Set3', 'Pastel1', 'Dark24', etc.
        color_map = {c: palette[i % len(palette)] for i, c in enumerate(unique_colegios)}
        colors = df_general['Colegio'].map(color_map)

        # Create horizontal bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=df_general['Puntaje'],
                y=df_general['Colegio'],
                orientation='h',
                text=df_general['Puntaje'].round(1),
                textposition='auto',
                marker=dict(
            color=df_general['Puntaje'],
            colorscale='Viridis',
            showscale=True
        )
                
            )
        ])

        # Update layout
        fig.update_layout(
            title='Puntajes Globales ICFES por Institución Oficial 2025',
            xaxis_title='Puntaje',
            yaxis_title='Institución Educativa',
            height=800,  # Make plot taller to accommodate all institutions
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        st.plotly_chart(fig)
    
        colegio_seleccionado = st.selectbox("Selecciona la institución:", options=df["Colegio"].unique(), index=0)

        df_general = df[(df['Area'] == 'General') & (df.Colegio == colegio_seleccionado)].copy()
        
        df_general['Puntaje'] = pd.to_numeric(df_general['Puntaje'], errors='coerce')

        # Sort by Puntaje descending
        df_general = df_general.sort_values('Periodo', ascending=True)
        # Create horizontal bar chart
        fig = px.line(df_general,
                x='Periodo',
                y='Puntaje',
                #barmode='group',
                color='Colegio',
                markers=True,
                line_group='Colegio',
                hover_name='Colegio',
                #orientation='h',
                category_orders={'Periodo': ['2016-2', '2017-2', '2018-2', '2019-4', '2020-4','2021-4', '2022-4', '2023-4','2024-3', '2025-3']},
                text=df_general['Puntaje'].round(1),
            )

        # Update layout
        fig.update_layout(
            title='Puntajes Globales ICFES por Institución',
            xaxis_title='Puntaje',
            yaxis_title='Institución Educativa',
            height=800,  # Make plot taller to accommodate all institutions
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        st.plotly_chart(fig)
        ###################################################################################################
        DF = df[(df['Area'] == area_seleccionada)
                & (df['Sector'].isin(sector_seleccionado))
                 & ~(df.Colegio.isin(['INSTITUCIÓN EDUCATIVA ALIANZA PARA LA EDUCACIÓN EDUCANDO S.A.S']))
                 ].copy()
        st.dataframe(DF.sort_values('Periodo', ascending=True))
        DF = DF.sort_values('Periodo', ascending=True)
        fig = px.line(
        DF,
        x='Periodo',
        y='Puntaje',
        color='Colegio',
        markers=True,
        line_group='Colegio',
        hover_name='Colegio',
        title='Evolución del Puntaje por Colegio',
        )

        fig.update_layout(
            xaxis_title='Periodo',
            yaxis_title='Puntaje ICFES',
            height=700
        )

        st.plotly_chart(fig)
        ###################################################################################################
        fig = px.bar(
        DF,
        x='Puntaje',
        y='Colegio',
        color='Colegio',
        animation_frame='Periodo',
        orientation='h',
        range_x=[DF['Puntaje'].min(), DF['Puntaje'].max()],
        title='Evolución de Puntajes ICFES por Colegio a través del tiempo'
        )

        fig.update_layout(height=800)

        #st.plotly_chart(fig)
        ######################################################################################################
        
        colegio_destacado = st.selectbox("Selecciona la institución:", options=DF["Colegio"].unique(), index=0)
        colegio_destacado = colegio_destacado
        #DF['Colegio'] = DF['Colegio'].str.slice(0, 25)  # corta los nombres a 25 caracteres
        
        
        # Asegurar que los periodos estén en orden correcto
        DF['Periodo'] = pd.Categorical(DF['Periodo'], ordered=True,
                               categories=sorted(DF['Periodo'].unique()))
        #st.write(sorted(DF['Periodo'].unique()))
        #st.dataframe(DF)
        # Calcular cambio porcentual por colegio
        DF = DF.sort_values(['Periodo','Colegio'])
        #st.dataframe(DF)

        # Agregamos un slider para seleccionar el tiempo entre frame
        duracion_frame = st.slider("Seleccione un valor", min_value=0, max_value=5000, step=10)
        # Agregamos un slider para seleccionar la transición
        duracion_transicion = st.slider("Seleccione un valo", min_value=0, max_value=5000, step=10)

        DF['Cambio_%'] = DF.groupby('Colegio')['Puntaje'].pct_change() * 100
        DF['Cambio_%'] = DF['Cambio_%'].fillna(0)

        # Calcular promedio general por periodo
        promedios = DF.groupby('Periodo')['Puntaje'].mean().reset_index(name='Promedio')

        # Color verde si sube, rojo si baja
        #DF['Color'] = DF['Cambio_%'].apply(lambda x: 'green' if x > 0 else ('red' if x < 0 else 'gray'))
        DF['Color'] = DF['Colegio'].apply(lambda x: 'red' if x == colegio_destacado else 'lightgray')

        # Rellenar el primer periodo (NaN) con 0
        #DF['Cambio_%'] = DF['Cambio_%'].fillna(0)

        # Crear texto combinando puntaje y cambio porcentual
        DF['texto_barra'] = (
            #DF['Colegio'] + '<br>' +       # 👈 agrega el nombre arriba o abajo del puntaje
            DF['Puntaje'].round(1).astype(str)# +
            #' (' + DF['Cambio_%'].round(1).astype(str) + '%)'
        )

        fig = px.bar(
            DF,
            x='Puntaje',
            y='Colegio',
            color='Color',
            orientation='h',
            animation_frame='Periodo',
            animation_group='Colegio',
            text='texto_barra',
            
            #range_x=[DF['Puntaje'].min() * 0.95, DF['Puntaje'].max() * 1.05],
            range_x=[200, 350],
            #text=DF['Puntaje'].round(1),
            #color_discrete_sequence=px.colors.qualitative.Set3,
            title=f'🏁 Evolución del Puntaje ICFES {colegio_destacado}',
            color_discrete_map={'gold': 'red', 'lightgray': 'lightblue'}
        )

        #fig.update_traces(
        #    textposition='outside'#,   # o 'auto' si quieres que ajuste
        ##    insidetextanchor='middle'
        #)

        # 🔧 Configuraciones adicionales
        fig.update_layout(
            xaxis_title='Puntaje ICFES',
            yaxis_title='Institución Educativa',
            height=1000,
            showlegend=False,
            margin=dict(l=80, r=20, t=60, b=20),
            font=dict(size=16, color='black', family='Arial Black')
        )

        


        # Hace que las barras cambien su orden cada frame
        fig.update_yaxes(categoryorder='total ascending')
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = int(duracion_frame)  # 1s entre frames
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = int(duracion_transicion)

        st.plotly_chart(fig)

        fig2 = px.line(
        DF[DF['Colegio'] == colegio_destacado],
        x='Periodo',
        y='Puntaje',
        markers=True,
        title=f'Evolución del Puntaje de {colegio_destacado}'
        )
        st.plotly_chart(fig2)
        ##############################################################################################
        
        ##############################################################################################

        
    except Exception as e:
        st.error(f"Error al cargar la pantalla de análisis por área: {e}")

        # Mostrar mensaje de error y sugerencia
        st.error("No se pudo cargar el análisis por área. Por favor, verifica los datos o intenta más tarde.")