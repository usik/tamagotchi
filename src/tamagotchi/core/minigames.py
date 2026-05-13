from enum import Enum
import random

class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

def get_computer_move() -> Move:
    return random.choice(list(Move))

def determine_winner(player: Move, computer: Move) -> str:
    if player == computer:
        return "It's a tie!"
    elif (
        (player == Move.ROCK and computer == Move.SCISSORS) or \
        (player == Move.PAPER and computer == Move.ROCK) or \
        (player == Move.SCISSORS and computer == Move.PAPER)
    ):
        return "You win!"
    else:
        return "Computer wins!"