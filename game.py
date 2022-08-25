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

    num_cols = 7
    num_rows = 6
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
        for col in range(Board.num_cols):
            self.slots.append([])
            for row in range(Board.num_rows):
                self.slots[col].append(Slot(Color.BLANK, (Board.index_to_col[col], row)))


class Player:

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.num_tokens = 21


class Game:

    def __init__(self, player1=Player("Player 1", Color.RED), player2=Player("Player 2", Color.YELLOW)):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.players = [self.player1, self.player2]

    def insert_token(self, player, column_string):
        col = Board.col_to_index[column_string]
        first_blank_slot_row = 0
        for i in range(Board.num_rows):
            if self.board.slots[col][i].state == Color.BLANK:
                first_blank_slot_row = i
                break
            if i == Board.num_rows - 1:
                print("Invalid play - column {} is full.".format(column_string))
                return False
        self.board.slots[col][first_blank_slot_row] = Slot(player.color, (col, first_blank_slot_row))
        return True

    def play_turn(self, player):
        finished = False
        print("It's {}'s turn.".format(player.name))
        while not finished:
            column_string = input("Which column will you drop your token in? ")
            finished = self.insert_token(player, column_string)
        # The player has successfully inserted a token
        player.num_tokens -= 1

    def check_columns_for_win(self, player):
        for col in self.board.slots:
            col_index = self.board.slots.index(col)
            consecutive_counter = 0
            current_row = 0
            while consecutive_counter < 4 and current_row < Board.num_rows:
                if self.board.slots[col_index][current_row].state == player.color:
                    consecutive_counter += 1
                else:
                    consecutive_counter = 0
                current_row += 1
            if consecutive_counter == 4:
                return True
        return False

    def check_win_condition(self):
        #check columns
        for player in self.players:
            if self.check_columns_for_win(player):
                print("{} wins!".format(player.name))
                return True
        #TODO - check rows next

        #TODO - finally, check diagonals
        return False


if __name__ == "__main__":
    print("Welcome to Connect Four!\n")
    player1_name = input("Enter Player 1's name: ")
    print('Hello, ' + player1_name)
    color_letter = input("Choose your color: R for red, Y for yellow: ")

    player1_color = Color.RED
    if color_letter == "Y":
        player1_color = Color.YELLOW

    player1 = Player(player1_name, player1_color)

    print("Player 1: {}, color {}".format(player1.name, player1.color.value))

    player2_name = input("Enter Player 2's name: ")
    print('Hello, ' + player2_name)

    if color_letter == "R":
        player2_color = Color.YELLOW
    else:
        player2_color = Color.RED

    player2 = Player(player2_name, player2_color)
    print("Player 2: {}, color {}".format(player2.name, player2.color.value))

    game = Game(player1, player2)
    win_condition = False
    player1_turn = True
    print(game.board)

    while not win_condition and player1.num_tokens > 0: #player 2 can't run out of tokens before player 1
        if player1_turn:
            game.play_turn(player1)
        else:
            game.play_turn(player2)
        #switch players
        player1_turn = not player1_turn

        print(game.board)
        win_condition = game.check_win_condition()

    #If player1_turn == True, player2 won. If player1_turn == False, player1 won.






