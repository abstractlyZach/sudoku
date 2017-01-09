# sudoku_gui.py

import tkinter

DEFAULT_FONT = ('Helvetica', 20)
ALL_SIDES = tkinter.N + tkinter.S + tkinter.E + tkinter.W

class SudokuApplication:
	def __init__(self):
		# text that goes in the sidebar
		self._sidebar_text = ''
		self._create_main_window()

	def _create_main_window(self):
		# main window
		self._root_window = tkinter.Tk()

		# title text (row 0, column 0)
		self._create_title()

		# sidebar (row 0-1, column 1)
		self._create_sidebar()

		# board (row 1, column 0)
		self._create_board_view()

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
			anchor=tkinter.N) 
		self._sidebar.grid(row=0, column=1, padx=10, pady=15, rowspan=2, sticky=ALL_SIDES)

	def _create_board_view(self):
		# sudoku board view
		self._board_frame = tkinter.Frame(master=self._root_window, background='#FFFFFF')
		self._board_frame.grid(row=1, column=0, padx=10, pady=10, sticky=ALL_SIDES)

		# boxes
		for row in range(3):
			for column in range(3):
				self._create_box(row, column)

		# for row in range(9):
		# 	for column in range(9):
		# 		cell = tkinter.Button(master=self._board_frame, 
		# 			text='{}, {}'.format(row, column),
		# 			font=DEFAULT_FONT)
		# 		cell.grid(row=row, column=column, sticky=ALL_SIDES)

		# # board row configuration
		# for row in range(9):
		# 	self._board_frame.rowconfigure(row, weight=1)

		# # board column configuration
		# for column in range(9):
		# 	self._board_frame.columnconfigure(column, weight=1)

	def _create_box(self, board_row, board_column):
		# coords of the first cell in the box
		first_row = board_row * 3
		first_column = board_column * 3
		box = tkinter.Frame(master=self._board_frame, background='#000000')
		box.grid(row=board_row, column=board_column, padx=20, pady=20, sticky=ALL_SIDES)
		for row in range(3):
			for column in range(3):
				cell = tkinter.Button(master=box, 
					text='{}, {}'.format(first_row + row, first_column + column))
				cell.grid(row=row, column=column, sticky=ALL_SIDES)


	def run(self):
		self._root_window.mainloop()

if __name__ == '__main__':
	SudokuApplication().run()
