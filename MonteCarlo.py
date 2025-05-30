import random
import math
import copy
import time
from board import Board


class MonteCarloNode:
    def __init__(self, board_state, player, parent=None, move=None):
        self.board_state = board_state  # l'état du jeu correspondant au noeud
        self.player = player  # le joueur à qui est le tour (dans ce même état)
        self.parent = parent  # le noeud parent
        self.move = move  # le coup joué depuis le noeud parent pour amener à cet état
        self.children = []  # noeuds enfants
        self.wins = 0  # nombre de simulations gagnées depuis ce noeud
        self.visits = 0  # nombre de simulations qui sont passées par ce noeud
        self.untried_moves = None  # coups qui doivent encore être explorés depuis ce noeud

    def get_untried_moves(self):
        if self.untried_moves is None:
            self.board_state.compute_possible_moves(self.player)
            self.untried_moves = list(self.board_state.get_possible_moves())
            random.shuffle(self.untried_moves)
        return self.untried_moves

    def uct_select_child(self, exploration_constant=1.414):
        visited_children = [child for child in self.children if child.visits > 0]  # pour éviter la division par 0
        if not visited_children:
            return random.choice(self.children) if self.children else None

        log_total_visits = math.log(self.visits)

        selected_child = max(visited_children, key=lambda c: (c.wins / c.visits) + exploration_constant * math.sqrt(
            log_total_visits / c.visits))
        return selected_child

    def add_child(self, move, board_state, next_player):
        child = MonteCarloNode(board_state=board_state, player=next_player, parent=self, move=move)
        self.children.append(child)

        if move in self.untried_moves:
            self.untried_moves.remove(move)  # on retire le coup des coups non explorés
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result  # result = 1 pour win et 0 pour nul ou défaite


class MonteCarlo:
    def __init__(self, iteration_limit=1000, time_limit=None):
        self.iteration_limit = iteration_limit
        self.time_limit = time_limit

    def monte_carlo_tree_search(self, initial_board_state, current_player, pygame):
        root_node = MonteCarloNode(board_state=copy.deepcopy(initial_board_state), player=current_player)

        start_time = time.time()
        iterations = 0

        while True:
            pygame.event.pump()
            iterations += 1
            if self.iteration_limit is not None and iterations > self.iteration_limit:
                break
            if self.time_limit is not None and time.time() - start_time > self.time_limit:
                print(f"MCTS Time limit reached after {iterations} iterations.")
                break

            node = root_node
            sim_board = copy.deepcopy(root_node.board_state)
            sim_player = root_node.player

            # parcours de l'arbre jusqu'à ce qu'un noeud non exploré soit trouvé
            while node.get_untried_moves() == [] and node.children != []:
                node = node.uct_select_child()
                if node is None:
                    print("Error: uct_select_child returned None unexpectedly.")
                    break
                sim_board.set_pawns(1 - node.player, node.move[0], node.move[1])
                sim_player = node.player

            if node is None: continue

            # si le noeud a des coups non explorés on en teste un
            untried_moves = node.get_untried_moves()
            if untried_moves:
                move = untried_moves.pop()
                next_player = 1 - sim_player
                sim_board.set_pawns(sim_player, move[0], move[1])
                node = node.add_child(move, copy.deepcopy(sim_board), next_player)
                sim_player = next_player

            current_sim_player = node.player
            temp_sim_board = copy.deepcopy(node.board_state)

            while not temp_sim_board.is_game_finished(current_sim_player):
                temp_sim_board.compute_possible_moves(current_sim_player)
                possible_moves = list(temp_sim_board.get_possible_moves())

                if not possible_moves:
                    current_sim_player = 1 - current_sim_player  # on passe son tour
                    continue

                chosen_move = random.choice(possible_moves)
                temp_sim_board.set_pawns(current_sim_player, chosen_move[0], chosen_move[1])
                current_sim_player = 1 - current_sim_player

            winner = temp_sim_board.compute_winner()

            # Backpropagation
            while node is not None:
                parent_player = 1 - node.player
                result_for_node = 0  # par défaut sur défaite
                if winner == parent_player:
                    result_for_node = 1.0
                elif winner == 2:  # match nul
                    result_for_node = 0.5

                node.update(result_for_node)
                node = node.parent



        if not root_node.children:
            initial_board_state.compute_possible_moves(current_player)
            fallback_moves = list(initial_board_state.get_possible_moves())
            print("Warning: MCTS root has no children. Returning random move.")
            return random.choice(fallback_moves) if fallback_moves else None

        best_child = max(root_node.children, key=lambda c: c.visits)
        return best_child.move
