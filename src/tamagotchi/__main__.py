"""Entry point — `tama` or `tamagotchi` CLI command."""
import sys


def main() -> None:
    args = sys.argv[1:]

    if args and args[0] == "status":
        _cmd_status(args[1:])
    elif args and args[0] == "install":
        _cmd_install(args[1:])
    elif args and args[0] == "share":
        _cmd_share(args[1:])
    elif args and args[0] in ("--version", "version"):
        from tamagotchi import __version__
        print(f"tamagotchi {__version__}")
    else:
        _cmd_tui()


def _cmd_tui() -> None:
    from tamagotchi.ui.app import TamagotchiApp
    TamagotchiApp().run()


def _cmd_status(args: list[str]) -> None:
    """Print pet status — inline, no TUI.

    Usage:
        tama status                  # pretty print
        tama status --json           # JSON output (for tmux/starship)
        tama status --name Pixel     # specific pet
    """
    import json
    from tamagotchi.core.persistence import list_saved_pets, load_pet
    from tamagotchi.core.evolution import CHARACTER_NAMES

    json_mode = "--json" in args

    # Resolve pet name
    name = None
    if "--name" in args:
        idx = args.index("--name")
        if idx + 1 < len(args):
            name = args[idx + 1]

    if name is None:
        saved = list_saved_pets()
        if not saved:
            if json_mode:
                print(json.dumps({"error": "no pet found"}))
            else:
                print("No pet found. Run `tama` to hatch one.")
            sys.exit(1)
        name = saved[0]

    pet = load_pet(name)
    if pet is None:
        if json_mode:
            print(json.dumps({"error": f"pet '{name}' not found"}))
        else:
            print(f"Pet '{name}' not found.")
        sys.exit(1)

    # Tick once to catch up on time-based decay
    pet.tick()

    if json_mode:
        print(json.dumps({
            "name":             pet.name,
            "stage":            pet.stage.value,
            "character":        pet.character.value,
            "character_name":   CHARACTER_NAMES.get(pet.character, pet.character.value),
            "mood":             pet.mood.value,
            "hunger":           pet.hunger,
            "happy":            pet.happy,
            "weight":           pet.weight,
            "discipline":       pet.discipline,
            "sick":             pet.sick,
            "poop_count":       pet.poop_count,
            "lights_on":        pet.lights_on,
            "care_mistakes":    pet.care_mistakes,
            "age":              pet.age_display,
            "needs_attention":  pet.needs_attention,
            "attention_reason": pet.attention_reason,
        }))
        return

    # Pretty print with rich
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text

    console = Console()

    def bar(val: int, max_val: int = 4, width: int = 8) -> str:
        filled = round((val / max_val) * width)
        color = "bright_green" if val / max_val > 0.6 else ("yellow" if val / max_val > 0.3 else "red")
        return f"[{color}]{'█' * filled}{'░' * (width - filled)}[/]"

    char_name = CHARACTER_NAMES.get(pet.character, pet.character.value)

    table = Table.grid(padding=(0, 1))
    table.add_column(justify="right", style="bold", width=12)
    table.add_column()

    table.add_row("Name",      f"[bright_cyan]{pet.name}[/]")
    table.add_row("Character", f"[bright_white]{char_name}[/] ({pet.stage.value})")
    table.add_row("Age",       pet.age_display)
    table.add_row("Mood",      f"[bright_yellow]{pet.mood.value}[/]")
    table.add_row("Hunger",    f"{bar(pet.hunger)}  {pet.hunger}/4")
    table.add_row("Happy",     f"{bar(pet.happy)}   {pet.happy}/4")
    table.add_row("Weight",    str(pet.weight))
    table.add_row("Discipline",f"{pet.discipline}%")
    table.add_row("Health",    "[red]🤒 Sick[/]" if pet.sick else "[bright_green]❤️  OK[/]")

    if pet.needs_attention:
        table.add_row("Attention", f"[bold red]❗ {pet.attention_reason.upper()}[/]")

    border_color = {
        "happy": "bright_green", "hungry": "orange3",
        "unhappy": "blue", "sick": "red", "sleeping": "grey50", "dead": "grey30"
    }.get(pet.mood.value, "bright_white")

    console.print(Panel(table, title=f"[bold]{pet.name}[/]",
                         border_style=border_color, width=38))


def _cmd_share(args: list[str]) -> None:
    """Generate a shareable ASCII card of your pet.

    Usage:
        tama share              # print card to stdout
        tama share --copy       # copy to clipboard
        tama share --save       # save as <name>_card.txt
        tama share --name Pixel # share a specific pet
    """
    from tamagotchi.cli.share import run_share
    run_share(args)


def _cmd_install(args: list[str]) -> None:
    """Auto-detect AI coding agents and wire tamagotchi hooks.

    Usage:
        tama install              # interactive (detect + confirm)
        tama install --all        # install all detected, no prompts
        tama install --claude-code --aider --goose --starship --tmux
        tama install --dry-run    # preview only
    """
    from tamagotchi.cli.install import run_install
    run_install(args)


if __name__ == "__main__":
    main()
