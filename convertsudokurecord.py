# convertsudokurecord.py

# Converts a .txt file into one or more game state .csv files that the system can recognize

# "python3 convertsudokurecord.py {text file input} [{destination folder}]"

import sys
import os
import board

class CellCounter():
	def __init__(self):
		self.row = 0
		self.column = 0

	def increment(self):
		if self.row + 1 >= 9:
			self.column += 1
			self.row = 0
		else:
			self.row += 1

if __name__ == '__main__':
	if len(sys.argv) == 3:
		destination = sys.argv[2]
	elif len(sys.argv) == 2:
		destination = 'sudoku_states'
	file_path = sys.argv[1]
	file_name = os.path.basename(file_path)
	file_prefix = file_name.split('.')[0] # the identifier for the pack
	with open(file_path, 'r', encoding='utf-8') as read_file:
		for index, line in enumerate(read_file):
			assert len(line) == 82 # 81 entries + \n
			cell_counter = CellCounter()
			sudoku_board = board.Board()
			for character in line:
				if character != '0' and character != '\n':
					sudoku_board.add(cell_counter.row, cell_counter.column, int(character))
				cell_counter.increment()
			output_file_name = file_prefix + '_{:05d}.csv'.format(index)
			sudoku_board.to_csv(os.path.join(destination, output_file_name))

	# add the current pack to the packlist and then reduce duplicates
	current_packs = []
	try:
		with open('sudokupacklist.txt', 'r', encoding='utf-8') as packlist_file:
			current_packs = packlist_file.readlines()
			print(current_packs)
	except FileNotFoundError:
		pass
	current_packs.append(file_prefix)
	current_packs = set(current_packs)

	# write the new packlist
	with open('sudokupacklist.txt', 'w', encoding='utf-8') as packlist_file:
		for pack in current_packs:
			packlist_file.write(pack + '\n')

