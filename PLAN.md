# Tamagotchi — Product Plan

**Vision:** Start as a terminal virtual pet, evolve into the social platform for the AI coding era. Your pet is raised in the terminal, shaped by how you work, and becomes your developer identity in a shared virtual world.

**Last updated:** April 2026

---

## The Big Picture

```
Phase 1 — Terminal Pet       you raise it, it reacts to your work
Phase 2 — AI Agent Awareness your pet watches your AI coding agents
Phase 3 — Peer Discovery     pets visit each other, hangout in rooms
Phase 4 — Social Platform    the developer world your pet lives in
```

The terminal is where you *raise* your pet.
The web is where it *lives* — with everyone else's.

---

## Phase 1 — Terminal Pet ✅ In Progress

**Goal:** A complete, faithful Tamagotchi in the terminal. Make people care about their pet before anything else.

### Core mechanics
- [x] Life stages: Egg → Baby → Child → Teen → Adult → Elder → Death
- [x] Stats: Hunger, Happiness, Weight, Discipline, Health
- [x] Real-time decay — pet ages even when app is closed
- [x] Care-driven evolution — 3 paths (Good / Normal / Poor) per stage
- [x] Poop, sickness, attention calls, lights on/off (sleep)
- [x] Auto-save to `~/.tamagotchi/`

### TUI
- [x] Animated ASCII sprites per character and mood
- [x] Color-coded stat bars
- [x] 8-icon action menu (original button layout)
- [x] Event log with real-time updates
- [x] New pet screen, help screen

### Plugin system
- [x] `BasePlugin` with lifecycle hooks
- [x] Entry-point discovery + `~/.tamagotchi/plugins/` drop-in

### Remaining Phase 1 work
- [ ] Mini-game for the Play action (simple guess/reaction game in TUI)
- [ ] Pet graveyard screen (view deceased pets)
- [ ] Multiple pet slots (switch between pets)
- [ ] `tama status` CLI command (show pet stats without launching full TUI)
- [ ] Publish to PyPI

---

## Phase 2 — AI Agent Awareness 🔜

**Goal:** Pet reacts to what your AI coding agent is doing — not just that it's running, but *what* it's doing.

### Behavioral classifier
Classify agent activity from hook events into meaningful states:

| State | Trigger | Pet reaction |
|-------|---------|-------------|
| SHIPPING | Agent writing files, tests passing | Happy +1 |
| LOOPING | Same tool called 5+ times | Happy −1, Hungry −1, anxious animation |
| EXPLORING | Many file reads, no writes | Curious animation, no stat change |
| BLOCKED | Repeated errors or permission denials | Happy −1, worried animation |
| DONE_SUCCESS | Stop event, task complete | Happy +2, celebrate animation |
| DONE_FAILURE | Stop event, task failed | Happy −1, sad animation |
| TESTS_PASSED | bash tool ran pytest → exit 0 | Happy +2, dance animation |
| TESTS_FAILED | bash tool ran pytest → exit 1 | Happy −1 |
| SUBAGENT_SPAWNED | SubagentStart hook | Anxious animation |

### Plugins to build
- [ ] **Claude Code plugin** (skeleton done — needs polish + all behavioral states)
- [ ] **Cursor plugin** — hook into Cursor agent JSONL logs
- [ ] **GitHub Copilot plugin** — monitor Copilot completions
- [ ] **Windsurf plugin**
- [ ] **Git plugin** — pet reacts to commits, merges, failed rebases
- [ ] **CI/CD plugin** — celebrate passing pipelines, mourn failures

### Pet memory
- [ ] Long-term memory of project history (read Claude Code JSONL over time)
- [ ] Pet references past events: "Last time you worked on auth, it took 3 hours"
- [ ] Regression detection: "We've seen this error before"

---

## Phase 3 — Peer Discovery 🔜

**Goal:** Pets find each other and visit. The social layer begins.

