class Board:
    def __init__(self, player_name):
        self.player_name = player_name
        self.own_board = [[0 for _ in range(5)] for _ in range(5)]  # Tablero propio con barcos
        self.enemy_board = [[0 for _ in range(5)] for _ in range(5)]  # Registro de disparos al enemigo
        self.remaining_ships = 5
        self.state = "PLAYING"

    def place_ship(self, x, y):
        if self.own_board[x][y] == 0:
            self.own_board[x][y] = 1
            return True
        else:
            return False  # Ya hay un barco en esa posición

    def receive_fire(self, x, y):
        if self.own_board[x][y] == 1:
            self.own_board[x][y] = -1  # Barco hundido
            self.remaining_ships -= 1
            hit = True
        else:
            self.own_board[x][y] = -2  # Agua
            hit = False
        return hit

    def fire(self, x, y, enemy_board):
        hit = enemy_board.receive_fire(x, y)
        self.enemy_board[x][y] = -1 if hit else -2
        return hit

    def check_loss(self):
        if self.remaining_ships == 0:
            self.state = "LOSE"
            return True
        return False

           