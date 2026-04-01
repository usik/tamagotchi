# Contributing to Tamagotchi

Thanks for being here. This is an early-stage project with a lot of room to grow — your contribution, however small, genuinely matters.

---

## Your First PR in 10 Minutes

The fastest way to contribute is to add or improve an ASCII sprite. No architecture knowledge needed.

1. Fork the repo and clone it
   ```bash
   git clone https://github.com/<your-username>/tamagotchi
   cd tamagotchi
   uv sync
   uv run tama   # make sure it runs
   ```

2. Open `src/tamagotchi/sprites/ascii.py`

3. Find a character you want to improve (e.g. `ADULT_GOOD_HAPPY`) and redraw it. Each sprite is 13 chars wide × 7 lines tall:
   ```python
   MY_SPRITE = _pad([
       "   .-----.   ",
       "  ( ^   ^ )  ",
       "  (  ___  )  ",
       "   '-----'   ",
       "    |   |    ",
       "   /     \\   ",
       "  /       \\  ",
   ])
   ```

4. Run `uv run tama` to see it live, then open a PR

That's it.

---

## What We Need Help With

### 🎨 Good first issues — no deep knowledge required
- **Better ASCII sprites** — the current art is functional but rough. Redraw any character.
- **New idle animations** — add a second frame to any character that only has one
- **Sprite for sick/sleeping** — most characters share the baby sick/sleep sprite. Unique ones per stage would be great.

### 🔌 Plugin contributions — medium effort
Each of these is a self-contained plugin file. You only need to understand the `BasePlugin` interface.
- **Cursor plugin** — hook into Cursor agent JSONL logs (`~/.cursor/logs/`)
- **GitHub Copilot plugin** — monitor Copilot completions via VS Code extension logs
- **Git plugin** — react to commits, merges, rebases (read `.git/` events)
- **CI/CD plugin** — poll GitHub Actions / CircleCI API for pipeline results

See `plugins/claude_code/plugin.py` as the reference implementation.

### 🎮 Mechanics — medium effort
- **Mini-game for Play** — a simple reaction or guess game rendered in Textual
- **Pet graveyard screen** — a TUI screen showing deceased pets with their stats
- **Multiple pet slots** — switch between more than one pet
- **`tama status` CLI command** — print pet stats without launching the full TUI

### 🌐 Phase 3 — larger effort (coordinate first)
- **WebSocket peer sync** — the server that lets terminals find each other
- **The Lounge** — the 2D web world (Next.js + Canvas)
- **mDNS peer discovery** — LAN-only, no server needed

---

## How to Contribute

1. **Check existing issues** before starting — someone may already be working on it
2. **For big changes**, open an issue first to discuss the approach
3. **For small changes** (sprites, typos, docs), just open a PR directly

### Branch naming
```
feat/cursor-plugin
fix/poop-decay-bug
sprite/adult-good-rework
docs/contributing-guide
```

### Commit style
```
feat: add Cursor agent plugin
fix: poop count not resetting after flush
sprite: redraw adult_good idle animation
docs: add plugin development guide
```

### PR checklist
- [ ] `uv run pytest` passes (49+ tests)
- [ ] New behavior has a test in `tests/test_core.py`
- [ ] Sprites use `_pad()` and are exactly 13×7
- [ ] No new dependencies added without discussion

---

## Running Tests

```bash
uv run pytest           # run all tests
uv run pytest -v        # verbose output
uv run pytest -k sprite # run only sprite tests
```

---

## Project Structure

```
tamagotchi/
├── src/tamagotchi/
│   ├── core/           # Pet engine — touch this carefully, tests required
│   │   ├── pet.py      # Stats, lifecycle, actions, decay, death
│   │   ├── evolution.py  # Evolution tree and character names
│   │   └── persistence.py  # Save/load JSON
│   ├── ui/             # Textual TUI — screens and widgets
│   │   ├── screens/    # MainScreen, NewPetScreen, HelpScreen
│   │   └── widgets/    # PetDisplay, StatBars, ActionMenu
│   ├── sprites/
│   │   └── ascii.py    # All ASCII art — safest place to start
│   └── plugins/
│       ├── base.py     # BasePlugin — read this before writing a plugin
│       └── __init__.py # Plugin loader
├── plugins/
│   └── claude_code/    # Reference plugin implementation
└── tests/
    └── test_core.py    # All tests live here for now
```

---

## Compensation & Recognition

This project is early but we want to be transparent about how contributors are valued.

**Right now:**
- Every contributor gets named in `CONTRIBUTORS.md` and release notes
- Major contributors (merged features, plugins) get a shoutout on launch posts
- When the social world ships (Phase 3), top contributors get a **named character** in the world — your pet design, permanently in the game

**When revenue starts (Phase 4):**
- 10% of monthly revenue goes into a contributor pool, distributed via [Open Collective](https://opencollective.com) based on merged contributions
- Transparent, public accounting — you can see exactly what's in the pool and how it's split
- Bounties will be posted for specific high-priority work (watch for `bounty` label on issues)

**Long term:**
- If this grows into a real company, top contributors are the first people we talk to about joining

---

## Contributor License Agreement (CLA)

By submitting a pull request you agree that:

1. Your contribution is your original work (or you have the right to submit it)
2. You grant the project maintainer a perpetual, worldwide, non-exclusive, royalty-free license to use, modify, and redistribute your contribution under any license — including future license changes (e.g. a dual MIT / AGPL model when the platform ships)
3. You understand this project may eventually have a commercial component, and your contribution may be included in that

This is a lightweight CLA — no forms to sign. Submitting a PR is your agreement.

**Why this matters:** Without this, we can't change the license later without tracking down every contributor. With it, we stay flexible as the project grows.

---

## Code of Conduct

Be kind. This is a fun project — keep it that way. We won't tolerate harassment, gatekeeping, or dismissiveness toward new contributors.

If something feels off, open an issue or email the maintainer directly.

---

## Questions?

Open a [GitHub Discussion](https://github.com/usik/tamagotchi/discussions) or drop a message in an issue. We respond fast.
