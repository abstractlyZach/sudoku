# sudoku_button.py

import tkinter

# text that buttons show when there is no entry at the moment
_EMPTY_TEXT = '  '
_DEFAULT_BUTTON_COLOR = '#d9d9d9'
_DISABLED_BUTTON_COLOR = '#a9a9a9'

class SudokuButton(tkinter.Button):
	def __init__(self, *args, **kwargs):
		# inherit from tkinter.Button
		super().__init__(*args, **kwargs)
		# set button color to default
		self.config(bg=_DEFAULT_BUTTON_COLOR)
		# set up the button text
		self._button_text = tkinter.StringVar()
		self._button_text.set(_EMPTY_TEXT)
		self.config(textvariable=self._button_text)
		# initialize the number
		self._number = 0

	def get_coords(self):
		return (self._row, self._column)

	def get_row(self):
		return self._row

	def get_column(self):
		return self._column

	def get_number(self):
		return self._number

	def increment(self):
		self._number += 1
		if self._number >= 10:
			self._number = 1
		self.update_text()

	def clear(self):
		self._number = 0
		self.update_text()

	def update_text(self):
		if self._number == 0:
			self._button_text.set(_EMPTY_TEXT)
		else:
			self._button_text.set(str(self._number))

	def lock(self):
		'Grays out and disables the button'
		self.config(state=tkinter.DISABLED)
		self.config(bg=_DISABLED_BUTTON_COLOR)

	def unlock(self):
		self.config(state=tkinter.NORMAL)
		self.config(bg=_DEFAULT_BUTTON_COLOR)

	def get_state(self):
		return self.cget('state')

	def is_locked(self):
		return self.get_state() == 'disabled'