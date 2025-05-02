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
            title=f"Distribución de puntajes por área grado {st.session_state.grado_seleccionado}"
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
        
        


    

        