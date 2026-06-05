from abc import ABC, abstractmethod
from enums.symbol import Symbol
from core.board import Board

class WinningStrategy(ABC):
    @abstractmethod
    def check_win(self, board: 'Board', row: int, col: int, symbol: Symbol) -> bool:
        """Check if the move at (row, col) with the given symbol results in a win."""
        pass