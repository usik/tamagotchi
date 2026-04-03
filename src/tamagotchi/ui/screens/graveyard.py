"""
Graveyard screen — view deceased pets.
"""
from __future__ import annotations

import datetime
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Header, Footer, ListItem, ListView
from textual.containers import Vertical, ScrollableContainer
from rich.panel import Panel
from rich.text import Text

from tamagotchi.core.persistence import list_dead_pets, load_pet
from tamagotchi.core.evolution import CHARACTER_NAMES


class MemorialStone(Static):
    """Small ASCII memorial stone for a pet."""
    
    def __init__(self, name: str, age: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.age = age

    def on_mount(self) -> None:
        stone = Text.assemble(
            "  .-------.\n",
            "  | R.I.P |\n",
            f"  | {self.name[:5]:^5} |\n",
            f"  | {self.age:^5} |\n",
            "  '-------'"
        )
        self.update(stone)


class PetMemorial(ListItem):
    """A single pet's entry in the graveyard."""
    
    def __init__(self, pet_name: str, **kwargs):
        super().__init__(**kwargs)
        self.pet_name = pet_name

    def compose(self) -> ComposeResult:
        pet = load_pet(self.pet_name, dead=True)
        if not pet:
            yield Static("Error loading pet.")
            return

        death_date = "Unknown"
        if pet.death_timestamp:
            dt = datetime.datetime.fromtimestamp(pet.death_timestamp)
            death_date = dt.strftime("%Y-%m-%d %H:%M")

        char_name = CHARACTER_NAMES.get(pet.character, "Unknown")
        cause = pet.cause_of_death or "Unknown"

        with Vertical():
            yield MemorialStone(pet.name, pet.age_display)
            yield Static(f"[bold]{pet.name}[/] ({char_name})")
            yield Static(f"Died: {death_date} | Cause: {cause}")
            yield Static(f"Age: {pet.age_display} | Care Mistakes: {pet.care_mistakes}")


class GraveyardScreen(Screen):
    """Screen showing all deceased pets."""
    
    BINDINGS = [
        ("escape", "back", "Back"),
        ("q", "back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("[bold magenta]The Pet Graveyard[/]", id="graveyard_title")
        
        dead_pets = list_dead_pets()
        if not dead_pets:
            yield Static("\n\n[grey50]The graveyard is empty. All pets are currently alive (or haven't been born yet).[/]", id="empty_msg")
        else:
            with ScrollableContainer():
                yield ListView(*[PetMemorial(name) for name in dead_pets])
        
        yield Footer()

    def action_back(self) -> None:
        self.app.pop_screen()
