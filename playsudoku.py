# playsudoku.py

import sudokugame
import gameexceptions
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

def zero_and_eight_inclusive(integer_to_test):
	'Used for checking row and column input.'
	return 0 <= integer_to_test <= 8

while not game.check_victory():
	try:
		row = prompt.for_int('Enter row', is_legal=zero_and_eight_inclusive)
		column = prompt.for_int('Enter column', is_legal=zero_and_eight_inclusive)
		print("Cell ({}, {}) contains: {}".format(row, column, game.get_cell(row, column)))
		number = prompt.for_int('Enter number', is_legal=(lambda x: 1 <= x <=9))
		game.make_move(row, column, number)
		turn_counter += 1
		print('TURN: {}'.format(turn_counter))
		game.print_board()
	except gameexceptions.get_game_exceptions() as inst:
		print('INVALID MOVE') # this will be more detailed later when I further study exceptions
		print(inst)
	except Exception as inst:
		print(inst)

