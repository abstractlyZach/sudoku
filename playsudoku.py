# playsudoku.py

# Sets up the game and then lets the player loose to play the game.

import sudokugame
import os
import commandlinegame
import constants

game = sudokugame.Game()
turn_counter = 0

sudoku_pack = commandlinegame.get_sudoku_pack_from_input()
sudoku_number = commandlinegame.get_sudoku_number_from_input()
game.load_state(os.path.join(constants.STATE_STORAGE_DIRECTORY, 
							'{}_{:05d}'.format(sudoku_pack, sudoku_number)))

commandlinegame.play(game)