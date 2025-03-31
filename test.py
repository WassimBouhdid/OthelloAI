import board

board = board.Board()
print(board.print_table())
board.computer_possible_moves(0)
copy_board = board
print(board.get_possible_moves())
board.set_pawns(0, 4, 4)
print(board.print_table())
board.set_board(copy_board)
print(board.print_table())
