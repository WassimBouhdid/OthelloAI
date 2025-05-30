import pygame
import sys
import math
import time

import board
import Minimax
import MonteCarlo

pygame.init()

DIMENSION = 8
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // DIMENSION
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

FONT_LARGE = pygame.font.Font(None, 100)
FONT_MEDIUM = pygame.font.Font(None, 50)
FONT_SMALL = pygame.font.Font(None, 36)

BG_COLOR = (75, 53, 42)
TEXT_COLOR = (255, 255, 255)  # Blanc
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)


def draw_text(text, font, color, surface, x, y, center=True):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def draw_board(board_instance, screen):
    screen.fill((83, 125, 93))  # Updated board background
    for i in range(1, DIMENSION):
        pygame.draw.line(screen, (0, 0, 0), (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), 5)
        pygame.draw.line(screen, (0, 0, 0), (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), 5)

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            pawn = board_instance.get_board()[r][c]
            if pawn == 0:
                pygame.draw.circle(screen, "black",
                                   (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 5)
            elif pawn == 1:
                pygame.draw.circle(screen, "white",
                                   (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 5)


def draw_return_button():
    return_img = pygame.image.load("icons/return-green.png").convert_alpha()
    return_hover_img = pygame.image.load("icons/return-orange.png").convert_alpha()
    return_rect = return_img.get_rect(topleft=(10, 10))

    mouse_pos = pygame.mouse.get_pos()
    is_hovered = return_rect.collidepoint(mouse_pos)

    SCREEN.blit(return_hover_img if is_hovered else return_img, return_rect)
    return is_hovered


def show_splash_screen():
    waiting = True

    # Define custom fonts by category
    FONT_TITLE = pygame.font.Font("fonts/pixel.otf", 90)
    FONT_SUBTITLE = pygame.font.SysFont("consolas", 20)
    FONT_CREDITS = pygame.font.SysFont("consolas", 20)
    FONT_BUTTON = pygame.font.Font("fonts/pixel.otf", 32)

    # Button colors
    BUTTON_COLOR = (178, 205, 156)
    BUTTON_HOVER_COLOR = (202, 120, 66)
    BUTTON_TEXT_COLOR = (75, 53, 42)  # Hex #4B352A

    while waiting:
        SCREEN.fill(BG_COLOR)

        # Title
        draw_text("Othello", FONT_TITLE, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 6)

        # Subtitle
        draw_text("Developed by:", FONT_SUBTITLE, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2.5)

        # Contributors in code font
        draw_text("Wassim Bouhdid (000596875)", FONT_CREDITS, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2.2)
        draw_text("Leila Bourouf (000592462)", FONT_CREDITS, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2.0)
        draw_text("Maxime Van den Broeck (000461666)", FONT_CREDITS, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 1.85)

        # 'Click to start !' styled box
        click_text = "Click to start !"
        click_surface = FONT_BUTTON.render(click_text, True, BUTTON_TEXT_COLOR)
        click_rect = click_surface.get_rect(center=(WIDTH // 2, HEIGHT * 2.5 / 3))

        padding = 20
        box_rect = click_rect.inflate(padding, padding)

        mouse_pos = pygame.mouse.get_pos()
        is_hovered = box_rect.collidepoint(mouse_pos)

        pygame.draw.rect(SCREEN, BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR, box_rect)
        pygame.draw.rect(SCREEN, TEXT_COLOR, box_rect, width=2)
        SCREEN.blit(click_surface, click_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and is_hovered:
                waiting = False


def create_button(text, rect):
    # Local styling (same as "Click to start!" button)
    font = pygame.font.Font("fonts/pixel.otf", 32)  # Replace with your .otf filename
    box_color = (178, 205, 156)
    hover_color = (202, 120, 66)
    border_color = (255, 255, 255)
    text_color = (75, 53, 42)  # Hex #4B352A

    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)

    # Draw box
    pygame.draw.rect(SCREEN, hover_color if is_hovered else box_color, rect)
    pygame.draw.rect(SCREEN, border_color, rect, width=2)

    # Draw text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    SCREEN.blit(text_surface, text_rect)

    return is_hovered


def main_menu():
    button_hvh = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 60)
    button_hva = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)
    button_ava = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 60)
    FONT_TITLE = pygame.font.Font("fonts/block.otf", 90)

    while True:
        SCREEN.fill(BG_COLOR)
        draw_text("Main menu", FONT_TITLE, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 4)

        hvh_hovered = create_button("Human vs Human", button_hvh)
        hva_hovered = create_button("Human vs IA", button_hva)
        ava_hovered = create_button("IA vs IA", button_ava)
        return_hovered = draw_return_button()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_hovered:
                    return "back"  # Go back to splash
                if hvh_hovered:
                    return "hvh"
                if hva_hovered:
                    return "hva"
                if ava_hovered:
                    return "ava"


def select_ai_menu(title="Choose an AI"):
    button_minimax = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 60)
    button_mcts = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 60)
    FONT_TITLE = pygame.font.Font("fonts/block.otf", 40)

    while True:
        SCREEN.fill(BG_COLOR)
        draw_text(title, FONT_TITLE, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 4)

        minimax_hovered = create_button("Minimax", button_minimax)
        mcts_hovered = create_button("Monte-Carlo", button_mcts)
        return_hovered = draw_return_button()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_hovered:
                    return None
                if minimax_hovered:
                    return "minimax"
                if mcts_hovered:
                    return "mcts"


