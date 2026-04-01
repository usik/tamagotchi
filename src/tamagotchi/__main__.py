"""Entry point — `tama` or `tamagotchi` CLI command."""
import sys
from pathlib import Path


def main() -> None:
    from tamagotchi.ui.app import TamagotchiApp
    app = TamagotchiApp()
    app.run()


if __name__ == "__main__":
    main()
