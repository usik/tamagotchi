"""
tama share — generate a shareable ASCII card of your pet.

Usage:
    tama share              # print card to stdout
    tama share --copy       # copy to clipboard
    tama share --save       # save card.txt to current directory
    tama share --gist       # upload to GitHub Gist, get embed URL
    tama share --name Pixel # share a specific pet
"""
from __future__ import annotations

import sys
from pathlib import Path


HEARTS = ["♡", "♥"]
MOOD_ICONS = {
    "happy":    "😊",
    "neutral":  "😐",
    "hungry":   "😋",
    "unhappy":  "😢",
    "sick":     "🤒",
    "sleeping": "💤",
    "dead":     "💀",
}


def _hearts(val: int, max_val: int = 4) -> str:
    return "".join(HEARTS[1] if i < val else HEARTS[0] for i in range(max_val))


def _build_card(pet) -> str:
    from tamagotchi.core.evolution import CHARACTER_NAMES
    from tamagotchi.sprites.ascii import get_sprite

    char_name  = CHARACTER_NAMES.get(pet.character, pet.character.value)
    mood_icon  = MOOD_ICONS.get(pet.mood.value, "😐")
    sprite     = get_sprite(pet.character, pet.mood)

    # Card is 37 chars wide inside the border
    W = 37

    def center(text: str) -> str:
        # Center plain text (strip ANSI for length calc, but we have none here)
        pad = max(0, W - len(text))
        return " " * (pad // 2) + text + " " * (pad - pad // 2)

    def row(label: str, value: str) -> str:
        gap = W - len(label) - len(value)
        return label + " " * max(1, gap) + value

    top    = "┌" + "─" * W + "┐"
    bottom = "└" + "─" * W + "┘"
    div    = "├" + "─" * W + "┤"

    def line(content: str = "") -> str:
        # Pad to width W, wrap in border
        visible_len = _visible_len(content)
        pad = max(0, W - visible_len)
        return "│" + content + " " * pad + "│"

    # Header
    stage_label = pet.stage.value.capitalize()
    header = center(f"  {pet.name}  •  {char_name}  •  {stage_label}  ")

    # Sprite lines (7 lines, 13 chars wide) — pad to left, stats to right
    sprite_lines = sprite  # list of 7 strings, each 13 chars

    stat_lines = [
        f"  Hunger   {_hearts(pet.hunger)}",
        f"  Happy    {_hearts(pet.happy)}",
        f"  Weight   {pet.weight}",
        f"  Age      {pet.age_display}",
        f"  Mood   {mood_icon} {pet.mood.value.capitalize()}",
        f"  Health   {'🤒 Sick' if pet.sick else '❤️  OK'}",
        "",
    ]

    # Combine sprite + stats side by side
    combined_lines = []
    for i in range(7):
        spr = sprite_lines[i] if i < len(sprite_lines) else " " * 13
        sta = stat_lines[i]   if i < len(stat_lines)   else ""
        content = "  " + spr + " " + sta
        combined_lines.append(line(content))

    # Footer
    footer1 = center("tamagotchi · github.com/usik/tamagotchi")

    card_lines = [
        top,
        line(header),
        div,
        *combined_lines,
        div,
        line(footer1),
        bottom,
    ]

    return "\n".join(card_lines)


def _visible_len(s: str) -> int:
    """Approximate visible length — counts emoji as 2 chars."""
    count = 0
    for ch in s:
        cp = ord(ch)
        # Emoji / wide chars
        if cp > 0x2E7F:
            count += 2
        else:
            count += 1
    return count


def run_share(args: list[str]) -> None:
    from tamagotchi.core.persistence import list_saved_pets, load_pet

    copy_mode = "--copy" in args
    save_mode = "--save" in args
    gist_mode = "--gist" in args

    # Resolve pet
    name = None
    if "--name" in args:
        idx = args.index("--name")
        if idx + 1 < len(args):
            name = args[idx + 1]

    if name is None:
        saved = list_saved_pets()
        if not saved:
            print("No pet found. Run `tama` to hatch one.")
            sys.exit(1)
        name = saved[0]

    pet = load_pet(name)
    if pet is None:
        print(f"Pet '{name}' not found.")
        sys.exit(1)

    pet.tick()

    card = _build_card(pet)

    # Always print
    print(card)
    print()

    share_text = f"{card}\n\nRaise your own at: github.com/usik/tamagotchi"

    if copy_mode:
        _copy_to_clipboard(card)
        print("✓ Copied to clipboard")

    if save_mode:
        out = Path(f"{pet.name.lower()}_card.txt")
        out.write_text(share_text)
        print(f"✓ Saved to {out}")

    if gist_mode:
        from tamagotchi.cli.share_gist import upload_gist, print_embed_instructions
        result = upload_gist(card, pet.name)
        if result:
            gist_url, raw_url = result
            print_embed_instructions(pet.name, gist_url, raw_url)

    if not copy_mode and not save_mode and not gist_mode:
        print("  tama share --copy   copy to clipboard")
        print("  tama share --save   save as <name>_card.txt")
        print("  tama share --gist   upload to GitHub Gist + README embed snippet")


def _copy_to_clipboard(text: str) -> None:
    import subprocess
    import platform

    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
        elif system == "Linux":
            # Try xclip, then xsel, then wl-copy (Wayland)
            for cmd in [["xclip", "-selection", "clipboard"],
                        ["xsel", "--clipboard", "--input"],
                        ["wl-copy"]]:
                try:
                    subprocess.run(cmd, input=text.encode(), check=True)
                    return
                except (FileNotFoundError, subprocess.CalledProcessError):
                    continue
            print("⚠️  No clipboard tool found (install xclip, xsel, or wl-copy)")
        elif system == "Windows":
            subprocess.run(["clip"], input=text.encode("utf-16"), check=True)
    except Exception as e:
        print(f"⚠️  Clipboard copy failed: {e}")
