# playsudoku.py

import sudokugame
import prompt
import os

game = sudokugame.Game()
turn_counter = 0

sudoku_pack = prompt.for_string('Choose the sudoku pack you want to use ', default='0', 
								error_message='Not a valid sudoku pack.')
sudoku_number = prompt.for_int('Choose the sudoku number you want to use ', default=0,
								error_message='Not a valid sudoku game in the pack.')
game.load_state(os.path.join('sudoku_states', 
							'{}_{:05d}'.format(sudoku_pack, sudoku_number)))

print('TURN: {}'.format(turn_counter))
game.print_board()
while not game.check_victory():
	try:
		row = prompt.for_int('Enter row')
		column = prompt.for_int('Enter column')
		number = prompt.for_int('Enter number')
		game.make_move(row, column, number)
		turn_counter += 1
		print('TURN: {}'.format(turn_counter))
		game.print_board()
	except sudokugame.get_game_exceptions() as inst:
		print('INVALID MOVE') # this will be more detailed later when I further study exceptions
		print(inst)
	except Exception as inst:
		print(inst)