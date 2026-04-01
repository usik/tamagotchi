"""
Root Textual application.
"""
from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding

from tamagotchi.core.pet import Pet
from tamagotchi.core.persistence import list_saved_pets, load_pet, save_pet


class TamagotchiApp(App):
    """Root application — manages screens."""

    TITLE = "Tamagotchi"
    CSS = """
    Screen {
        background: $surface;
    }

    #top_row {
        height: auto;
        margin: 1 0;
    }

    #pet_display {
        width: 24;
        height: auto;
        margin: 0 1;
    }

    #stat_bars {
        width: 1fr;
        height: auto;
        margin: 0 1;
    }

    #event_log {
        height: 10;
        margin: 0 1;
    }

    #action_menu {
        height: auto;
        margin: 0 1;
        dock: bottom;
    }

    #new_pet_form {
        width: 50;
        height: auto;
        align: center middle;
        margin: 4 0;
    }

    Center {
        align: center middle;
    }

    Button {
        margin: 0 0 1 0;
        width: 100%;
    }
    """

    def on_mount(self) -> None:
        saved = list_saved_pets()
        if saved:
            # Load the most recently saved pet
            pet = load_pet(saved[0])
            if pet:
                self.switch_to_main(pet)
                return
        self._show_new_pet_screen()

    def _show_new_pet_screen(self) -> None:
        from tamagotchi.ui.screens.new_pet import NewPetScreen
        self.push_screen(NewPetScreen(id="new_pet"))

    def switch_to_main(self, pet: Pet) -> None:
        from tamagotchi.ui.screens.main import MainScreen
        # Pop any existing screen before pushing main (but not the default base screen)
        if len(self.screen_stack) > 1:
            self.pop_screen()
        self.push_screen(MainScreen(pet, id="main"))

    def get_screen(self, name: str):
        from tamagotchi.ui.screens.help import HelpScreen
        from tamagotchi.ui.screens.new_pet import NewPetScreen
        from tamagotchi.ui.screens.graveyard import GraveyardScreen
        if name == "help":
            return HelpScreen(id="help")
        if name == "new_pet":
            return NewPetScreen(id="new_pet")
        if name == "graveyard":
            return GraveyardScreen(id="graveyard")
        return super().get_screen(name)
