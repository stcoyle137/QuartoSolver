from abc import ABC, abstractmethod
from token_structure import *
from board_structure import *
import random

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
    def decision_place(self, board_manager, token_manager, token_to_place):
        return random.choice(board_manager.get_valid_placements())

    def decision_choose(self, board_manager, token_manager, last_token_placed):
        return token_manager.choose_token(random.choice(token_manager.get_remaining_bank())[0])
    def win(self):
        print(self.name + " won")

class TakeWinBot(RandomBot):
    def decision_place(self, board_manager, token_manager, token_to_place):
        wp = TakeWinBot.win_placement(board_manager, token_to_place)
        if wp != None:
            return wp
        return random.choice(board_manager.get_valid_placements())

    def win_placement(board_manager, token_to_place):
        for l in board_manager.board:
            for c in l:
                if c.coord in board_manager.get_valid_placements():
                    good = c.try_value(token_to_place)
                    if good:
                        return c.coord

class DontLoseBot(RandomBot):
    def decision_choose(self, board_manager, token_manager, last_token_placed):
        return token_manager.choose_token(DontLoseBot.lose_choose(board_manager, token_manager))

    def lose_choose(board_manager, token_manager):
        x = token_manager.get_remaining_bank()
        random.shuffle(x)
        for i,desired_pick in x:
            if not TakeWinBot.win_placement(board_manager, desired_pick):
                return i
        return random.choice(token_manager.get_remaining_bank())[0]

class TakeWinAndDontLoseBot(TakeWinBot, DontLoseBot):
    def __init__(self, name, idenfier):
        super().__init__(name, idenfier)

class SamsStupidPlanBot(RandomBot):
    def decision_choose(self, board_manager, token_manager, last_token_placed):
        for i in range(len(token_manager.bank)):
            if token_manager.bank[i] == last_token_placed:
                return token_manager.choose_token(15-i)
class SamsStupidPlanAndTakeWinBot(TakeWinBot, SamsStupidPlanBot):
    def __init__(self, name, idenfier):
        super().__init__(name, idenfier)

class SamsStupidPlanAndDontLoseBot(RandomBot):
    def __init__(self, name, idenfier):
        super().__init__(name, idenfier)

    def decision_choose(self, board_manager, token_manager, last_token_placed):
        for i in range(len(token_manager.bank)):
            if token_manager.bank[i] == last_token_placed:
                if not token_manager.bank[15-i].available:
                    return token_manager.choose_token(DontLoseBot.lose_choose(board_manager, token_manager))
                elif not TakeWinBot.win_placement(board_manager, token_manager.bank[15-i]):
                    return token_manager.choose_token(15-i)
                else:
                    return token_manager.choose_token(DontLoseBot.lose_choose(board_manager, token_manager))

class SamsStupidPlanAndDontLoseAndTakeWinBot(SamsStupidPlanAndDontLoseBot, TakeWinBot):
    def __init__(self, name, idenfier):
        super().__init__(name, idenfier)




'''
Current Stats
Two Randoms-                                                                            1: 4951, 2: 4844, Tie: 205

First Player Random, Second Player TakeWinBot-                                          1: 1016, 2: 8971, Tie: 13
First Player TakeWinBot, Second Player Random-                                          1: 8992, 2: 982,  Tie: 26
First Player TakeWinBot, Second Player TakeWinBot-                                      1: 4988, 2: 5001, Tie: 11

First Player Random, Second Player DontLoseBot-                                         1: 3901, 2: 5895, Tie: 204
First Player DontLoseBot, Second Player Random-                                         1: 6142, 2: 3648, Tie: 210
First Player DontLoseBot, Second Player DontLoseBot-                                    1: 4893, 2: 4926, Tie: 181

First Player TakeWinBot, Second Player DontLoseBot-                                     1: 6450, 2: 3423, Tie: 127
First Player DontLoseBot, Second Player TakeWinBot-                                     1: 3532, 2: 6348, Tie: 120

First Player Random, Second Player TakeWinAndDontLoseBot-                               1: 237,  2: 9748, Tie: 15
First Player TakeWinAndDontLoseBot, Second Player Random-                               1: 9749, 2: 233,  Tie: 18
First Player TakeWinAndDontLoseBot, Second Player TakeWinAndDontLoseBot-                1: 4990, 2: 4928, Tie: 82


First Player Random, Second Player SamsStupidPlanBot-                                   1: 3948, 2: 5857, Tie: 195

First Player Random, Second Player SamsStupidPlanAndTakeWinBot-                         1: 552,  2: 9431, Tie: 17

First Player Random, Second Player SamsStupidPlanAndDontLoseBot-                        1: 3980, 2: 5822, Tie: 198

First Player Random, Second Player SamsStupidPlanAndDontLoseAndTakeWinBot-              1: 283,  2: 9695, Tie: 22
'''
def run_game():
    player = [RandomBot("Idiot 1", 0), SamsStupidPlanAndDontLoseAndTakeWinBot("Real Idiot 2", 1)]
    win_count = {player[0].name : 0, player[1].name : 0, "Tie" : 0}
    for i in range(10000):
        t = TokenManager()
        b = BoardManager(4, t)
        current_player = 0
        #FirstMove
        tok = player[current_player].choose(b, t, None)
        while(True):
            current_player = 1 if current_player == 0 else 0
            coord = player[current_player].place(b,t,tok)
            b.place_token(coord,tok)
            if b.won:
                win_count[player[current_player].name] += 1
                break
            if not b.alive:
                win_count["Tie"] += 1
                break
            tok = player[current_player].choose(b,t,tok)
        print(i)
    print(win_count)



def run_game_human():
    player = [HumanPlayer("Idiot 1", 0), SamsStupidPlan("Idiot 2", 1)]
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
            print(b)
            player[current_player].win()
            break
        if not b.alive:
            print("Tie")
            break
        print("Player: " + player[current_player].name)
        tok = player[current_player].choose(b,t,tok)


if __name__ == "__main__": run_game()
