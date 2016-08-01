#!/usr/bin/python3

# board.py

class Board():
	'Class for handling the board state. This class is ignorant of game logic rules.'

	def __init__(self):
		'Creates a blank 9x9 board and sets the current display_method.'
		pass

	def get_board(self):
		'Returns the current board.'
		pass

	def get_cell(self, row: int, column: int):
		'Returns the value of a cell.'
		pass

	def get_row(self, row: int):
		'Returns the values of a row.'
		pass

	def get_column(self, column: int):
		'Returns the values of a column.'
		pass

	def get_box(self, row: int, column: int):
		'Returns the values of the 3x3 box that the given cell is a member of.'
		pass

	def add(self, row: int, column: int, number):
		'Changes the value of a cell to a certain number.'
		pass

	def clear(self, row: int, column: int):
		'Clears the given cell and returns the number that was there.'
		pass

	def to_csv(self, filename):
		'Saves board to a csv file format at the given filename.'
		pass

	def read_csv(self, filename):
		'Loads board from the csv file at the given filename.'
		pass

	def print_board(self):
		'Prints the board.'
		pass

	def display_board(self, display_method):
		'Displays the board, defaulting to the current display method.'
		pass

	def set_display_method(self, display_method):
		'Sets the current display method.'
		pass

	def _box_indices(self, row: int, column: int):
		'Returns the indices for all the members of the given 3x3 box.'
		pass
