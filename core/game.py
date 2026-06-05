import threading
from typing import Optional
from core.board import Board
from enums.game_status import GameStatus
from enums.symbol import Symbol
from entities.player import Player
from strategy.winning_strategy import WinningStrategy
from strategy.row_winning_strategy import RowWinningStrategy
from strategy.column_winning_strategy import ColumnWinningStrategy
from strategy.diagonal_winning_strategy import DiagonalWinningStrategy
from observer.game_observer import GameObserver
from exceptions.invalid_move_exception import InvalidMoveException

class Game:
    def __init__(self, player1: 'Player', player2: 'Player', board_size: int = 3):
        self._board = Board(board_size)
        self._players: list['Player'] = [player1, player2]
        self._current_player_index: int = 0
        self._status = GameStatus.IN_PROGRESS
        self._winning_strategies = self._initialize_winning_strategies()
        self._observers: list[GameObserver] = []
        self._lock = threading.Lock()
    
    def _initialize_winning_strategies(self) -> list[WinningStrategy]:
        return [
            RowWinningStrategy(),
            ColumnWinningStrategy(),
            DiagonalWinningStrategy()
        ]
    
    def make_move(self, row: int, col: int) -> None:
        with self._lock:
            # Check if game is already over
            if self._status != GameStatus.IN_PROGRESS:
                raise InvalidMoveException("Game is already over.")
            
            # Validate the move
            if not self._board.is_cell_empty(row, col):
                raise InvalidMoveException(f"Cell ({row}, {col}) is already occupied.")
            
            # Place the symbol on the board
            current_player = self._players[self._current_player_index]
            self._board.place_symbol(row, col, current_player.symbol)

            # Check for win
            if self._check_win(row, col, current_player.symbol):
                self._status = (GameStatus.WINNER_X if current_player.symbol == Symbol.X else GameStatus.WINNER_O)
                self._notify_observers()
                return
            
            # Check for draw
            if self._board.is_full():
                self._status = GameStatus.DRAW
                self._notify_observers()
                return
            
            # Switch to the next player
            self._current_player_index = (self._current_player_index + 1) % 2
    
    def _check_win(self, row: int, col: int, symbol: Symbol) -> bool:
        for strategy in self._winning_strategies:
            if strategy.check_win(self._board, row, col, symbol):
                return True
        return False
    
    def add_observer(self, observer: GameObserver) -> None:
        self._observers.append(observer)
    
    def _notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self)
    
    @property
    def board(self) -> Board:
        return self._board
    
    @property
    def current_player(self) -> Player:
        return self._players[self._current_player_index]
    
    @property
    def status(self) -> GameStatus:
        return self._status
    
    @property
    def winner(self) -> Optional[Player]:
        if self._status == GameStatus.WINNER_X:
            return next((player for player in self._players if player.symbol == Symbol.X), None)
        elif self._status == GameStatus.WINNER_O:
            return next((player for player in self._players if player.symbol == Symbol.O), None)
        return None
    
    def print_board(self) -> None:
        self._board.print_board()