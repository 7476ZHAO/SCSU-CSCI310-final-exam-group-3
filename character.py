import random

class Character:
    def __init__(self, row: int, column: int, name: str):
        self.row = row
        self.column = column
        self.name = name
        self.has_flag = False

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
        self.row = max(0, min(self.row, 5))
        self.column = max(0, min(self.column, 5))

    def teleport(self):
        self.row = random.randint(0, 5)
        self.column = random.randint(0, 5)

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
