# 🥚 Tamagotchi — Terminal Virtual Pet

A faithful Tamagotchi recreation that lives in your terminal. Raise a virtual pet through 6 life stages, with full original mechanics — hunger, happiness, weight, discipline, sickness, poop, and care-driven evolution.

Built for developers who live in the terminal. Phase 2 brings AI coding agent awareness. Phase 3 brings peer-to-peer pet visits.

```
╔═══════════════════════════╗
║   TAMAGOTCHI              ║
║   terminal virtual pet    ║
╚═══════════════════════════╝
```

## Features

**Full Tamagotchi mechanics**
- 6 life stages: Egg → Baby → Child → Teen → Adult → Elder
- Stats: Hunger, Happiness, Weight, Discipline, Health
- Care-driven evolution — 3 paths (Good / Normal / Poor) per stage
- Real-time aging — pet lives on even when game is closed
- Sickness, poop, attention system, discipline
- Lights on/off (pet sleeps)
- Auto-save every 30 seconds

**Terminal-native TUI**
- Animated ASCII sprites per character and mood
- Color-coded stat bars
- 8-icon action menu (original button layout)
- Event log with real-time updates

**Plugin system**
- Extend via Python entry points or `~/.tamagotchi/plugins/`
- Built-in Claude Code plugin — pet reacts to agent behavior
- Hook events: shipping, looping, exploring, blocked, tests pass/fail

## Install

```bash
# With uv (recommended)
uv tool install tamagotchi

# Or pip
pip install tamagotchi
```

## Run

```bash
tama
# or
tamagotchi
```

## Controls

| Key | Action |
|-----|--------|
| `M` | Feed meal (hunger) |
| `S` | Feed snack (happy) |
| `P` | Play (happy + weight) |
| `C` | Clean poop |
| `D` | Give medicine |
| `I` | Discipline |
| `L` | Toggle lights |
| `T` | Show status |
| `← →` | Browse action menu |
| `Enter` | Confirm action |
| `?` | Help |
| `Q` | Save and quit |

## Life Stages & Evolution

```
Egg (5min) → Baby (1h) → Child (8h) → Teen (1d) → Adult (3d) → Elder (2d) → Death
```

Evolution at each stage depends on **care mistakes**:
- `< 2 mistakes` → Good path (Mimitchi, Ojitchi)
- `2–4 mistakes` → Normal path (Mametchi, Otokitchi)
- `5+ mistakes`  → Poor path (Maskutchi, Tarakotchi)

Care mistakes happen when you:
- Overfeed (hunger already full)
- Give medicine when healthy
- Ignore attention calls

## Claude Code Plugin

Wire up Claude Code hooks so your pet reacts to what your AI agent is doing:

```json
// ~/.claude/settings.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "",
      "hooks": [{"type": "command", "command": "tama-hook post-tool $CLAUDE_TOOL_NAME $CLAUDE_TOOL_EXIT_CODE"}]
    }],
    "Stop": [{
      "matcher": "",
      "hooks": [{"type": "command", "command": "tama-hook stop $CLAUDE_STOP_REASON"}]
    }]
  }
}
```

Behavioral states your pet reacts to:
| State | Pet reaction |
|-------|-------------|
| SHIPPING | Happy +1 (Claude is writing code) |
| LOOPING | Happy -1, Hungry -1 (Claude is stuck) |
| BLOCKED | Happy -1 (repeated errors) |
| TESTS PASS | Happy +2 (celebrates!) |
| TESTS FAIL | Happy -1 |
| DONE | Happy +2 (task complete) |

## Plugin Development

```python
# ~/.tamagotchi/plugins/my_plugin.py
from tamagotchi.plugins.base import BasePlugin

class MyPlugin(BasePlugin):
    name = "my_plugin"
    description = "Does something cool"

    def on_tick(self, pet):
        # Called every second
        pass

    def on_agent_event(self, event_type, data):
        # React to AI agent events
        if event_type == "test_passed":
            pet.happy = min(4, pet.happy + 1)
```

## Roadmap

- [x] Phase 1 — Core Tamagotchi (this release)
- [ ] Phase 2 — AI agent awareness (Claude Code, Cursor, Copilot plugins)
- [ ] Phase 3 — Peer discovery (pets visit each other over LAN/Tailscale)
- [ ] Phase 4 — Social platform (developer identity, pet history, team leaderboards)

## Development

```bash
git clone https://github.com/yourusername/tamagotchi
cd tamagotchi
uv sync --dev
uv run pytest
uv run tama
```

## License

MIT