### 3a — Terminal peer sync
- [ ] WebSocket server (lightweight, self-hostable)
- [ ] Peer registration: each `tama` instance announces itself
- [ ] Pet visit protocol: visiting pet appears in your terminal for ~5 min
- [ ] LAN discovery via mDNS (no server needed for local teams)
- [ ] Tailscale support for remote teams

### 3b — The World (web)
A 2D virtual world rendered in the browser. Your terminal pet becomes your avatar. Pets walk between named rooms, each with its own vibe and purpose.

```
╔══════════════════════════════════════════════════════╗
║  ☕ Coffee Chat                          8 online    ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║   [Mimitchi]                                         ║
║      yusik: "anyone tried the new Claude 4?"         ║
║                        [Mametchi]                    ║
║                           sara: "yes it's fast 🔥"   ║
║                                        [Tamatchi]    ║
║    ~~~~~ coffee bar ~~~~~                bob: "..."   ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║  > yeah the latency is way better         [Enter]    ║
╚══════════════════════════════════════════════════════╝
```

#### Rooms

Each room has a distinct atmosphere, theme, and social dynamic. Pets can walk between rooms freely.

| Room | Vibe | Purpose |
|------|------|---------|
| **☕ Coffee Chat** | Casual, warm | Low-stakes chat, daily standup energy, intros |
| **🔥 Fireside Chat** | Intimate, focused | Longer discussions, AMAs, deep dives with a guest speaker pet |
| **🏕️ The Lounge** | Chill, open | Default hangout, idle pets wander here |
| **📚 The Library** | Quiet, focused | No chat — pets sit and work, agent activity visible |
| **⚡ The Hackathon Floor** | Energetic, loud | Active building sessions, agent metrics on the wall |
| **🌱 The Garden** | Peaceful | Pet care focus — feed, play, check stats |
| **🪦 The Graveyard** | Solemn | Memorial room for deceased pets, always accessible |
| **🔒 Team Rooms** | Private | Invite-only rooms for orgs / squads (Phase 4) |

#### Room mechanics
- [ ] Real-time 2D room with pet avatars (pixel or ASCII art)
- [ ] Arrow key movement within a room
- [ ] Room switcher — walk to a door to change rooms
- [ ] Room capacity limits (Fireside: 20 max, Lounge: 100+)
- [ ] Pet mood/health visible to others (hungry pets droop, healthy pets bounce)
- [ ] Room-specific ambient decoration (Library has bookshelves, Garden has grass)
- [ ] Agent activity indicator per pet (small icon showing SHIPPING / LOOPING / IDLE)

### 3c — Social feed
- [ ] Speech bubbles above pets in the world
- [ ] Message history / bulletin board per room
- [ ] Reactions: 🔥 (shipping) 💀 (debugging hell) 🤝 (helping) ✅ (shipped)
- [ ] No likes — only contextual developer reactions

### Tech stack for Phase 3
```
Backend:  FastAPI + WebSockets
Auth:     GitHub OAuth (devs already have accounts)
DB:       PostgreSQL (pet state, messages, presence)
Realtime: Redis pub/sub (positions, presence)
Frontend: Next.js + HTML Canvas (2D world)
Hosting:  Single server to start, scale later
```

---

## Phase 4 — Social Platform 💭

**Goal:** The developer world your pet lives in. Your pet's history is your developer identity.

### Pet profiles
- [ ] Public profile page per pet: evolution path, age, care history
- [ ] "How I raised this pet" — a timeline of care decisions and agent activity
- [ ] Pet lineage tree (if breeding/egg-gifting is added)
- [ ] Character rarity display — earned, not bought

### Developer identity
Your pet's evolution path is a reflection of how you actually code:
- Raised a **Mimitchi** (Good path)? You're meticulous, low mistakes, consistent care.
- Raised a **Maskutchi** (Poor path)? You ship fast, you neglect the details.
- **Elder** with full stats? You've been at this for months.

This is not a profile you fill out — it's a record of how you worked.

