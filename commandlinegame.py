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
	show_board = True

	while not game.check_victory():
		try:
			if show_board:
				print('TURN: {}'.format(turn_counter))
				game.print_board()

			decision = main_turn_menu()
			if decision == '':
				turn_counter = targeted_action(game, turn_counter)

			elif decision == 'u':
				game.undo_move()
				turn_counter -= 1

			elif decision == 'r':
				game.redo_move()
				turn_counter += 1

			elif decision == 'o': 
				show_board = False
				continue # jump back to main menu

			elif decision == 'q':
				print('Goodbye!')
				print()
				return

			show_board = True
			print()
			print()
			
		except gameexceptions.get_game_exceptions() as inst:
			print('INVALID MOVE') # this will be more detailed later when I further study exceptions
			print(inst)
		except Exception as inst: # any other exceptions that aren't game exceptions
			print(inst)

	print('Turns taken: {}'.format(turn_counter))
	game.print_board()
	print('YOU WIN!!!')
	print()
	return


def targeted_action(game, turn_counter):
	row, column = get_row_and_column_from_input(game)
	valid_action = False
	while not valid_action:
		action = prompt.for_string(
			'Enter action ("o" for options) ',
			default='').lower()
		if action == '':	# add number
			number = prompt.for_int('Enter number', is_legal=(lambda x: 1 <= x <=9))
			game.make_move(row, column, number)
			turn_counter += 1
			valid_action = True
		elif action == 'r': # remove number
			game.remove(row, column)
			turn_counter += 1
			valid_action = True
		elif action == 'c': # change number
			number = prompt.for_int('Enter number', is_legal=(lambda x: 1 <= x <=9))
			game.change(row, column, number)
			turn_counter += 1
			valid_action = True
		elif action == 'o': # list options
			print('{:>10}:\t Add piece'.format('<Enter>'))
			print('{:>10}:\t Remove piece'.format('r'))
			print('{:>10}:\t Change piece'.format('c'))
			print('{:>10}:\t Return to main menu'.format('e'))
		elif action == 'e': # exit the current prompt
			valid_action = True
	return turn_counter


def main_turn_menu():
	decision_valid = False
	while not decision_valid:
		decision = prompt.for_string('Next action ("o" to read options) ', default='')
		if decision in ['', 'u', 'r', 'o', 'q']:
			decision_valid = True
			if decision == 'o':
				print('{:>10}:\t Targeted action'.format('<Enter>'))
				print('{:>10}:\t Undo move'.format('u'))
				print('{:>10}:\t Redo move'.format('r'))
				print('{:>10}:\t Quit'.format('q'))
	return decision


def get_row_and_column_from_input(game=None):
	row = prompt.for_int('Enter row', is_legal=zero_and_eight_inclusive)
	column = prompt.for_int('Enter column', is_legal=zero_and_eight_inclusive)
	print("Cell ({}, {}) contains: {}".format(row, column, game.get_cell(row, column)))
	return row, column


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