def get_num_matches_screen():
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    user_text = ''

    FONT_TITLE = pygame.font.Font("fonts/block.otf", 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.isdigit() and int(user_text) > 0:
                        return int(user_text)
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.unicode.isdigit():
                    user_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if draw_return_button():
                    return None  # Return to main menu

        SCREEN.fill(BG_COLOR)
        draw_text("Number of games ?", FONT_TITLE, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2 - 100)

        pygame.draw.rect(SCREEN, TEXT_COLOR, input_box, 2)
        draw_text(user_text, FONT_TITLE, TEXT_COLOR, SCREEN, input_box.centerx, input_box.centery)

        draw_return_button()
        pygame.display.flip()


def game_loop(game_mode, ai_type=None):
    board_game = board.Board()
    player = 0  # Noir commence
    ai_player = None
    ai_instance = None
    score = 0

    FONT_TITLE = pygame.font.Font("fonts/block.otf", 30)

    if game_mode == 'hva':
        ai_player = 1  # L'IA joue en tant que joueur blanc
        if ai_type == "minimax":
            ai_instance = Minimax.MiniMax()
        elif ai_type == "mcts":
            ai_instance = MonteCarlo.MonteCarlo(time_limit=3)

    running = True
    while running:
        if board_game.is_game_finished(player):
            running = False
            break

        board_game.compute_possible_moves(player)
        current_possible_moves = board_game.get_possible_moves()

        is_ai_turn = (game_mode == 'hva' and player == ai_player)

        if is_ai_turn:
            if current_possible_moves:
                draw_text(f"L'IA ({ai_type}) reflechit...", FONT_TITLE, TEXT_COLOR, SCREEN, WIDTH // 2, 20)
                pygame.display.flip()
                if ai_type == "minimax":
                    ai_move, score = ai_instance.minimax(-math.inf, math.inf, board_game, 6, True, 1, pygame)
                else:
                    ai_move = ai_instance.monte_carlo_tree_search(board_game, player, pygame)

                if ai_move and board_game.is_valid_move(ai_move[0], ai_move[1]):
                    board_game.set_pawns(player, ai_move[0], ai_move[1])
                    player = 1 - player
                else:
                    player = 1 - player  # Passe son tour
            else:
                player = 1 - player  # Passe son tour si aucun mouvement possible
        else:  # Tour du joueur humain
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  # Retour au menu principal
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if current_possible_moves:
                        print(current_possible_moves)
                        pos_x, pos_y = event.pos
                        col = pos_x // SQUARE_SIZE
                        row = pos_y // SQUARE_SIZE
                        print((row, col))
                        if (row, col) in current_possible_moves:
                            board_game.set_pawns(player, row, col)
                            player = 1 - player
                    else:  # Si pas de coup possible, le joueur doit quand même cliquer pour passer son tour
                        player = 1 - player

        draw_board(board_game, SCREEN)
        pygame.display.flip()

    winner = board_game.compute_winner()
    winner_text = f"The {'White' if winner == 1 else 'Black'} player won !" if winner != 2 else "Draw !"
    draw_text(winner_text, FONT_TITLE, (255, 200, 0), SCREEN, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    time.sleep(4)


def ai_vs_ai_simulation(num_matches, first_ai_type):
    ai1_name = "Minimax" if first_ai_type == "minimax" else "Monte-Carlo"
    ai2_name = "Monte-Carlo" if first_ai_type == "minimax" else "Minimax"

    FONT_TITLE = pygame.font.Font("fonts/block.otf", 30)

    if first_ai_type == "minimax":
        ai1 = Minimax.MiniMax()
        ai2 = MonteCarlo.MonteCarlo(time_limit=0.5)
    else:
        ai1 = MonteCarlo.MonteCarlo(time_limit=0.5)
        ai2 = Minimax.MiniMax()

    ai1_wins = 0

    for i in range(num_matches):
        pygame.event.pump()
        pygame.display.flip()
        SCREEN.fill(BG_COLOR)
        draw_text("Simulation in progress...", FONT_TITLE, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(f"Partie {i + 1} / {num_matches}", FONT_TITLE, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2 + 20)
        pygame.event.pump()
        pygame.display.flip()

        sim_board = board.Board()
        current_player = 0

        while not sim_board.is_game_finished(current_player):
            pygame.event.pump()
            pygame.display.flip()
            sim_board.compute_possible_moves(current_player)
            if not sim_board.get_possible_moves():
                current_player = 1 - current_player
                continue

            move = None
            if current_player == 0:
                if first_ai_type == "minimax":
                    move = ai1.minimax(-math.inf, math.inf, sim_board, 3, True, 0, pygame)[0]
                else:
                    move = ai1.monte_carlo_tree_search(sim_board, current_player, pygame)
            else:

                if first_ai_type == "minimax":
                    move = ai2.monte_carlo_tree_search(sim_board, current_player, pygame)
                else:
                    move = ai2.minimax(-math.inf, math.inf, sim_board, 3, True, 1, pygame)[0]

            if move:
                sim_board.set_pawns(current_player, move[0], move[1])
            current_player = 1 - current_player
        if sim_board.compute_winner() == 0:
            ai1_wins += 1

    pygame.event.pump()
    pygame.display.flip()

    SCREEN.fill(BG_COLOR)
    draw_text("Simulation Completed", FONT_TITLE, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 3)
    result_text = f"Victories {ai1_name} (IA 1): {(ai1_wins / num_matches) * 100:.2f}%"
    draw_text(result_text, FONT_TITLE, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2)

    draw_return_button()
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and draw_return_button():
                return
        pygame.display.flip()


def main():
    while True:
        show_splash_screen()  # Always start with splash
        while True:
            choice = main_menu()
            if choice == "back":
                break  # Go back to splash screen
            if choice == "hvh":
                game_loop("hvh")
            elif choice == "hva":
                ai_choice = select_ai_menu("Choose which AI to challenge")
                if ai_choice is None:
                    continue  # Back to main menu
                game_loop("hva", ai_type=ai_choice)
            elif choice == "ava":
                num_matches = get_num_matches_screen()
                if num_matches:
                    first_ai = select_ai_menu("Who is AI n1 (Black) ?")
                    if first_ai:
                        ai_vs_ai_simulation(num_matches, first_ai)


if __name__ == "__main__":
    main()
