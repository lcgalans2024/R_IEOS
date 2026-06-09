import streamlit as st
import pandas as pd
import plotly.express as px
from load_data import agrupar_por_afirmacion

def asignar_nivel_lc(puntaje):
    if 0 <= puntaje < 36.0:
        return 1
    elif 36.0 <= puntaje < 51.0:
        return 2
    elif 51.0 <= puntaje < 66.0:
        return 3
    elif 66.0 <= puntaje <= 100.0:
        return 4
    else:
        return None  # en caso de valores fuera de rango

def asignar_nivel_M(puntaje):
    if 0 <= puntaje < 36.0:
        return 1
    elif 36.0 <= puntaje < 51.0:
        return 2
    elif 51.0 <= puntaje < 71.0:
        return 3
    elif 71.0 <= puntaje <= 100.0:
        return 4
    else:
        return None  # en caso de valores fuera de rango
    
def asignar_nivel_CN(puntaje):
    if 0 <= puntaje < 41.0:
        return 1
    elif 41.0 <= puntaje < 56.0:
        return 2
    elif 56.0 <= puntaje < 71.0:
        return 3
    elif 71.0 <= puntaje <= 100.0:
        return 4
    else:
        return None  # en caso de valores fuera de rango
    
def asignar_nivel_ingles(puntaje):
    if 0.0 <= puntaje < 37.0:
        return "Pre A1"
    elif 37.0 <= puntaje < 58.0:
        return "A1"
    elif 58.0 <= puntaje < 71.0:
        return "A2"
    elif 71.0 <= puntaje <= 100.0:
        return "B1"
    else:
        return None  # en caso de valores fuera de rango
    
def asignar_nivel_ingles_numerico(puntaje):
    if 0.0 <= puntaje < 37.0:
        return 1
    elif 37.0 <= puntaje < 58.0:
        return 2
    elif 58.0 <= puntaje < 71.0:
        return 3
    elif 71.0 <= puntaje <= 100.0:
        return 4
    else:
        return None  # en caso de valores fuera de rango
    
# Columna con color según semáforo
def color_hex(val):
    if val >= 70:
        return "green"
    elif 40 <= val < 70:
        return "#FFD966"
    elif 21 <= val < 40:
        return "orange"
    else:
        return "red"
    
# Tabla con colores
def color_semaforo(val):
    if val >= 70:
        color = "green"
    elif 40 <= val < 70:
        color = "#FFD966"
    elif 21 <= val < 40:
        color = "orange"
    else:
        color = "red"
    return f"background-color: {color}; color: black;"

""" Asignar niveles de desempeño para cada área según los puntajes obtenidos.
Los niveles son: Bajo, Básico, Alto, Superior."""

def asignar_nivel_desempeno(df):
    df['Nivel_LC'] = df['Lectura crítica'].apply(lambda x: asignar_nivel_lc(x)).astype(str)
    df['Nivel_M'] = df['Matemáticas'].apply(lambda x: asignar_nivel_M(x)).astype(str)
    df['Nivel_CN'] = df['Ciencias naturales'].apply(lambda x: asignar_nivel_CN(x)).astype(str)
    df['Nivel_SC'] = df['Sociales y ciudadanas'].apply(lambda x: asignar_nivel_CN(x)).astype(str)
    df['Nivel_IG'] = df['Inglés'].apply(lambda x: asignar_nivel_ingles(x)).astype(str)
    df['Nivel_ingles_numerico'] = df['Inglés'].apply(lambda x: asignar_nivel_ingles_numerico(x)).astype(str)
    return df

def tabla_afirmaciones(df):
    # Crear vista resumida con código de afirmación
    #df = agrupar_por_afirmacion(df1).copy()
    df["Código"] = [f"Af{i+1}" for i in range(len(df))]
    df["Afirmación corta"] = df["Afirmaciones"].str.slice(0, 50) + "..."

    # Diccionario código → texto completo
    map_afirmaciones = dict(zip(df["Código"], df["Afirmaciones"]))

    # Columna con color según semáforo
    df["Color"] = df["% ACIERTOS"].apply(color_hex)
    return df

def BartChartRace(df):

    st.header("Evolución de los resultados ICFES desde 2016")
    st.markdown("Da clic en el botón de play ▶️ para observar la evolución del puntaje ICFES a lo largo de los años.")
    
    df.rename(columns={'Promedio':'Puntaje'},inplace=True)

    # Definimos dos columnas
    col1, col2 = st.columns(2)

    with col1:
        # Obtener todas las opciones del selectbox
        opciones = df["Colegio"].unique().tolist()
        # Definir el nombre del colegio por defecto
        colegio_default = "INSTITUCIÓN EDUCATIVA ORESTE SINDICI"
        # Asegurar que exista en la lista y obtener su índice
        index_default = opciones.index(colegio_default) if colegio_default in opciones else 0
        colegio_destacado = st.selectbox("Selecciona la institución a revisar su evolución:", options=opciones, index = index_default)
    with col2:
        sector_seleccionado = st.multiselect("Selecciona el sector:",
                             df["Sector"].unique().tolist(),
                             default=df["Sector"].unique().tolist()
        )
    # Si el sector vacio mostrar mensaje
    if not sector_seleccionado:
        st.warning("Por favor, selecciona al menos un sector.")

    DF = df[(df['Area'] == 'General')
        & (df['Sector'].isin(sector_seleccionado))
         & ~(df.Colegio.isin(['INSTITUCIÓN EDUCATIVA ALIANZA PARA LA EDUCACIÓN EDUCANDO S.A.S']))
         ].copy()
    
    DF = DF.sort_values('Periodo', ascending=True)
    
    # Asegurar que los periodos estén en orden correcto
    DF['Periodo'] = pd.Categorical(DF['Periodo'], ordered=True,
               categories=sorted(DF['Periodo'].unique()))
    # Calcular cambio porcentual por colegio
    DF = DF.sort_values(['Periodo','Colegio'])
    DF['Cambio_%'] = DF.groupby('Colegio')['Puntaje'].pct_change() * 100
    DF['Cambio_%'] = DF['Cambio_%'].fillna(0)
    # Calcular promedio general por periodo
    promedios = DF.groupby('Periodo')['Puntaje'].mean().reset_index(name='Promedio')
    DF['Color'] = DF['Colegio'].apply(lambda x: 'red' if x == colegio_destacado else 'lightgray')
    # Crear texto combinando puntaje y cambio porcentual
    DF['texto_barra'] = (
        #DF['Colegio'] + '<br>' +       # 👈 agrega el nombre arriba o abajo del puntaje
        DF['Puntaje'].round(1).astype(str)
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
            
            range_x=[DF['Puntaje'].min() * 0.95, DF['Puntaje'].max() * 1.1],
            title=f'🏁 Evolución del Puntaje ICFES {colegio_destacado}',
            color_discrete_map={'gold': 'red', 'lightgray': 'lightblue'}
        )

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
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = int(1500)  # 1s entre frames
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = int(1200)
    st.plotly_chart(fig)
    fig2 = px.line(
    DF[DF['Colegio'] == colegio_destacado],
    x='Periodo',
    y='Puntaje',
    markers=True,
    title=f'Evolución del Puntaje de {colegio_destacado}'
    )
    st.plotly_chart(fig2)

    #return st.dataframe(DF)
 