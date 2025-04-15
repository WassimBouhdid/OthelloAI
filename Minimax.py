import copy
import math
import board

DIMENSION = 4


class MiniMax:
    def __init__(self):
        self.count = 0

    def minimax(self, alpha, beta, board, depth, is_maximizing):

        # print(depth)

        # print(self.count)
        # self.count +=1
        board.compute_possible_moves(is_maximizing)

        if depth == 0:
            return self.board_evaluation(board, is_maximizing)
        elif board.is_game_finished(is_maximizing):
            if board.compute_winner():
                return math.inf
            else:
                return -math.inf

        best_score = -math.inf if is_maximizing else math.inf
        best_move = []

        if board.get_possible_moves():
            for i in board.get_possible_moves():

                copy_board = copy.deepcopy(board)
                copy_board.set_pawns(is_maximizing, i[0], i[1])
                score = self.minimax(alpha, beta, board, depth - 1, 1 - is_maximizing)
                # best_score = max(best_score, score) if is_maximizing else min(best_score, score)

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
                # max_score = score
                # move = (i[0], i[1])
        else:
            best_move, best_score = self.minimax(alpha, beta, board, depth - 1, 1 - is_maximizing)

        return best_move, best_score

    # def best_move(self, board, player):
    #     board.compute_possible_moves(player)
    #     max_score = -math.inf
    #     move = None
    #     for i in board.get_possible_moves():
    #         copy_board = copy.deepcopy(board)
    #         copy_board.set_pawns(1, i[0], i[1])
    #         score = self.minimax(board, 0, 1 - player)
    #         print(score)
    #         if score > max_score:
    #             max_score = score
    #             move = (i[0], i[1])
    #     # print(self.count)
    #     return move

    def board_evaluation(self, board, is_maximizing):
        score = 0
        for x in range(len(board.get_board())):
            for y in range(len(board.get_board()[0])):
                if board.get_board()[x][y] == is_maximizing:
                    score += board.get_weighted_board()[x][y]
        return score
