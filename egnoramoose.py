class Pawn:
	def __init__(self,location):
		self.location = location

class Game:
	grid = []
	rows = 5

	def __init__(self):
		self.pawn_count = 15
		self.grid = self.new_game()
		self.moves = 0
		self.active = True

	def new_game(self):
		self.grid = [[None] * i for i in range(1,self.rows + 1)]
		return self.grid

	def populate_grid(self):
		for row_index,row in enumerate(self.grid):
			for column_index,column in enumerate(row):
				self.grid[row_index][column_index] = Pawn(str(row_index) + str(column_index))
				
	def remove_pawn(self,row,column):
		# First move lets you remove any piece regardless
		if self.moves < 1:
			self.grid[row][column] = None

		else:
			if self.grid[row][column]:
				self.grid[row][column] = None
			else:
				print("[{}][{}] filled".format(row,column))
				return False
		
		self.moves += 1
		return self.grid

	def show_grid(self):
		spaces_list = [12,9,6,3,0]
		for row_index,row in enumerate(self.grid):
			spaces = " " * (spaces_list[row_index])
			print(spaces , end="")
			for column_index,column in enumerate(row):

				if self.grid[row_index][column_index]: 
					print(self.grid[row_index][column_index].location , end="    ")
				else:
					print("--" , end= "    ")
			print("\n")

	def validate_jump(self,pawn_location,empty_location):
		pass

	def exit(self):
		self.active = False
		print("Thanks for playing...")

def main():
	game = Game()
	print(game)

	game.populate_grid()
	game.show_grid()

	while game.active:
		player_decision = input(">_: ")
		
		game_options = {
			'show': game.show_grid,
			'quit': game.exit,
			'move': game.validate_jump 
		}
		
		args = player_decision.split(" ")
		if args[0] in game_options:
			if args[0] == 'move':
				game_options[args[0]](args[1],args[2]) if len(args) > 2 else print("Move needs two arguments: A pawn location and new location ")
			elif args[0] == 'help':
				pass
			else:
				game_options[player_decision]()

if __name__ == '__main__':
	main()
