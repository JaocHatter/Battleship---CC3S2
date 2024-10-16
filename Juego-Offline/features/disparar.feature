# language: es
Característica: Disparar en el juego de batalla naval

Escenario: Disparo acertado
  Dado que la matriz tiene un barco en la posición (2, 3)
  Cuando disparo a la posición (2, 3)
  Entonces el disparo debería ser un acierto

Escenario: Disparo fallado
  Dado que la matriz no tiene un barco en la posición (0, 0)
  Cuando disparo a la posición (0, 0)
  Entonces el disparo debería ser un fallo
