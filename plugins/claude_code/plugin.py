"""
Claude Code Plugin for Tamagotchi.

Hooks into Claude Code's event system to feed behavioral signals
to the pet engine.

Setup:
  1. Install this plugin: `uv pip install -e ".[claude-code]"`
  2. Add hooks to your ~/.claude/settings.json:

  {
    "hooks": {
      "PreToolUse": [{
        "matcher": "",
        "hooks": [{"type": "command", "command": "tama-hook pre-tool $CLAUDE_TOOL_NAME"}]
      }],
      "PostToolUse": [{
        "matcher": "",
        "hooks": [{"type": "command", "command": "tama-hook post-tool $CLAUDE_TOOL_NAME $CLAUDE_TOOL_EXIT_CODE"}]
      }],
      "Stop": [{
        "matcher": "",
        "hooks": [{"type": "command", "command": "tama-hook stop $CLAUDE_STOP_REASON"}]
      }],
      "SubagentStart": [{
        "matcher": "",
        "hooks": [{"type": "command", "command": "tama-hook subagent-start"}]
      }]
    }
  }

Behavioral classification:
  SHIPPING  — agent writing files / running tests that pass
  LOOPING   — same tool called 5+ times without a write
  EXPLORING — reading many files without writing
  BLOCKED   — permission denied / errors accumulating
  DONE      — Stop event with success reason
"""
from __future__ import annotations

import json
import time
from collections import Counter, deque
from pathlib import Path
from typing import Any

from tamagotchi.plugins.base import BasePlugin
from tamagotchi.core.pet import Pet


# Path where Claude Code hook script writes events
HOOK_EVENT_FILE = Path.home() / ".tamagotchi" / "claude_events.jsonl"


class AgentBehaviorClassifier:
    """
    Classifies Claude Code agent behavior from a stream of tool events.
    Uses a rolling window of recent tool calls.
    """

    WINDOW = 20  # analyze last N tool calls

    def __init__(self):
        self._tool_calls: deque[dict] = deque(maxlen=self.WINDOW)
        self._last_write_at: float = 0
        self._error_count: int = 0
        self._loop_counter: Counter = Counter()

    def record_tool_call(self, tool: str, exit_code: int = 0) -> str:
        """Record a tool call and return current behavioral state."""
        now = time.time()
        self._tool_calls.append({"tool": tool, "ts": now, "exit": exit_code})
        self._loop_counter[tool] += 1

        if tool in ("write_file", "edit_file", "bash") and exit_code == 0:
            self._last_write_at = now
            self._loop_counter.clear()

        if exit_code != 0:
            self._error_count += 1
        else:
            self._error_count = max(0, self._error_count - 1)

        return self.classify()

    def classify(self) -> str:
        if self._error_count >= 5:
            return "BLOCKED"
        if any(count >= 5 for count in self._loop_counter.values()):
            return "LOOPING"
        recent_tools = [e["tool"] for e in self._tool_calls]
        write_tools = {"write_file", "edit_file", "bash", "str_replace_editor"}
        read_tools = {"read_file", "list_dir", "grep", "glob"}
        writes = sum(1 for t in recent_tools if t in write_tools)
        reads = sum(1 for t in recent_tools if t in read_tools)
        if writes > reads:
            return "SHIPPING"
        if reads > 5 and writes == 0:
            return "EXPLORING"
        return "WORKING"


# Pet reactions to behavioral states
BEHAVIOR_REACTIONS = {
    "SHIPPING": {
        "happy_delta":    +1,
        "hunger_delta":   -0,
        "message":        "🚀 {name} is excited watching Claude ship code!",
    },
    "LOOPING": {
        "happy_delta":    -1,
        "hunger_delta":   -1,
        "message":        "😰 {name} is anxious — Claude seems stuck in a loop...",
    },
    "EXPLORING": {
        "happy_delta":    0,
        "hunger_delta":   0,
        "message":        "🔍 {name} watches Claude explore the codebase...",
    },
    "BLOCKED": {
        "happy_delta":    -1,
        "hunger_delta":   -1,
        "message":        "😤 {name} is frustrated — Claude keeps hitting errors!",
    },
    "WORKING": {
        "happy_delta":    0,
        "hunger_delta":   0,
        "message":        "👀 {name} watches Claude work...",
    },
    "DONE_SUCCESS": {
        "happy_delta":    +2,
        "hunger_delta":   +1,
        "message":        "🎉 {name} celebrates! Claude finished the task!",
    },
    "DONE_FAILURE": {
        "happy_delta":    -1,
        "hunger_delta":   -1,
        "message":        "😔 {name} is sad... Claude couldn't finish.",
    },
    "TESTS_PASSED": {
        "happy_delta":    +2,
        "hunger_delta":   +1,
        "message":        "✅ {name} does a happy dance! All tests pass!",
    },
    "TESTS_FAILED": {
        "happy_delta":    -1,
        "hunger_delta":   0,
        "message":        "❌ {name} frowns... tests are failing.",
    },
}


