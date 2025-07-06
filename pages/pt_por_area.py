import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards

def puntaje_por_area():
    st.header("Análisis por Área 🧮")

    # Verifica si los datos están en session_state
    if "datos_filtrados" not in st.session_state:
        st.warning("No se han cargado datos aún.")
        return
    
    # cargar los datos
    df = st.session_state["datos_filtrados"].groupby(['SIMULACRO'])[["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().round(2).reset_index()
    df_p = st.session_state["datos_filtrados"].groupby(['Grupo'
                                                         #,'SIMULACRO'
                                                         ])[["Matemáticas",
                                                             "Lectura crítica",
                                                             "Ciencias naturales",
                                                             "Sociales y ciudadanas",
                                                             "Inglés"
                                                             ]].mean().round(2).reset_index()
    st.dataframe(df_p.reset_index(drop=True), use_container_width=True, hide_index=True)
    # deretir datos por columnas de areas
    df_melt = df_p.melt(id_vars=['Grupo'], var_name="Área", value_name="Promedio")
    st.dataframe(df_melt.reset_index(drop=True), use_container_width=True, hide_index=True)
    # Crear gráfico de barras
    fig = px.bar(df_melt,
                 x ="Área",
                 y="Promedio",
                 color="Grupo",
                 barmode= "group",#['stack', 'group', 'overlay', 'relative'],
                 text_auto=True,
                 #category_orders={'Grupo': df_p['Grupo'].unique()},  # <- Orden definido
                 color_discrete_map={
                        '1': '#83c9ff',
                        '2': 'red',
                        '3': 'teal',
                        '4': 'pink',
                        '5': "#1466c3"
                    }
                 ) 
    # Actualizar el diseño para etiquetas y título
    fig.update_layout(
        xaxis_title="Grupos",
        yaxis_title="Puntaje promedio",
        title=f"Comportamiento en las areas por grupo"
        #,xaxis_tickangle=-45,
    )
    # Mostrar el gráfico
    st.plotly_chart(fig)

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
                     text_auto=True,
                 category_orders={'SIMULACRO': ['S1', 'S2', 'S3', 'ED1', 'ICFES']},  # <- Orden definido
                 color_discrete_map={
                        'S1': '#83c9ff',
                        'S2': 'red',
                        'ED1': 'teal',
                        'S3': 'pink',
                        'ICFES': "#1466c3"
                    }
                     )
        
        # Actualizar el diseño para etiquetas y título
        fig.update_layout(
            xaxis_title="Áreas",
            yaxis_title="Puntaje promedio",
            title=f"Distribución de puntajes por área para cada prueba"
            #,xaxis_tickangle=-45,
        )

        # Mostrar el gráfico
        st.plotly_chart(fig)

        col1, col2, col3 = st.columns(3)

        with col1:
            # seleccionar el area
            area_seleccionada = st.selectbox("Seleccione un área:", df.columns[1:], key="area_seleccionada")

        # Filtrar los datos según el área y el simulacro seleccionados
        
        datos_filtrados_area = st.session_state["datos_filtrados"][['SIMULACRO','Grupo',area_seleccionada]].copy()

        #st.dataframe(datos_filtrados_area.reset_index(drop=True), use_container_width=True, hide_index=True)

        with col2:
            # Seleccionar el simulacro
            simulacro_seleccionado = st.selectbox("Seleccione un simulacro:", df["SIMULACRO"].unique(), key="simulacro_seleccionado")

        # Filtrar los datos según el área y el simulacro seleccionados
        datos_filtrados_simulacro = datos_filtrados_area[(datos_filtrados_area.SIMULACRO == simulacro_seleccionado)].copy()

        # Validar si hay datos filtrados
        if datos_filtrados_simulacro.empty:
            st.warning("⚠️ No se tienen datos aún para este grado en el año seleccionado.")
        else:
            minimo = min(datos_filtrados_simulacro[f'{area_seleccionada}'])
            maximo = max(datos_filtrados_simulacro[f'{area_seleccionada}'])
            media = datos_filtrados_simulacro[f'{area_seleccionada}'].mean()
            desviacion = datos_filtrados_simulacro[f'{area_seleccionada}'].std()
        # Mostrar tarjetas con las métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label=f"Promedio Grado {st.session_state.grado_seleccionado}", value=f"{media:.2f}")
        with col2:
            st.metric(label=f"Máximo Grado {st.session_state.grado_seleccionado}", value=f"{maximo:.2f}")
        with col3:
            st.metric(label=f"Mínimo Grado {st.session_state.grado_seleccionado}", value=f"{minimo:.2f}")
        style_metric_cards(border_color="#3A74E7")

        # Validar si hay datos filtrados
        if datos_filtrados_area.empty:
            st.warning(f"⚠️ No se tienen datos aún para este grado en el año seleccionado.")
        else:
            # Crear gráfico de barras
            fig = px.bar(datos_filtrados_area.groupby(['Grupo','SIMULACRO'])[area_seleccionada].mean().round(2).reset_index(),
                         x="Grupo",
                         y=area_seleccionada,
                         color="SIMULACRO",
                         barmode='group',
                         text_auto=True,
                 category_orders={'SIMULACRO': ['S1', 'S2', 'S3', 'ED1', 'ICFES']},  # <- Orden definido
                 color_discrete_map={
                        'S1': '#83c9ff',
                        'S2': 'red',
                        'ED1': 'teal',
                        'S3': 'pink',
                        'ICFES': "#1466c3"
                    }
                         )

            # Actualizar el diseño para etiquetas y título
            fig.update_layout(
                xaxis_title="Grupo",
                yaxis_title="Puntaje promedio",
                title=f"Distribución de puntaje en {area_seleccionada} por grupo"
            )

            # Mostrar el gráfico
            st.plotly_chart(fig)
        
        try:
            if area_seleccionada == "Lectura crítica":
                nivel_seleccionado = 'ND_LC'
            elif area_seleccionada == "Matemáticas":
                nivel_seleccionado = 'ND_M'
            elif area_seleccionada == "Ciencias naturales":
                nivel_seleccionado = 'ND_CN'

            df_N_simulacro = st.session_state["datos_filtrados"][st.session_state["datos_filtrados"]['SIMULACRO'] == simulacro_seleccionado].copy()
            df_N = df_N_simulacro.groupby(['Grupo',nivel_seleccionado])[area_seleccionada].count().reset_index()
            df_N["porcentaje"] = df_N.groupby(['Grupo'])[area_seleccionada].transform(lambda x: x / x.sum() * 100).round(2)
            #st.dataframe(df_N.reset_index(drop=True), use_container_width=True, hide_index=True)

            # Crear gráfico de barras
            fig = px.bar(df_N,
                         x="Grupo",
                         y="porcentaje",
                         color=nivel_seleccionado,
                         barmode='relative',
                         text_auto=True,
                 category_orders={nivel_seleccionado: ['1', '2', '3', '4']},  # <- Orden definido
                 color_discrete_map={
                        '1': 'red',
                        '2': 'orange',
                        '3': 'yellow',
                        '4': 'green'
                    }
                         )
            # Actualizar el diseño para etiquetas y título
            fig.update_layout(
                xaxis_title="Grupo",
                yaxis_title="Porcentaje",
                title=f"Distribución porcentual nivel de desempeño en {area_seleccionada} por grupo"
            )
            # Mostrar el gráfico
            st.plotly_chart(fig)
        except:
            st.warning(f"⚠️ Para el área {area_seleccionada} no se tienen niveles de desempeño definidos.")
            

        #st.subheader(f"Mejores y perores puntajes en el {simulacro_seleccionado} para el area de {area_seleccionada}")
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
                    Mejores y peores puntajes en el 
                    <span style='color:#1f77b4'>{simulacro_seleccionado}</span> 
                    para el área de 
                    <span style='color:#d62728'>{area_seleccionada}</span>
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        # filtrar datos2 por grupo seleccionado, area seleccionada y simulacro seleccionado
        datos3 = st.session_state["datos_filtrados"][(st.session_state["datos_filtrados"]['SIMULACRO'] == simulacro_seleccionado)][["Grupo","Nombre alumno", area_seleccionada]].copy()

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
            st.dataframe(datos3.sort_values(by=area_seleccionada, ascending=False).head(10).reset_index(drop=True), use_container_width=True, hide_index=True)
        
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
            st.dataframe(datos3.sort_values(by=area_seleccionada, ascending=False).tail(10).reset_index(drop=True), use_container_width=True, hide_index=True)
        
        


    

        