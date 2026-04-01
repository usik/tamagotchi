"""
PetDisplay widget — animated ASCII art of the pet.
"""
from __future__ import annotations

from textual.widget import Widget
from textual.reactive import reactive
from textual.app import RenderResult
from rich.text import Text
from rich.panel import Panel
from rich.align import Align

from tamagotchi.core.pet import Pet, Mood, PetCharacter, LifeStage
from tamagotchi.sprites.ascii import get_animation_frames, get_sprite, ATTENTION_ICON, SLEEP_ICON


MOOD_COLORS: dict[Mood, str] = {
    Mood.HAPPY:    "bright_green",
    Mood.NEUTRAL:  "yellow",
    Mood.HUNGRY:   "orange3",
    Mood.UNHAPPY:  "blue",
    Mood.SICK:     "red",
    Mood.SLEEPING: "grey50",
    Mood.DEAD:     "grey30",
}

STAGE_COLORS: dict[LifeStage, str] = {
    LifeStage.EGG:   "white",
    LifeStage.BABY:  "bright_cyan",
    LifeStage.CHILD: "bright_green",
    LifeStage.TEEN:  "bright_yellow",
    LifeStage.ADULT: "bright_magenta",
    LifeStage.ELDER: "bright_white",
    LifeStage.DEAD:  "grey30",
}


class PetDisplay(Widget):
    """Animated ASCII pet widget."""

    frame_index: reactive[int] = reactive(0)
    pet: reactive[Pet | None] = reactive(None)

    def on_mount(self) -> None:
        self.set_interval(0.8, self._advance_frame)

    def _advance_frame(self) -> None:
        self.frame_index = (self.frame_index + 1) % 2

    def render(self) -> RenderResult:
        pet = self.pet
        if pet is None:
            return Panel("No pet loaded", title="[grey50]Tamagotchi[/]", width=20)

        mood = pet.mood
        character = pet.character
        frames = get_animation_frames(character, mood)
        frame = frames[self.frame_index % len(frames)]

        color = MOOD_COLORS.get(mood, "white")
        stage_color = STAGE_COLORS.get(pet.stage, "white")

        # Build sprite text
        sprite_text = Text()
        for line in frame:
            sprite_text.append(line + "\n", style=color)

        # Poop indicator
        if pet.poop_count > 0 and pet.is_alive:
            sprite_text.append("💩" * pet.poop_count + "\n", style="")

        # Attention / sleep indicator
        if pet.needs_attention and pet.is_alive:
            sprite_text.append(f"  {ATTENTION_ICON} {pet.attention_reason.upper()}\n", style="bold bright_red")
        elif not pet.lights_on:
            sprite_text.append(f"  {SLEEP_ICON} sleeping\n", style="grey50")

        title = f"[{stage_color}]{pet.name}[/] [{color}]({pet.mood.value})[/]"
        return Panel(Align.center(sprite_text), title=title, border_style=color, width=22)
