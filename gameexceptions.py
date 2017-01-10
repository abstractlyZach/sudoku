#!/usr/bin/python3

# gameexceptions.py

def get_game_exceptions():
	'Returns all of the exceptions so that other modules can use them in their error handling'
	return (OccupiedCellException, CellOutOfBoundsException, SameRowException,
			SameColumnException, SameBoxException, InvalidEntryException, UndoStackException,
			RedoStackException, BoardException, PermanentCellException)


class PermanentCellException(Exception):
	'Exception for editing a permanent cell.'
	def __init__(self, cell):
		message = "PermanentCellException: Cell {} is marked as permanent."
		super(Exception, self).__init__(message.format(cell))


class OccupiedCellException(Exception):
	'Exception for trying to make a move on an occupied cell.'
	def __init__(self, cell, number_in_cell):
		message = "OccupiedCellException: Cell {} currently has the value {}."
		super(Exception, self).__init__(message.format(cell, number_in_cell))


class CellOutOfBoundsException(Exception):
	'Exception for giving coordinates that are outside of the board.'
	def __init__(self, row, column):
		message = "CellOutOfBoundsException: ({}, {}) is not within the board's bounds."
		super(Exception, self).__init__(message.format(row, column))


class SameRowException(Exception):
	'Exception for moves whose numbers have already been seen in the same row.'
	def __init__(self, row, column_of_move, column_of_repeater, number):
		self.row = row
		message = 'SameRowException: ({}, {}) is in the same row as ({}, {}) '
		message += 'and already contains the number {}.'
		super(Exception, self).__init__(message.format(row, column_of_repeater, 
														row, column_of_move, number))


class SameColumnException(Exception):
	'Exception for moves whose numbers have already been seen in the same column.'
	def __init__(self, row_of_move, row_of_repeater, column, number):
		self.column = column
		message = 'SameColumnException: ({}, {}) is in the same column as ({}, {}) '
		message += 'and already contains the number {}.'
		super(Exception, self).__init__(message.format(row_of_repeater, column,
														row_of_move, column, number))


class SameBoxException(Exception):
	'Exception for moves whose numbers have already been seen in the same box.'
	def __init__(self, row, column, index_of_repeater, number):
		self.coord = (row, column)
		message = 'SameBoxException: There is an entry in the {} '
		message += 'cell in the same box as ({}, {}) with the number {}.'
		repeater_column = index_of_repeater % 3
		repeater_row = index_of_repeater // 3

		# figure out the string representation of the position of the repeater e.g. top-left, bottom-center
		repeater_position_in_box = ''
		if repeater_row == 0:
			repeater_position_in_box += 'top' 
		elif repeater_row == 1:
			repeater_position_in_box += 'center'
		else: # repeater_row == 2:
			repeater_position_in_box += 'bottom'

		if repeater_column == 0:
			repeater_position_in_box += '-left' 
		elif repeater_column == 1:
			if repeater_row == 1:
				pass
			else:
				repeater_position_in_box += '-center'
		else: # repeater_row == 2:
			repeater_position_in_box += '-right'

		super(Exception, self).__init__(message.format(repeater_position_in_box, 
														row, column, number))


class InvalidEntryException(Exception):
	'Exception for entries that are not 1-9'
	def __init__(self, number):
		message = 'InvalidEntryException: {} is not in the range [1-9]'
		super(Exception, self).__init__(message.format(number))


class UndoStackException(Exception):
	'Exception for when the undo stack is empty and someone tries to undo a move.'
	def __init__(self):
		message = "UndoStackException: Undo stack is empty and an undo action was attempted."
		super(Exception, self).__init__(message)


class RedoStackException(Exception):
	'Exception for when the redo stack is empty and someone tries to redo a move.'
	def __init__(self):
		message = 'RedoStackException: Redo stack is empty and a redo action was attempted.'
		super(Exception, self).__init__(message)


class BoardException(Exception):
	'Exception for when there are problems with the board.'
	def __init__(self, message):
		super(Exception, self).__init__(message)

class TooManyRowsException(BoardException):
	'Exception for when there are too many rows on the board.'
	def __init__(self, number_of_rows):
		message = 'TooManyRowsException: There are {} rows on the board.'
		super(BoardException, self).__init__(message.format(number_of_rows))

class TooManyColumnsException(BoardException):
	'Exception for when there are too many columns on the board.'
	def __init__(self, number_of_columns, row_that_has_too_many_columns):
		message = 'TooManyColumnsException: There are {} columns in row {}.'
		super(BoardException, self).__init__(message.format(number_of_columns, row_that_has_too_many_columns))

