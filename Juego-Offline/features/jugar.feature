# language: es
Característica: Jugar el juego de batalla naval

Escenario: Turno del jugador 1 acertado
  Dado la matriz del oponente está preparada
  Y la matriz tiene un barco en la posición (2, 3)
  Cuando el jugador 1 dispara a la posición (2, 3)
  Entonces el disparo del jugador 1 debería ser un acierto

Escenario: Fin del juego
  Dado que todos los barcos han sido hundidos
  Cuando el jugador dispara
  Entonces el juego debería terminar con la victoria del jugador
