# sudoku_button.py

import tkinter
import gameexceptions

# text that buttons show when there is no entry at the moment
_EMPTY_TEXT = '  '
_DEFAULT_BUTTON_COLOR = '#d9d9d9'
_DISABLED_BUTTON_COLOR = '#a9a9a9'
_BLACK = '#000000'

class SudokuButton(tkinter.Button):
	def __init__(self, *args, **kwargs):
		'''
		Same init as tkinter.Button, but also requires 'row' and 'column'
		keyword arguments.
		'''
		# set the row and column
		self._row = kwargs.pop('row')
		self._column = kwargs.pop('column')
		# inherit from tkinter.Button
		super().__init__(*args, **kwargs)
		# set button color to default
		self.set_color(_DEFAULT_BUTTON_COLOR)
		# set text color when button is disabled
		self.config(disabledforeground=_BLACK)
		# this variable tracks what color the button should be when it's not highlighted
		self._base_button_color = _DEFAULT_BUTTON_COLOR
		# set up the button text
		self._button_text = tkinter.StringVar()
		self._button_text.set(_EMPTY_TEXT)
		self.config(textvariable=self._button_text)
		# initialize the number
		self._number = 0
		# initialize superlock
		self._superlocked = False

	def get_coords(self):
		return (self._row, self._column)

	def get_row(self):
		return self._row

	def get_column(self):
		return self._column

	def get_number(self):
		return self._number

	def set_number(self, new_number):
		new_number = int(new_number)
		if not 1 <= new_number <= 9:
			raise gameexceptions.InvalidEntryException(new_number)
		self._number = new_number
		self.update_text()

	def set_color(self, color):
		'''Temporarily sets the button to a certain color. 
		Does not change the base button color'''
		self.config(bg=color)

	def highlight(self, color):
		self.set_color(color)

	def dehighlight(self):
		self.set_color(self._base_button_color)

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
		if not self._superlocked:
			self.config(state=tkinter.DISABLED)
			self.set_color(_DISABLED_BUTTON_COLOR)
			self._base_button_color = _DISABLED_BUTTON_COLOR


	def superlock(self):
		'''Permanently locks down this button. Be careful!
		Used for setting down the inital board state.'''
		self.lock()
		self._superlocked = True

	def unlock(self):
		"Undoes a lock unless it's a superlock"
		if not self._superlocked:
			self.config(state=tkinter.NORMAL)
			self.set_color(_DEFAULT_BUTTON_COLOR)			
			self._base_button_color = _DEFAULT_BUTTON_COLOR

	def toggle_lock(self):
		'Toggles the status of the lock, doing nothing in the case of superlocks'
		if self.is_locked():
			self.unlock()
		else:
			self.lock()

	def get_state(self):
		return self.cget('state')

	def is_locked(self):
		return self.get_state() == 'disabled'