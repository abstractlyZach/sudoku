# gameactions.py

# Objects that carry details of each move as well as information from the cell before the move.

class GameAction:
	def get_coordinates(self):
		return self._row, self._column

	def get_old_number(self):
		return self._old_number

	def get_new_number(self):
		return self._new_number

	def __eq__(self, other_action):
		equivalent = True
		equivalent = equivalent and (type(self) == type(other_action))
		equivalent = equivalent and (self.get_coordinates() == other_action.get_coordinates())
		equivalent = equivalent and (self.get_old_number() == other_action.get_old_number())
		equivalent = equivalent and (self.get_new_number() == other_action.get_new_number())
		return equivalent

class AddAction(GameAction):
	def __init__(self, row, column, number):
		self._row = row
		self._column = column
		self._old_number = 0 # can only create an AddAction if the cell is empty
		self._new_number = number 

class RemoveAction(GameAction):
	def __init__(self, row, column, old_number):
		self._row = row
		self._column = column
		self._old_number = old_number
		self._new_number = 0 # RemoveAction always clears the cell


class ChangeAction(GameAction):
	def __init__(self, row, column, new_number, old_number):
		self._row = row
		self._column = column
		self._old_number = old_number
		self._new_number = new_number

