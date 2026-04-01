"""
Aider Plugin for Tamagotchi.

Reads events from ~/.tamagotchi/aider_events.jsonl and reacts to
Aider coding sessions — commit events, error events, session start/stop.

Setup (automatic):
    tama install --aider

Manual setup — add to ~/.aider.conf.yml:
    pre-commit-cmd: tama-hook pre-tool bash
    post-commit-cmd: tama-hook post-tool bash 0
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from tamagotchi.plugins.base import BasePlugin
from tamagotchi.core.pet import Pet

AIDER_EVENT_FILE = Path.home() / ".tamagotchi" / "aider_events.jsonl"

# Reactions: aider tends to be commit-by-commit, so we reward commits directly
AIDER_REACTIONS = {
    "commit":        {"happy_delta": +1, "hunger_delta":  0},
    "session_start": {"happy_delta":  0, "hunger_delta":  0},
    "stop_success":  {"happy_delta": +1, "hunger_delta": +1},
    "stop_error":    {"happy_delta": -1, "hunger_delta":  0},
    "lint_error":    {"happy_delta": -1, "hunger_delta":  0},
    "test_pass":     {"happy_delta": +2, "hunger_delta": +1},
    "test_fail":     {"happy_delta": -1, "hunger_delta":  0},
}


class AiderPlugin(BasePlugin):
    name = "aider"
    description = "Reacts to Aider coding agent sessions"
    version = "0.1.0"

    def __init__(self):
        self._last_line = 0

    def on_load(self) -> None:
        AIDER_EVENT_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not AIDER_EVENT_FILE.exists():
            AIDER_EVENT_FILE.touch()

    def on_tick(self, pet: Pet) -> None:
        if not AIDER_EVENT_FILE.exists():
            return
        lines = AIDER_EVENT_FILE.read_text().splitlines()
        new_lines = lines[self._last_line:]
        self._last_line = len(lines)

        for line in new_lines:
            try:
                event = json.loads(line)
                self._apply(pet, event)
            except Exception:
                pass

    def _apply(self, pet: Pet, event: dict) -> None:
        etype = event.get("type", "")
        reaction = AIDER_REACTIONS.get(etype)
        if reaction:
            pet.happy  = max(0, min(4, pet.happy  + reaction["happy_delta"]))
            pet.hunger = max(0, min(4, pet.hunger + reaction["hunger_delta"]))
