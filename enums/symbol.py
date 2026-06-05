from enum import Enum

class Symbol(Enum):
    X = 'X'
    O = 'O'
    EMPTY = '_'

    @property
    def display_char(self) -> str:
        return self.value