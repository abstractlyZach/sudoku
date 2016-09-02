#!/usr/bin/python3

#test_sudokugame.py

import unittest
import sudokugame
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
 					[1, 3, 0, 6, 7, 2, 0, 0, 0], #16
 					[0, 0, 0, 3, 0, 0, 0, 8, 0],
 					[0, 0, 0, 4, 1, 0, 3, 0, 9],#16
 					[7, 1, 6, 8, 3, 0, 0, 0, 0],
 					[0, 9, 0, 0, 0, 0, 7, 0, 0],#13
 					[2, 7, 3, 1, 6, 8, 5, 9, 0],
 					[0, 8, 0, 0, 0, 3, 0, 2, 0],
 					[0, 0, 1, 9, 0, 0, 8, 0, 0]] # 45 open cells

all_cells = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), 
			(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), 
			(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), 
			(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), 
			(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), 
			(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), 
			(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), 
			(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), 
			(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]

class BasicUtilitiesTestCase(unittest.TestCase):
	def test_init(self):
		game = sudokugame.Game()
		self.assertEqual(game._board.get_board(), empty_board)
		self.assertEqual(game._undo_stack, [])
		self.assertEqual(game._redo_stack, [])

	def test_get_board(self):
		game = sudokugame.Game()
		self.assertEqual(game.get_board(), empty_board)
		game._board.set_board(full_board)
		self.assertEqual(game.get_board(), full_board)
		game._board.set_board(incomplete_board)
		self.assertEqual(game.get_board(), incomplete_board)

	def test_load_state(self):
		game = sudokugame.Game()
		game.load_state('save_state2')
		self.assertEqual(game.get_board(), full_board)
		game.load_state('save_state3')
		self.assertEqual(game.get_board(), incomplete_board)


class AdvancedUtilitiesTestCase(unittest.TestCase):
	def setUp(self):
		self.game1 = sudokugame.Game()
		self.game2 = sudokugame.Game()
		self.game3 = sudokugame.Game()
		self.game1.load_state('save_state')
		self.game2.load_state('save_state2')
		self.game3.load_state('save_state3')

	def test_open_cells(self):
		open_cells = self.game1.open_cells()
		self.assertEqual(len(open_cells), 81)
		self.assertEqual(open_cells, all_cells)
		open_cells = self.game2.open_cells()
		self.assertEqual(len(open_cells), 0)
		self.assertEqual(open_cells, [])
		open_cells = self.game3.open_cells()
		self.assertEqual(len(open_cells), 45)

	


	
if __name__ == '__main__':	
	test_board = board.Board()
	test_board.to_csv('save_state.csv')
	test_board.set_board(full_board)
	test_board.to_csv('save_state2.csv')
	test_board.set_board(incomplete_board)
	test_board.to_csv('save_state3.csv')
	
	unittest.main()

	os.remove('save_state.csv')
	os.remove('save_state2.csv')
	os.remove('save_state3.csv')