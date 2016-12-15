#!/usr/bin/python3

# board.py

import csv

class Board():
	'''
	Class for handling the board state. This class is ignorant of game logic rules.
		
	Board dimensions are 9x9.

	Empty cells are represented as the integer "0" and filled cells are represented
		as their respective integers ("1" through "9").
	'''

	def __init__(self):
		'Creates a blank 9x9 board and sets the current display_method.'
		self._board = [[0 for i in range(9)] for j in range(9)]
		self.set_display_method('print')

	def get_board(self):
		'Returns the current board.'
		return self._board

	def get_cell(self, row: int, column: int):
		'Returns the value of a cell.'
		return self.get_board()[row][column]

	def get_row(self, row: int):
		'Returns the values of a row.'
		return self.get_board()[row]

	def get_column(self, column: int):
		'Returns the values of a column.'
		return [self.get_board()[row][column] for row in range(9)]

	def get_box(self, row: int, column: int):
		'Returns the values of the 3x3 box that the given cell is a member of.'
		value_list = []
		for box_row, box_column in self._box_indices(row, column):
			value_list.append(self.get_cell(box_row, box_column))
		return value_list

	def add(self, row: int, column: int, number):
		'Changes the value of a cell to a certain number.'
		self._board[row][column] = number

	def clear(self, row: int, column: int):
		'Clears the given cell and returns the number that was there.'
		number = self.get_cell(row, column)
		self._board[row][column] = 0
		return number

	def to_csv(self, filename):
		'Saves board to a csv file format at the given filename.'
		with open(filename, 'w') as write_file:
			writer = csv.writer(write_file, delimiter=',')
			for row in self._board:
				writer.writerow(row)

	def read_csv(self, filename):
		'Loads board from the csv file at the given filename.'
		with open(filename, 'r') as read_file:
			reader = csv.reader(read_file, delimiter=',')
			new_board = []
			for row in reader:
				row_list = []
				for cell in row:
					row_list.append(int(cell))
				new_board.append(row_list)
		self.set_board(new_board)


	def print_board(self):
		'Prints the board.'
		for index, row in enumerate(self.get_board()):
			if index % 3 == 0:
				print('-' * 25)
			row_list = []
			for i in range(9):
				if i % 3 == 0:
					row_list.append('|')
				else:
					pass
				if row[i] == 0:
					row_list.append(' ')
				else:
					row_list.append(row[i])
			row_list.append('|')
			print(' '.join(map(str, row_list)))
		print('-' * 25)

	def display_board(self):
		'Displays the board according to the current display method.'
		self._display_method()

	def set_display_method(self, display_method):
		'Sets the current display method.'
		if display_method == 'print':
			self._display_method = self.print_board
		else:
			raise Exception

	def set_board(self, board):
		'Sets the current board to the given board.'
		assert len(board) == 9
		for row_index in range(9):
			assert len(board[row_index]) == 9
		self._board = board

	def _box_indices(self, row: int, column: int):
		'Returns the indices for all the members of the given 3x3 box.'
		index_list = []
		first_row = (row // 3) * 3
		first_column = (column // 3) * 3
		for i in range(first_row, first_row + 3):
			for j in range(first_column, first_column + 3):
				index_list.append((i, j))
		return index_list
