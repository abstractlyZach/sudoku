#!/usr/bin/python3

# sudokugame.py

class Game():
	'''Handles all the game logic and interfaces with the board to execute moves.'''

	def __init__(self):
		'Starts a new game'
		pass

	def validate_move(self, row: int, column: int, number: int):
		'''
		Validates a move. If no exceptions are raised, the move is valid.
		This function will raise the appropriate exception for the validity of the move
		Needs to check:
			(1) Cell is within the board's bounds
			(2) Cell is not occupied
			(3) The move doesn't have any of the same entry in the same column, row, or box.
			(4) The number to enter is not 1-9
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
		'''
		Executes a move if it's valid. Otherwise, throws an error. Making a move clears
		the redo stack and adds an item to the undo stack.
		'''
		pass

	def undo_move(self):
		"Undoes the last move if possible. Otherwise throws and exception."
		pass

	def redo_move(self):
		"Redoes the last move if possible. Otherwise throws an exception."
		pass

# I'm considering removing this method. Why would someone ever remove a move when
#	they have a ton of other decisions that probably relied on that move?
#	Undoing all the way back to the move in question seems to be the only one that makes sense
	def remove(self, row: int, column: int):
		"Remove a number from the given cell"
		pass

# maybe have save states include undo and redo stacks. I'm still trying to figure out if that makes sense or not.
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

	def _is_in_bounds(self, row: int, column: int):
		'Checks if the move is in bounds.'
		pass

	def _is_cell_occupied(self, row: int, column: int):
		'Checks if the move is in an occupied cell.'
		pass

	def _is_move_in_same_row(self, row: int, number: int):
		'Checks if the number is in the same row.'
		pass

	def _is_move_in_same_column(self, column: int, number: int):
		'Checks if the number is in the same column.'
		pass

	def _is_move_in_same_box(self, row: int, column: int, number: int):
		'Checks if the number is in the same box.'
		pass

	def _is_number_valid(self, number: int):
		'Checks if the number is 1-9.'
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

class InvalidEntryException(Exception):
	'Exception for entries that are not 1-9'
	pass

class UndoStackException(Exception):
	'Exception for when the undo stack is empty and someone tries to undo a move.'
	pass

class RedoStackException(Exception):
	'Exception for when the redo stack is empty and someone tries to redo a move.'
	pass