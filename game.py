from enum import Enum


class Color(Enum):

    BLANK = "BLANK"
    RED = "RED"
    YELLOW = "YELLOW"


class Slot:

    def __init__(self, state=Color.BLANK, position=(0, 0)):
        self.state = state
        self.position = position
        self.name = "{}{}".format(str(position[0]), str(position[1]))

    def __repr__(self):
        if self.state == Color.RED:
            return "(R)"
        elif self.state == Color.YELLOW:
            return "(Y)"
        return "( )"


class Board:

    index_to_col = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G"}
    col_to_index = {val: key for key, val in index_to_col.items()}

    def __init__(self):
        self.slots = []
        self.fill_new_board()

    def __repr__(self):
        self_string = ""
        for row in range(5, -1, -1):
            self_string_components = [str(self.slots[col][row]) for col in range(7)]
            self_string += " ".join(self_string_components) + "\n"
        self_string += " A   B   C   D   E   F   G\n"
        return self_string

    def fill_new_board(self):
        for col in range(7):
            self.slots.append([])
            for row in range(6):
                self.slots[col].append(Slot(Color.BLANK, (Board.index_to_col[col], row)))


class Player:

    def __init__(self, name, color, my_turn):
        self.name = name
        self.color = color
        self.my_turn = my_turn
        self.num_tokens = 21


class Game:

    def __init__(self, player1=Player("Player 1", Color.RED, True), player2=Player("Player 2", Color.YELLOW, False)):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.players = [self.player1, self.player2]

    def insert_token(self, player, column=0):
        self.board.slots[column][0] = Slot(player.color, (column, 0))
        player.num_tokens -= 1
        player.my_turn = not player.my_turn


if __name__ == "__main__":
    print("Welcome to Connect Four!\n")
    player1_name = input("Enter Player 1's name: ")
    print('Hello, ' + player1_name)
    color_letter = input("Choose your color: R for red, Y for yellow: ")

    player1_color = Color.RED
    if color_letter == "Y":
        player1_color = Color.YELLOW

    player1 = Player(player1_name, player1_color, True)

    print("Player 1: {}, color {}".format(player1.name, player1.color.value))

    player2_name = input("Enter Player 2's name: ")
    print('Hello, ' + player2_name)

    if color_letter == "R":
        player2_color = Color.YELLOW
    else:
        player2_color = Color.RED

    player2 = Player(player2_name, player2_color, False)
    print("Player 2: {}, color {}".format(player2.name, player2.color.value))





