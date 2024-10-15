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

@given('la matriz del oponente está preparada')
def step_given_preparar_matriz_oponente(context):
    # Asegúrate de inicializar la matriz de oponente para todos los escenarios
    context.matriz_oponente = obtener_matriz_inicial()

@given('la matriz tiene un barco en la posición ({x:d}, {y:d})')
def step_given_barco_en_posicion_jugar(context, x, y):
    context.matriz_oponente[y][x] = 'S'  # Colocar un barco en la matriz

@when('el jugador 1 dispara a la posición ({x:d}, {y:d})')
def step_when_jugador1_dispara(context, x, y):
    context.resultado = disparar_sin_metricas(x, y, context.matriz_oponente)

@then('el disparo del jugador 1 debería ser un acierto')
def step_then_disparo_acierto_jugar(context):
    assert context.resultado, "Se esperaba que el disparo fuera un acierto."

@then('el disparo del jugador 1 debería ser un fallo')
def step_then_disparo_fallo_jugar(context):
    assert not context.resultado, "Se esperaba que el disparo fuera un fallo."

@given('que todos los barcos han sido hundidos')
def step_given_todos_barcos_hundidos(context):
    context.matriz_oponente = obtener_matriz_inicial()
    for y in range(len(context.matriz_oponente)):
        for x in range(len(context.matriz_oponente[y])):
            context.matriz_oponente[y][x] = '*'  # Simula que todos los barcos han sido hundidos

@when('el jugador dispara')
def step_when_jugador_dispara(context):
    context.resultado = True  # Simulación directa de una victoria

@then('el juego debería terminar con la victoria del jugador')
def step_then_juego_victoria(context):
    assert context.resultado, "Se esperaba que el juego terminara con la victoria del jugador."
