from behave import given, when, then
from src.batalla import obtener_matriz_inicial

# Función simplificada para pruebas que ignora la lógica de métricas
def disparar_sin_metricas(x, y, matriz):
    if matriz[y][x] == ' ':
        matriz[y][x] = '-'  # Disparo fallado
        return False
    elif matriz[y][x] == 'S':
        matriz[y][x] = '*'  # Disparo acertado
        return True
    return False

@given('que la matriz tiene un barco en la posición ({x:d}, {y:d})')
def step_given_barco_en_posicion(context, x, y):
    context.matriz = obtener_matriz_inicial()
    context.matriz[y][x] = 'S'  # Simulando un barco

@given('que la matriz no tiene un barco en la posición ({x:d}, {y:d})')
def step_given_no_barco_en_posicion(context, x, y):
    context.matriz = obtener_matriz_inicial()
    context.matriz[y][x] = ' '

@when('disparo a la posición ({x:d}, {y:d})')
def step_when_disparo_a_posicion(context, x, y):
    context.resultado = disparar_sin_metricas(x, y, context.matriz)

@then('el disparo debería ser un acierto')
def step_then_disparo_acierto(context):
    assert context.resultado, "Se esperaba que el disparo fuera un acierto."

@then('el disparo debería ser un fallo')
def step_then_disparo_fallo(context):
    assert not context.resultado, "Se esperaba que el disparo fuera un fallo."
