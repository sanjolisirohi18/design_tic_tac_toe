from enum import Enum

class GameStatus(Enum):
    IN_PROGRESS = 'in_progress'
    DRAW = 'draw'
    WINNER_X = 'winner_x'
    WINNER_O = 'winner_o'
