#!/usr/bin/python3

# sudokugame.py

import os
import board
import constants
import gameexceptions
import gameactions
import copy

class Game():
	'''Handles all the game logic and interfaces with the board to execute moves.'''

	def __init__(self):
		'Starts a new game'
		self._board = board.Board()
		self._undo_stack = []
		self._redo_stack = []

	def validate_add(self, row: int, column: int, number: int):
		'''
		Validates an add action. If no exceptions are raised, the move is valid.
		This function will raise the appropriate exception for the validity of the move
		Needs to check:
			(1) Cell is within the board's bounds
			(2) Cell is not occupied
			(3) The move doesn't have any of the same entry in the same column, row, or box.
			(4) The number to enter is not 1-9
		'''
		if not self._is_in_bounds(row, column):
			raise gameexceptions.CellOutOfBoundsException(row, column)
		if self._is_cell_occupied(row, column):
			raise gameexceptions.OccupiedCellException((row, column), self.get_cell(row, column))
		if self._is_move_in_same_row(row, number):
			column_of_repeater = self.get_row(row).index(number)
			raise gameexceptions.SameRowException(row, column, column_of_repeater, number)
		if self._is_move_in_same_column(column, number):
			row_of_repeater = self.get_column(column).index(number)
			raise gameexceptions.SameColumnException(row, row_of_repeater, column, number)
		if self._is_move_in_same_box(row, column, number):
			index_in_box = self.get_box(row, column).index(number)
			raise gameexceptions.SameBoxException(row, column, index_in_box, number)
		if not self._is_number_valid(number):
			raise gameexceptions.InvalidEntryException(number)

	def validate_remove(self, row: int, column: int):
		'''
		Validates a remove command.
		'''
		if not self._is_in_bounds(row, column):
			raise gameexceptions.CellOutOfBoundsException(row, column)
	
	def validate_change(self, row: int, column: int, number: int):
		'''
		Validates a change command.
		'''
		if not self._is_in_bounds(row, column):
			raise gameexceptions.CellOutOfBoundsException(row, column)
		if self._is_move_in_same_row(row, number):
			column_of_repeater = self.get_row(row).index(number)
			raise gameexceptions.SameRowException(row, column, column_of_repeater, number)
		if self._is_move_in_same_column(column, number):
			row_of_repeater = self.get_column(column).index(number)
			raise gameexceptions.SameColumnException(row, row_of_repeater, column, number)
		if self._is_move_in_same_box(row, column, number):
			index_in_box = self.get_box(row, column).index(number)
			raise gameexceptions.SameBoxException(row, column, index_in_box, number)
		if not self._is_number_valid(number):
			raise gameexceptions.InvalidEntryException(number)	

	def validate_force_change(self, row: int, column: int, number: int):
		if not self._is_in_bounds(row, column):
			raise gameexceptions.CellOutOfBoundsException(row, column)		
		if not self._is_number_valid(number):
			raise gameexceptions.InvalidEntryException(number)	

	def validate_board(self):
		'Validates the whole board and throws the first exception it finds'
		for row_index in range(9):				
			row = self.get_row(row_index)
			for number in range(1, 10):
				if row.count(number) > 1:
					column_of_repeater = row.index(number)
					# column of repeater is doubled because it's a lot of extra work 
					# for an exception that won't be seen
					raise gameexceptions.SameRowException(row_index, 
						column_of_repeater, column_of_repeater, number)
		for column_index in range(9):
			column = self.get_column(column_index)
			for number in range(1, 10):
				if column.count(number) > 1:
					# same as column of repeater above
					row_of_repeater = column.index(number)
					raise gameexceptions.SameColumnException(row_of_repeater, row_of_repeater,
						column_index, number)
		for box_coord in [(0, 0), (3, 0), (6, 0), 
							(0, 3), (3, 3), (6, 3), 
							(0, 6), (3, 6), (6, 6)]:
			row, column = box_coord
			box = self.get_box(row, column)
			for number in range(1, 10):
				if box.count(number) > 1:
					index_in_box = box.index(number)
					# same as above
					raise gameexceptions.SameBoxException(99, 99, index_in_box, number)

	def new_game(self):
		'Undoes all moves to reset back to the loaded board.'
		for move in range(len(self._undo_stack)):
			self.undo_move()

	def get_board(self):
		'Returns a representation of the game board.'
		return copy.deepcopy(self._board.get_board())

	def set_board(self, board):
		'Given a board, sets the internal board if possible.'
		self._board.set_board(copy.deepcopy(board))

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
		self.validate_add(row, column, number)
		self._board.add(row, column, number)
		action = gameactions.AddAction(row, column, number)
		self._undo_stack.append(action)
		self._redo_stack = []

	def undo_move(self):
		'''Undoes the last move if possible. Otherwise throws an exception.'''
		if len(self._undo_stack) == 0:
			raise gameexceptions.UndoStackException
		action = self._undo_stack.pop()
		# assuming the undo stack only involves non-permanent cells
		number = action.get_old_number()
		row, column = action.get_coordinates()
		self._board.add(row, column, number)
		self._redo_stack.append(action)

	def redo_move(self):
		"Redoes the last move if possible. Otherwise throws an exception."
		if len(self._redo_stack) == 0:
			raise gameexceptions.RedoStackException
		action = self._redo_stack.pop()
		# assuming the undo stack only involves non-permanent cells
		number = action.get_new_number()
		row, column = action.get_coordinates()
		self._board.add(row, column, number)
		self._undo_stack.append(action)
		

	def remove(self, row: int, column: int):
		'''Remove a number from the given cell if that cell isn't permanent.
			Returns the number removed.'''
		self.validate_remove(row, column)
		if self.is_permanent(row, column):
			raise gameexceptions.PermanentCellException((row, column))
		else:
			number = self._board.clear(row, column)
			action = gameactions.RemoveAction(row, column, number)
			self._undo_stack.append(action)
			self._redo_stack = []
			return number

	def change(self, row: int, column: int, number: int):
		'''Changes a number if its cell isn't permanent.
			Returns the old number.'''
		self.validate_change(row, column, number)
		if self.is_permanent(row, column):
			raise gameexceptions.PermanentCellException((row, column))
		else:
			old_number = self._board.add(row, column, number)
			action = gameactions.ChangeAction(row, column, number, old_number)
			self._undo_stack.append(action)
			self._redo_stack = []
			return old_number

	def force_change(self, row: int, column: int, number: int):
		'''Forces a change on a cell without checking for conflicts'''
		self.validate_force_change(row, column, number)
		if self.is_permanent(row, column):
			raise gameexceptions.PermanentCellException((row, column))
		else:
			old_number = self._board.add(row, column, number)
			action = gameactions.ChangeAction(row, column, number, old_number)
			self._undo_stack.append(action)
			self._redo_stack = []
			return old_number 

	def is_permanent(self, row: int, column: int):
		'Returns true if a cell is permanent.'
		return self._board.is_permanent(row, column)

	def set_permanent(self):
		'Sets all filled cells as permanent.'
		self._board.set_permanent()

