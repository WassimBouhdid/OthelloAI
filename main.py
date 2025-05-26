import argparse
import math
import sys
import time
from random import *
import pygame
import Minimax
import MonteCarlo
import board


def draw_board(board, dimension, height, width, screen):
    # Draws the black line in order to create all the squares of the board
    for i in range(1, dimension):
        pygame.draw.line(screen, (0, 0, 0), [0, 0 + (height / dimension) * i],
                         [width, 0 + (height / dimension) * i], 5)
    for i in range(1, dimension):
        pygame.draw.line(screen, (0, 0, 0), [0 + (height / dimension) * i, 0],
                         [0 + (height / dimension) * i, width], 5)

    # draw a black pawn where there is a 0 in the gameBoard
    # draw a white pawn where there is a 1 in the gameBoard
    for x in range(len(board.get_board())):
        for y in range(len(board.get_board()[0])):
            if board.get_board()[x][y] == 0:
                pygame.draw.circle(screen, "black", [((width / dimension) / 2) + (width / dimension) * y,
                                                     ((width / dimension) / 2) + (width / dimension) * x], 25)
            elif board.get_board()[x][y] == 1:
                pygame.draw.circle(screen, "white", [((width / dimension) / 2) + (width / dimension) * y,
                                                     ((width / dimension) / 2) + (width / dimension) * x], 25)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('Player1',
                        type=str,
                        help='Choose player 1 (minimax, human, montecarlo) ')

    parser.add_argument('Player2',
                        type=str,
                        help='Choose player 2 (minimax, human, montecarlo)')

    parser.add_argument('rounds',
                        type=int,
                        help='The number of rounds the players will do')

    args = parser.parse_args()

    # initialising the parameters of the game board
    DIMENSION = 8
    WIDTH = 600
    HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    pygame.display.set_caption("Othello AI Project")

    clock = pygame.time.Clock()
    running = True
    player = 0
    boardgame = board.Board()
    # boardgame.compute_possible_moves(player)

    minimax_ai = Minimax.MiniMax()
    mcts_ai = MonteCarlo.MonteCarlo(iteration_limit=1000)

    # ai_player = minimax_ai

    playersMode = [args.Player1, args.Player2]
    rounds = int(args.rounds)
    Player1Wins = 0

    print(f"Using {args.Player1.upper()} for Player 1 (White)")
    print(f"Using {args.Player2.upper()} for Player 2 (Black)")
    print(f"les deux adversaire vont s'affronter pendant {rounds}")
    while running:
        while rounds >= 0:
            if boardgame.is_game_finished(player):
                print("END")
                winner = boardgame.compute_winner()

                font = pygame.font.Font(None, 74)
                text = ""

                if winner == 1:
                    text = font.render("White team Wins !", True, (255, 255, 255))
                    print("white team wins")
                    print(f"{playersMode[player]} wins")
                elif winner == 0:
                    text = font.render("Black team Wins !", True, (0, 0, 0))
                    print("black team wins")
                    print(f"{playersMode[player]} wins")
                    Player1Wins += 1
                else:
                    text = font.render("Draw !", True, (128, 128, 128))
                    print("MATCH NUL")

                text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                screen.blit(text, text_rect)
                pygame.display.flip()

                boardgame.print_table()

                pygame.time.wait(3000)
                boardgame.reset_board()
                rounds -= 1

                continue

            # moves possibles pour le joueur actuel
            boardgame.compute_possible_moves(player)
            current_possible_moves = boardgame.get_possible_moves()

            # tour du joueur humain (le joueur 0)
            if playersMode[player] == "human":
                played_move = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        rounds = -1
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if current_possible_moves:
                            coord_x = int(event.pos[1] // (HEIGHT / DIMENSION))
                            coord_y = int(event.pos[0] // (WIDTH / DIMENSION))

                            if boardgame.is_valid_move(coord_x, coord_y):
                                print(f"Player 0 played: ({coord_x}, {coord_y})")  # pour voir dans la console
                                boardgame.set_pawns(player, coord_x, coord_y)
                                player = 1 - player  # au tour de l'IA
                                played_move = True
                                pygame.display.flip()
                                break
                        else:
                            print("Player 0 has no moves, click ignored.")

                if not running: continue

                # si aucun coup n'a été joué via clic et que le joueur n'avait pas de coups possibles
                if not played_move and not current_possible_moves:
                    print(f"Player {player} has no possible moves. Passing turn.")
                    player = 1 - player  # passe son tour

            # tour de l'ia (le joueur 1)
            elif playersMode[player] == "mcts" or playersMode[player] == "minimax":
                print(
                    f"AI Turn - Possible Moves: {current_possible_moves}")  # détaille les moves possible de l'ia dans la console
                if current_possible_moves:

                    ai_move = None
                    start_ai_time = time.time()

                    if playersMode[player] == "minimax":
                        ai_move, score = minimax_ai.minimax(-math.inf, math.inf, boardgame, 5, player)
                        pygame.display.flip()
                        print(f"Minimax AI returned: Move={ai_move}, Score={score}")
                    elif playersMode[player] == "mcts":
                        ai_move = mcts_ai.monte_carlo_tree_search(boardgame, player)
                        pygame.display.flip()
                        print(f"MCTS AI returned: Move={ai_move}")
                    else:
                        print("Error: Unknown AI algorithm specified!")
                        ai_move = random.choice(list(current_possible_moves)) if current_possible_moves else None

                    end_ai_time = time.time()
                    print(f"AI calculation time: {end_ai_time - start_ai_time:.4f} seconds")

                    # au cas où l'ia ne retourne pas de coups mais qu'il y a au moins un coup à jouer
                    if ai_move is None and current_possible_moves:
                        print(
                            f"{args.Player1} returned None, but moves exist. Forcing AI to play first possible move.")
                        ai_move = list(current_possible_moves)[0]
                        # ne met pas à jour le score de Minimax ici, car il vient de l'évaluation qui a échoué à choisir

                    if ai_move is not None and boardgame.is_valid_move(ai_move[0], ai_move[1]):
                        print(f"AI playing move: {ai_move}")
                        boardgame.set_pawns(player, ai_move[0], ai_move[1])
                        player = 1 - player
                    elif ai_move is not None:
                        print(f"!!! Error: AI proposed an invalid move: {ai_move}. Available: {current_possible_moves}")
                        ai_move = random.choice(list(current_possible_moves))
                        print(f"AI playing random valid move instead: {ai_move}")
                        boardgame.set_pawns(player, ai_move[0], ai_move[1])
                        player = 1 - player
                    else:
                        print("AI has no move (algorithm returned None and no fallback possible). Passing turn.")
                        player = 1 - player
                else:
                    print(f"Player {player} (AI) has no possible moves. Passing turn.")
                    player = 1 - player

            # colors the background in green
            screen.fill("green")
            # screen.fill((0, 128, 0))

            draw_board(boardgame, DIMENSION, HEIGHT, WIDTH, screen)

            pygame.display.flip()

            clock.tick(30)

    pygame.quit()

    print("the black team has a win porcentage of " + str((Player1Wins / rounds) * 100))

    with open("results.txt", "a") as f:
        f.write("Player1 : " + playersMode[0] + "," + "Player2 : " + playersMode[
            1] + ",number of rounds : " + args.rounds + ", results Player1: " + str(
            (Player1Wins / rounds) * 100) + ", results Player2: " + str(100 - ((Player1Wins / rounds) * 100)))
