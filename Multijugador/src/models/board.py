class Board():
    def __init__(self, player_name):
        self.p_name = player_name
        self.board = [[0,0,0,0,0],
                      [0,0,0,0,0],
                      [0,0,0,0,0],
                      [0,0,0,0,0],
                      [0,0,0,0,0]]
        self.restant_ships = 5
        self.players = {
            "board":self.board,
            "ship": self.restant_ships
        }
        self.state = "PLAYING"
    def fire(self,x,y):
        if self.players["board"][x][y] == 1:
            print("HIT")
            self.players["ship_p2"] -= 1
            self.players["board"][x][y] = 0

    def verify(self):
        if self.players["ship"] == 0:
            print(f"{self.p_name} LOSE!")
            self.state = "LOSE"
            return self.state
        return self.state
           