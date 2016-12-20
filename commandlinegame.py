# commandlinegame.py

import sudokugame
import gameexceptions
import prompt
import os
import constants

def play(game):
	'''Given a Game object, allows the player to perform various actions, 
	such as saving its current state, adding pieces, or removing pieces.'''
	turn_counter = 0

	print('TURN: {}'.format(turn_counter))
	game.print_board()

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
		except Exception as inst: # any other exceptions that aren't game exceptions
			print(inst)


def zero_and_eight_inclusive(integer_to_test):
	'Used for checking row and column input.'
	return 0 <= integer_to_test <= 8


def get_sudoku_pack_from_input():
	sudoku_pack = ""
	while True:
		sudoku_pack = prompt.for_string(
							'Choose the sudoku pack you want to use ("o" to read options) ', 
							default='0', error_message='Not a valid sudoku pack.')
		if sudoku_pack.lower() == 'o':
			with open(constants.PACKLIST, 'r', encoding='utf-8') as pack_list_file:
				print(pack_list_file.readline().strip())
		else:
			break
	return sudoku_pack


def get_sudoku_number_from_input():
	sudoku_number = prompt.for_int('Choose the sudoku number you want to use ', 
								default=0,
								error_message='Please enter a non-negative integer.')
	return sudoku_number


