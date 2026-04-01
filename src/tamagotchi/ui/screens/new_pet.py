"""
New Pet screen — name input and hatch.
"""
from __future__ import annotations

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Input, Button, Header
from textual.containers import Vertical, Center
from textual import events
from rich.panel import Panel
from rich.text import Text

from tamagotchi.core.pet import Pet
from tamagotchi.core.persistence import list_saved_pets, load_pet


class NewPetScreen(Screen):
    """Screen for creating or loading a pet."""

    BINDINGS = [("escape", "go_back", "Back")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical(id="new_pet_form"):
                yield Static(self._banner(), id="banner")
                yield Static("\n[bold]Enter a name for your new pet:[/]\n")
                yield Input(placeholder="e.g. Tama, Pixel, Mochi...", id="name_input")
                yield Button("🥚  Hatch New Pet", id="hatch_btn", variant="success")
                saved = list_saved_pets()
                if saved:
                    yield Static("\n[bold]— or continue with a saved pet —[/]\n")
                    for name in saved:
                        safe_id = name.lower().replace(" ", "_").replace(".", "_")
                        yield Button(f"▶  {name}", id=f"load_{safe_id}", variant="default")

    def _banner(self) -> Text:
        t = Text(justify="center")
        t.append("╔═══════════════════════════╗\n", style="bright_cyan")
        t.append("║  ", style="bright_cyan")
        t.append(" TAMAGOTCHI ", style="bold bright_white on dark_green")
        t.append("  ║\n", style="bright_cyan")
        t.append("║   terminal virtual pet    ║\n", style="bright_cyan")
        t.append("╚═══════════════════════════╝\n", style="bright_cyan")
        return t

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "hatch_btn":
            name_input = self.query_one("#name_input", Input)
            name = name_input.value.strip() or "Tama"
            self._start_new_pet(name)
        elif btn_id and btn_id.startswith("load_"):
            # Reverse the safe_id back to the display name by checking saved pets
            from tamagotchi.core.persistence import list_saved_pets
            for name in list_saved_pets():
                safe_id = "load_" + name.lower().replace(" ", "_").replace(".", "_")
                if btn_id == safe_id:
                    pet = load_pet(name)
                    if pet:
                        self.app.switch_to_main(pet)
                    break

    def _start_new_pet(self, name: str) -> None:
        pet = Pet(name=name)
        self.app.switch_to_main(pet)

    def action_go_back(self) -> None:
        self.app.pop_screen()
