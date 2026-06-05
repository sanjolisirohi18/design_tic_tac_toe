from core.tic_tac_toe_system import TicTacToeSystem
from entities.player import Player
from enums.symbol import Symbol

def main():
    system = TicTacToeSystem()
    alice = Player("Alice", Symbol.X)
    bob = Player("Bob", Symbol.O)

    # Game 1: Alice wins
    print("========== Game 1 ==========")
    system.create_game(alice, bob)

    system.make_move(alice, 0, 0)  # Alice
    system.make_move(bob, 1, 0)    # Bob    
    system.make_move(alice, 0, 1)  # Alice
    system.make_move(bob, 1, 1)    # Bob    
    system.make_move(alice, 0, 2)  # Alice wins

    print(f"Game 1 result: {system.game_status}")

    # Game 2: Bob wins
    print("\n========== Game 2 ==========")
    system.create_game(alice, bob)          

    system.make_move(alice, 0, 0)  # Alice
    system.make_move(bob, 1, 1)    # Bob
    system.make_move(alice, 0, 1)  # Alice
    system.make_move(bob, 0, 2)    # Bob
    system.make_move(alice, 2, 0)  # Alice
    system.make_move(bob, 2, 2)    # Bob wins

    print(f"Game 2 result: {system.game_status}")

    # Game 3: Draw
    print("\n========== Game 3 ==========")
    system.create_game(alice, bob)

    system.make_move(alice, 0, 0)  # Alice
    system.make_move(bob, 0, 1)    # Bob
    system.make_move(alice, 0, 2)  # Alice
    system.make_move(bob, 1, 1)    # Bob
    system.make_move(alice, 1, 0)  # Alice
    system.make_move(bob, 1, 2)    # Bob
    system.make_move(alice, 2, 1)  # Alice
    system.make_move(bob, 2, 0)    # Bob
    system.make_move(alice, 2, 2)  # Alice

    print(f"Game 3 result: {system.game_status}")

    # Final scoreboard
    system.print_scoreboard()

if __name__ == "__main__":
    main()