from abc import ABC, abstractmethod

class GameObserver(ABC):
    @abstractmethod
    def update(self, game: 'Game') -> None:
        """Called when the game state changes. Implement this method to react to game updates."""
        pass