import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards

def puntaje_global(df, filtros, variable=None):
    st.header("Puntaje Global 📈")

    # Gráfico de barras del puntaje global promedio por año
    if filtros["grupo"] != "Todos":
        df_plot = df[df.Grupo == filtros["grupo"]].groupby("AÑO")[variable].mean().round(0).reset_index()
        titulo = f"Comparativo del puntaje global por año para el grupo {filtros['grupo']}"
    else:
        df_plot = df.groupby("AÑO")[variable].mean().round(0).reset_index()
        titulo = f"Comparativo del puntaje global por año"
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
            title=titulo
        )
    st.altair_chart(final_chart, use_container_width=True)

# Grafico de barras del puntaje global promedio por grupo
def puntaje_por_grupo(df, filtros, variable=None):
    st.header("Puntaje Global por Grupo 📊")

    # Definimos dos columnas
    col1, col2 = st.columns(2)
    with col1:
        # Selector de año para gráfico por grupo
        año_seleccionado = st.selectbox("Selecciona el año:", options=df["AÑO"].unique(), key="select_año_area", index=1)
    with col2:
        st.write(" ")

    # Gráfico de barras del puntaje global promedio por grupo
    df_plot = df[df.AÑO == año_seleccionado].groupby(['Grupo','AÑO'])['Puntaje global'].mean().round(0).reset_index()
    #Validar si hay datos
    if df_plot.empty:
        st.warning("⚠️ No se tienen datos aún para este año seleccionado.")
    else:

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
                title=f"Promedio puntaje global por grupo año {año_seleccionado}"
            )
        st.altair_chart(final_chart, use_container_width=True)