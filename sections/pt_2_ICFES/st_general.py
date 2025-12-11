import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards

def puntaje_global(df, variable=None):
    st.header("Puntaje Global 📈")

    # Gráfico de barras del puntaje global promedio por año
    df_plot = df.groupby("AÑO")[variable].mean().round(0).reset_index()
    chart = alt.Chart(df_plot).mark_bar().encode(
        x=alt.X("AÑO:N", title="Año", axis=alt.Axis(labelAngle=0)),
        y=alt.Y(f"{variable}:Q", title=variable),
        color="AÑO:N",
        tooltip=["AÑO", variable]
    )
    text = alt.Chart(df_plot).mark_text(
            align='center',
            baseline='bottom',
            dy=-5,  # Desplazamiento vertical de la etiqueta
            fontSize=16
        ).encode(
            x=alt.X("AÑO:N"),
            y=alt.Y("Puntaje global:Q"),
            text=alt.Text("Puntaje global:Q", format=".0f", )
        )
    final_chart = (chart + text).properties(
            width=600,
            height=400,
            title="Promedio del puntaje global por año"
        )
    st.altair_chart(final_chart, use_container_width=True)

# Grafico de barras del puntaje global promedio por grupo
def puntaje_por_grupo(df, variable=None):
    st.header("Puntaje Global por Grupo 📊")

    # Gráfico de barras del puntaje global promedio por grupo
    df_plot = df[df.AÑO == '2025'].groupby(['Grupo','AÑO'])['Puntaje global'].mean().round(0).reset_index()
    chart = alt.Chart(df_plot).mark_bar().encode(
        x=alt.X("Grupo:N", title="Grupo", axis=alt.Axis(labelAngle=0)),
        y=alt.Y(f"{variable}:Q", title=variable),
        color="Grupo:N",
        tooltip=["Grupo", variable]
    )
    text = alt.Chart(df_plot).mark_text(
            align='center',
            baseline='bottom',
            dy=-5,  # Desplazamiento vertical de la etiqueta
            fontSize=16
        ).encode(
            x=alt.X("Grupo:N"),
            y=alt.Y("Puntaje global:Q"),
            text=alt.Text("Puntaje global:Q", format=".0f", )
        )
    final_chart = (chart + text).properties(
            width=600,
            height=400,
            title="Promedio puntaje global por grupo año 2025"
        )
    st.altair_chart(final_chart, use_container_width=True)