#!/usr/bin/python3

# test_board.py
# TODO: unit test permanency

import unittest
import board
import os

empty_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0, 0, 0],
			   [0, 0, 0, 0, 0, 0, 0, 0, 0]]

full_board = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
			  [4, 5, 6, 7, 8, 9, 1, 2, 3],
			  [7, 8, 9, 1, 2, 3, 4, 5, 6],
			  [2, 3, 4, 5, 6, 7, 8, 9, 1],
			  [5, 6, 7, 8, 9, 1, 2, 3, 4],
			  [8, 9, 1, 2, 3, 4, 5, 6, 7],
			  [3, 4, 5, 6, 7, 8, 9, 1, 2],
			  [6, 7, 8, 9, 1, 2, 3, 4, 5],
			  [9, 1, 2, 3, 4, 5, 6, 7, 8]]

incomplete_board = [[4, 2, 0, 0, 0, 0, 0, 7, 3],
 					[1, 3, 0, 6, 7, 2, 0, 0, 0],
 					[0, 0, 0, 3, 0, 0, 0, 8, 0],
 					[0, 0, 0, 4, 1, 0, 3, 0, 9],
 					[7, 1, 6, 8, 3, 0, 0, 0, 0],
 					[0, 9, 0, 0, 0, 0, 7, 0, 0],
 					[2, 7, 3, 1, 6, 8, 5, 9, 0],
 					[0, 8, 0, 0, 0, 3, 0, 2, 0],
 					[0, 0, 1, 9, 0, 0, 8, 0, 0]]



class BasicBoardTestCase(unittest.TestCase):
	def test_init(self):
		test_board = board.Board()
		self.assertEqual(test_board._board, empty_board)

	def test_get_board(self):
		test_board = board.Board()
		self.assertEqual(test_board._board, test_board.get_board())
		self.assertEqual(test_board.get_board(), empty_board)

	def test_set_board(self):
		test_board = board.Board()
		test_board.set_board(empty_board)
		self.assertEqual(test_board.get_board(), empty_board)

		test_board.set_board(full_board)
		self.assertEqual(test_board.get_board(), full_board)

		test_board.set_board(incomplete_board)
		self.assertEqual(test_board.get_board(), incomplete_board)


