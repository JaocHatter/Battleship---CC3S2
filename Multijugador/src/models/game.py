from src.models.board import Board

class Game:
    def __init__(self, room_id):
        self.room_id = room_id
        self.players = {}  # Diccionario con los jugadores y sus tableros
        self.turn = None  # Jugador que tiene el turno

    def add_player(self, sid, player_name):
        self.players[sid] = Board(player_name)
        if self.turn is None:
            self.turn = sid  # El primer jugador que se une inicia el juego

    def get_opponent_sid(self, sid):
        for player_sid in self.players:
            if player_sid != sid:
                return player_sid
        return None

    def make_move(self, sid, x, y):
        if sid != self.turn:
            return {'status': 'error', 'message': 'No es tu turno'}
        opponent_sid = self.get_opponent_sid(sid)
        if opponent_sid is None:
            return {'status': 'error', 'message': 'Esperando al oponente'}
        opponent_board = self.players[opponent_sid]
        player_board = self.players[sid]
        hit = player_board.fire(x, y, opponent_board)
        # Cambiar el turno
        self.turn = opponent_sid
        # Verificar si el oponente ha perdido
        if opponent_board.check_loss():
            return {'status': 'win', 'hit': hit}
        else:
            return {'status': 'continue', 'hit': hit}
