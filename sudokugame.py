#!/usr/bin/python3

# sudokugame.py

class Game():
	'''Handles all the game logic and interfaces with the board to execute moves.'''

	def __init__(self):
		'Starts a new game'
		pass

	def valid_move(self, row: int, column: int, number: int) -> bool:
		'''
		Returns a boolean describing whether or not the given move is valid on the board.
		Needs to check:
			(1) Cell is within the board's bounds
			(2) Cell is not occupied
			(3) The move doesn't have any of the same entry in the same column, row, or box.
		'''
		pass

	def new_game(self):
		'Creates a new board to start a new game'
		pass

	def get_board(self):
		'Returns a representation of the game board.'
		pass

	def open_cells(self):
		'Returns a list of the cells that are empty.'
		pass

	def make_move(self, row: int, column: int, number: int):
		"Executes a move if it's valid. Otherwise, throws an error."
		pass

	def remove(self, row: int, column: int):
		"Remove a number from the given cell"
		pass

	def save_state(self, state_name: str='save'):
		'''
		Saves the current state. Uses state_name to name the csv file in
		the board's to_csv call. 
		'''
		pass

	def load_state(self, state_name: str='save'):
		'Loads a board state'
		pass

	def check_victory(self) -> bool:
		'Checks the victory conditions have been met.'
		pass

	def print_board(self):
		"Prints the board using the board's print_board method"
		pass


class OccupiedCellException(Exception):
	'Exception for trying to make a move on an occupied cell.'
	pass

class CellOutOfBoundsException(Exception):
	'Exception for giving coordinates that are outside of the board.'
	pass

class SameRowException(Exception):
	'Exception for moves whose numbers have already been seen in the same row.'
	pass

class SameColumnException(Exception):
	'Exception for moves whose numbers have already been seen in the same column.'
	pass

class SameBoxException(Exception):
	'Exception for moves whose numbers have already been seen in the same box.'
	pass