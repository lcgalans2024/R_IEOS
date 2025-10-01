import streamlit as st
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
        return "PA1"
    elif 37.0 <= puntaje < 58.0:
        return "A1"
    elif 58.0 <= puntaje < 71.0:
        return "A2"
    elif 71.0 <= puntaje <= 100.0:
        return "B1"
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
 