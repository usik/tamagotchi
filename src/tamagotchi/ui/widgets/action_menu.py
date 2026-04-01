"""
ActionMenu widget — icon-based action bar replicating the original Tamagotchi button layout.
Actions: Feed Meal | Feed Snack | Play | Clean | Medicine | Discipline | Lights | Status
"""
from __future__ import annotations

from textual.widget import Widget
from textual.reactive import reactive
from textual.app import RenderResult
from textual import events
from rich.table import Table
from rich.text import Text
from rich.panel import Panel


ACTIONS = [
    ("🍱", "Meal",       "feed_meal"),
    ("🍬", "Snack",      "feed_snack"),
    ("⭐", "Play",       "play"),
    ("🚿", "Clean",      "flush_poop"),
    ("💊", "Medicine",   "give_medicine"),
    ("📣", "Discipline", "discipline"),
    ("💡", "Lights",     "toggle_lights"),
    ("📊", "Status",     "show_status"),
]


class ActionMenu(Widget):
    """8-icon action menu like the original Tamagotchi."""

    can_focus = True
    selected: reactive[int] = reactive(0)

    def on_mount(self) -> None:
        self.focus()

    def render(self) -> RenderResult:
        table = Table.grid(padding=(0, 1))
        for col in range(len(ACTIONS)):
            table.add_column(justify="center", width=7)

        icons = []
        labels = []
        for i, (icon, label, _) in enumerate(ACTIONS):
            style = "bold bright_white on dark_green" if i == self.selected else "dim"
            icons.append(Text(icon,   style=style, justify="center"))
            labels.append(Text(label, style=style, justify="center"))

        table.add_row(*icons)
        table.add_row(*labels)

        hint = "[grey50]← → select  [bright_white]Enter[/] confirm  [grey50]or press key shortcut[/]"
        return Panel(table, title=f"[bold]Actions[/]  {hint}", border_style="bright_black")

    # Key handling is done at the screen level via BINDINGS in MainScreen
    # so it works regardless of which widget has focus.


from textual.message import Message


class ActionSelected(Message):
    """Posted when user selects an action."""
    def __init__(self, action: str) -> None:
        super().__init__()
        self.action = action
