from strategy.winning_strategy import WinningStrategy
from enums.symbol import Symbol 
from core.board import Board

class ColumnWinningStrategy(WinningStrategy):
    def check_win(self, board: 'Board', row: int, col: int, symbol: Symbol) -> bool:
        # Check if all cells in the specified column contain the same symbol
        for r in range(board.size):
            if board.get_cell(r, col).symbol != symbol:
                return False    
            
        return True