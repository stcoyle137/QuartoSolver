from abc import ABC, abstractmethod
from token_structure import *
from board_structure import *

class Player():
    """
    Needs to store
        - token
        - idenfier (int)
        - name
        - next player indenfier
    Functionality
        - init with a tokens
        - past on input
        - give next players
    """

    def __init__(self, name, idenfier):
        self.name = name
        self.idenfier = idenfier

    def place(self, board_manager, token_manager, token_to_place):
        """Using infomation from the board to generate a player movement. Uses algorithrim in subclasses 'decision_making' function"""
        coordinate = self.decision_place(board_manager, token_manager, token_to_place)
        return coordinate

    def choose(self, board_manager, token_manager, last_token_placed):
        token = self.decision_choose(board_manager, token_manager, last_token_placed)
        return token

    @abstractmethod
    def decision_place(self, board_manager, token_manager, token_to_place):
        pass

    @abstractmethod
    def decision_choose(self, board_manager, token_manager, last_token_placed):
        pass

    @abstractmethod
    def win(self):
        pass

class HumanPlayer(Player):
    def __init__(self, name, idenfier):
        super().__init__(name, idenfier)

    def decision_place(self, board_manager, token_manager, token_to_place):
        print(board_manager)
        print("To place: " + str(token_to_place))
        print("Where you dropping chief?")
        y = int(input("x: "))
        x = int(input("y: "))
        return Coord(x,y)

    def decision_choose(self, board_manager, token_manager, last_token_placed):
        print(token_manager)
        print()
        print(board_manager)
        print("What you passing off?")
        i = int(input("id: "))
        print()
        print()
        return token_manager.choose_token(i)
    def win(self):
        print(self.name + " won")

class RandomBot(Player):
    def __init__(self, name, idenfier):
        super().__init__(name, idenfier)
    def decision_place(self, board_manager, token_manager, token_to_place):
        print(board_manager)
        return Coord(x,y)

    def decision_choose(self, board_manager, token_manager, last_token_placed):
        print(token_manager)
        print()
        print(board_manager)
        print("What you passing off?")
        i = int(input("id: "))
        print()
        print()
        return token_manager.choose_token(i)
    def win(self):
        print(self.name + " won")



def run_game_human():
    player = [HumanPlayer("Idiot 1", 0), HumanPlayer("Idiot 2", 1)]
    t = TokenManager()
    b = BoardManager(4, t)
    current_player = 0
    #FirstMove
    print("Player: " + player[current_player].name)
    tok = player[current_player].choose(b, t, None)
    while(True):
        current_player = 1 if current_player == 0 else 0
        print("Player: " + player[current_player].name)
        coord = player[current_player].place(b,t,tok)
        b.place_token(coord,tok)
        if b.won:
            player[current_player].win()
            break
        if not b.alive:
            print("Tie")
            break
        print("Player: " + player[current_player].name)
        tok = player[current_player].choose(b,t,tok)



if __name__ == "__main__": run_game_human()
