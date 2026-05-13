"""
Main game screen — central screen of the TUI app.
Layout:
  ┌─────────────────────────────────────────┐
  │  [Pet Display]   [Stat Bars]            │
  │                                         │
  │  [Event Log]                            │
  │                                         │
  │  [Action Menu]                          │
  └─────────────────────────────────────────┘
"""
from __future__ import annotations

from collections import deque
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Header, Footer
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel

from tamagotchi.core.pet import Pet, LifeStage
from tamagotchi.core.persistence import save_pet
from tamagotchi.ui.widgets.pet_display import PetDisplay
from tamagotchi.ui.widgets.stat_bars import StatBars
from tamagotchi.ui.widgets.action_menu import ActionMenu, ActionSelected


class EventLog(Static):
    """Scrolling log of pet events."""

    MAX_LINES = 6

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines: deque[str] = deque(maxlen=self.MAX_LINES)

    def add(self, msg: str) -> None:
        self._lines.append(msg)
        lines_text = Text()
        for line in self._lines:
            lines_text.append(line + "\n")
        self.update(Panel(lines_text, title="[bold]Events[/]", border_style="bright_black"))

    def on_mount(self) -> None:
        self.update(Panel("[grey50]Waiting for events...[/]", title="[bold]Events[/]", border_style="bright_black"))


