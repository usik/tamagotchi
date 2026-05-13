from __future__ import annotations

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Header, Footer
from textual.binding import Binding

from tamagotchi.core.pet import Pet
from tamagotchi.core.minigames import Move, get_computer_move, determine_winner


class MinigameScreen(Screen):

    BINDINGS = [
        ("q", "go_back", "Back"),
        ("1", "choose_rock",     "Rock"),
        ("2", "choose_paper",    "Paper"),
        ("3", "choose_scissors", "Scissors"),
        ("space", "go_back", "Back"),
    ]

    def __init__(self, pet: Pet, **kwargs):
        super().__init__(**kwargs)
        self._pet = pet
        self._history: list[str] = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("🪨 📄 ✂️  Jokenpô!", id="title")
        yield Footer()
        yield Static("Choose your move:", id="prompt")
        yield Static("[ 1 ] 🪨 Rock    [ 2 ] 📄 Paper    [ 3 ] ✂️  Scissors", id="options")
        yield Static("", id="result")
        yield Static("", id="press_space")

    def action_go_back(self) -> None:
        self.app.pop_screen()
        
    def action_choose_rock(self) -> None:
        self._play(Move.ROCK)

    def action_choose_paper(self) -> None:
        self._play(Move.PAPER)

    def action_choose_scissors(self) -> None:
        self._play(Move.SCISSORS)

    def _play(self, player_move: Move) -> None:
        if self._pet.happy >= 4:
            self.query_one("#press_space", Static).update("✅ Your pet is already happy! Press space or Q to go back.")
            return
    
        computer_move = get_computer_move()
        result = determine_winner(player_move, computer_move)

        if result == "You win!":
            self._pet.happy = min(4, self._pet.happy + 2)
            msg = f"You played {player_move.name} | Computer played {computer_move.name}\n🎉 You win! +2 happiness"
        elif result == "It's a tie!":
            msg = f"You played {player_move.name} | Computer played {computer_move.name}\n🤝 It's a tie!"
        else:
            self._pet.happy = max(0, self._pet.happy - 1)
            msg = f"You played {player_move.name} | Computer played {computer_move.name}\n😢 You lost! -1 happiness"

        self._history.append(msg)
        self.query_one("#result", Static).update("\n".join(self._history))

        if self._pet.happy >= 4:
            self.query_one("#press_space", Static).update("✅ Pet is happy! [bold]Press space to go back[/]")
        else:
            self.query_one("#press_space", Static).update("[dim]Press space to go back or keep playing[/]")