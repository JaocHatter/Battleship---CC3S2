class GameController:
    def __init__(self, player1_name, player2_name):
        self.players = {
            'player1': {'name': player1_name, 'board': self.init_board(), 'ships': 5},
            'player2': {'name': player2_name, 'board': self.init_board(), 'ships': 5}
        }
        self.current_turn = 'player1'
    
    def init_board(self):
        return [[0 for _ in range(5)] for _ in range(5)]
    
    def place_ships(self, player, board):
        if player in self.players:
            self.players[player]['board'] = board
            return True
        return False

    def fire(self, player, x, y):
        opponent = 'player2' if player == 'player1' else 'player1'
        opponent_board = self.players[opponent]['board']
        
        if opponent_board[x][y] == -1 or opponent_board[x][y] == -2:
            return "Invalid", None  
        
        if opponent_board[x][y] == 1:
            opponent_board[x][y] = -1  
            self.players[opponent]['ships'] -= 1
            return "Hit", self.check_winner()
        else:
            opponent_board[x][y] = -2 
            self.switch_turn()
            return "Miss", None

    def switch_turn(self):
        self.current_turn = 'player2' if self.current_turn == 'player1' else 'player1'

    def check_winner(self):
        if self.players['player1']['ships'] == 0:
            return 'player2'
        elif self.players['player2']['ships'] == 0:
            return 'player1'
        return None
