from strategy.winning_strategy import WinningStrategy
from enums.symbol import Symbol
from core.board import Board

class RowWinningStrategy(WinningStrategy):
    def check_win(self, board: 'Board', row: int, col: int, symbol: Symbol) -> bool:
        # Check if all cells in the specified row contain the same symbol
        for c in range(board.size):
            if board.get_cell(row, c).symbol != symbol:
                return False    
            
        return True