from dataclasses import dataclass
from enums.symbol import Symbol

@dataclass(frozen=True)
class Player:
    name: str
    symbol: Symbol

    def __post_init__(self):
        if self.symbol == Symbol.EMPTY:
            raise ValueError("Player symbol cannot be EMPTY.")
        
    def __str__(self):
        return f"{self.name} ({self.symbol.display_char})"