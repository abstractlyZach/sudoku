# sudoku_gui.py

import tkinter
import sudoku_button
import sudokugame
import board
import gameexceptions

DEFAULT_FONT = ('Helvetica', 20)
ALL_SIDES = tkinter.N + tkinter.S + tkinter.E + tkinter.W
_ERROR_HIGHLIGHT_COLOR = '#FF0000'

class SudokuApplication:
	def __init__(self, game=sudokugame.Game()):
		# game model
		self._game = game

		# container for accessing buttons. 2-D array
		self._buttons = [[None for i in range(9)] for i in range(9)]

		# main window
		self._root_window = tkinter.Tk()

		# set lock mode
		self._lock_mode = False
		
		# text that goes in the sidebar
		self._sidebar_text = tkinter.StringVar(master=self._root_window)

		self._create_main_window()
		self.write_to_sidebar("Press 'a' to turn lock mode on/off.")

		self._root_window.bind("a", self._toggle_lock_mode)

		self.load_game('0_00000')
		# self.load_game('almost_complete')

	def _create_main_window(self):
		# title text (row 0, column 0)
		self._create_title()

		# sidebar (row 0-1, column 1)
		self._create_sidebar()

		# board (row 1, column 0)
		self._create_board_view()

		# button dock (row 2, column 0)
		self._create_button_dock()

		self._mode_text = tkinter.StringVar(master=self._root_window)
		self._mode_label = tkinter.Label(master=self._root_window, 
			textvariable=self._mode_text)
		self._mode_label.grid(row=3, column=0, padx=10, pady=10, 
			sticky=tkinter.S + tkinter.W)

		# main window row configuration
		self._root_window.rowconfigure(0, weight=0)
		self._root_window.rowconfigure(1, weight=1)

		# main window column configuration
		self._root_window.columnconfigure(0, weight=1)
		self._root_window.columnconfigure(1, weight=0)

	def _create_title(self):
		self._top_text_box = tkinter.Label(master=self._root_window, font=DEFAULT_FONT, 
			text='SUDOKUUUUUU')
		self._top_text_box.grid(row=0, column=0, padx=10, pady=10,
			sticky=tkinter.N+tkinter.S)	

	def _create_sidebar(self):
		self._sidebar = tkinter.Label(master=self._root_window, 
			font=('Times New Roman', 15), textvariable=self._sidebar_text,
			background='#FFFFFF', width=40, wraplength=400, 
							# wraplength 400 is really 40. idk why.
							# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/label.html
			# anchors the text to the top of the widget
			anchor=tkinter.N + tkinter.W) 
		self._sidebar.grid(row=0, column=1, padx=10, pady=15, rowspan=2, sticky=ALL_SIDES)

	def _create_board_view(self):
		# sudoku board view
		self._board_frame = tkinter.Frame(master=self._root_window, background='#000000')
		self._board_frame.grid(row=1, column=0, padx=10, pady=10, sticky=ALL_SIDES)

		# boxes
		for row in range(3):
			for column in range(3):
				self._create_box(row, column)

		# box grid configuration
		for row in range(3):
			self._board_frame.rowconfigure(row, weight=1)
		for column in range(3):
			self._board_frame.columnconfigure(column, weight=1)


	def _create_box(self, board_row, board_column):
		# coords of the first cell in the box
		first_row = board_row * 3
		first_column = board_column * 3
		# box divider thickness
		box_pad = 1

		# set up the buttons
		box = tkinter.Frame(master=self._board_frame)
		box.grid(row=board_row, column=board_column, padx=box_pad, pady=box_pad, 
			sticky=ALL_SIDES)
		for row_in_box in range(3):
			for column_in_box in range(3):
				row = row_in_box + first_row
				column = column_in_box + first_column
				cell = sudoku_button.SudokuButton(master=box, row=row, column=column)
				cell.bind('<Button-1>', self._handle_left_click)
				cell.bind('<Button-3>', self._handle_right_click)
				# add row and column attributes to make the button into a useful object
				cell.grid(row=row_in_box, column=column_in_box, sticky=ALL_SIDES)
				# place the button into the button container
				self._buttons[row][column] = cell

				# set up the button according to the game model
				number = self._game.get_cell(row, column)
				if number == 0:
					cell.clear()
				else:
					cell.set_number(number)
				if self._game.is_permanent(row, column):
					cell.superlock()

		# configuration of this box
		for row_in_box in range(3):
			box.rowconfigure(row_in_box, weight=1)
		for column_in_box in range(3):
			box.columnconfigure(column_in_box, weight=1)

	def _create_button_dock(self):
		self._button_dock = tkinter.Frame(master=self._root_window)
		self._button_dock.grid(row=2, column=0, padx=20, pady=20, sticky=ALL_SIDES, 
			columnspan=2)

		# save button
		save_button = tkinter.Button(master=self._button_dock,
			text='Save', 
			command=self._save_to_default)
		save_button.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.W)

		# load button
		load_button = tkinter.Button(master=self._button_dock, 
			text='Load',
			command=self._load_from_default)
		load_button.grid(row=0, column=1, padx=10, pady=10, sticky=tkinter.E)

		# clear button
		clear_button = tkinter.Button(master=self._button_dock,
			text='Clear',
			command=self._clear_board)
		clear_button.grid(row=0, column=2, padx=10, pady=10)
		# should add an "are you sure?" dialog

		# undo button
		undo_button = tkinter.Button(master=self._button_dock,
			text='Undo',
			command=self._undo)
		undo_button.grid(row=0, column=3, padx=10, pady=10)

		# redo button
		redo_button = tkinter.Button(master=self._button_dock,
			text='Redo',
			command=self._redo)
		redo_button.grid(row=0, column=4, padx=10, pady=10)

	def _save_to_default(self):
		self._game.save_state()

	def _load_from_default(self):
		self.load_game()

	def _clear_board(self):
		'Clears the board except for the original numbers'
		self._game.reset()
		# self._board_frame.destroy()
		self._create_board_view()
		self.refresh_borders()

	def _undo(self):
		action = self._game.undo_move()
		row, column = action.get_coordinates()
		old_number = action.get_old_number()
		if old_number == 0:
			self.get_button(row, column).clear()
		else:
			self.get_button(row, column).set_number(old_number)
		self.refresh_borders()

	def _redo(self):
		action = self._game.redo_move()
		row, column = action.get_coordinates()
		new_number = action.get_new_number()
		if new_number == 0:
			self.get_button(row, column).clear()
		else:
			self.get_button(row, column).set_number(new_number)
		self.refresh_borders()

	def _handle_left_click(self, button_press_event):
		button = button_press_event.widget
		if self._lock_mode:
			button.toggle_lock()
		else:
			if not button.is_locked():
				button.increment()
				row, column = button.get_coords()
				number = button.get_number()
				self._game.force_change(row, column, number)
				self.refresh_borders()

				# check victory condition
				if self._game.check_victory():
					string_append(self._sidebar_text, 'You win!\n')
					for row in range(9):
						self.highlight_row(row, '#00FF00')

	def _handle_right_click(self, button_press_event):
		button = button_press_event.widget
		if not button.is_locked():
			button.clear()
			row, column = button.get_coords()
			self._game.remove(row, column)
			self.refresh_borders()

	def _toggle_lock_mode(self, key_press_event):
		"Allows a user to change the lock state of cells unless they're superlocked"
		self._lock_mode = not self._lock_mode
		if self._lock_mode:
			self._mode_text.set("lock mode")
		else:
			self._mode_text.set("")

	def load_game(self, state_name=None):
		'''Loads a save state and its permanency data. Every cell marked permanent 
		gets superlocked on the GUI'''
		if state_name == None:
			self._game.load_state()
		else:
			self._game.load_state(state_name)
		# self._board_frame.destroy()
		self._create_board_view()
		self.refresh_borders()

	def get_button(self, row, column):
		return self._buttons[row][column]

	def highlight_row(self, row, color=_ERROR_HIGHLIGHT_COLOR):
		'Highlights a row of buttons'
		for button_index in range(9):
			button = self.get_button(row, button_index)
			button.highlight(color)

	def highlight_column(self, column, color=_ERROR_HIGHLIGHT_COLOR):
		'Highlights a column of buttons'
		for button_index in range(9):
			button = self.get_button(button_index, column)
			button.highlight(color)

	def highlight_box(self, row, column, color=_ERROR_HIGHLIGHT_COLOR):
		'Highlights the buttons that are in the same box'
		box_coords = board.Board.get_box_indices(None, row, column)
		for box_coord in box_coords:
			row, column = box_coord
			button = self.get_button(row, column)
			button.highlight(color)

	def clear_highlighting(self):
		'Clears highlighting for all buttons.'
		for row_index in range(9):
			for column_index in range(9):
				button = self.get_button(row_index, column_index)
				button.dehighlight()

	def border_row(self, row, color=_ERROR_HIGHLIGHT_COLOR):
		'Borders a row of buttons'
		for button_index in range(9):
			button = self.get_button(row, button_index)
			button.border(color, 1)

	def border_column(self, column, color=_ERROR_HIGHLIGHT_COLOR):
		'Highlights a column of buttons'
		for button_index in range(9):
			button = self.get_button(button_index, column)
			button.border(color, 1)

	def border_box(self, row, column, color=_ERROR_HIGHLIGHT_COLOR):
		'Highlights the buttons that are in the same box'
		box_coords = board.Board.get_box_indices(None, row, column)
		for box_coord in box_coords:
			row, column = box_coord
			button = self.get_button(row, column)
			button.border(color, 1)

	def clear_borders(self):
		'Removes borders for all buttons.'
		for row_index in range(9):
			for column_index in range(9):
				button = self.get_button(row_index, column_index)
				button.remove_border()

	def refresh_borders(self):
		'Clears highlighting and highlights the first problem it finds.'
		self.clear_borders()
		try:
			self._game.validate_board()
		except gameexceptions.SameRowException as e:
			self.border_row(e.row)
		except gameexceptions.SameColumnException as e:
			self.border_column(e.column)
		except gameexceptions.SameBoxException as e:
			self.border_box(*e.coord)

	def update_board_view(self):
		# TODO: figure out how to run AI code and display it through the GUI
		self.refresh_borders()

	def write_to_sidebar(self, text, end='\n'):
		'Adds a line of text to the sidebar'
		string_append(self._sidebar_text, text + end)

	def run(self):
		self._root_window.mainloop()


def string_append(string_var, text):
	'Takes a tkinter.StringVar and appends text to it.'
	string_var.set(string_var.get() + text)

if __name__ == '__main__':
	SudokuApplication().run()
