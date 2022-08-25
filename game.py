from enum import Enum


class Color(Enum):

    BLANK = 0
    RED = 1
    YELLOW = 2


class Slot:

    def __init__(self, state=Color.BLANK, position=(0, 0)):
        self.state = state
        self.position = position
        self.name = "{}{}".format(str(position[0]), str(position[1]))

    def __repr__(self):
        return "{} {}".format(self.name, self.state)


class Board:

    index_to_col = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G"}
    col_to_index = {val: key for key, val in index_to_col.items()}

    def __init__(self):
        self.slots = []
        self.fill_new_board()

    def fill_new_board(self):
        for col in range(7):
            self.slots.append([])
            for row in range(6):
                self.slots[col].append(Slot(Color.BLANK, (Board.index_to_col[col], row)))


class Player:

    def __init__(self, name="Player", color=Color.RED):
        self.name = name
        self.color = color
        self.my_turn = True
        self.num_tokens = 21

    def play_turn(self):
        self.num_tokens -= 1


class Game:

    index_to_col = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G"}
    col_to_index = {val: key for key, val in index_to_col.items()}
    players = [Player(), Player()]
    board = Board()


# debug code
board = Board()
print(board.slots)
