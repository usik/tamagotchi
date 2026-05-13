from __future__ import annotations

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Header, Footer
from textual.binding import Binding

from tamagotchi.core.pet import Pet
from tamagotchi.core.minigames import Move, get_computer_move, determine_winner


class MinigameScreen(Screen):

    BINDINGS = [
        ("q", "go_back", "Voltar"),
        ("1", "choose_rock",     "Pedra"),
        ("2", "choose_paper",    "Papel"),
        ("3", "choose_scissors", "Tesoura"),
        ("j", "action_minigame", "Jokenpô"),
    ]

    def __init__(self, pet: Pet, **kwargs):
        super().__init__(**kwargs)
        self._pet = pet

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("🪨 📄 ✂️  Jokenpô!", id="title")
        yield Footer()
        yield Static("Escolha sua jogada:", id="prompt")
        yield Static("[ 1 ] 🪨 Pedra    [ 2 ] 📄 Papel    [ 3 ] ✂️  Tesoura", id="options")
        yield Static("", id="result")

    def action_go_back(self) -> None:
        self.app.pop_screen()
        
    def action_choose_rock(self) -> None:
        self._play(Move.ROCK)

    def action_choose_paper(self) -> None:
        self._play(Move.PAPER)

    def action_choose_scissors(self) -> None:
        self._play(Move.SCISSORS)

    def _play(self, player_move: Move) -> None:
        computer_move = get_computer_move()
        result = determine_winner(player_move, computer_move)

        if result == "You win!":
            self._pet.play()
            msg = f"Você jogou {player_move.name} | Computador jogou {computer_move.name}\n🎉 {result} {self._pet.name} ficou feliz!"
        elif result == "Computer wins!":
            msg = f"Você jogou {player_move.name} | Computador jogou {computer_move.name}\n😢 {result}"
        else:
            msg = f"Você jogou {player_move.name} | Computador jogou {computer_move.name}\n🤝 {result}"

        self.query_one("#result", Static).update(msg)
        
    