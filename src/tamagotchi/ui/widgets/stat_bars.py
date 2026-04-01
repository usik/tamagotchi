"""
StatBars widget — shows all pet stats as visual bars.
"""
from __future__ import annotations

from textual.widget import Widget
from textual.app import RenderResult
from rich.table import Table
from rich.text import Text
from rich.panel import Panel

from tamagotchi.core.pet import Pet, LifeStage
from tamagotchi.core.evolution import CHARACTER_NAMES


def _bar(value: int, max_val: int = 4, width: int = 8, full: str = "█", empty: str = "░") -> str:
    filled = round((value / max_val) * width)
    return full * filled + empty * (width - filled)


def _color_for_value(value: int, max_val: int = 4) -> str:
    ratio = value / max_val
    if ratio > 0.6:
        return "bright_green"
    if ratio > 0.3:
        return "yellow"
    return "red"


class StatBars(Widget):
    """Displays pet stats as colored bars."""

    def __init__(self, pet: Pet | None = None, **kwargs):
        super().__init__(**kwargs)
        self._pet = pet

    def update_pet(self, pet: Pet) -> None:
        self._pet = pet
        self.refresh()

    def render(self) -> RenderResult:
        pet = self._pet
        if pet is None:
            return Panel("[grey50]No pet[/]", title="Stats")

        table = Table.grid(padding=(0, 1))
        table.add_column(justify="right", style="bold", width=12)
        table.add_column(width=10)
        table.add_column(justify="left", width=6)

        if pet.stage == LifeStage.EGG:
            table.add_row("[yellow]Stage[/]",  "Egg 🥚",   "")
            table.add_row("[grey50]Hatching soon...[/]", "", "")
        elif pet.stage == LifeStage.DEAD:
            table.add_row("[grey30]Stage[/]", "Dead 💀", "")
            table.add_row("[grey30]Age[/]", pet.age_display, "")
        else:
            h_bar   = _bar(pet.hunger,     4)
            hp_bar  = _bar(pet.happy,      4)
            wt_bar  = _bar(min(pet.weight, 30), 30, width=8)
            disc_bar = _bar(pet.discipline, 100, width=8)

            h_color   = _color_for_value(pet.hunger)
            hp_color  = _color_for_value(pet.happy)
            wt_color  = "yellow" if 8 <= pet.weight <= 22 else ("bright_green" if pet.weight < 8 else "red")
            disc_color = _color_for_value(pet.discipline, 100)

            character_name = CHARACTER_NAMES.get(pet.character, pet.character.value)

            table.add_row(
                "[bright_white]Character[/]",
                Text(character_name, style="bright_cyan"),
                ""
            )
            table.add_row(
                "[bright_white]Stage[/]",
                Text(pet.stage.value.capitalize(), style="bright_yellow"),
                Text(f"Age {pet.age_display}", style="grey50"),
            )
            table.add_row(
                "[bright_white]Hunger[/]",
                Text(h_bar,   style=h_color),
                Text(f"{pet.hunger}/4", style=h_color),
            )
            table.add_row(
                "[bright_white]Happy[/]",
                Text(hp_bar,  style=hp_color),
                Text(f"{pet.happy}/4", style=hp_color),
            )
            table.add_row(
                "[bright_white]Weight[/]",
                Text(wt_bar,  style=wt_color),
                Text(str(pet.weight), style=wt_color),
            )
            table.add_row(
                "[bright_white]Discipline[/]",
                Text(disc_bar, style=disc_color),
                Text(f"{pet.discipline}%", style=disc_color),
            )
            table.add_row(
                "[bright_white]Health[/]",
                Text("🤒 Sick" if pet.sick else "❤️  OK", style="red" if pet.sick else "bright_green"),
                ""
            )
            table.add_row(
                "[bright_white]Mistakes[/]",
                Text(str(pet.care_mistakes), style="yellow" if pet.care_mistakes < 5 else "red"),
                ""
            )

        return Panel(table, title="[bold]Stats[/]", border_style="bright_black")
