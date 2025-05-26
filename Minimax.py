import copy
import math
import board

class MiniMax:
    def __init__(self):
        self.count = 0

    def minimax(self, alpha, beta, board, depth, is_maximizing):

        score = 0
        board.compute_possible_moves(is_maximizing)
        allmoves = board.get_possible_moves()
        score += ((len(allmoves)) * 15) * (1 if is_maximizing else -1)

        if depth == 0:
            score += self.board_evaluation(board, is_maximizing)
            return None, score
        elif board.is_game_finished(is_maximizing):
            if board.compute_winner():
                return None, math.inf
            else:
                return None, -math.inf

        best_score = -math.inf if is_maximizing else math.inf
        # best_move = []
        best_move = None


        if board.get_possible_moves():
            for i in board.get_possible_moves():

                copy_board = copy.deepcopy(board)
                copy_board.set_pawns(is_maximizing, i[0], i[1])
                score = self.minimax(alpha, beta, copy_board, depth - 1, 1 - is_maximizing)[1]

                if is_maximizing:
                    if score > best_score:
                        best_score = score
                        best_move = i
                    alpha = max(alpha, best_score)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = i
                    beta = min(beta, best_score)

                if alpha >= beta:
                    break
        else:
            best_move, best_score = self.minimax(alpha, beta, board, depth - 1, 1 - is_maximizing)

        return best_move, best_score

    def board_evaluation(self, board, is_maximizing):
        score = 0
        nbrPons = 0
        for x in range(len(board.get_board())):
            for y in range(len(board.get_board()[0])):
                if board.get_board()[x][y] == is_maximizing:
                    nbrPons += 1
                    score += board.get_weighted_board()[x][y]
        if is_maximizing:
            score += nbrPons * 10
        else:
            score += nbrPons * -10
        return score

