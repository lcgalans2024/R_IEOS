# utils/data.py
from pathlib import Path
import streamlit as st
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Cargar datos del simulacro ICFES
@st.cache_data(show_spinner="Cargando datos…")
def cargar_datos():
    df = pd.read_excel(DATA_DIR / "Resultados_Simulacro_ICFES.xlsx").dropna()
    # eliminar columnas de niveles si existen
    for col in ['ND_LC', 'ND_M', 'ND_CN', 'ND_Inglés']:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Convertir la columnas a string para evitar problemas de tipo
    df["Grupo"] = df["Grupo"].astype(str)
    df["AÑO"] = df["AÑO"].astype(str)
    # Redondear columnas numéricas a 2 decimales
    for col in df.select_dtypes(include=['float64', 'float32']):
        df[col] = df[col].round(2)

    # eliminar registo por documento, AÑO y SIMULACRO
    documentos_a_ignorar = ["1035976977","nn_1001"]
    df = df[~((df["DOCUMENTO"].isin(documentos_a_ignorar)) & (df["AÑO"] == "2025") & (df["SIMULACRO"] == "S1"))]

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
        if filtros["piar"]:
            df = df[~(df["Inglés"] == 0)]

    return df