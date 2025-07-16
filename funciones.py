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
 