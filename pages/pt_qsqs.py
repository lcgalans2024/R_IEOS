import streamlit as st
#import plotly.express as px
#import plotly.graph_objects as go
#import matplotlib.pyplot as plt
#from streamlit_extras.metric_cards import style_metric_cards

# Función para la pantalla de Quiero Ser Quiero Saber
def puntaje_qsqs():
    st.header("Quiero Ser Quiero Saber 📚")
    # Validar si 'datos' tiene registros
    if "datos_qsqs" not in st.session_state:
        st.warning("No se han cargado datos aún.")
        return
    # cargar los datos
    df = st.session_state["datos_qsqs"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    # filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        area = st.multiselect(
            "Selecciona el área",
            df['Área'].unique().tolist(),
            default=df['Área'].unique().tolist()
        )
    with col2:
        grupo = st.multiselect(
            "Selecciona el grupo", 
            df['GRUPO'].unique().tolist(),
            default=df['GRUPO'].unique().tolist()
        )
    df1 = df[df['GRUPO'].isin(grupo) & df['Área'].isin(area)]
    # Correctas por Afirmación
    correctas_afirmacion = df1.groupby(['Área', 'Competencia', 'Afirmaciones'])['CORRECTA'].sum().reset_index()
    total_por_afirmacion = df1.groupby(['Área', 'Competencia', 'Afirmaciones'])['CORRECTA'].count().reset_index()
    correctas_afirmacion = correctas_afirmacion.merge(total_por_afirmacion, on=['Área', 'Competencia', 'Afirmaciones'])
    correctas_afirmacion.rename(columns={'CORRECTA_x': 'ACIERTOS', 'CORRECTA_y': 'TOTAL'}, inplace=True)
    correctas_afirmacion['% ACIERTOS'] = (correctas_afirmacion['ACIERTOS'] / correctas_afirmacion['TOTAL'] * 100).round(2)
    st.subheader("Aciertos por Afirmación")
    #dk = correctas_afirmacion[correctas_afirmacion['GRUPO'].isin(grupo) & correctas_afirmacion['Área'].isin(area)]
    #dk = correctas_afirmacion[correctas_afirmacion['Área'].isin(area)]
    st.dataframe(correctas_afirmacion[['Competencia', 'Afirmaciones','% ACIERTOS']], use_container_width=True, hide_index=True)

