import copy
import math

import board


class MiniMax:

    def minimax(self, board: board.Board, depth, is_maximizing):

        if board.is_game_finished():
            winner = board.compute_winner()[0]
            if winner == "b":
                return 100 + depth
            elif winner == "w":
                return 100 - depth
            else:
                return 0
        if is_maximizing:
            board.computer_possible_moves(1)
            best_score = -math.inf
            for i in board.get_possible_moves():
                copy_board = copy.deepcopy(board)
                board.set_pawns(1, i[0], i[1])
                score = self.minimax(board, depth + 1, False)
                board.set_board(copy_board.get_board())
                best_score = max(best_score, score)
            return best_score
        else:
            board.computer_possible_moves(0)
            best_score = math.inf
            for i in board.get_possible_moves():
                copy_board = copy.deepcopy(board)
                board.set_pawns(0, i[0], i[1])
                score = self.minimax(board, depth + 1, True)
                board.set_board(copy_board.get_board())
                best_score = min(best_score, score)
            return best_score

    def best_move(self, board):
        board.computer_possible_moves(1)
        max_score = -math.inf
        move = None
        for i in board.get_possible_moves():

            copy_board = copy.deepcopy(board)
            board.set_pawns(1, i[0], i[1])
            score = self.minimax(board, 0, False)
            board.set_board(copy_board.get_board())
            if score > max_score:
                max_score = score
                move = (i[0], i[1])
        return move