class ClaudeCodePlugin(BasePlugin):
    """
    Reads Claude Code hook events and applies them to pet behavior.
    """

    name = "claude_code"
    description = "Reacts to Claude Code agent behavior"
    version = "0.1.0"

    def __init__(self):
        self._classifier = AgentBehaviorClassifier()
        self._last_event_line = 0
        self._last_behavior = "WORKING"
        self._behavior_tick = 0

    def on_load(self) -> None:
        HOOK_EVENT_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not HOOK_EVENT_FILE.exists():
            HOOK_EVENT_FILE.touch()

    def on_tick(self, pet: Pet) -> None:
        """Poll for new Claude Code hook events every tick."""
        self._poll_events(pet)
        self._behavior_tick += 1
        # Apply behavior effect every 60 ticks (~1 min)
        if self._behavior_tick % 60 == 0:
            self._apply_behavior(pet, self._last_behavior)

    def _poll_events(self, pet: Pet) -> None:
        """Read new lines from the hook event file."""
        if not HOOK_EVENT_FILE.exists():
            return
        lines = HOOK_EVENT_FILE.read_text().splitlines()
        new_lines = lines[self._last_event_line:]
        self._last_event_line = len(lines)

        for line in new_lines:
            try:
                event = json.loads(line)
                self._process_event(pet, event)
            except Exception:
                pass

    def _process_event(self, pet: Pet, event: dict) -> None:
        etype = event.get("type", "")
        if etype == "pre_tool":
            pass  # pre-tool — not actionable yet
        elif etype == "post_tool":
            tool = event.get("tool", "unknown")
            exit_code = event.get("exit_code", 0)
            behavior = self._classifier.record_tool_call(tool, exit_code)
            self._last_behavior = behavior
            # Test detection
            if tool == "bash" and "pytest" in event.get("command", ""):
                if exit_code == 0:
                    self.on_agent_event("test_passed", event)
                else:
                    self.on_agent_event("test_failed", event)
        elif etype == "stop":
            reason = event.get("reason", "")
            if reason in ("task_complete", "success"):
                self.on_agent_event("task_complete", event)
            else:
                self.on_agent_event("task_failed", event)
        elif etype == "subagent_start":
            # Subagent spawned — pet gets anxious
            pet.happy = max(0, pet.happy - 1)

    def on_agent_event(self, event_type: str, data: dict[str, Any]) -> None:
        # This gets called by _process_event above and by the plugin manager
        pass  # Reactions handled via behavior classification

    def _apply_behavior(self, pet: Pet, behavior: str) -> None:
        reaction = BEHAVIOR_REACTIONS.get(behavior, BEHAVIOR_REACTIONS["WORKING"])
        pet.happy  = max(0, min(4, pet.happy  + reaction["happy_delta"]))
        pet.hunger = max(0, min(4, pet.hunger + reaction["hunger_delta"]))


# ---------------------------------------------------------------------------
# Hook CLI script — called by Claude Code hooks
# ---------------------------------------------------------------------------
# This is a separate entry point: `tama-hook`
# Claude Code hook commands write events to HOOK_EVENT_FILE as JSONL

def hook_main() -> None:
    """CLI called by Claude Code hook commands. Writes events to JSONL file."""
    import sys
    args = sys.argv[1:]
    if not args:
        return

    HOOK_EVENT_FILE.parent.mkdir(parents=True, exist_ok=True)
    event: dict = {"ts": time.time()}

    if args[0] == "pre-tool" and len(args) >= 2:
        event.update({"type": "pre_tool", "tool": args[1]})
    elif args[0] == "post-tool" and len(args) >= 3:
        event.update({"type": "post_tool", "tool": args[1], "exit_code": int(args[2])})
    elif args[0] == "stop" and len(args) >= 2:
        event.update({"type": "stop", "reason": args[1]})
    elif args[0] == "subagent-start":
        event.update({"type": "subagent_start"})

    with HOOK_EVENT_FILE.open("a") as f:
        f.write(json.dumps(event) + "\n")
