# Show HN Draft

> Post to: https://news.ycombinator.com/submit
> Title limit: 80 chars. Body is optional but converts better with one.

---

## Title options (pick one)

**Option A** (feature-forward)
```
Show HN: Tamagotchi that lives in your terminal and reacts to your AI coding agent
```

**Option B** (curiosity-first)
```
Show HN: I built a Tamagotchi for the terminal — it watches Claude Code so you don't have to
```

**Option C** (short and punchy)
```
Show HN: Terminal Tamagotchi – raise a virtual pet in your CLI
```

Recommendation: **Option A**. It leads with the unique angle (AI agent awareness) which is what separates this from every other terminal pet project.

---

## Body

```
Hey HN,

I built a terminal Tamagotchi in Python — a faithful recreation of the original
mechanics (hunger, happiness, weight, discipline, sickness, poop, care-driven
evolution) that lives in your CLI as a Textual TUI.

The twist: it watches your AI coding agent.

If you use Claude Code, you can wire up hooks so the pet reacts to what the
agent is actually doing — not just that it's running. Pet gets excited when
tests pass, anxious when Claude loops on the same file five times, and
celebrates when the task is done. It classifies behavior as SHIPPING /
LOOPING / EXPLORING / BLOCKED and adjusts mood and stats accordingly.

Right now it's Phase 1: the core pet mechanics work, 49 tests pass, and the
Claude Code plugin is functional. The roadmap goes to a 2D virtual world
(Phase 3) where pets can hang out in named rooms — Coffee Chat, Fireside Chat,
The Lounge — with real-time movement and a social feed. The pet you raise in
the terminal becomes your avatar there, and its evolution path (how well you
cared for it) becomes a kind of developer identity.

Built with:
- Python 3.12 + Textual (TUI)
- Plugin system for AI agent integrations
- Real-time decay — pet ages even when the app is closed

Install: pip install tamagotchi (or uv tool install tamagotchi)
GitHub: https://github.com/usik/tamagotchi

Would love feedback on the mechanics, sprite art, and whether the AI agent
angle is actually useful or just a gimmick. Happy to answer questions about
the architecture.
```

---

## Posting tips

- Post Tuesday–Thursday, 9–11am US Eastern — highest HN traffic
- Don't post on a Monday or Friday
- Be in the thread for the first 2 hours to respond to comments — velocity in
  the first hour determines front page placement
- Don't defensively justify design choices in comments — just say "good point,
  noted" or explain the reasoning briefly
- If someone says it already exists, acknowledge it and explain the
  differentiation (ccpet, termagotchi, vscode-pets all have meaningful gaps
  vs this — see COMPETITIVE_ANALYSIS.md)

## Cross-post after HN (same day or next day)

1. Reddit r/commandline — paste the body, add a screenshot or GIF
2. Reddit r/Python — focus on the Textual TUI architecture
3. Dev.to — longer writeup: "Building a terminal Tamagotchi with Textual"
4. X/Twitter — tag @textualize (Textual's account), mention Claude Code

## Before posting — checklist

- [ ] `pip install tamagotchi` works (publish to PyPI first)
- [ ] There's a demo GIF or screenshot in the README
- [ ] The GitHub repo has a description and topics set
- [ ] At least 5 `good first issue` labels are live
- [ ] Discussions tab is enabled on the repo
