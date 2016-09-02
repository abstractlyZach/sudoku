#!/usr/bin/python3

# sudokugame.py

import board

class Game():
	'''Handles all the game logic and interfaces with the board to execute moves.'''

	def __init__(self):
		'Starts a new game'
		self._board = board.Board()
		self._undo_stack = []
		self._redo_stack = []

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
		if not self._is_in_bounds(row, column):
			raise CellOutOfBoundsException
		if not self._is_cell_occupied(row, column):
			raise OccupiedCellException
		if not self._is_move_in_same_row(row, number):
			raise SameRowException
		if not self._is_move_in_same_column(column, number):
			raise SameColumnException
		if not self._is_move_in_same_box(row, column, number):
			raise SameBoxException
		if not self._is_number_valid(number):
			raise InvalidEntryException

	def new_game(self):
		'Undoes all moves to reset back to the loaded board.'
		for move in range(len(self._undo_stack)):
			self.undo_move()

	def get_board(self):
		'Returns a representation of the game board.'
		return self._board.get_board()

	def get_cell(self, row: int, column: int):
		'Returns the value of a cell.'
		return self._board.get_cell(row, column)

	def get_row(self, row: int):
		'Returns the values of a row.'
		return self._board.get_row(row)

	def get_column(self, column: int):
		'Returns the values of a column.'
		return self._board.get_column(column)

	def get_box(self, row: int, column: int):
		'Returns the values of the 3x3 box that the given cell is a member of.'
		return self._board.get_box(row, column)

	def open_cells(self):
		'Returns a list of the cells that are empty.'
		open_list = []
		for row in range(9):
			for column in range(9):
				if self.get_cell(row, column) == 0:
					open_list.append((row, column))
		return open_list

	def make_move(self, row: int, column: int, number: int):
		'''
		Executes a move if it's valid. Otherwise, throws an error. Making a move clears
		the redo stack and adds an item to the undo stack.
		'''
		self.validate_move(row, column, number)
		self._board.add(row, column, number)
		self._undo_stack.append((row, column, number))
		self._redo_stack = []

	def undo_move(self):
		"Undoes the last move if possible. Otherwise throws an exception."
		if len(self._undo_stack) == 0:
			raise UndoStackException
		row, column, number = self._undo_stack.pop()
		self._redo_stack.append(row, column, number)
		self._board.clear(row, column)

	def redo_move(self):
		"Redoes the last move if possible. Otherwise throws an exception."
		if len(self._redo_stack) == 0:
			raise RedoStackException
		row, column, number = self._redo_stack.pop()
		self._undo_stack.append(row, column, number)
		self._board.add(row, column, number)

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
		self._board.to_csv(state_name + '.csv')

	def load_state(self, state_name: str='save'):
		'Loads a board state'
		self._board.read_csv(state_name + '.csv')

	def check_victory(self) -> bool:
		'Checks the victory conditions have been met.'
		# check for a legal board
		if len(self.get_board()) != 9:
			raise BoardException
		for row in self.get_board():
			if len(row) != 9:
				raise BoardException
		# make sure rows have all numbers
		for row_index in range(9):
			row = self.get_row(row_index)
			for i in range(1, 10):
				if i not in row:
					return False
		# make sure columns have all numbers
		for column_index in range(9):
			column = self.get_column(column_index)
			for i in range(1, 10):
				if i not in column:
					return False
		# make sure boxes have all numbers
		for box_coord in [(0, 0), (3, 0), (6, 0), 
							(0, 3), (3, 3), (6, 3), 
							(0, 6), (3, 6), (6, 6)]:
			box = self.get_box(box_coord)
			for i in range(1, 10):
				if i not in box:
					return False
		return True

	def print_board(self):
		"Prints the board using the board's print_board method"
		self._board.print_board()

	def _is_in_bounds(self, row: int, column: int):
		'Checks if the move is in bounds.'
		return (row <= 8) and (row >= 0) and (column <= 8) and (column >= 0)

	def _is_cell_occupied(self, row: int, column: int):
		'Checks if the move is in an occupied cell.'
		return self.get_cell(row, column) == 0

	def _is_move_in_same_row(self, row: int, number: int):
		'Checks if the number is in the same row.'
		return number in self.get_row(row)

	def _is_move_in_same_column(self, column: int, number: int):
		'Checks if the number is in the same column.'
		return number in self.get_column(column)

	def _is_move_in_same_box(self, row: int, column: int, number: int):
		'Checks if the number is in the same box.'
		return number in self.get_box(row, column)

	def _is_number_valid(self, number: int):
		'Checks if the number is 1-9.'
		return (number <= 9) and (number >= 1)


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

class BoardException(Exception):
	'Exception for when something is wrong with the board.'
	pass