from strategy.winning_strategy import WinningStrategy
from enums.symbol import Symbol 
from core.board import Board

class DiagonalWinningStrategy(WinningStrategy):
    def check_win(self, board: 'Board', row: int, col: int, symbol: Symbol) -> bool:
        # Check the main diagonal (top-left to bottom-right)
        if row == col:
            for i in range(board.size):
                if board.get_cell(i, i).symbol != symbol:
                    break
            else:
                return True
        
        # Check the anti-diagonal (top-right to bottom-left)
        if row + col == board.size - 1:
            for i in range(board.size):
                if board.get_cell(i, board.size - 1 - i).symbol != symbol:
                    break
            else:
                return True
        
        return False