# maybe have save states include undo and redo stacks. I'm still trying to figure out if that makes sense or not.
	def save_state(self, state_name: str='save'):
		'''
		Saves the current state. Uses state_name to name the csv file in
		the board's to_csv call.
		'''
		file_name = state_name + '.csv'
		file_path = os.path.join(constants.STATE_STORAGE_DIRECTORY, file_name)
		self._board.to_csv(file_path)
		permanency_file_path = os.path.join(constants.PERMANENCY_DIRECTORY, file_name)
		self._board.write_permanency(permanency_file_path)
		

	def load_state(self, state_name: str='save'):
		'''Loads a board state. If the permanency file does not exist, then this is 
		the original puzzle, so all non-zero cells must be permanent'''
		file_name = state_name + '.csv'
		file_path = os.path.join(constants.STATE_STORAGE_DIRECTORY, file_name)
		self._board.read_csv(file_path)
		permanency_file_path = os.path.join(constants.PERMANENCY_DIRECTORY, file_name)
		try:
			self._board.read_permanency(permanency_file_path)
		except FileNotFoundError: # permanency file doesn't exist
			self.set_permanent()

	def check_victory(self) -> bool:
		'Checks the victory conditions have been met.'
		# check for a legal board
		if len(self.get_board()) != 9:
			raise gameexceptions.TooManyRowsException(len(self.get_board()))
		for row in self.get_board():
			if len(row) != 9:
				raise gameexceptions.TooManyColumnsException(len(row), row)
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
			box = self.get_box(box_coord[0], box_coord[1])
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
		return self.get_cell(row, column) != 0

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
