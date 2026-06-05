from typing import Optional
import threading
from observer.scorecard import Scorecard
from core.game import Game
from entities.player import Player
from enums.game_status import GameStatus

class TicTacToeSystem:
    _instance: Optional['TicTacToeSystem'] = None
    _lock = threading.Lock()

    def __init__(self):
        # Prevent direct instantiation
        if TicTacToeSystem._instance is not None:
            raise RuntimeError("Use get_instance() to access the TicTacToeSystem singleton.")
        self._scorecard = Scorecard()
        self._current_game: Optional[Game] = None
    
    @classmethod
    def get_instance(cls) -> 'TicTacToeSystem':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        
        return cls._instance
    
    def create_game(self, player1: 'Player', player2: 'Player') -> Game:
        self._current_game = Game(player1, player2)
        self._current_game.add_observer(self._scorecard)
        print(f"New game created between {player1.name} and {player2.name}.")

        return self._current_game
    
    def make_move(self, player: 'Player', row: int, col: int) -> None:
        if self._current_game is None:
            raise RuntimeError("No active game. Please create a game first.")
        
        if self._current_game.winner is not None:
            raise RuntimeError("Game is already over. Please create a new game.")
        
        print(f"{player.name} is making a move at ({row}, {col}).")
        self._current_game.make_move(row, col)
        self._current_game.print_board()
    
    @property
    def game_status(self) -> GameStatus:
        if self._current_game is None:
            raise RuntimeError("No active game. Please create a game first.")
        
        return self._current_game.status
    
    def print_scoreboard(self):
        self._scorecard.print_scoreboard()
    
    @classmethod
    def reset_instance(cls):
        """
        Reset the singleton instance for testing purposes.
        """
        with cls._lock:
            cls._instance = None