import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards

def puntaje_por_grupo(df,filtros):
    st.header("Análisis por Grupo 👥")

    col1, col2, col3 = st.columns(3)

    with col1:
        # seleccionar el area
        grupo_seleccionado = st.selectbox("Seleccione un grupo:", df.Grupo.unique(), key="grupo_seleccionada")

        datos_grupos = df.groupby(['Grupo','SIMULACRO'])[["Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().round(0).reset_index()

    # derretir datos_agrupados por columnas de areas
    datos_derretidos = datos_grupos.melt(id_vars=['Grupo','SIMULACRO'], var_name="Área", value_name="Promedio")

    # Seleccionamos grupo
    datos_grupo_seleccionado = datos_derretidos[datos_derretidos.Grupo== grupo_seleccionado]

    # Crear gráfico de barras por area
    fig = px.bar(datos_grupo_seleccionado,
                 x="Área",
                 y="Promedio",
                 color = 'SIMULACRO',
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
          xaxis_title="Áreas",
          yaxis_title="Promedios",
          title=f"Distribución de puntajes por área del grupo {grupo_seleccionado} en el año {filtros["anio"]}"
          #xaxis_tickangle=-45,
    )

    # Mostrar el gráfico
    #fig.show()
    st.plotly_chart(fig)

    col1, col2, col3 = st.columns(3)

    with col1:
        # seleccionar el area
        area = st.selectbox("Seleccione un área:", datos_grupos.columns[2:], key="areaseleccionada")
    # Filtrar los datos según el área y el simulacro seleccionados
    
    #datos_filtrados_area = st.session_state["datos_filtrados"][['SIMULACRO','Grupo',area]].copy()
    #st.dataframe(datos_filtrados_area.reset_index(drop=True), use_container_width=True, hide_index=True)
    with col2:
        # Seleccionar el simulacro
        simulacro_seleccionado = st.selectbox("Seleccione un simulacro:", datos_grupo_seleccionado["SIMULACRO"].unique(), key="simulacroseleccionado")
    # Filtrar los datos según el área y el simulacro seleccionados
    datos4 = df[(df["Grupo"]==grupo_seleccionado) &
                                                 (df["SIMULACRO"]==simulacro_seleccionado)
                                                 ][["Nombre alumno", area]].copy()
    # Validar si hay datos filtrados
    if datos4.empty:
        st.warning("⚠️ No se tienen datos aún para este grado en el año seleccionado.")
    else:
        minimo = min(datos4[f'{area}'])
        maximo = max(datos4[f'{area}'])
        media = datos4[f'{area}'].mean()
        desviacion = datos4[f'{area}'].std()
    # Mostrar tarjetas con las métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label=f"Promedio Grupo {grupo_seleccionado}", value=f"{media:.0f}")
    with col2:
        st.metric(label=f"Máximo Grupo {grupo_seleccionado}", value=f"{maximo:.0f}")
    with col3:
        st.metric(label=f"Mínimo Grupo {grupo_seleccionado }", value=f"{minimo:.0f}")
    #style_metric_cards(border_color="#3A74E7")

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
                Mejores y peores puntajes en la prueba 
                <span style='color:#1f77b4'>{simulacro_seleccionado}</span> 
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
        st.dataframe(datos4.sort_values(by=area, ascending=False).head(10).reset_index(drop=True), use_container_width=True, hide_index=True)
    
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
        st.dataframe(datos4.sort_values(by=area, ascending=False).tail(10).reset_index(drop=True), use_container_width=True, hide_index=True)
    