#!/usr/bin/python3

#test_sudokugame.py

import unittest
import sudokugame
import board

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
		test_board = board.Board()
		test_board.set_board(full_board)
		test_board.to_csv('save_state.csv')
		game = sudokugame.Game()
		game.load_state('save_state')
		self.assertEqual(game.get_board(), full_board)
		test_board.set_board(incomplete_board)
		test_board.to_csv('save_state2.csv')
		game.load_state('save_state2')
		self.assertEqual(game.get_board(), incomplete_board)
