# utils/data.py
from pathlib import Path
import streamlit as st
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Cargar datos del simulacro ICFES
#@st.cache_data(show_spinner="Cargando datos…")
def cargar_datos():
    df = pd.read_excel(DATA_DIR / "Resultados_Simulacro_ICFES.xlsx").dropna()
    # eliminar columnas de niveles si existen
    for col in ['ND_LC', 'ND_M', 'ND_CN', 'ND_Inglés']:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Convertir la columnas a string para evitar problemas de tipo
    df["Grupo"] = df["Grupo"].astype(str)
    df["AÑO"] = df["AÑO"].astype(str).apply(lambda x: str(x).strip())
    # Redondear columnas numéricas a 2 decimales
    for col in df.select_dtypes(include=['float64', 'float32']):
        df[col] = df[col].round(2)

    # eliminar registo por documento, AÑO y SIMULACRO
    documentos_a_ignorar = ["1035976977","nn_1001"]
    df = df[~((df["DOCUMENTO"].isin(documentos_a_ignorar)) & (df["AÑO"] == "2025") & (df["SIMULACRO"] == "S1"))]

    # Filtrar datos sin PIAR
    df = df[~(df['Inglés'] == 0)].copy()
    df = df[~(df['Inglés'] == "-")].copy()

    df["AÑO"] = df["AÑO"].astype(str)

    return df

# Filtros de datos por grado y año
def filtrar_datos(df, filtros):
    # Aplicar filtros
    if filtros:
        if filtros["anio"]:
            df = df[df["AÑO"] == filtros["anio"]]
        if filtros["grado"]:
            df = df[df["Grupo"].str.startswith(filtros["grado"])]
        if filtros["high_fs"]:
            df = df[df["Grupo"].isin(['1101','1102','1103','1104'])]
        #if filtros["piar"]:
        #    df = df[~(df["Inglés"] == 0)]

    return df

def diagnosticar_columna(df, columna):
    """
    Muestra un diagnóstico detallado de una columna:
    - Tipos de datos presentes
    - Cantidad de valores nulos
    - Valores únicos (si pocos)
    - Ejemplos de valores
    """
    st.subheader(f"🧪 Diagnóstico de la columna: `{columna}`")

    if columna not in df.columns:
        st.error(f"La columna '{columna}' no existe en el DataFrame.")
        return

    serie = df[columna]

    st.write("🔍 Tipos encontrados:")
    st.write(serie.apply(type).value_counts())

    st.write("❌ Valores nulos:", serie.isna().sum())

    if serie.dtype == "object" or serie.dtype.name == "category":
        vacios = (serie == "").sum()
        st.write("📭 Celdas vacías como string:", vacios)

    n_unicos = serie.nunique(dropna=True)
    st.write("🔢 Cantidad de valores únicos:", n_unicos)

    if n_unicos <= 20:
        st.write("🧾 Valores únicos:")
        st.write(serie.unique())
    else:
        st.write("📌 Ejemplos de valores:")
        st.write(serie.dropna().sample(n=min(10, len(serie)), random_state=42))

def cargar_datos_qsqs():
    # Cargar datos de Quiero Ser Quiero Saber
    try:
        df = pd.read_excel("Resultados_QSQS.xlsx", sheet_name="G5")
    except Exception as e:
        st.error(f"Error al cargar los datos de Quiero Ser Quiero Saber: {e}")

    return df


# Agrupar por afirmación
def agrupar_por_afirmacion(df):
    correctas_afirmacion = df.groupby(['Área', 'Competencia', 'Afirmaciones'])['CORRECTA'].sum().reset_index()
    total_por_afirmacion = df.groupby(['Área', 'Competencia', 'Afirmaciones'])['CORRECTA'].count().reset_index()
    correctas_afirmacion = correctas_afirmacion.merge(total_por_afirmacion, on=['Área', 'Competencia', 'Afirmaciones'])
    correctas_afirmacion.rename(columns={'CORRECTA_x': 'ACIERTOS', 'CORRECTA_y': 'TOTAL'}, inplace=True)
    correctas_afirmacion['% ACIERTOS'] = (correctas_afirmacion['ACIERTOS'] / correctas_afirmacion['TOTAL'] * 100).round(2)
    return correctas_afirmacion

def cargar_datos_historicos():
    df = pd.read_excel(DATA_DIR / "Resultados_historico_2016_2024.xlsx")

    return df