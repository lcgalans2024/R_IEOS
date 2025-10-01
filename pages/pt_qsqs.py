import streamlit as st
import altair as alt
import pandas as pd
from load_data import agrupar_por_afirmacion
from funciones import color_hex, color_semaforo, tabla_afirmaciones


# Función para la pantalla de Quiero Ser Quiero Saber
def puntaje_qsqs():
    st.header("Quiero Ser Quiero Saber 📚")
    # Validar si 'datos' tiene registros
    if "datos_qsqs" not in st.session_state:
        st.warning("No se han cargado datos aún.")
        return
    # cargar los datos
    df = st.session_state["datos_qsqs"]
    #st.dataframe(df, use_container_width=True, hide_index=True)

    # filtros
    col1, col2, col3 = st.columns(3)

    # Filtro por Área
    with col1:
        area = st.multiselect(
            "Selecciona el área",
            df['Área'].unique().tolist(),
            default=df['Área'].unique().tolist()
        )
    # Filtro por Grupo
    with col2:
        grupo = st.multiselect(
            "Selecciona el grupo", 
            df['GRUPO'].unique().tolist(),
            default=df['GRUPO'].unique().tolist()
        )
    # Aplicar filtros
    df1 = df[df['GRUPO'].isin(grupo) & df['Área'].isin(area)]
    #############################################################################################################################
    #st.subheader("Aciertos por Afirmación")
    
    #st.dataframe(correctas_afirmacion[['Competencia', 'Afirmaciones','% ACIERTOS']], use_container_width=True, hide_index=True)
    df_resumen = agrupar_por_afirmacion(df1).copy()

    df_resumen = tabla_afirmaciones(df_resumen)

    # Tabla con colores
    #styled_df = (
    #    df_resumen[["Código", "Competencia", "Afirmación corta", "% ACIERTOS"]]
    #    .style.applymap(color_semaforo, subset=["% ACIERTOS"])
    #)
    #st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # Gráfico de barras con Altair
    #st.markdown("### 📊 Gráfico de % de aciertos por afirmación")
    #chart = alt.Chart(df_resumen).mark_bar().encode(
    #    x=alt.X("% ACIERTOS:Q", title="% Aciertos"),
    #    y=alt.Y("Código:N", sort="-x", title="Afirmaciones"),
    #    color=alt.Color("Color:N", scale=None),  # usamos la columna ya calculada
    #    tooltip=["Código", "Competencia", "% ACIERTOS"]
    #).properties(width=600, height=400)
#
    #st.altair_chart(chart, use_container_width=True)
#
    ## Expanders en dos columnas
    #st.markdown("### 📖 Detalle de las Afirmaciones")
    #col1, col2 = st.columns(2)
