import random

class Character:
    def __init__(self, row: int, column: int, name: str, board_size: int = 5):
        self.row = row
        self.column = column
        self.name = name
        self.has_flag = False
        self.board_size = board_size

    def set_row(self, new_row: int):
        self.row = new_row

    def set_column(self, new_column: int):
        self.column = new_column

    def set_name(self, new_name: str):
        self.name = new_name

    def change_flag(self):
        self.has_flag = not self.has_flag

    def move(self):
        row_chg = random.randint(-1, 1)
        column_chg = random.randint(-1, 1)
        self.row += row_chg
        self.column += column_chg

        # keep within 0–4 boundaries (5×5 grid)
        self.row = max(0, min(self.row, self.board_size - 1))
        self.column = max(0, min(self.column, self.board_size - 1))

    def teleport(self):
        self.row = random.randint(0, self.board_size - 1)
        self.column = random.randint(0, self.board_size - 1)

    def __eq__(self, other):
        if not isinstance(other, Character):
            return False
        return self.row == other.row and self.column == other.column

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def __repr__(self):
        return f"Character(name='{self.name}', row={self.row}, column={self.column}, has_flag={self.has_flag})"
