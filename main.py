import time

import pygame

import Minmax
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
    for y in range(len(board.get_board())):
        for x in range(len(board.get_board()[0])):

            if board.get_board()[x][y] == 0:
                pygame.draw.circle(screen, "black", [((width / dimension) / 2) + (width / dimension) * x,
                                                     ((width / dimension) / 2) + (width / dimension) * y], 25)
            elif board.get_board()[x][y] == 1:
                pygame.draw.circle(screen, "white", [((width / dimension) / 2) + (width / dimension) * x,
                                                     ((width / dimension) / 2) + (width / dimension) * y], 25)


if __name__ == '__main__':

    # initialising the parameters of the game board
    DIMENSION = 4
    WIDTH = 600
    HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((HEIGHT, WIDTH))

    clock = pygame.time.Clock()
    running = True
    player = 0
    boardgame = board.Board()
    boardgame.computer_possible_moves(player)
    minimax = Minmax.MiniMax()

    player_moves = {"white": [], "black": []}

    player1_has_moves = True
    player2_has_moves = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Wait for a mouse click event

                # Get the coordinates of where the player has clicked
                coord_x = int(pygame.mouse.get_pos()[0] // (WIDTH / DIMENSION))
                coord_y = int(pygame.mouse.get_pos()[1] // (HEIGHT / DIMENSION))

                # If the coordinate is one of the valid move
                # We put a pawn of the player's color on that coordinate
                # and we change the color of the enemies pawn that are sandwiched between this pawn and other pawns
                # of the player

                if not player:
                    if boardgame.is_valid_move(coord_x, coord_y):
                        boardgame.set_pawns(player, coord_x, coord_y)
                        draw_board(boardgame, DIMENSION, HEIGHT, WIDTH, screen)
                        player = 1 - player  # change the player's turn
                    if boardgame.is_game_finished():
                        running = False
                        continue
                    draw_board(boardgame, DIMENSION, HEIGHT, WIDTH, screen)

            boardgame.computer_possible_moves(player)
            if bool(player):
                player_moves["white"] = boardgame.get_possible_moves()
            else:
                player_moves["black"] = boardgame.get_possible_moves()

            print(player_moves["white"])
            # print(player_moves["black"])
            if player_moves["black"] == [] and player_moves["white"] == []:
                print(boardgame.compute_winner())
                running = False
                continue

            if not boardgame.get_possible_moves():
                print("pas de moves pour le joueur", player)
                player = 1 - player

            if bool(player):
                ai_move = minimax.best_move(boardgame)
                boardgame.set_pawns(player, ai_move[0], ai_move[1])
                player = 1 - player

        # colors the background in green
        screen.fill("green")

        draw_board(boardgame, DIMENSION, HEIGHT, WIDTH, screen)

        pygame.display.flip()

        clock.tick(60)
