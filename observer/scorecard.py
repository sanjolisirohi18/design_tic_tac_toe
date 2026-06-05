import threading
from collections import defaultdict
from core.game import Game
from observer.game_observer import GameObserver
from entities.player import Player

class Scorecard(GameObserver):
    def __init__(self):
        self._scores: dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()

    def update(self, game: Game) -> None:
        winner = game.winner

        if winner is not None:
            self.record_win(winner)
            print(f"Scoreboard updated: {winner.name} wins!")
    
    def record_win(self, player: Player) -> None:
        with self._lock:
            self._scores[player.name] += 1

    def get_scores(self, player: Player) -> int:
        return self._scores.get(player.name, 0)
    
    def print_scoreboard(self):
        print("\n ==== Scoreboard ====")

        if not self._scores:
            print("No games played yet.")
        else:
            for player_name, score in self._scores.items():
                print(f"{player_name}: {score} wins")
        
        print("====================\n")