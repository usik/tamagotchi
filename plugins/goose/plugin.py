"""
Goose Plugin for Tamagotchi (Block's AI coding agent).

Reads events from ~/.tamagotchi/goose_events.jsonl written by the
shell shim installed via `tama install --goose`.

The shim wraps the `goose` command and records session start/stop.
Within a session, longer tool call sequences are inferred from timing.

Setup (automatic):
    tama install --goose

Manual setup:
    See integrations/goose/README.md
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from tamagotchi.plugins.base import BasePlugin
from tamagotchi.core.pet import Pet

GOOSE_EVENT_FILE = Path.home() / ".tamagotchi" / "goose_events.jsonl"

# Infer session length from timestamps
SHORT_SESSION  = 60   # < 1 min — probably just a check
MEDIUM_SESSION = 300  # 1–5 min — real work
LONG_SESSION   = 900  # > 15 min — deep work


class GoosePlugin(BasePlugin):
    name = "goose"
    description = "Reacts to Goose (Block) agent sessions"
    version = "0.1.0"

    def __init__(self):
        self._last_line = 0
        self._session_start: float | None = None

    def on_load(self) -> None:
        GOOSE_EVENT_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not GOOSE_EVENT_FILE.exists():
            GOOSE_EVENT_FILE.touch()

    def on_tick(self, pet: Pet) -> None:
        if not GOOSE_EVENT_FILE.exists():
            return
        lines = GOOSE_EVENT_FILE.read_text().splitlines()
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
        ts = event.get("ts", time.time())

        if etype == "session_start":
            self._session_start = ts

        elif etype == "stop":
            reason = event.get("reason", "error")
            duration = (ts - self._session_start) if self._session_start else 0
            self._session_start = None

            if reason == "success":
                if duration >= LONG_SESSION:
                    # Long successful session — big reward
                    pet.happy  = min(4, pet.happy + 2)
                    pet.hunger = min(4, pet.hunger + 1)
                elif duration >= MEDIUM_SESSION:
                    pet.happy = min(4, pet.happy + 1)
                # short sessions — no change
            else:
                # Failed session
                pet.happy = max(0, pet.happy - 1)

        elif etype == "tool_call":
            # Future: Goose exposes tool events via GOOSE_TOOLSHIM
            tool = event.get("tool", "")
            exit_code = event.get("exit_code", 0)
            if exit_code != 0:
                pet.happy = max(0, pet.happy - 1)
