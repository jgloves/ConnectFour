from enum import Enum


class Color(Enum):

    BLANK = "BLANK"
    RED = "X"
    YELLOW = "O"


class Slot:

    def __init__(self, state=Color.BLANK, position=(0, 0)):
        self.state = state
        self.position = position
        self.name = "{}{}".format(str(position[0]), str(position[1]))

    def __repr__(self):
        if self.state == Color.RED:
            return "(X)"
        elif self.state == Color.YELLOW:
            return "(O)"
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

    def check_rows_for_win(self, player):
        for row in range(Board.num_rows):
            consecutive_counter = 0
            for col in range(Board.num_cols):
                current_slot = self.board.slots[col][row]
                if current_slot.state == player.color:
                    consecutive_counter += 1
                else:
                    consecutive_counter = 0
                if consecutive_counter == 4:
                    return True
        return False

    def check_increasing_diagonals_for_win(self, player):
        starting_diagonal_slot_locations = [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (3, 0)]
        for location in starting_diagonal_slot_locations:
            col = location[0]
            row = location[1]
            consecutive_counter = 0
            while col < Board.num_cols and row < Board.num_rows:
                current_slot = self.board.slots[col][row]
                if current_slot.state == player.color:
                    consecutive_counter += 1
                else:
                    consecutive_counter = 0
                if consecutive_counter == 4:
                    return True
                col += 1
                row += 1
        return False

    def check_decreasing_diagonals_for_win(self, player):
        starting_diagonal_slot_locations = [(0, 3), (0, 4), (0, 5), (1, 5), (2, 5), (3, 5)]
        for location in starting_diagonal_slot_locations:
            col = location[0]
            row = location[1]
            consecutive_counter = 0
            while col < Board.num_cols and row >= 0:
                current_slot = self.board.slots[col][row]
                if current_slot.state == player.color:
                    consecutive_counter += 1
                else:
                    consecutive_counter = 0
                if consecutive_counter == 4:
                    return True
                col += 1
                row -= 1
            return False

    def check_win_condition(self):
        for player in self.players:
            # check columns
            if self.check_columns_for_win(player):
                return True
            # check rows
            if self.check_rows_for_win(player):
                return True
            # check increasing diagonals
            if self.check_increasing_diagonals_for_win(player):
                return True
            # check decreasing diagonals
            if self.check_decreasing_diagonals_for_win(player):
                return True
        return False


if __name__ == "__main__":
    print("Welcome to Connect Four!\n")
    player1_name = input("Enter Player 1's name: ")
    print('Hello, ' + player1_name)
    color_letter = input("Choose your token symbol: the letter X or the letter O ").upper()

    player1_color = Color.RED
    if color_letter == "O":
        player1_color = Color.YELLOW

    player1 = Player(player1_name, player1_color)

    print("Player 1: {}, symbol {}".format(player1.name, player1.color.value))

    player2_name = input("Enter Player 2's name: ")
    print('Hello, ' + player2_name)

    if color_letter == "X":
        player2_color = Color.YELLOW
    else:
        player2_color = Color.RED

    player2 = Player(player2_name, player2_color)
    print("Player 2: {}, symbol {}".format(player2.name, player2.color.value))

    game = Game(player1, player2)
    win_condition = False
    player1_turn = True
    print(game.board)

    while not win_condition and player2.num_tokens > 0:
        if player1_turn:
            game.play_turn(player1)
        else:
            game.play_turn(player2)

        print()
        print(game.board)
        win_condition = game.check_win_condition()

        if win_condition:
            winner = ""
            if player1_turn:
                winner = player1.name
            else:
                winner = player2.name
            print("{} wins!".format(winner))
            win_condition = True
        else:
            # switch players
            player1_turn = not player1_turn

    if not win_condition:
        print("It's a tie!")
