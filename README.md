# 🥚 Tamagotchi — Terminal Virtual Pet

> Raise a virtual pet that lives in your terminal. A faithful recreation of the original Tamagotchi — hunger, happiness, sickness, poop, discipline, and care-driven evolution — built for developers who never leave the CLI.

![Python](https://img.shields.io/badge/python-3.12+-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/status-alpha-orange?style=flat-square)

![Tamagotchi demo](docs/assets/demo.gif)

```
╔═══════════════════════════════════════════════╗
║                                               ║
║     .-----.        Hunger   ████████  4/4     ║
║    ( ^   ^ )       Happy    ████████  4/4     ║
║    (  ___  )       Weight   ████░░░░  12      ║
║     '-----'        Discpln  ██████░░  75%     ║
║     _| | |_        Health   ❤️  OK            ║
║                                               ║
║  🍱 Meal  🍬 Snack  ⭐ Play  🚿 Clean         ║
║  💊 Med   📣 Disc   💡 Light 📊 Status        ║
╚═══════════════════════════════════════════════╝
```

---

## Features

- **Full Tamagotchi mechanics** — Hunger, Happiness, Weight, Discipline, Health, Poop, Sickness, Lights/Sleep
- **6 life stages** — Egg → Baby → Child → Teen → Adult → Elder
- **Care-driven evolution** — 3 paths (Good / Normal / Poor) based on how well you care for your pet
- **Real-time aging** — pet lives on even when the game is closed
- **Animated ASCII sprites** — unique art per character and mood
- **Plugin system** — extend with your own plugins or hook into AI coding agents
- **Claude Code plugin** — pet reacts to what your AI agent is doing (shipping, looping, stuck, celebrating)
- **Auto-save** — state persists to `~/.tamagotchi/`

---

## Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1** — Core Tamagotchi | ✅ In progress | Full pet mechanics, TUI, plugin system |
| **Phase 2** — AI Agent Awareness | 🔜 Planned | Claude Code, Cursor, Copilot plugins |
| **Phase 3** — Peer Discovery | 🔜 Planned | Pets visit each other over LAN / Tailscale |
| **Phase 4** — Social Platform | 💭 Vision | Developer identity, team leaderboards, pet history |

---

## Install

```bash
# With uv (recommended)
uv tool install tamagotchi

# With pip
pip install tamagotchi
```

## Run

```bash
tama
# or
tamagotchi
```

---

## Controls

| Key | Action |
|-----|--------|
| `← →` | Navigate action menu |
| `Enter` | Confirm selected action |
| `M` | Feed meal (restores hunger) |
| `S` | Feed snack (boosts happiness) |
| `P` | Play (boosts happiness, lowers weight) |
| `C` | Clean poop |
| `D` | Give medicine |
| `I` | Discipline |
| `L` | Toggle lights (pet sleeps) |
| `T` | Show status |
| `Ctrl+S` | Save |
| `Q` | Save and quit |
| `?` | Help |

---

## Life Stages & Evolution

```
Egg (5min) → Baby (1h) → Child (8h) → Teen (1d) → Adult (3d) → Elder (2d) → Death
```

Evolution at each stage is driven by **care mistakes**:

| Path | Condition | Adult form | Elder form |
|------|-----------|------------|------------|
| Good | < 2 mistakes | Mimitchi | Ojitchi |
| Normal | 2–4 mistakes | Mametchi | Otokitchi |
| Poor | 5+ mistakes | Maskutchi | Tarakotchi |

**Care mistakes** happen when you:
- Overfeed (meal when hunger is already full)
- Give medicine when the pet isn't sick
- Ignore an attention call for too long

---

## Claude Code Plugin

Wire up Claude Code hooks so your pet reacts to your AI agent's behavior in real time.

**1. Add hooks to `~/.claude/settings.json`:**

```json
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

**2. Pet reactions:**

| Agent state | Pet reaction |
|-------------|-------------|
| Shipping code | Happy +1 |
| Stuck in a loop | Happy −1, Hungry −1 |
| Hitting repeated errors | Happy −1 |
| Tests pass | Happy +2 🎉 |
| Tests fail | Happy −1 |
| Task complete | Happy +2 |

---

## Plugin Development

Drop a `.py` file in `~/.tamagotchi/plugins/` — no install needed.

```python
# ~/.tamagotchi/plugins/my_plugin.py
from tamagotchi.plugins.base import BasePlugin

class MyPlugin(BasePlugin):
    name = "my_plugin"
    description = "Does something cool"

    def on_tick(self, pet):
        """Called every second."""
        pass

    def on_evolve(self, pet, old_stage, new_stage):
        """Called when pet evolves."""
        print(f"{pet.name} evolved to {new_stage}!")

    def on_agent_event(self, event_type, data):
        """React to AI coding agent events."""
        if event_type == "test_passed":
            pet.happy = min(4, pet.happy + 1)

    def on_peer_visit(self, visitor_pet):
        """Called when a peer's pet comes to visit (Phase 3)."""
        pass
```

Or register via `pyproject.toml` entry points for distributable plugins:

```toml
[project.entry-points."tamagotchi.plugins"]
my_plugin = "my_package.plugin:MyPlugin"
```

---

## Development Setup

```bash
git clone https://github.com/usik/tamagotchi
cd tamagotchi
uv sync --dev
uv run pytest          # run tests
uv run tama            # run the game
```

---

## Contributing

Contributions are welcome — whether it's a bug fix, a new ASCII sprite, a plugin, or a feature from the roadmap.

### How to contribute

1. **Fork** the repo and create a branch from `main`
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes.** Keep these in mind:
   - Run `uv run pytest` and make sure all tests pass
   - Add tests for new behavior in `tests/`
   - Keep sprites in `src/tamagotchi/sprites/ascii.py`
   - Keep new plugins in `plugins/` (built-in) or document how to install as external

3. **Open a pull request** with a clear description of what you changed and why

### Good first contributions

| Area | Ideas |
|------|-------|
| 🎨 **Sprites** | New ASCII art for existing characters, better idle animations |
| 🔌 **Plugins** | Cursor plugin, GitHub Copilot plugin, WakaTime integration |
| 🎮 **Mechanics** | Mini-game for the Play action, better discipline logic |
| 🌐 **Phase 3** | Peer discovery via mDNS or Tailscale, pet visit protocol |
| 🧪 **Tests** | More coverage for edge cases, async tick tests |
| 📖 **Docs** | Better plugin docs, video demo, wiki |

### Project structure

```
tamagotchi/
├── src/tamagotchi/
│   ├── core/           # Pet engine — stats, evolution, persistence
│   ├── ui/             # Textual TUI — screens and widgets
│   │   ├── screens/    # MainScreen, NewPetScreen, HelpScreen
│   │   └── widgets/    # PetDisplay, StatBars, ActionMenu
│   ├── sprites/        # ASCII art for all characters and moods
│   └── plugins/        # Plugin loader and BasePlugin
├── plugins/
│   └── claude_code/    # Built-in Claude Code integration
└── tests/              # pytest test suite
```

### Plugin ideas we'd love to see

- **Cursor plugin** — hooks into Cursor agent events
- **GitHub Copilot plugin** — reacts to Copilot completions
- **Git plugin** — pet reacts to commits, merges, rebases
- **CI/CD plugin** — pet celebrates passing pipelines, mourns failures
- **Peer discovery** (Phase 3) — pets visit each other over a local network

### Code of conduct

Be kind. This is a fun project — keep it that way.

---

## License

MIT — do whatever you want with it.