class MainScreen(Screen):
    """Primary game screen."""

    BINDINGS = [
        ("q",     "quit_game",      "Quit"),
        ("ctrl+s","save",           "Save"),
        ("n",     "new_game",       "New pet"),
        ("?",     "show_help",      "Help"),
        ("left",  "menu_left",      ""),
        ("right", "menu_right",     ""),
        ("enter", "menu_confirm",   ""),
        ("m",     "action_meal",    ""),
        ("s",     "action_snack",   ""),
        ("p",     "action_play",    ""),
        ("c",     "action_clean",   ""),
        ("d",     "action_medicine",""),
        ("i",     "action_discipline",""),
        ("l",     "action_lights",  ""),
        ("t",     "action_status",  ""),
        ("j", "action_minigame", "Jokenpô"),
    ]

    def __init__(self, pet: Pet, **kwargs):
        super().__init__(**kwargs)
        self._pet = pet
        self._tick_count = 0

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="top_row"):
            yield PetDisplay(id="pet_display")
            yield StatBars(self._pet, id="stat_bars")
        yield EventLog(id="event_log")
        yield ActionMenu(id="action_menu")
        yield Footer()

    def on_mount(self) -> None:
        # Wire pet into pet display
        display = self.query_one("#pet_display", PetDisplay)
        display.pet = self._pet

        # Game loop: tick every second
        self.set_interval(1.0, self._game_tick)
        # Auto-save every 30s
        self.set_interval(30.0, self._auto_save)

        log = self.query_one("#event_log", EventLog)
        log.add(f"🥚 {self._pet.name} is waiting for you...")

    # -----------------------------------------------------------------------
    # Game loop
    # -----------------------------------------------------------------------

    def _game_tick(self) -> None:
        events = self._pet.tick()
        if events:
            self._handle_events(events)
        self._check_milestones()
        self._refresh_stats()

    def _check_milestones(self) -> None:
        pet = self._pet
        log = self.query_one("#event_log", EventLog)
        # Peak form: both hunger and happy at max
        if pet.hunger == 4 and pet.happy == 4 and not getattr(self, "_peak_shared", False):
            self._peak_shared = True
            log.add("⭐ Peak form! Run: tama share --copy")
        elif pet.hunger < 4 or pet.happy < 4:
            self._peak_shared = False

    def _refresh_stats(self) -> None:
        stat_bars = self.query_one("#stat_bars", StatBars)
        stat_bars.update_pet(self._pet)
        display = self.query_one("#pet_display", PetDisplay)
        display.pet = self._pet

    def _handle_events(self, events: list[str]) -> None:
        log = self.query_one("#event_log", EventLog)
        from tamagotchi.plugins import plugin_manager
        for event in events:
            if event.startswith("evolved:"):
                stage = event.split(":")[1]
                log.add(f"✨ {self._pet.name} evolved into {stage.upper()}!")
                log.add("📸 Share the moment: tama share --copy")
                self.app.bell()
                plugin_manager.emit("on_evolve", pet=self._pet,
                                    old_stage="", new_stage=stage)
            elif event == "hungry":
                log.add(f"🍱 {self._pet.name} is getting hungry!")
                self.app.bell()
            elif event == "unhappy":
                log.add(f"😢 {self._pet.name} is unhappy!")
                self.app.bell()
            elif event == "poop":
                log.add(f"💩 {self._pet.name} made a mess!")
            elif event == "sick":
                log.add(f"🤒 {self._pet.name} got sick! Give medicine!")
                self.app.bell()
            elif event.startswith("died:"):
                cause = event.split(":")[1]
                log.add(f"💀 {self._pet.name} has died ({cause})...")
                self.app.bell()
                plugin_manager.emit("on_death", pet=self._pet, cause=cause)

    # -----------------------------------------------------------------------
    # Action handling
    # -----------------------------------------------------------------------

    def on_action_selected(self, message: ActionSelected) -> None:
        self._dispatch_action(message.action)

    def _dispatch_action(self, action: str) -> None:
        log = self.query_one("#event_log", EventLog)
        pet = self._pet

        if action == "feed_meal":
            result = pet.feed_meal()
        elif action == "feed_snack":
            result = pet.feed_snack()
        elif action == "play":
            result = pet.play()
        elif action == "flush_poop":
            result = pet.flush_poop()
        elif action == "give_medicine":
            result = pet.give_medicine()
        elif action == "discipline":
            result = pet.scold()
        elif action == "toggle_lights":
            result = pet.toggle_lights()
        elif action == "show_status":
            result = (
                f"Age: {pet.age_display} | "
                f"Hunger: {pet.hunger}/4 | "
                f"Happy: {pet.happy}/4 | "
                f"Weight: {pet.weight} | "
                f"Discipline: {pet.discipline}%"
            )
        else:
            result = "?"

        log.add(result)
        self._refresh_stats()

        # Notify plugins
        from tamagotchi.plugins import plugin_manager
        plugin_manager.emit("on_action", action=action, pet=pet)

    # -----------------------------------------------------------------------
    # Keybindings
    # -----------------------------------------------------------------------

    def action_quit_game(self) -> None:
        save_pet(self._pet)
        self.app.exit()

    def action_save(self) -> None:
        save_pet(self._pet)
        log = self.query_one("#event_log", EventLog)
        log.add("💾 Game saved!")

    def _auto_save(self) -> None:
        save_pet(self._pet)

    def action_new_game(self) -> None:
        self.app.push_screen("new_pet")

    def action_show_help(self) -> None:
        self.app.push_screen("help")

    # -----------------------------------------------------------------------
    # Menu navigation (screen-level so arrow keys always work)
    # -----------------------------------------------------------------------

    def action_menu_left(self) -> None:
        from tamagotchi.ui.widgets.action_menu import ACTIONS
        menu = self.query_one("#action_menu", ActionMenu)
        menu.selected = (menu.selected - 1) % len(ACTIONS)

    def action_menu_right(self) -> None:
        from tamagotchi.ui.widgets.action_menu import ACTIONS
        menu = self.query_one("#action_menu", ActionMenu)
        menu.selected = (menu.selected + 1) % len(ACTIONS)

    def action_menu_confirm(self) -> None:
        from tamagotchi.ui.widgets.action_menu import ACTIONS
        menu = self.query_one("#action_menu", ActionMenu)
        self._dispatch_action(ACTIONS[menu.selected][2])
        
    def action_action_minigame(self) -> None:
        from tamagotchi.ui.screens.minigame import MinigameScreen
        self.app.push_screen(MinigameScreen(self._pet))

    def action_action_meal(self)        -> None: self._dispatch_action("feed_meal")
    def action_action_snack(self)       -> None: self._dispatch_action("feed_snack")
    def action_action_play(self)        -> None: self._dispatch_action("play")
    def action_action_clean(self)       -> None: self._dispatch_action("flush_poop")
    def action_action_medicine(self)    -> None: self._dispatch_action("give_medicine")
    def action_action_discipline(self)  -> None: self._dispatch_action("discipline")
    def action_action_lights(self)      -> None: self._dispatch_action("toggle_lights")
    def action_action_status(self)      -> None: self._dispatch_action("show_status")


