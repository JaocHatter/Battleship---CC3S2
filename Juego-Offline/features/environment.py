from src.batalla import obtener_matriz_inicial

def before_scenario(context, scenario):
    context.matriz = obtener_matriz_inicial()
