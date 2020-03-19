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
		self.jumps = 0
		self.active = True

	def new_game(self):
		self.grid = [[None] * i for i in range(1,self.rows + 1)]
		return self.grid

	def populate_grid(self):
		for row_index,row in enumerate(self.grid):
			for column_index,column in enumerate(row):
				#self.pawns.append(str(row_index) + str(column_index))
				self.grid[row_index][column_index] = Pawn(str(row_index) + str(column_index))
				
	def remove_pawn(self,row,column):
		if row >= len(self.grid) or column >= len(self.grid[row]):
			return None

		# First move lets you remove any piece regardless
		if self.moves < 1 or self.grid[row][column]:
			self.grid[row][column] = None

		else:
			print("Invalid")
			return False
		
		self.moves += 1
		self.pawn_count -= 1
		self.show_grid()
		return self.grid

	def show_grid(self):
		spaces_list = [12,9,6,3,0]
		for row_index,row in enumerate(self.grid):
			spaces = " " * (spaces_list[row_index]) #Amt of spaces vary for each row
			print("\t\t" + spaces , end=" ")
			for column_index,column in enumerate(row):
				if self.grid[row_index][column_index]: 
					print(self.grid[row_index][column_index].location , end="    ")
				else:
					print("--" , end= "    ")
			print("\n")

	def validate_jump(self,pawn_location,empty_location):
		jumped_pawn = str(int(int(pawn_location) + ((int(empty_location) - int(pawn_location)) / 2))) # The math for determining jumped cell location given old and new cell locations
		
		# Can't jump if new cell is occupied or jumped cell is empty or cell difference isnt 2 20 22
		if self.grid[int(empty_location[0])][int(empty_location[1])] or self.grid[int(jumped_pawn[0])][int(jumped_pawn[1])] == None or abs(int(empty_location) - int(pawn_location)) not in [2,20,22]: 
			print("Invalid Move")
		else:
			self.grid[int(empty_location[0])][int(empty_location[1])] = self.grid[int(pawn_location[0])][int(pawn_location[1])]
			self.grid[int(pawn_location[0])][int(pawn_location[1])] = None
			self.grid[int(empty_location[0])][int(empty_location[1])].location = empty_location[0] + empty_location[1]

			self.jumps += 1
			print("Jumped: {}".format(jumped_pawn))
			self.remove_pawn(int(jumped_pawn[0]),int(jumped_pawn[1]))
		return None

	def show_stats(self):
		print("Moves: {}\nJumps: {} \nPawn Count: {}\nPawns: ".format(self.moves,self.jumps,self.pawn_count))

	def show_moves(self,pawn_location):
		return []

	def exit(self):
		self.active = False
		print("Thanks for playing...")


def initiate_game():
	game = Game()
	game.populate_grid()
	game.show_grid()

	while game.active:
		if game.moves == 0:
			cell = input("Select Cell # to remove: ")
			game.remove_pawn(int(cell[0]),int(cell[1]))

		player_decision = input(">_: ")
		game_options = {
			'show': game.show_grid,
			'quit': game.exit,
			'move': game.validate_jump,
			'stats': game.show_stats 
		}
		
		args = player_decision.split(" ")
		if args[0] in game_options:
			if args[0] == 'move':
				game_options[args[0]](args[1],args[2]) if len(args) > 2 else print("Move needs two arguments: A pawn location and new location ")
			elif args[0] == 'help':
				pass
			else:
				game_options[args[0]]()
def main():
	initiate_game()

if __name__ == '__main__':
	main()