### Team rooms
- [ ] Private rooms for teams/orgs (GitHub org auth)
- [ ] Team leaderboard: whose pet is healthiest? whose agent is shipping most?
- [ ] Collective quests: team's agents must collectively ship N features for all pets to get a bonus evolution
- [ ] Team graveyard: memorial wall for pets that didn't make it

### Platform features
- [ ] Pet trading / gifting (eggs as gifts)
- [ ] Seasonal events (hackathon week: double XP; debugging week: sickness spreads)
- [ ] Open API for third-party integrations
- [ ] Mobile companion app (view pet, receive notifications)

### Monetization — TUI-style ads

When the world has meaningful traffic, a non-intrusive ad placement fits naturally into the terminal aesthetic. The key constraint: ads must feel native to the environment, never disruptive.

**Placement**
- A single banner slot rendered as a TUI panel — below the 2D room, above the chat input
- Looks like part of the terminal UI, not a web ad
- In-room "sponsored" objects: a branded coffee machine in Coffee Chat, a sponsor logo on the Hackathon Floor board

**Format**
```
╔══════════════════════════════════════════════════════╗
║  sponsored by Vercel — deploy your next project in  ║
║  seconds.  vercel.com/new                [dismiss]  ║
╚══════════════════════════════════════════════════════╝
```

**Rules**
- Developers only — no consumer brands. Target: dev tools, cloud infra, SaaS
- Max 1 ad per session, dismissible, never animated
- Paid pet cosmetics as an alternative revenue stream (earned or bought — buyer's choice)
- Free tier always gets the full experience. Ads are additive, not paywalled

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Terminal Client (Python)               │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  Core    │  │    TUI       │  │   Plugin System   │  │
│  │  Engine  │  │  (Textual)   │  │  Claude Code      │  │
│  │          │  │              │  │  Cursor / Copilot │  │
│  └────┬─────┘  └──────────────┘  └───────────────────┘  │
└───────┼─────────────────────────────────────────────────┘
        │ WebSocket / REST (Phase 3+)
        ▼
┌─────────────────────────────────────────────────────────┐
│                  API Server (FastAPI)                    │
│  ┌────────────┐ ┌──────────────┐ ┌──────────────────┐   │
│  │ Pet state  │ │  Room/world  │ │  Social / feed   │   │
│  │    sync    │ │    engine    │ │     service      │   │
│  └────────────┘ └──────────────┘ └──────────────────┘   │
│  ┌────────────┐ ┌──────────────┐                         │
│  │  GitHub    │ │  Presence    │                         │
│  │   OAuth    │ │ (Redis)      │                         │
│  └────────────┘ └──────────────┘                         │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│              Web Frontend (Next.js)                     │
│  ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐  │
│  │  2D World    │ │  Social feed │ │  Pet profiles   │  │
│  │  (Canvas)    │ │  / chat      │ │  & identity     │  │
│  └──────────────┘ └──────────────┘ └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Principles

1. **The terminal is home.** The web amplifies it — doesn't replace it.
2. **Earned, not bought.** Every cosmetic and identity signal comes from actual play. No pay-to-win.
3. **Developer-native.** GitHub OAuth, CLI-first, SSH-friendly, works in tmux.
4. **The pet is the identity.** Its history reflects real behavior, not a curated profile.
5. **Start small, stay real.** Phase 1 must be genuinely good before Phase 2 begins. Don't skip steps.

---

## What We're NOT Building

- A productivity tracker (that's WakaTime)
- An analytics dashboard (that's BurnRate)
- A Discord replacement (that's Discord)
- A game with IAP or cosmetic stores
- A crypto thing

---

## Current Status

| Phase | Status | Next action |
|-------|--------|-------------|
| Phase 1 | 🟡 In progress | Mini-game, graveyard, PyPI publish |
| Phase 2 | ⬜ Not started | Polish Claude Code plugin, add Cursor |
| Phase 3 | ⬜ Not started | Design WebSocket peer protocol |
| Phase 4 | ⬜ Vision only | — |
