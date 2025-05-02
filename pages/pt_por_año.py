import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards

def puntaje_por_año():
    st.header("Análisis por Año 📅")

    # Verifica si los datos están en session_state
    if "datos_filtrados" not in st.session_state:
        st.warning("No se han cargado datos aún.")
        return
    
    # cargar los datos
    df = st.session_state["datos"]

    # filtrar datos por grado once de 2025 y grado decimo de 2024
    df1 = df[((df['AÑO'] == '2025') & (df['Grupo'].str.startswith('110'))) | ((df['AÑO'] == '2024') & (df['Grupo'].str.startswith('100')))]

    # Agrupamos por año y calculamos los promedios de las areas
    df2 = df1.groupby(['AÑO'])[["Puntaje global","Matemáticas", "Lectura crítica", "Ciencias naturales", "Sociales y ciudadanas", "Inglés"]].mean().round(2).reset_index().melt(id_vars="AÑO", var_name="Área", value_name="Promedio")

    # Realizamos grafico de barras
    fig = px.bar(df2[df2["Área"] == "Puntaje global"],
                 x="Promedio",
                 y="Área",
                 color = 'AÑO',
                 barmode='group',
                 text_auto=True
                 )
    # Actualizar el diseño para etiquetas y título
    fig.update_layout(
        xaxis_title="Área",
        yaxis_title="Puntaje promedio",
        title=f"Comparativo puntaje global décimo 2024 vs once 2025"
    )
    # Mostrar el gráfico
    st.plotly_chart(fig)

    # Realizamos grafico de barras
    fig = px.bar(df2[df2["Área"] != "Puntaje global"],
                 x="Área",
                 y="Promedio",
                 color = 'AÑO',
                 barmode='group',
                 text_auto=True
                 )
    # Actualizar el diseño para etiquetas y título
    fig.update_layout(
        xaxis_title="Área",
        yaxis_title="Puntaje promedio",
        title=f"Comparativo décimo 2024 vs once 2025 por área"
    )
    # Mostrar el gráfico
    st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    with col1:

        # Mostrar los 10 primeros registros de los datos filtrados
        st.subheader("Mejores 10 puntaje global en 2024")
        df_top_10_2024 = df1[df1.AÑO == "2024"].sort_values(by='Puntaje global', ascending=False).head(10)
        df_top_10_2024 = df_top_10_2024[["Grupo","Nombre alumno","Puntaje global"]].reset_index(drop=True)

        st.dataframe(df_top_10_2024, use_container_width=True, hide_index=True)
    with col2:
        # Mostrar los 10 primeros registros de los datos filtrados
        st.subheader("Mejores 10 puntaje global en 2025")
        df_top_10_2025 = df1[df1.AÑO == "2025"].sort_values(by='Puntaje global', ascending=False).head(10)
        df_top_10_2025 = df_top_10_2025[["Grupo","Nombre alumno","Puntaje global"]].reset_index(drop=True)

        st.dataframe(df_top_10_2025, use_container_width=True, hide_index=True)
    #st.dataframe(st.session_state["datos"])
    #st.dataframe(df2.reset_index(drop=True), use_container_width=True, hide_index=True)
