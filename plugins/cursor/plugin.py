"""
Cursor Plugin for Tamagotchi.

Tails Cursor agent logs to feed behavioral signals to the pet engine.

Setup:
  1. Install this plugin: `uv pip install -e ".[cursor]"`
  2. The plugin automatically looks for logs in `~/.cursor/logs/*.jsonl`

Behavioral classification:
  SHIPPING  — agent writing files / running tests that pass
  LOOPING   — same tool called 5+ times without a write
  EXPLORING — reading many files without writing
  BLOCKED   — permission denied / errors accumulating
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from tamagotchi.plugins.base import BasePlugin, AgentBehaviorClassifier
from tamagotchi.core.pet import Pet


# Path where Cursor writes logs
CURSOR_LOG_DIR = Path.home() / ".cursor" / "logs"

# Reuse reactions from Claude Code (could be shared, but copying for isolation)
BEHAVIOR_REACTIONS = {
    "SHIPPING": {
        "happy_delta":    +1,
        "hunger_delta":   -0,
        "message":        "🚀 {name} is excited watching Cursor ship code!",
    },
    "LOOPING": {
        "happy_delta":    -1,
        "hunger_delta":   -1,
        "message":        "😰 {name} is anxious — Cursor seems stuck in a loop...",
    },
    "EXPLORING": {
        "happy_delta":    0,
        "hunger_delta":   0,
        "message":        "🔍 {name} watches Cursor explore the codebase...",
    },
    "BLOCKED": {
        "happy_delta":    -1,
        "hunger_delta":   -1,
        "message":        "😤 {name} is frustrated — Cursor keeps hitting errors!",
    },
    "WORKING": {
        "happy_delta":    0,
        "hunger_delta":   0,
        "message":        "👀 {name} watches Cursor work...",
    },
}


class CursorPlugin(BasePlugin):
    """
    Reads Cursor JSONL logs and applies them to pet behavior.
    """

    name = "cursor"
    description = "Reacts to Cursor agent behavior"
    version = "0.1.0"

    def __init__(self):
        self._classifier = AgentBehaviorClassifier()
        self._last_processed_file: Path | None = None
        self._last_line_idx = 0
        self._last_behavior = "WORKING"
        self._behavior_tick = 0

    def on_load(self) -> None:
        if not CURSOR_LOG_DIR.exists():
            # Graceful no-op if Cursor isn't installed
            return

    def on_tick(self, pet: Pet) -> None:
        """Poll for new Cursor log events every tick."""
        self._poll_logs(pet)
        self._behavior_tick += 1
        # Apply behavior effect every 60 ticks (~1 min)
        if self._behavior_tick % 60 == 0:
            self._apply_behavior(pet, self._last_behavior)

    def _poll_logs(self, pet: Pet) -> None:
        """Find the latest JSONL log file and read new lines."""
        if not CURSOR_LOG_DIR.exists():
            return

        # Find latest .jsonl file
        log_files = sorted(CURSOR_LOG_DIR.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
        if not log_files:
            return
        
        latest_file = log_files[-1]
        
        if latest_file != self._last_processed_file:
            self._last_processed_file = latest_file
            self._last_line_idx = 0

        try:
            lines = latest_file.read_text().splitlines()
            new_lines = lines[self._last_line_idx:]
            self._last_line_idx = len(lines)

            for line in new_lines:
                try:
                    event = json.loads(line)
                    self._process_event(pet, event)
                except Exception:
                    pass
        except Exception:
            pass

    def _process_event(self, pet: Pet, event: dict) -> None:
        # Map Cursor log fields to classifier
        # Typical fields: toolName, status/exitCode, or type
        tool = event.get("toolName") or event.get("tool") or event.get("command")
        if not tool:
            return

        exit_code = 0
        if "exitCode" in event:
            exit_code = int(event["exitCode"])
        elif "status" in event and event["status"] == "error":
            exit_code = 1

        behavior = self._classifier.record_tool_call(tool, exit_code)
        self._last_behavior = behavior

    def _apply_behavior(self, pet: Pet, behavior: str) -> None:
        reaction = BEHAVIOR_REACTIONS.get(behavior, BEHAVIOR_REACTIONS["WORKING"])
        pet.happy  = max(0, min(4, pet.happy  + reaction["happy_delta"]))
        pet.hunger = max(0, min(4, pet.hunger + reaction["hunger_delta"]))