class AdvancedBoardTestCase(unittest.TestCase):
	def setUp(self):
		self.test_board = board.Board()
		self.test_board2 = board.Board()
		self.test_board2.set_board(full_board)
		self.test_board3 = board.Board()
		self.test_board3.set_board(incomplete_board)
		self.test_boards = [self.test_board, self.test_board2, self.test_board3]

	def test_get_cell(self):
		for a_board in self.test_boards:
			for row in range(9):
				for column in range(9):
					self.assertEqual(a_board.get_cell(row, column), 
									a_board.get_board()[row][column])

	def test_get_row(self):
		for a_board in self.test_boards:
			for row in range(9):
				self.assertEqual(a_board.get_row(row), a_board.get_board()[row])

	def test_get_column(self):
		for a_board in self.test_boards:
			for column in range(9):
				self.assertEqual(a_board.get_column(column), 
								[a_board.get_board()[row][column] for row in range(9)])

	def test_box_indices(self):
		box0_indices = [(0,0), (0,1), (0,2),
						(1,0), (1,1), (1,2),
						(2,0), (2,1), (2,2)]
		box3_indices = [(0,6), (0,7), (0,8),
						(1,6), (1,7), (1,8),
						(2,6), (2,7), (2,8)]
		box8_indices = [(6,6), (6,7), (6,8),
						(7,6), (7,7), (7,8),
						(8,6), (8,7), (8,8)]
		for row in range(9):
			for column in range(9):
				if (row // 3 == 0) and (column // 3 == 0):
					self.assertEqual(self.test_board._box_indices(row, column), box0_indices)
				if (row // 3 == 0) and (column // 3 == 2):
					self.assertEqual(self.test_board._box_indices(row, column), box3_indices)
				if (row // 3 == 2) and (column // 3 == 2):
					self.assertEqual(self.test_board._box_indices(row, column), box8_indices)

	def test_get_box(self):
		for row in range(9):
			for column in range(9):
				self.assertEqual(self.test_board.get_box(row, column), [0 for i in range(9)])
		for row in range(3):
			for column in range(3):
				self.assertEqual(self.test_board2.get_box(row, column), [1,2,3,4,5,6,7,8,9])
		for row in range(6,9):
			for column in range(3):
				self.assertEqual(self.test_board2.get_box(row, column), [3,4,5,6,7,8,9,1,2])
		for row in range(3):
			for column in range(6, 9):
				self.assertEqual(self.test_board3.get_box(row, column), [0,7,3,0,0,0,0,8,0])

	def test_add(self):
		self.test_board.add(0, 0, 1)
		for row in range(9):
			for column in range(9):
				if (row, column) == (0, 0):
					self.assertEqual(self.test_board.get_cell(row, column), 1)
				else:
					self.assertEqual(self.test_board.get_cell(row, column), 0)

		self.test_board.add(0, 0, 2)
		for row in range(9):
			for column in range(9):
				if (row, column) == (0, 0):
					self.assertEqual(self.test_board.get_cell(row, column), 2)
				else:
					self.assertEqual(self.test_board.get_cell(row, column), 0)

		for row in range(9):
			for column in range(9):
				self.test_board.add(row, column, full_board[row][column])
		self.assertEqual(self.test_board.get_board(), full_board)

	def test_clear(self):
		self.test_board.add(0, 0, 1)
		self.test_board.clear(0, 0)
		self.assertEqual(self.test_board.get_board(), empty_board)

		self.test_board2.clear(5, 7)
		for row in range(9):
			for column in range(9):
				if (row, column) == (5, 7):
					self.assertEqual(self.test_board2.get_cell(row, column), 0)
				else:
					self.assertEqual(self.test_board2.get_cell(row, column), full_board[row][column])

	def test_to_csv(self):
		self.test_board.to_csv('test_board.csv')
		self.test_board2.to_csv('test_board2.csv')
		self.test_board3.to_csv('test_board3.csv')

		with open('test_board.csv', 'r') as file:
			text = file.readlines()
			self.assertEqual(len(text), 9)
			for row_number, row in enumerate(text):
				self.assertEqual(row, ','.join(map(str, empty_board[row_number])) + '\n')

		with open('test_board2.csv', 'r') as file:
			text = file.readlines()
			self.assertEqual(len(text), 9)
			for row_number, row in enumerate(text):
				self.assertEqual(row, ','.join(map(str, full_board[row_number])) + '\n')

		with open('test_board3.csv', 'r') as file:
			text = file.readlines()
			self.assertEqual(len(text), 9)
			for row_number, row in enumerate(text):
				self.assertEqual(row, ','.join(map(str, incomplete_board[row_number])) + '\n')

		os.remove('test_board.csv')
		os.remove('test_board2.csv')
		os.remove('test_board3.csv')

	def test_read_csv(self):
		self.test_board.to_csv('test_board.csv')
		self.test_board2.to_csv('test_board2.csv')
		self.test_board3.to_csv('test_board3.csv')
		test_board_a = board.Board()
		test_board_a.read_csv('test_board.csv')
		test_board_b = board.Board()
		test_board_b.read_csv('test_board2.csv')
		test_board_c = board.Board()
		test_board_c.read_csv('test_board3.csv')
		self.assertEqual(self.test_board.get_board(), test_board_a.get_board())
		self.assertEqual(self.test_board2.get_board(), test_board_b.get_board())
		self.assertEqual(self.test_board3.get_board(), test_board_c.get_board())
		os.remove('test_board.csv')
		os.remove('test_board2.csv')
		os.remove('test_board3.csv')


if __name__ == '__main__':
		unittest.main()