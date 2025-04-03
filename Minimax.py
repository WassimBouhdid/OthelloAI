import copy
import math
import board

DIMENSION = 4


class MiniMax:
    def __init__(self):
        self.count = 0

    def minimax(self, board, depth, is_maximizing):
        # print(depth)

        # print(self.count)
        # self.count +=1
        if board.is_game_finished(is_maximizing):
            if board.compute_winner():
                return DIMENSION * DIMENSION + depth
            else:
                return DIMENSION * DIMENSION - depth

        board.compute_possible_moves(is_maximizing)
        best_score = -math.inf if is_maximizing else math.inf
        # print(board.get_possible_moves())
        if board.get_possible_moves():
            for i in board.get_possible_moves():
                copy_board = copy.deepcopy(board)
                board.set_pawns(is_maximizing, i[0], i[1])
                score = self.minimax(board, depth + 1, 1 - is_maximizing)
                board.set_board(copy_board.get_board())
                best_score = max(best_score, score) if is_maximizing else min(best_score, score)
        else:
            # print("pas de move pour", is_maximizing)
            best_score = self.minimax(board, depth + 1, 1 - is_maximizing)

        return best_score

    def best_move(self, board, player):
        board.compute_possible_moves(player)
        max_score = -math.inf
        move = None
        print(board.get_possible_moves())
        for i in board.get_possible_moves():
            copy_board = copy.deepcopy(board)
            board.set_pawns(1, i[0], i[1])
            score = self.minimax(board, 0, 1- player)
            board.set_board(copy_board.get_board())
            print(score)
            if score > max_score:
                max_score = score
                move = (i[0], i[1])
        # print(self.count)
        return move

