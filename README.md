# Tic Tac Toe — Low-Level Design

A cleanly architected, object-oriented Tic Tac Toe game built in Python, demonstrating several core design patterns: Strategy, Observer, and Singleton.

## Overview

This project models a two-player Tic Tac Toe system where players take turns placing symbols on a 3×3 board. The design emphasizes separation of concerns, extensibility, and thread safety.

## Project Structure

```
design_tic_tac_toe/
├── main.py                         # Entry point
├── core/
│   ├── board.py                    # Board grid management
│   ├── game.py                     # Game orchestration and turn logic
│   └── tic_tac_toe_system.py       # Singleton system facade
├── entities/
│   ├── cell.py                     # Individual board cell
│   └── player.py                   # Player dataclass
├── enums/
│   ├── symbol.py                   # X, O, EMPTY symbols
│   └── game_status.py              # IN_PROGRESS, DRAW, WINNER_X, WINNER_O
├── strategy/
│   ├── winning_strategy.py         # Abstract strategy interface
│   ├── row_winning_strategy.py     # Row win check
│   ├── column_winning_strategy.py  # Column win check
│   └── diagonal_winning_strategy.py# Diagonal win check
├── observer/
│   ├── game_observer.py            # Abstract observer interface
│   └── scorecard.py                # Tracks wins per player
└── exceptions/
    └── invalid_move_exception.py   # Custom exception for invalid moves
```

## Design Patterns Used

**Strategy Pattern** — Win detection is decoupled from the `Game` class. Each win condition (row, column, diagonal) is encapsulated in its own strategy class implementing `WinningStrategy`. Adding new win conditions (e.g., for larger boards or custom rules) requires no changes to `Game`.

**Observer Pattern** — The `Scorecard` observes the `Game` and automatically updates scores when a game ends with a winner. New observers (e.g., logging, analytics, replay recording) can be added without modifying game logic.

**Singleton Pattern** — `TicTacToeSystem` uses a thread-safe singleton to ensure a single game management entry point across the application.

## Class Diagram

```mermaid
classDiagram
    class TicTacToeSystem {
        -_scorecard: Scorecard
        -_current_game: Game
        +create_game(player1, player2) Game
        +make_move(player, row, col) void
        +game_status: GameStatus
        +print_scoreboard() void
    }

    class Game {
        -_board: Board
        -_players: list~Player~
        -_current_player_index: int
        -_status: GameStatus
        -_winning_strategies: list~WinningStrategy~
        -_observers: list~GameObserver~
        +make_move(row, col) void
        +add_observer(observer) void
        +current_player: Player
        +status: GameStatus
        +winner: Player
    }

    class Board {
        -_size: int
        -_grid: list~list~Cell~~
        +place_symbol(row, col, symbol) void
        +is_cell_empty(row, col) bool
        +is_full() bool
        +get_cell(row, col) Cell
        +size: int
    }

    class Cell {
        -_symbol: Symbol
        +symbol: Symbol
        +is_empty() bool
    }

    class Player {
        +name: str
        +symbol: Symbol
    }

    class Symbol {
        <<enumeration>>
        X
        O
        EMPTY
        +display_char: str
    }

    class GameStatus {
        <<enumeration>>
        IN_PROGRESS
        DRAW
        WINNER_X
        WINNER_O
    }

    class WinningStrategy {
        <<abstract>>
        +check_win(board, row, col, symbol)* bool
    }

    class RowWinningStrategy {
        +check_win(board, row, col, symbol) bool
    }

    class ColumnWinningStrategy {
        +check_win(board, row, col, symbol) bool
    }

    class DiagonalWinningStrategy {
        +check_win(board, row, col, symbol) bool
    }

    class GameObserver {
        <<abstract>>
        +update(game)* void
    }

    class Scorecard {
        -_scores: dict
        +update(game) void
        +record_win(player) void
        +get_scores(player) int
    }

    class InvalidMoveException {
        <<exception>>
    }

    TicTacToeSystem --> Game : manages
    TicTacToeSystem --> Scorecard : owns
    Game --> Board : has
    Game --> Player : has 2
    Game --> WinningStrategy : uses
    Game --> GameObserver : notifies
    Board --> Cell : contains
    Cell --> Symbol : holds
    Player --> Symbol : assigned
    Game --> GameStatus : tracks
    WinningStrategy <|-- RowWinningStrategy
    WinningStrategy <|-- ColumnWinningStrategy
    WinningStrategy <|-- DiagonalWinningStrategy
    GameObserver <|-- Scorecard
```

## Sequence Diagrams

### 1. Game Creation

```mermaid
sequenceDiagram
    participant Client
    participant System as TicTacToeSystem
    participant Game
    participant Scorecard

    Client->>System: create_game(alice, bob)
    System->>Game: new Game(alice, bob)
    Game->>Game: _initialize_winning_strategies()
    System->>Game: add_observer(scorecard)
    Game->>Game: store observer reference
    System-->>Client: Game created
```

### 2. Making a Move (No Win)

```mermaid
sequenceDiagram
    participant Client
    participant System as TicTacToeSystem
    participant Game
    participant Board
    participant Cell
    participant Strategy as WinningStrategy

    Client->>System: make_move(alice, 0, 0)
    System->>Game: make_move(0, 0)
    Game->>Board: is_cell_empty(0, 0)
    Board-->>Game: true
    Game->>Board: place_symbol(0, 0, Symbol.X)
    Board->>Cell: set symbol = X
    Game->>Strategy: check_win(board, 0, 0, X)
    Strategy-->>Game: false
    Game->>Board: is_full()
    Board-->>Game: false
    Game->>Game: switch to next player
    System->>Board: print_board()
```

### 3. Making a Winning Move

```mermaid
sequenceDiagram
    participant Client
    participant System as TicTacToeSystem
    participant Game
    participant Board
    participant Strategy as WinningStrategy
    participant Scorecard

    Client->>System: make_move(alice, 0, 2)
    System->>Game: make_move(0, 2)
    Game->>Board: is_cell_empty(0, 2)
    Board-->>Game: true
    Game->>Board: place_symbol(0, 2, Symbol.X)
    Game->>Strategy: check_win(board, 0, 2, X)
    Strategy-->>Game: true (row complete)
    Game->>Game: status = WINNER_X
    Game->>Scorecard: update(game)
    Scorecard->>Scorecard: record_win(alice)
    System->>Board: print_board()
    System-->>Client: Game over — Alice wins
```

### 4. Invalid Move Handling

```mermaid
sequenceDiagram
    participant Client
    participant System as TicTacToeSystem
    participant Game
    participant Board

    Client->>System: make_move(bob, 0, 0)
    System->>Game: make_move(0, 0)
    Game->>Board: is_cell_empty(0, 0)
    Board-->>Game: false (already occupied)
    Game-->>System: raise InvalidMoveException
    System-->>Client: InvalidMoveException
```

## How to Run

```bash
cd design_tic_tac_toe
python main.py
```

## Key Design Decisions

**Frozen dataclass for Player** — Players are immutable value objects. Once created with a name and symbol, they cannot be changed, which prevents accidental mutation during gameplay.

**Property with setter on Cell** — Unlike Player, cells are mutable by design since symbols are placed on them during the game. The `@property` pattern allows future validation in the setter without changing the public API.

**Thread safety** — Both `Game` and `Scorecard` use threading locks to protect shared mutable state, making the system safe for concurrent access scenarios.

**Strategy pattern for win detection** — Rather than hardcoding win checks in the Game class, each direction of win (row, column, diagonal) is a separate strategy. This makes it trivial to extend to larger boards or custom win conditions.