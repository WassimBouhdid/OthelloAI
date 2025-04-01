DIMENSION = 4


class Board:
    def __init__(self):
        # self.game_board = [
        #     [None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None],
        #
        #     [None, None, None, 1, 0, None, None, None],
        #     [None, None, None, 0, 1, None, None, None],
        #     [None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None],
        # ]

        self.game_board = [
            [None, None, None, None],

            [None, 1, 0, None],
            [None, 0, 1, None],
            [None, None, None, None],
        ]

        self.adj = [(-1, -1), (-1, 0),
                    (0, -1), (1, 0), (1, 1),
                    (0, 1), (1, -1), (-1, 1)]
        self.possible_moves = set()
        self.coord_possible_change_color = set()
        self.black_pawn = 0
        self.white_pawn = 0
        self.no_moves_player = False

    # Get all th possible movesof a player by detecting a streak
    # A streak is a succession of 1 or more enemy pawns that finishes with a None
    def computer_possible_moves(self, player):
        self.possible_moves = set()
        # We loop through all the possible position of the board
        for x in range(len(self.game_board)):
            for y in range(len(self.game_board[0])):
                # we get the position of all our pawns
                if self.game_board[x][y] == player:
                    # We check the adjacent squares of the players pawn
                    for direction in self.adj:
                        steak_length = 0
                        current_node = (x + direction[0], y + direction[1])
                        while self.in_range(*current_node):
                            if self.game_board[current_node[0]][current_node[1]] is None and steak_length > 0:
                                # If the streak has begun, and we detect an empty square then we had that empty square
                                # to the possible_moves list
                                self.possible_moves.add(current_node)
                                break
                            elif self.game_board[current_node[0]][current_node[1]] == player:
                                # If we detect any player's pawn in a streak, then we check the next adjacent square
                                break
                            elif self.game_board[current_node[0]][current_node[1]] == 1 - player:
                                # If we detect an enemy pawn, it means that a streak begins, then we chack the
                                # following pawn until the streak is over
                                steak_length += 1
                            elif self.game_board[current_node[0]][current_node[1]] is None and steak_length == 0:
                                # If we detect a None square and the streak i equal to 0, we check the next adjacent
                                # square
                                break

                            current_node = (current_node[0] + direction[0], current_node[1] + direction[1])

    # Checks if the given coordinates is a valid move
    def is_valid_move(self, x, y):
        return (x, y) in self.possible_moves

    # Puts a pawn of the board of the player's color and change the color of the enemy pawns streak that he created
    def set_pawns(self, player, x, y):
        if player is not None:
            self.game_board[x][y] = player
            self.change_color(x, y, player)
        else:
            self.game_board[x][y] = None

    def change_color(self, x, y, player):
        for direction in self.adj:
            found_streak = False
            current_node = (x + direction[0], y + direction[1])
            while self.in_range(*current_node):
                if self.game_board[current_node[0]][current_node[1]] is None:
                    break
                elif self.game_board[current_node[0]][current_node[1]] == player:
                    found_streak = True
                    break

                current_node = (current_node[0] + direction[0], current_node[1] + direction[1])
            if found_streak:
                direction = (direction[0] * -1, direction[1] * -1)

                while current_node != (x, y):
                    self.game_board[current_node[0]][current_node[1]] = player
                    current_node = (current_node[0] + direction[0], current_node[1] + direction[1])

    # Return True if the coordinate is in the board game
    # Return False if not
    def in_range(self, x, y):
        return DIMENSION > x >= 0 and DIMENSION > y >= 0

    def get_possible_moves(self):
        return self.possible_moves

    # Return True if there are no empty squares to play left
    def is_game_finished(self):
        for x in range(len(self.game_board[0])):
            for y in range(len(self.game_board)):
                if self.game_board[x][y] == None:
                    return False
        return True

    # Compute the winner by counting the number of black and white pawns
    # The winner is the one that hase the most pawns on the board
    def compute_winner(self):
        for l in self.game_board:
            for c in l:
                if c == 1:
                    self.white_pawn += 1
                elif c == 0:
                    self.black_pawn += 0

        return "black player" if self.black_pawn > self.white_pawn else "white player"

    def get_board(self):
        return self.game_board

    def set_board(self, board):
        self.game_board = board

    def set_no_moves_player1(self, value):
        self.no_moves_player = value

    def get_no_moves_player1(self):
        return self.no_moves_player

    # Print the table board in console
    def print_table(self):
        for l in range(len(self.game_board[0])):
            for c in range(len(self.game_board)):
                print("-" if self.game_board[c][l] is None else self.game_board[c][l], end="")
            print()
