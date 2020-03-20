class Pawn:
    pass


class Location:
    def __init__(self, *location):
        self.row = -1
        self.column = -1
        self._convert(location)

    def __sub__(self, other):
        return Location(self.row-other.row, self.column-other.column)

    def __str__(self):
        return '{}{}'.format(self.row, self.column)

    @staticmethod
    def _list_to_int(list_obj):
        return [int(i) for i in list_obj]

    def _convert(self, location):
        if len(location) == 1:
            location_str = location[0]
            assert len(location_str) == 2
            self.row, self.column = Location._list_to_int(location_str)
        elif len(location) == 2:
            for arg in location:
                if isinstance(arg, str):
                    assert len(arg) == 1
            self.row, self.column = Location._list_to_int(location)

    @property
    def location(self):
        return (self.row, self.column)


class Game:
    VALID_JUMP_DIFFERENCES = [(0, 2), (2, 0), (2, 2)]
    rows = 5

    def __init__(self):
        self.pawn_count = 15
        self.moves = 0
        self.active = True
        self.grid = Game._create_grid()
        self.display_char = ' '
        self.cell_size = 2
        self.cell_gap_size = self.cell_size*2
        self.cell_center_offset = int((self.cell_gap_size - self.cell_size)/2)
        self.gap_display = self.display_char*self.cell_gap_size
        self.game_shift_size = 2
        self.game_shift_char = '\t'

    @classmethod
    def _create_grid(cls):
        return [[Pawn()]*i for i in range(1, cls.rows+1)]

    def remove_pawn(self, row, column):
        cell_location = Location(row, column)
        if not self._is_removable(cell_location):
            print("Invalid")
            return
        self._remove(cell_location)

    def _is_removable(self, cell_location):
        return self._is_location_on_board(cell_location) and \
            not self._is_occupied(cell_location)

    def _is_location_on_board(self, location):
        return (location.row < len(self.grid)) and \
            (location.column < len(self.grid[location.row]))

    def _remove(self, cell_location):
        self.grid[cell_location.row][cell_location.column] = None
        self.moves += 1
        self.pawn_count -= 1

    def move(self, src, dest):
        print('Src {} Dest {}'.format(src, dest))
        src_location, dest_location = Location(src), Location(dest)
        if not self._is_move_possible(src_location, dest_location):
            print("Invalid Move")
            return
        self._move(src_location, dest_location)

    def _is_move_possible(self, src_location, dest_location):
        jumped_location = self._get_jumped_location(
            src_location, dest_location)
        return self._is_move_valid(src_location, dest_location) and \
            not self._is_occupied(dest_location) and \
            self._is_occupied(jumped_location)

    def _get_jumped_location(self, src_location, dest_location):
        jumped_row = int((src_location.row + dest_location.row) / 2)
        jumped_column = int((src_location.column + dest_location.column) / 2)
        return Location(jumped_row, jumped_column)

    def _is_move_valid(self, src_location, dest_location):
        diff_location = dest_location - src_location
        return (abs(diff_location.row), abs(diff_location.column)) in Game.VALID_JUMP_DIFFERENCES

    def _move(self, src_location, dest_location):
        self.grid[dest_location.row][dest_location.column] = Pawn()
        self.grid[src_location.row][src_location.column] = None

    def show_grid(self):
        for row_index in range(len(self.grid)):
            print("{}{}".format(
                self.game_shift_char*self.game_shift_size,
                self._get_row_display(row_index)))

    def _get_row_display(self, row_index):
        cell_diff = len(self.grid) - (row_index + 1)
        left_adjusted_display = self.display_char * \
            (self.cell_center_offset + self.cell_size) * cell_diff
        row_display = ""
        for column_index in range(row_index+1):
            loc = Location(row_index, column_index)
            row_display += str(loc) if self._is_occupied(loc) else "--"
            row_display += self.gap_display if column_index < row_index else ""
        return left_adjusted_display + row_display + "\n"

    def _is_occupied(self, cell_location):
        return bool(self.grid[cell_location.row][cell_location.column])

    def show_stats(self):
        print("Moves: {}\nPawn Count: {}".format(self.moves, self.pawn_count))

    def show_moves(self, pawn_location):
        return []

    def exit(self):
        self.active = False
        print("Thanks for playing...")


def initiate_game():
    game = Game()
    game_options = {
        'quit': game.exit,
        'move': game.move,
        'stats': game.show_stats
    }

    game.show_grid()
    while game.active:
        if game.moves == 0:
            cell = input("Select Cell # to remove: ")
            game.remove_pawn(int(cell[0]), int(cell[1]))

        game.show_grid()
        player_decision = input(">_: ")

        args = player_decision.split(" ")
        if args[0] not in game_options:
            continue

        if args[0] == 'move':
            if len(args) > 2:
                game_options[args[0]](args[1], args[2])
            else:
                print("Move needs two arguments: A pawn location and new location ")
        elif args[0] == 'help':
            pass
        else:
            game_options[player_decision]()


def main():
    initiate_game()


if __name__ == '__main__':
    main()
