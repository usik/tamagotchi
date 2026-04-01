"""Help screen."""
from __future__ import annotations

from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Header, Footer
from textual.containers import Center
from rich.panel import Panel
from rich.text import Text
from rich.table import Table


HELP_TEXT = """\
[bold bright_cyan]TAMAGOTCHI — Controls[/]

[bold]Action shortcuts:[/]
  [bright_white]M[/]  Feed Meal      [bright_white]S[/]  Feed Snack
  [bright_white]P[/]  Play           [bright_white]C[/]  Clean poop
  [bright_white]D[/]  Give Medicine  [bright_white]I[/]  Discipline
  [bright_white]L[/]  Toggle Lights  [bright_white]T[/]  Status

[bold]Navigation:[/]
  [bright_white]← →[/]  Browse action menu
  [bright_white]Enter[/]  Confirm selected action
  [bright_white]Q[/]  Save and quit
  [bright_white]?[/]  This help screen

[bold]Life stages:[/]
  Egg → Baby (1h) → Child (8h) → Teen (1d) → Adult (3d) → Elder (2d) → [grey50]Death[/]

[bold]Tips:[/]
  • Feed meals when hunger is low, snacks boost happiness
  • Too many snacks = high weight (bad)
  • Clean poop before it causes sickness
  • Give medicine immediately when sick
  • Don't discipline unless pet is misbehaving
  • Turn lights off at night so pet can sleep
  • Fewer care mistakes = better evolution path

[bold]Evolution paths:[/]
  Good (< 2 mistakes) → Mimitchi / Ojitchi
  Normal (2–4)         → Mametchi / Otokitchi
  Poor (5+)            → Maskutchi / Tarakotchi
"""


class HelpScreen(Screen):
    BINDINGS = [("escape", "go_back", "Close"), ("q", "go_back", "Close")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Static(Panel(HELP_TEXT, title="[bold]Help[/]", border_style="bright_cyan", width=60))
        yield Footer()

    def action_go_back(self) -> None:
        self.app.pop_screen()