#
    #for i, row in df_resumen.iterrows():
    #    titulo = f"{row['Código']} | {row['Competencia']} | {row['% ACIERTOS']}%"
    #    target_col = col1 if i % 2 == 0 else col2
    #    with target_col.expander(titulo, expanded=False):
    #        st.write(row["Afirmaciones"])
    #############################################################################################################################
    st.subheader("Aciertos por Evidencia")

    # Correctas por evidencia
    correctas_evidencia = df1.groupby(['Área', 'Competencia', 'Afirmaciones', 'Evidencia'])['CORRECTA'].sum().reset_index()
    total_por_evidencia = df1.groupby(['Área', 'Competencia', 'Afirmaciones', 'Evidencia'])['CORRECTA'].count().reset_index()
    correctas_evidencia = correctas_evidencia.merge(total_por_evidencia, on=['Área', 'Competencia', 'Afirmaciones', 'Evidencia'])
    correctas_evidencia.rename(columns={'CORRECTA_x': 'ACIERTOS', 'CORRECTA_y': 'TOTAL'}, inplace=True)
    correctas_evidencia['% ACIERTOS'] = (correctas_evidencia['ACIERTOS'] / correctas_evidencia['TOTAL'] * 100).round(2)
    
    #st.dataframe(correctas_afirmacion[['Competencia', 'Afirmaciones','% ACIERTOS']], use_container_width=True, hide_index=True)

    # Crear vista resumida con código de afirmación
    df_resumen = correctas_evidencia.copy()
    df_resumen["Código"] = [f"Ev{i+1}" for i in range(len(df_resumen))]
    df_resumen["Evidencia corta"] = df_resumen["Evidencia"].str.slice(0, 50) + "..."

    # Diccionario código → texto completo
    map_evidencias = dict(zip(df_resumen["Código"], df_resumen["Evidencia"]))

    # Columna con color según semáforo

    df_resumen["Color"] = df_resumen["% ACIERTOS"].apply(color_hex)

    styled_df = (
        df_resumen[["Código", "Competencia", "Evidencia corta", "% ACIERTOS"]]
        .style.applymap(color_semaforo, subset=["% ACIERTOS"])
    )
    #st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # Gráfico de barras con Altair
    st.markdown("### 📊 Gráfico de % de aciertos por evidencia")
    chart = alt.Chart(df_resumen).mark_bar().encode(
        x=alt.X("% ACIERTOS:Q", title="% Aciertos"),
        y=alt.Y("Código:N", sort="-x", title="Evidencias"),
        color=alt.Color("Color:N", scale=None),  # usamos la columna ya calculada
        tooltip=["Código", "Competencia", "% ACIERTOS"]
    )
    
    # Etiquetas de porcentaje
    text = chart.mark_text(
        align="left",
        baseline="middle",
        dx=3,  # separación horizontal del texto
        color="black"   # 👈 aquí forzamos el color de texto
    ).encode(
        text=alt.Text("% ACIERTOS:Q", format=".1f")
    )

    chart = (chart + text).properties(width=600, height=500)

    st.altair_chart(chart, use_container_width=True)

    # Expanders en dos columnas
    st.markdown("### 📖 Detalle de las Evidencias")
    col1, col2 = st.columns(2)

    for i, row in df_resumen.iterrows():
        titulo = f"{row['Código']} | {row['Competencia']} | {row['% ACIERTOS']}%"
        target_col = col1 if i % 2 == 0 else col2
        with target_col.expander(titulo, expanded=False):
            st.write(row["Evidencia"])

################################################################### Aciertos por pregunta #####################################################################
    st.subheader("Aciertos por Pregunta")

    correctas_pregunta = df1.groupby(['Área', 'Competencia', 'Afirmaciones', 'Evidencia', 'Pregunta ID'])['CORRECTA'].sum().reset_index()
    total_por_pregunta = df1.groupby(['Área', 'Competencia', 'Afirmaciones', 'Evidencia', 'Pregunta ID'])['CORRECTA'].count().reset_index()
    correctas_pregunta = correctas_pregunta.merge(total_por_pregunta, on=['Área', 'Competencia', 'Afirmaciones', 'Evidencia', 'Pregunta ID'])
    correctas_pregunta.rename(columns={'CORRECTA_x': 'ACIERTOS', 'CORRECTA_y': 'TOTAL'}, inplace=True)
    correctas_pregunta['% ACIERTOS'] = (correctas_pregunta['ACIERTOS'] / correctas_pregunta['TOTAL'] * 100).round(2)
    # mostrar tabla
    #st.dataframe(correctas_pregunta[['Evidencia', 'Pregunta ID','% ACIERTOS']], use_container_width=True, hide_index=True)
    #############################################################################################################################

    df_resumen = correctas_pregunta.copy()
    
    datos_preguntas = pd.read_excel("df_preguntas.xlsx")

    # Crear diccionario Pregunta ID → ENLACE
    map_preguntas = dict(zip(datos_preguntas["Pregunta ID"], datos_preguntas["ENLACE"]))
    # Agregar columna ENLACE al df_resumen
    df_resumen["ENLACE"] = df_resumen["Pregunta ID"].map(map_preguntas)

    #mostrar datos preguntas
    #st.dataframe(datos_preguntas, use_container_width=True, hide_index=True)
    
    # Columna con color según semáforo
    df_resumen["Color"] = df_resumen["% ACIERTOS"].apply(color_hex)

    def etiqueta_semaforo(val):
        if val >= 70:
            return f"🟢 {val}%"
        elif 40 <= val < 70:
            return f"🟡 {val}%"
        elif 20 < val < 40:
            return f"🟠 {val}%"
        else:
            return f"🔴 {val}%"

    df_resumen["% ACIERTOS (semáforo)"] = df_resumen["% ACIERTOS"].apply(etiqueta_semaforo)

    st.data_editor(
        df_resumen[['ENLACE', 'Pregunta ID','% ACIERTOS (semáforo)']],
        column_config={
            "ENLACE": st.column_config.LinkColumn("ENLACE", display_text="Abrir link")
        },
        hide_index=True,
        use_container_width=True
    )

