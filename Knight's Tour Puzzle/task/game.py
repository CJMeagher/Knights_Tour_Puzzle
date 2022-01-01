import re
from collections import namedtuple

Cell = namedtuple("Cell", "row column")
Move = namedtuple("Move", "rows columns")


class Board:
    def __init__(self):
        self.visited_cells = dict()
        self.reachable_cells = set()
        self.current_cell = None
        self.rows = 0
        self.columns = 0
        self.start_cell = Cell(0, 0)
        self.cell_width = 0
        self.unvisited_cell = " _____"
        self.visited_cell = "     *"
        self.knights_cell = "     X"
        self.cell_formatter = lambda number, width: "".join(
            ["{", str(number), ":>", str(width), "}"]
        )
        self.border = ""
        self.column_footer = ""
        self.row_number_width = 0
        self.input_matcher = r"(\d+) (\d+)[ ]*$"
        self.moves = [
            Move(1, 2),
            Move(1, -2),
            Move(-1, 2),
            Move(-1, -2),
            Move(2, 1),
            Move(2, -1),
            Move(-2, 1),
            Move(-2, -1),
        ]
        self.user_solves = False
        self.board_solved = lambda: len(self.visited_cells) == self.rows * self.columns
        self.dead_end = lambda: len(self.reachable_cells) == 0
        self.reachable_cell_count = lambda cell: len(self.find_reachable_cells(cell))

    def run(self):
        self.user_sets_board_dimensions()
        self.user_sets_start_cell()
        self.user_or_self_solves()
        if self.user_solves:
            self.user_plays()
        else:
            self.self_plays()

    def user_sets_board_dimensions(self):
        while True:
            try:
                numbers = input("Enter your board dimensions: ")
                self.rows, self.columns = (
                    int(d) for d in re.match(self.input_matcher, numbers).groups()
                )
                if not (self.rows > 0) & (self.columns > 0):
                    raise ValueError
                break
            except (AttributeError, ValueError):
                print("Invalid dimensions!")
        self.cell_width = len(str(self.rows)) + 2
        self.row_number_width = len(str(self.columns))
        self.unvisited_cell = self.unvisited_cell[: self.cell_width]
        self.visited_cell = self.visited_cell[-self.cell_width :]
        self.knights_cell = self.knights_cell[-self.cell_width :]

        self.border = " " * self.row_number_width + "-" * (
            self.cell_width * self.rows + 3
        )

        footer_formatter = "".join(
            self.cell_formatter(str(i), self.cell_width)
            for i in range(1, self.rows + 1)
        )
        self.column_footer = eval(
            'f"' + (" " * (self.row_number_width + 1) + footer_formatter + '"')
        )

    def user_sets_start_cell(self):
        while True:
            try:
                numbers = input("Enter the knight's starting position: ")
                row, column = (
                    int(d) for d in re.match(self.input_matcher, numbers).groups()
                )
                if not ((1 <= row <= self.rows) & (1 <= column <= self.columns)):
                    raise ValueError
                break
            except (AttributeError, ValueError):
                print("Invalid position!")
        self.start_cell = Cell(row, column)

    def user_or_self_solves(self):
        while True:
            try:
                response = input("Do you want to try the puzzle?  (y/n): ")
                if response.lower() in "yn":
                    self.user_solves = True if response.lower() == "y" else False
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid response! ", end="")

    def user_plays(self):
        self.self_plays()
        if self.board_solved():
            self.visited_cells.clear()
            self.update_board(self.start_cell)
        else:
            return

        while True:
            self.show_board()
            if self.board_solved():
                print("What a great tour! Congratulations!")
                break
            elif self.dead_end():
                print("No more possible moves!")
                print(f"Your knight visited {len(self.visited_cells)} squares!")
                break
            self.user_moves()

    def user_moves(self):
        while True:
            try:
                numbers = input("Enter your next move: ")
                row, column = (
                    int(d) for d in re.match(self.input_matcher, numbers).groups()
                )
                if Cell(row, column) not in self.reachable_cells:
                    raise ValueError
                break
            except (AttributeError, ValueError):
                print("Invalid move! ", end="")
        self.update_board(Cell(row, column))

    def self_plays(self):
        self.self_moves(self.start_cell)
        if self.board_solved():
            if not self.user_solves:
                print()
                print("Here's the solution!")
                self.show_board()
        else:
            print("No solution exists!")

    def self_moves(self, cell):
        self.update_board(cell)
        if self.board_solved() or self.dead_end():
            return
        sorted_reachables = sorted(
            [
                (self.reachable_cell_count(a_cell), a_cell)
                for a_cell in self.reachable_cells
            ]
        )
        for count, reachable_cell in sorted_reachables:
            self.self_moves(reachable_cell)
            if self.board_solved():
                return
            self.visited_cells.pop(cell)
            return

    def find_reachable_cells(self, from_cell):
        reachable_cells = set()
        for move in self.moves:
            to_cell = Cell(move.rows + from_cell.row, move.columns + from_cell.column)
            if (
                (1 <= to_cell.row <= self.rows)
                & (1 <= to_cell.column <= self.columns)
                & (to_cell not in self.visited_cells)
            ):
                reachable_cells.add(to_cell)
        return reachable_cells

    def update_board(self, new_current_cell):
        self.current_cell = new_current_cell
        self.visited_cells[self.current_cell] = len(self.visited_cells) + 1
        self.reachable_cells = self.find_reachable_cells(self.current_cell)

    def show_board(self):
        print(self.border)

        for column in range(-self.columns, 0):
            row_number_formatter = self.cell_formatter(
                abs(column), self.row_number_width
            )
            cells_formatter = "".join(
                self.format_cell(Cell(row, abs(column)))
                for row in range(1, self.rows + 1)
            )
            print(eval('f"' + row_number_formatter + "|" + cells_formatter + ' |"'))

        print(self.border)
        print(self.column_footer)
        print()

    def format_cell(self, cell):
        if cell == self.current_cell:
            if self.user_solves:
                return self.knights_cell
            else:
                return self.cell_formatter(self.visited_cells[cell], self.cell_width)
        elif cell in self.visited_cells:
            if self.user_solves:
                return self.visited_cell
            else:
                return self.cell_formatter(self.visited_cells[cell], self.cell_width)
        elif cell in self.reachable_cells:
            return self.cell_formatter(self.reachable_cell_count(cell), self.cell_width)
        else:
            return self.unvisited_cell


def main():
    board = Board()
    board.run()


if __name__ == "__main__":
    main()
