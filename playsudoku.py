# playsudoku.py

# Sets up the game and then lets the player loose to play the game.

import sudokugame
import os
import commandlinegame
import constants
import prompt

game = sudokugame.Game()
turn_counter = 0
file_found = False

if commandlinegame.prompt_load_pack():
	while not file_found:
		try:
			sudoku_pack = commandlinegame.get_sudoku_pack_from_input()
			sudoku_number = commandlinegame.get_sudoku_number_from_input()
			game.load_state('{}_{:05d}'.format(sudoku_pack, sudoku_number))
			file_found = True
		# except FileNotFoundError as e:
		# 	print(e)
		except Exception as e:
			print(e)
else:
	load_successful = False
	while not load_successful:
		try:
			save_state_name = prompt.for_string('Name of the save state ("q" to exit)')
			if save_state_name == 'q':
				load_successful = True
			else:
				game.load_state(save_state_name)
				load_successful = True
				turn_counter = 0 # reset turn counter now that a new game is loaded
		except FileNotFoundError as e:
			print(e)

commandlinegame.play(game)