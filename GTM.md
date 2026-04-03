# Terminal Tamagotchi — Go-To-Market Strategy

**Product**: `tamagotchi` — virtual pet in your CLI, reacts to AI coding agent behavior
**Date**: 2026-04-03
**Stage**: Pre-launch (alpha), building toward Show HN and Product Hunt
**GTM Motion**: Product-led growth — install → use → share → refer
**Budget**: Zero (organic/community only)
**Methodology**: Product Compass GTM

---

## Table of Contents

1. [Beachhead Segment Selection](#1-beachhead-segment-selection)
2. [Channel Evaluation Matrix](#2-channel-evaluation-matrix)
3. [Message-Market Fit per Segment](#3-message-market-fit-per-segment)
4. [Phased Launch Plan](#4-phased-launch-plan)
5. [KPI Targets](#5-kpi-targets)
6. [Risk Register](#6-risk-register)
7. [90-Day Execution Roadmap](#7-90-day-execution-roadmap)

---

## 1. Beachhead Segment Selection

### Selected Beachhead: Terminal Aesthetes (Persona 1 — "The Solo Craftsperson")

**Profile**: Senior/mid-level ICs who use macOS/Linux with Neovim + tmux + Starship. 6-8 hours per day in the terminal. Actively maintain dotfiles repos, post terminal setup screenshots on Twitter/X and r/unixporn, and belong to multiple developer Discord servers centered on CLI tooling.

**Why this segment first:**

| Criterion | Terminal Aesthetes | AI Agent Operators | Learners |
|---|---|---|---|
| Tolerance for alpha-stage rough edges | High — they debug their own dotfiles | High | Low — churn immediately |
| Distribution leverage | Very high — they screenshot and share setups as a hobby | Medium — less social, more utilitarian | High virality but shallow networks |
| Unlock condition today | Available now — tmux/Starship integrations ship | Requires Phase 2 agent polish | Available now but requires forgiving mechanics |
| Community access | r/unixporn, Neovim/Starship/dotfiles Discords are active and accessible | Claude/Aider/Cursor Discords exist but are transactional | CS student Discords, TikTok — harder to reach authentically |
| Revenue/growth trajectory | They pull in AI Operators as a second wave organically | They pull in team installs as a third wave | They pull in more learners — lower LTV |

**The decisive factor**: Terminal Aesthetes produce screenshots. Their core behavior — sharing a terminal setup image in a Discord channel or posting to r/unixporn — is the exact distribution mechanism the product needs. Every organic install from this segment arrives because someone saw a screenshot with a pet in the tmux status bar and thought "I want that." This is not a growth hack; it is the product's literal design intent.

**Adjacent segments activated by beachhead success:**

- AI Agent Operators are the natural second wave. Many Terminal Aesthetes already use Claude Code or Aider. The Phase 2 agent integration story is compelling *to them specifically* — it layers onto a setup they already have.
- The Learner/Student segment activates when the product appears on "cool terminal setups" content (TikTok, YouTube shorts, CS Discord shares). This happens organically once a critical mass of Terminal Aesthetes have pet screenshots in circulation.

**What "winning the beachhead" looks like**: 500 active installs (users who have run `tama` at least once in the past 7 days), with 30+ GitHub profile READMEs embedding a pet badge, and unprompted screenshots appearing in r/unixporn and developer Discords without the founder posting them.

---

## 2. Channel Evaluation Matrix

Scoring: 1 (lowest) to 5 (highest). Effort scored inversely — 5 = minimal effort, 1 = very high effort.

| Channel | Reach | Audience Fit | Effort (inverse) | Cost | Timing | Score | Priority |
|---|---|---|---|---|---|---|---|
| r/unixporn | 3 | 5 | 4 | 5 | Pre-launch + ongoing | **21/25** | P0 |
| Show HN (Hacker News) | 5 | 4 | 2 | 5 | Launch day | **21/25** | P0 |
| Dev Discord drops (Neovim, Starship, Aider, Claude) | 3 | 5 | 3 | 5 | Pre-launch + launch | **21/25** | P0 |
| GitHub organic (stars, README embeds, trending) | 4 | 5 | 4 | 5 | Ongoing post-launch | **23/25** | P0 |
| Twitter/X developer community | 4 | 4 | 3 | 5 | Launch week | **20/25** | P1 |
| Product Hunt | 4 | 3 | 2 | 5 | Launch day | **19/25** | P1 |
| dev.to / Hashnode narrative posts | 3 | 4 | 3 | 5 | Pre-launch + post | **18/25** | P1 |
| Open source contributors (GitHub issues) | 2 | 5 | 4 | 5 | Ongoing | **21/25** | P0 |
| AI tooling newsletters (TLDR Dev, Pointer.io, Bytes.dev) | 4 | 3 | 3 | 5 | Launch week | **18/25** | P1 |
| r/commandline / r/programming | 3 | 3 | 4 | 5 | Post-launch | **17/25** | P2 |
| YouTube / TikTok (terminal setup creators) | 5 | 3 | 1 | 5 | 60-90 days post | **17/25** | P2 |
| CS university Discords | 2 | 3 | 3 | 5 | 60+ days post | **14/25** | P3 |
| Developer conferences / lightning talks | 2 | 4 | 2 | 5 | 90+ days | **13/25** | P3 |

**Channel rationale details:**

**r/unixporn (P0)**: 350k+ members obsessed with terminal aesthetics. A single well-composed screenshot post routinely reaches 5k-20k views. This community's behavior — "I saw it in a post, I installed it" — is exactly the viral loop. Low effort because you have the screenshot already. Post policy: title as `"My terminal has a resident now. Tamagotchi in tmux + Neovim [OC]"` — never pitch, always show.

**Show HN (P0)**: Hacker News Show HN posts on a Tuesday or Wednesday 9am ET can hit the front page and drive 500-2000 unique visitors in 24 hours. The permanent inbound link from news.ycombinator.com carries long-tail SEO value. The AI agent hook differentiates this from the 20 other "terminal toy" submissions that get buried. The title `"Show HN: I built a Tamagotchi that lives in tmux and reacts to my Claude Code agent"` is distinct. Effort is high because you need pre-seeded early comments — but the payoff justifies it.

**Dev Discord drops (P0)**: The five highest-priority servers in ranked order are: (1) Neovim Discord — most Terminal Aesthetes per capita, `#plugins` channel; (2) Starship Discord — terminal prompt customizers, directly relevant; (3) Aider Discord — AI coding agent users, agent integration hook; (4) Claude.ai community Discord — the `tama install --claude-code` story lands perfectly; (5) dotfiles Discord (or the /r/unixporn Discord). Each requires a unique first line — copy-pasting the same message across servers gets flagged. The tmux screenshot is the payload in every case.

**GitHub organic (P0)**: Every `tama share --gist` embed in a developer's profile README is a passive impression. GitHub profile READMEs are indexed by Google and visible to recruiters, hiring managers, and fellow developers. The goal is to seed 50+ profile README embeds within 60 days of launch. The GitHub repo itself should have: description set to "Virtual pet for your terminal — reacts to Claude Code, Aider & Goose agents", topics set to `terminal`, `tamagotchi`, `cli-tool`, `claude-code`, `tmux`, `developer-tools`, `python`. GitHub Trending for Python/Terminal is achievable with 100+ stars in a 24-hour window — launch day coordination targets this.

**Open source contributors (P0)**: Contributors are not just a development resource — they are a GTM channel. Every contributor posts "I contributed to X" on their social. A contributor who writes a Cursor plugin carries the product into the Cursor community. The plugin system is architecturally contributor-friendly (drop a `.py` in a folder). Five labeled `good first issue` items covering sprites, plugins, and docs should exist on GitHub before launch day.

---

## 3. Message-Market Fit per Segment

### Segment 1: Terminal Aesthetes

**Core tension**: They want a terminal that feels alive and personal, but they've been burned by tools that require a 45-minute dotfiles setup and break on the next OS update.

**Message that resolves the tension**:
> "One command. Your terminal has something alive in it in under 60 seconds. Your pet lives in your tmux status bar, evolves through 6 stages based on how you actually code, and generates a shareable ASCII card for your GitHub README. `brew install tamagotchi`"

**Proof points to lead with**:
- `tama install --tmux` — one command, no manual dotfile editing
- The canonical screenshot: Neovim + tmux + Starship with the pet visible in the status bar, full color
- `tama share --gist` → GitHub README embed in three lines

**What NOT to say**: Do not lead with the Tamagotchi nostalgia angle in technical channels. Aesthetes care about their setup, not their childhood. Lead nostalgia only in Twitter/X threads as the acquisition hook, with the integration story as the payoff.

**Channels**: r/unixporn, Neovim Discord, Starship Discord, dotfiles-focused Twitter/X threads

---

### Segment 2: AI Agent Operators

**Core tension**: They run autonomous agents for 8-16 hours a day but have no ambient signal for agent health — they're stuck tailing logs or checking dashboards.

**Message that resolves the tension**:
> "You kick off a Claude Code agent and go to lunch. When you get back, do you tail the log or glance at a status bar? Your terminal Tamagotchi is a living mood indicator for your agent. Happy pet = shipping. Anxious pet = looping. One glance instead of one hundred lines of log. `tama install --claude-code`"

**Proof points to lead with**:
- The three-tmux-pane demo video: dev pane + two agent panes, each with a named pet, different moods
- The behavioral state table (SHIPPING → Happy +1, LOOPING → Anxious animation, TESTS_PASSED → dance)
- "One named pet per agent window" — the per-agent identity framing
- "No data leaves your machine" — local-first is trust-critical for this segment

**What NOT to say**: Do not use the word "monitoring" — it triggers surveillance anxiety. Use "ambient signal," "at a glance," "you notice before you look." The frame is companion, not dashboard.

**Channels**: Aider Discord `#tools`, Claude.ai Discord `#community`, Twitter/X threads tagged `#ClaudeAI`, TLDR AI newsletter brief

---

### Segment 3: Learner / New Developer

**Core tension**: They want coding to feel like a game, but the terminal is intimidating and habit-tracking tools feel like homework.

**Message that resolves the tension**:
> "Your terminal now has a pet. It hatches when you install it, evolves as you code, and sulks if you're away too long — but it won't die while you're on vacation (it hibernates). One brew command. Works in VS Code's terminal. It's the one reason to open your terminal today."

**Proof points to lead with**:
- The hibernation mechanic (not death) — explicitly stated, relieves the fear
- Egg hatching in 60 seconds from install — instant gratification
- `tama share` card — something to show friends who aren't developers
- Works in VS Code integrated terminal (no tmux required for this persona)

**What NOT to say**: Do not mention care mistakes, discipline stats, or evolution conditions in first-contact messaging. The mechanics sound punishing before the emotional attachment is established.

**Channels**: This segment is not a primary launch target. They activate through viral spillover from Aesthetes — TikTok and Instagram shares of pet screenshots, CS Discord word-of-mouth. Do not spend active effort here in the first 60 days.

---

### Segment 4: Engineering Manager / Team Lead

**Core tension**: They want team rituals that build cohesion without looking like surveillance or mandatory fun. They've been burned by gamification tools that caused leaderboard anxiety.

**Message that resolves the tension**:
> "Drop this link in your team Slack. Engineers install it themselves in 30 seconds. A week later there's a thread full of pet screenshots, nobody asked them to post. No admin setup. No IT approval. No data reported to you. Just your team, their terminals, and something with a heartbeat."

**Proof points to lead with**:
- MIT, local-first, no server, no telemetry
- "A single manager mention drives 5-10 organic installs" — word-of-mouth framing
- Phase 3 roadmap (peer discovery, team rooms) as the horizon story — gives them something to look forward to without requiring it now

**What NOT to say**: Do not mention any metrics, leaderboards, or team visibility features until Phase 3 ships. The mere suggestion of "see your team's activity" triggers "is this spyware?" concerns.

**Channels**: This segment is a second-wave target at 60+ days post-launch, when Phase 3 features are on the near-horizon. Reach via Engineering blog posts, EM Twitter/X accounts, and word-of-mouth from their own engineers who already use the product.

---

### Segment 5: Open Source Contributors

**Core tension**: They want to contribute to something used by real people, with a codebase they can actually understand in an afternoon, where their contribution ships and gets acknowledged.

**Message that resolves the tension**:
> "The evolution tree needs your sprites. The plugin system needs your agent integrations. A new ASCII character you draw this weekend ships to every installation. The architecture is clean (`core/`, `ui/`, `plugins/` separated), there are 52 passing tests, and the plugin API is one Python file. Here's a good first issue."

**Proof points to lead with**:
- Plugin drop-in: drop a `.py` in `~/.tamagotchi/plugins/` — no install needed, immediate feedback loop
- `good first issue` labeled issues: new ASCII sprites, Cursor plugin, WakaTime integration, hibernation mode
- Contributor acknowledgment in README and CHANGELOG

**Channels**: GitHub issues, Hacker News thread comments on launch day, dev.to post footnotes

---

## 4. Phased Launch Plan

### Phase 0 — Pre-Launch (Now through Launch Day minus 7 days)

**Goal**: Eliminate friction from the install-to-wow moment. Seed early supporters. Prepare all launch-day assets.

**Product gates** (nothing launches until these pass):
- `brew install tamagotchi && tama` completes in under 60 seconds on a fresh macOS shell
- Pet renders without broken characters in: iTerm2/macOS, Alacritty/macOS, Windows Terminal/WSL2, Kitty/Linux, VS Code integrated terminal
- `tama install --claude-code` succeeds and fires on the next agent session
- `tama share` generates a valid ASCII card and copies to clipboard
- `tama install --tmux` patches tmux.conf without requiring manual editing
- README has a GIF or screenshot above the fold, a one-line install visible without scrolling, and "no data leaves your machine" stated explicitly
- GitHub repo has description, 6+ topics, and 5+ labeled `good first issue` items

**Seeding actions**:
- Share the GitHub link privately with 15-20 developer friends and ask for honest feedback, not stars
- Recruit 5 people willing to post substantive first comments on HN and Product Hunt on launch day — give them a preview install
- Write the draft Show HN post, first comment, Product Hunt maker comment, and three Twitter/X launch tweets — have them ready to paste, not to write
- Record the 45-second demo video: three tmux panes, agent integration in action, `tama share` card generation. No voiceover, on-screen annotations only
- Take the canonical screenshot: Neovim + tmux + Starship on macOS with the pet in the status bar, sharp colors, no visual noise
- Post in three Discord servers (Neovim, Starship, dotfiles) as a "soft preview" — not a launch announcement, just "hey I'm building this, here's an early screenshot, what do you think?" — collect first reactions and fix the sharpest criticism

---

### Phase 1 — Launch Day

**Date**: Tuesday or Wednesday, time-coordinated across channels

**09:00 ET — Show HN submission**
- Title: `"Show HN: I built a Tamagotchi that lives in tmux and gets anxious when my Claude Code agent loops"`
- Immediately post the first comment: canonical screenshot, `brew install tamagotchi`, the three pet reactions table, link to `tama share` example card. Under 150 words.
- Text 5 pre-seeded supporters: "HN is up, please leave a comment"
- Do not link to Product Hunt yet

**09:00 ET — Twitter/X**
- Tweet 1: "I added a Tamagotchi to my tmux status bar. Here's what it looks like when my Claude Code agent passes tests." + 45-second demo video. No links in the body — link in reply.
- Pin this tweet

**09:30 ET — Discord drops** (staggered, 10 minutes apart, unique first line each)
- Neovim Discord `#plugins`: "Wrote a tmux plugin that puts a virtual pet in your status bar — it reacts to your Claude Code agent. Here's what it looks like in Neovim: [screenshot]"
- Starship Discord `#showcase`: "If you have Starship + tmux, `tama install --starship` puts a pet mood indicator in your prompt. Built this over the past few weeks. [screenshot]"
- Aider Discord `#tools`: "Built a Tamagotchi that wires into Aider hooks — pet gets anxious when your agent is looping. `tama install --aider` sets it up. [screenshot]"
- Claude.ai Discord `#community`: "Gave my Claude Code agent a virtual pet. When it's shipping, the pet dances. When it's stuck, it looks worried. `tama install --claude-code`. [demo video link]"
- dotfiles Discord / r/unixporn Discord: the terminal aesthetics screenshot, no description needed beyond "my tmux status bar now has a resident"

**10:00 ET — r/unixporn**
- Title: `"My terminal now has a resident. Tamagotchi in tmux + Neovim [OC]"`
- Body: the canonical screenshot only. Mention in the first comment that you built it and link the GitHub repo.

**12:01 AM PT (same day, launched at midnight the night before) — Product Hunt**
- Product Hunt page was created 48 hours prior, set to auto-publish at 12:01am PT
- Maker comment (post at 9am PT when traffic picks up): lead with AI agent hook, share the demo video, mention the Phase 3 peer discovery roadmap as the horizon story, state MIT + local-first explicitly
- At 8am PT: tweet the Product Hunt link separately from the HN thread
- At 8am PT: post Product Hunt link in the same Discord servers with: "Also on Product Hunt today if you want to support"

**13:00 ET — First engagement sweep**
- Reply to every HN comment within 2 hours
- Reply to every Discord message
- Retweet / quote-tweet the best user reactions

**17:00 ET — Day-1 wrap tweet**
- Post current GitHub star count, HN ranking if applicable, a thank-you to early commenters
- Quote-tweet the best screenshot or comment from the day

---

### Phase 2 — 30 Days Post-Launch

**Goal**: Convert launch spike into sustained organic growth. Establish community presence. Begin content velocity.

**Week 1-2 post-launch**:
- Publish the dev.to narrative post: "My terminal pet judged my coding style — and it was right." Narrative arc: raised a Maskutchi (Poor path), it mapped exactly to a week of shipping fast and messy. End with "I'm trying again." — sequel hook. Cross-post to Hashnode.
- Share the dev.to post on r/programming with a personal story frame: "I wrote about what my terminal Tamagotchi's evolution path revealed about how I code" — not a product pitch
- Reply to every Twitter/X mention within 24 hours for the first two weeks. The founder's engagement is disproportionately high-value at this stage.
- File 10 new GitHub issues from launch-day feature requests. Label them. Post in the Discord servers: "People asked for X — if anyone wants to contribute, here's the issue."

**Week 3-4 post-launch**:
- Reach out individually to the 5-10 developers who embedded the `tama share --gist` badge in their GitHub READMEs. Ask: "What's your pet's name? Would you be willing to be featured on the project's Twitter?" Featured users become advocates.
- Write a TLDR Dev / Pointer.io newsletter brief (150 words, lead with the demo video, not the README). Target: one newsletter pickup in the first 30 days.
- Monitor GitHub Trending for Python — if the repo hits trending, quote-tweet it immediately.
- Post a "one month in" update to HN as an Ask HN or in the original Show HN thread — share a short usage stat (stars, reported installs) and one unexpected thing users did with the product.

---

### Phase 3 — 60 Days Post-Launch

**Goal**: Activate AI Agent Operator segment. Begin seeding Phase 2 product features. Grow contributor community.

**Key actions**:
- Record the "three Claude Code agents, three pets" demo video. This is the canonical AI Agent Operator content. Post it as a new Twitter/X thread, not a reply to the launch thread.
- Submit a brief pitch to: TLDR AI, The Rundown AI, and Ben's Bites newsletters. Frame: "developer built a virtual pet that serves as an ambient health indicator for Claude Code agents" — this is a news story, not a product pitch.
- Open the first community-facing GitHub discussion: "What should the pet do when subagents spawn?" — engagement hook from the original tweet, now formalized. This pulls in AI-native contributors.
- If Phase 2 (agent awareness polish) is shipping, post a dedicated launch to Aider, Claude, and Cursor Discord servers focused entirely on the agent integration — separate from the original aesthetic launch.
- Post the GitHub repo to the `awesome-claude-code` list (if one exists) and equivalent `awesome-*` lists for Aider and Goose.

---

### Phase 4 — 90 Days Post-Launch

**Goal**: Establish the product as the default "developer terminal pet" in its category. Begin Phase 3 (peer discovery) narrative.

**Key actions**:
- Publish a "90 days of Terminal Tamagotchi" retrospective post on dev.to. Include: star count, unexpected use cases, evolution path distribution among users (what % raised a Mimitchi vs. Maskutchi), most common pet names. This is data journalism, not a product update.
- Begin seeding the Phase 3 (peer discovery) story in the AI agent communities: "What if your Claude Code agent's pet could visit other agents' pets on your team's Tailscale network?" — frame it as an open question, not a feature announcement.
- Identify the 3-5 most active contributors. Invite them to a private Discord channel or GitHub team. These become the product's core community, not just contributors.
- Submit a lightning talk proposal to a CLI/devtools meetup or conference — "I put a Tamagotchi in my terminal and now it watches my AI agents."
- Monitor: are Engineering Managers or Team Leads starting to appear in issues or Discord? If yes, start preparing the Phase 3 team rooms messaging.

---

## 5. KPI Targets

### North Star Metric

**Weekly Active Installs (WAI)**: Users who have run `tama` at least once in the past 7 days, as measured by opt-in anonymous telemetry (a single ping on launch with no user data — documented in the README and consent-gated).

Rationale: GitHub stars are a vanity metric — they measure curiosity, not habit formation. WAI measures whether the pet is actually alive in someone's terminal. This is the metric the product's core mechanic (ambient, daily presence) is designed to drive.

---

### KPI Table

| Metric | Baseline (Day 0) | 30-Day Target | 60-Day Target | 90-Day Target | Measurement Method |
|---|---|---|---|---|---|
| GitHub Stars | 0 | 500 | 900 | 1,300 | GitHub API |
| Weekly Active Installs (WAI) | 0 | 150 | 300 | 500 | Opt-in anonymous ping |
| D7 Retention (users active in week 2 who were active in week 1) | Unknown | Establish baseline | 30% | 35% | Opt-in telemetry cohort |
| D30 Retention | Unknown | Establish baseline | Establish baseline | 25% | Opt-in telemetry cohort |
| GitHub profile README embeds (`tama share --gist` uses) | 0 | 20 | 50 | 100 | Gist referrer logs |
| Contributors (PRs merged) | 0 | 3 | 8 | 15 | GitHub insights |
| Show HN score (launch day) | — | Top 5 on Show HN page | — | — | Manual check |
| Product Hunt votes | — | Top 10 of the day | — | — | Product Hunt |
| Organic Discord/Twitter mentions (unforced by founder) | 0 | 5/week | 15/week | 25/week | Manual monitoring |
| Newsletter pickups | 0 | 1 | 3 | 5 | Referral traffic in README badge / Gist logs |

---

### Measurement Infrastructure

**Telemetry design** (must be built before launch, not after):
- Single anonymous ping on `tama` first run: `{"event": "first_run", "os": "darwin", "version": "0.1.0"}` — no user identifier, no pet name, no file paths
- Weekly heartbeat: `{"event": "active", "version": "0.1.0"}` — no user identifier
- User can opt out with `tama config telemetry off`
- Telemetry status shown on first run: "Anonymous usage data is collected to improve the project. Run `tama config telemetry off` to disable."
- This is documented prominently in the README under a "Privacy" heading — "no data leaves your machine" applies to pet state; telemetry is separate and opt-out

**Manual tracking** (for metrics without clean automated measurement):
- GitHub README embed count: search GitHub for `gist.githubusercontent.com` combined with the project Gist URL monthly
- Discord/Twitter mention count: 15-minute scan of all relevant servers and Twitter search for "tamagotchi terminal" once per week
- Newsletter pickups: set up a Google Alert for the product name

---

### Leading Indicators vs. Lagging Indicators

The KPIs above are lagging. These leading indicators should be checked weekly and signal whether lagging KPIs will be met:

| Leading Indicator | What It Predicts | Check Frequency |
|---|---|---|
| New GitHub issues from users (feature requests, bugs) | Organic engagement — people care enough to report | Weekly |
| Screenshot posts in Discord without founder prompting | `tama share` virality is working | Weekly |
| New contributors opening PRs | Contributor GTM channel is working | Weekly |
| Discord server growth in AI agent channels | AI Operator segment activation is beginning | Bi-weekly |
| Inbound newsletter / podcast requests | Product has crossed a discovery threshold | Ongoing |

---

## 6. Risk Register

### R1 — Launch Day: Show HN gets buried (no front-page placement)

**Probability**: Medium (most Show HN posts don't front-page)
**Impact**: High — the entire coordinated launch plan depends on HN momentum
**Mitigation**:
- Have 5 pre-seeded supporters post substantive first comments within 30 minutes of submission. Comment velocity in the first hour is the strongest algorithmic signal.
- If the post is buried at hour 2, do not re-post (HN bans duplicates). Pivot immediately to the Discord and Twitter plan — these channels work independently of HN placement.
- The AI agent hook in the title differentiates from typical "terminal toy" posts. Test both title versions with the 5 pre-seeded supporters before launch: "reacts to my Claude Code agent" vs. "gets anxious when my AI agent loops" — the second is a stronger story.
- Fallback: if HN doesn't front-page, post a "Show HN: follow-up — we shipped X based on your feedback" in 30 days when there is a meaningful update. Second bites at HN are legitimate if there's genuinely new material.

---

### R2 — First-run experience breaks on a common terminal configuration

**Probability**: Medium-high (terminal rendering differences are unpredictable)
**Impact**: Very high — a broken first-run turns potential advocates into detractors
**Mitigation**:
- Do not launch until the product has been tested cold (fresh shell, no prior install) on: iTerm2/macOS, Alacritty/macOS, Windows Terminal/WSL2, Kitty/Linux, VS Code integrated terminal. Document this matrix in a pre-launch checklist.
- Add a fallback rendering mode (`tama --ascii-only`) that disables Unicode box-drawing characters and uses pure ASCII. Surface this in the README for edge cases.
- Keep a `KNOWN_ISSUES.md` in the repo and update it immediately when launch-day bug reports come in. Responding to a bug report within 2 hours on launch day with a fix or workaround turns a detractor into a loyal user.

---

### R3 — Pet death mechanic drives early churn among Learner/New Developer users

**Probability**: High — the USER_RESEARCH.md explicitly flags this as a known risk
**Impact**: Medium — Learners are not the launch target, but they are the viral pool
**Mitigation**:
- Default to hibernation mode, not permadeath. The pet enters a "frozen egg" state after 3 days of inactivity and can be revived with `tama revive`.
- Make permadeath an explicit opt-in flag: `tama config permadeath on`. Document it as "for the authentic experience."
- State the hibernation default prominently in the README and in the first-run experience: "Don't worry — your pet hibernates when you're away. It won't die while you're on vacation."

---

### R4 — Tamagotchi trademark creates legal risk at scale

**Probability**: Low at current scale, Medium at 10k+ installs
**Impact**: High — a C&D letter at the wrong moment could derail momentum
**Mitigation**:
- The product name "tamagotchi" is used as a category descriptor (lowercase, descriptive), not a brand name. The product's registered name is "tamagotchi" (the package) but the product can be referred to as "Terminal Pet" or "tama" in marketing materials.
- Maintain a backup brand name ready: "Tama" or "Terminal Pet" or "tama.sh" — the `tama` CLI command is the interface users actually interact with daily.
- Do not use Bandai Namco's logo, specific character IP names in official channels (Mimitchi, Mametchi etc. can stay in technical docs but should not be front-and-center in marketing).
- At 5,000+ stars, consult a lawyer for a 30-minute IP risk assessment. This is worth the cost.

---

### R5 — Solo founder burn-out causes post-launch radio silence

**Probability**: High — launch exhaustion is real and community expectations accelerate post-launch
**Impact**: High — community abandonment kills open source projects faster than technical debt
**Mitigation**:
- Set explicit response-time expectations in the README: "Issues are reviewed on weekends. PRs that pass CI are merged within 5 business days."
- Batch community management to two sessions per week (Monday morning, Friday afternoon) rather than checking continuously.
- Identify and formally invite 2-3 active contributors as project maintainers within 60 days of launch. Distribute the community management burden before burnout, not after.
- Prepare a "low-activity notice" GitHub issue template: if the project goes quiet for 2+ weeks, post a brief update so the community doesn't assume abandonment.

---

### R6 — The AI agent integration story requires Phase 2 polish that isn't done at launch

**Probability**: Medium — Phase 2 is explicitly listed as "not started" in PLAN.md
**Impact**: Medium — the agent integration is the strongest differentiator; if it's buggy, the HN story weakens
**Mitigation**:
- Set a hard pre-launch gate: `tama install --claude-code` must succeed and fire at least one pet reaction in a live Claude Code session before the Show HN post goes up. This is a binary launch criterion.
- If Phase 2 is not ready at launch, lead with the terminal aesthetics story only (r/unixporn + tmux screenshot) and hold the agent integration for a "v0.2 launch" 4-6 weeks later — a second HN moment with new material.
- The staged launch (aesthetics now, agents later) actually doubles the number of distinct launch moments, which is a GTM advantage.

---

### R7 — Empty social layer undermines the Phase 3 product story

**Probability**: High — peer discovery is months away from shipping
**Impact**: Low now, Medium at 90 days
**Mitigation**:
- Do not mention Phase 3 (peer discovery) in launch day messaging. It doesn't exist yet.
- When Phase 3 is referenced (e.g., in the Product Hunt maker comment), frame it as a "what we're building toward" rather than a feature. The sentence is: "Next up: pets that visit each other over your team's Tailscale network."
- Build the social layer only after 30-day retention is established for the single-player experience. Per USER_RESEARCH.md: "The fastest way to kill a social product is to launch with an empty social layer."

---

### R8 — Contributors write plugins that conflict with the core product direction

**Probability**: Low-Medium
**Impact**: Medium — a low-quality plugin that goes viral can become the first impression of the plugin system
**Mitigation**:
- Write a CONTRIBUTING.md section called "Plugin quality bar" that sets expectations: plugins must work without network calls by default, must not access files outside `~/.tamagotchi/`, must include a README with a screenshot.
- All plugins in the official repo are reviewed and must pass CI. Community plugins in `~/.tamagotchi/plugins/` are user-installed at their own risk — document this distinction clearly.

---

## 7. 90-Day Execution Roadmap

### Week-by-Week (First 4 Weeks)

---

#### Week 0 (Pre-launch — T-14 to T-7)

**Monday**: Run the full pre-launch product checklist. Time the install-to-first-pet sequence. If any step fails, fix before proceeding.

**Tuesday**: Take the canonical screenshot and record the 45-second demo video. These are your two most important marketing assets. Spend as much time on composition and terminal config as you would on a product demo for investors.

**Wednesday**: Write and finalize all launch-day copy in a single doc:
- Show HN title (two versions to test)
- Show HN first comment (under 150 words)
- Product Hunt tagline, description, maker comment
- Three Twitter/X tweets for launch day
- Five Discord opening lines (one per server, each unique)
- Answers to top 5 expected HN pushback questions

**Thursday**: Share the GitHub repo privately with 20 developer contacts. Ask specifically: "Does the pet render correctly in your terminal? Does `tama install --tmux` work without manual edits?" Collect and fix feedback.

**Friday**: Create the Product Hunt page. Set auto-publish for launch day 12:01am PT. Upload all screenshots and demo video. Write the maker comment but do not publish yet.

**Weekend**: Rest. The launch week will be high-intensity.

---

#### Week 1 (T-7 to T-1 — Final Seeding)

**Monday**: Post in three Discord servers (Neovim, Starship, Aider) as a soft preview. Not a launch announcement — a "hey I've been building this, here's a screenshot, would love early feedback." Monitor reactions. Fix anything that surfaces as a blocking concern.

**Tuesday**: Contact the 5 pre-seeded HN/Product Hunt supporters individually. Walk them through the product. Ask them to have a substantive comment ready for launch day — not a upvote request. Give them a specific thing to comment on (e.g., "what do you think about the hibernation vs. permadeath design decision?").

**Wednesday**: Add 5+ `good first issue` labels to open GitHub issues. Write clear descriptions. This ensures that launch-day HN readers who are interested in contributing have something actionable to do immediately.

**Thursday**: Final QA pass. Verify that `tama --version` returns a clean semver string. Verify that all five install methods work. Verify that `tama share` generates a valid card.

**Friday**: Schedule the three launch-day Twitter/X tweets for Tuesday 9am ET, 1pm ET, and 5pm ET. Write the r/unixporn post but do not submit yet. Get a full night's sleep before launch week.

**Weekend**: Do nothing product-related. Decompress.

---

#### Week 2 (Launch Week)

**Tuesday (Launch Day)** — follow the Launch Day plan from Section 4 exactly.

Key milestones to check:
- By 10am ET: HN post is live, 5+ comments posted by supporters
- By 11am ET: All 5 Discord drops posted
- By 12pm ET: r/unixporn post live
- By 1pm ET: Quote-tweet the best early reaction
- By 3pm ET: Product Hunt page live (published at 12:01am PT, now visible)
- By 6pm ET: Reply to every HN comment, every Discord message

**Wednesday**: Write a brief "Day 1 results" note for yourself — stars, HN position, Discord reactions, any unexpected feedback. This is input for the 30-day retrospective. Continue replying to all inbound. Fix any bug that's been reported more than once.

**Thursday**: Post the dev.to narrative post: "My terminal pet judged my coding style." This extends the launch-week content surface beyond HN. Share in r/programming with a personal story frame.

**Friday**: Identify the 3 most enthusiastic early users from Discord/HN. DM them asking if they'd be willing to be featured (their pet + their GitHub username) on the project's Twitter/X. Their posts will have higher credibility than founder posts.

**Weekend**: Review all GitHub issues opened this week. Label them. Reply to all open issues with a response, even if the response is "this is on the roadmap, not yet scheduled."

---

#### Week 3 (Consolidation)

**Focus**: Convert launch spike into sustained organic growth. Establish weekly cadence.

**Monday**: Check WAI telemetry for the first time. Record the baseline. This is the number to beat each week.

**Tuesday**: Reach out individually to every developer who has embedded the `tama share --gist` badge in their GitHub README. Thank them. Ask if they'd be open to a quick 20-minute chat about their experience. Aim for 3 conversations this week.

**Wednesday**: Post the first "what are you building?" prompt in a relevant Discord server — not product marketing, genuine curiosity. The goal is becoming a known participant in these communities, not just a product poster.

**Thursday**: Review the 30-day product gate: is the single-player loop tight enough to retain users for 30 days? Make a prioritized list of the top 3 improvements most likely to improve D7 retention.

**Friday**: Submit the newsletter brief to TLDR Dev (tldr.tech/submit). 150 words, lead with the demo video link, end with the `brew install tamagotchi` one-liner.

---

#### Week 4 (First Month Close)

**Focus**: Assess product-market fit signals. Set 60-day priorities.

**Monday**: Write the "30-day" dev.to or GitHub Discussions post. Share: star count, one surprising use case, the most-requested feature, the evolution path distribution. This is authentic developer content, not marketing copy.

**Tuesday**: Review user interview data from the 3 conversations in Week 3. Are D7 retention concerns driven by the pet degradation speed, the lack of integration, or something else? Update the product backlog based on what you heard, not what you assumed.

**Wednesday**: Decide whether to launch the AI agent integration story now (if Phase 2 is polished) or wait 2-4 more weeks. If waiting, post a GitHub discussion: "Claude Code plugin update — here's what's coming" to maintain momentum with the AI Operator segment.

**Thursday**: File a PR to add the project to the `awesome-python` and `awesome-cli-apps` GitHub lists. These are long-tail discovery channels that compound over time.

**Friday**: Month 1 retrospective. Compare actual KPIs to the 30-day targets in Section 5. Write 3 things that worked, 3 things that didn't, and 1 thing you'll do differently in Month 2.

---

### Monthly (30/60/90 Day Summary)

---

#### Month 1 (Days 1–30): Establish Beachhead

**Primary goal**: 150 WAI. 500 GitHub stars. 20 README embeds. r/unixporn and 5 Discord servers actively sharing screenshots without founder prompting.

**Channel focus**: r/unixporn, Show HN, Neovim/Starship/Aider Discord, GitHub organic, dev.to narrative post

**Product focus**: Nail the first-run experience. Fix every rendering bug reported. Ship `tama revive` (hibernation revival) if not already done.

**Success signal**: At least one person posts a pet screenshot in a Discord server you didn't personally post in, without being tagged.

---

#### Month 2 (Days 31–60): Activate AI Operator Segment

**Primary goal**: 300 WAI. 900 GitHub stars. 50 README embeds. 1 newsletter pickup. 8 contributors.

**Channel focus**: Claude.ai/Aider/Cursor Discord servers with the agent integration story. Twitter/X thread on "three agents, three pets" demo. TLDR AI newsletter brief.

**Product focus**: Phase 2 AI agent awareness — polish the Claude Code plugin to production quality. Begin Cursor plugin (ideally contributed by a community member). Ship the behavioral classifier states (LOOPING, BLOCKED, DONE_SUCCESS) with distinct animations.

**Key action**: Record and publish the "three Claude Code agents, three pets" demo video. This is the most shareable piece of content for the AI Operator segment.

**Success signal**: An inbound question from an AI engineering newsletter or podcast asking about the agent integration.

---

#### Month 3 (Days 61–90): Establish Category Leadership + Begin Phase 3 Narrative

**Primary goal**: 500 WAI. 1,300 GitHub stars. 100 README embeds. 5 newsletter pickups. 15 contributors. Phase 3 peer discovery design finalized (not yet shipped).

**Channel focus**: 90-day retrospective post (data journalism angle). Lightning talk submission to a CLI/devtools meetup. Begin seeding the Phase 3 "pets that visit each other" story in AI agent communities.

**Product focus**: Begin Phase 3 design work (WebSocket peer protocol, mDNS LAN discovery). Identify and invite 2-3 core contributors as co-maintainers. Ship the Cursor plugin if not already done.

**Key action**: Host the first community event — a "show your pet" async thread in the project's GitHub Discussions or a dedicated Discord server. Ask users to post their pet's evolution path and one story about it. This generates the testimonial content and community artifacts needed for the Phase 3 launch.

**Success signal**: An Engineering Manager posts in GitHub Discussions asking about team discovery features — this signals the Phase 4 audience is beginning to materialize.

---

## Appendix: Copy Bank

The following copy has been finalized and should be used verbatim or as a base for adaptation. Changing the wording without testing against the audience first will reduce effectiveness.

**Show HN title (preferred)**:
> Show HN: I built a Tamagotchi that lives in tmux and gets anxious when my Claude Code agent loops

**Show HN first comment opening line**:
> Here's what it looks like in a Neovim + tmux setup: [screenshot]. `brew install tamagotchi` — pet hatches in under 60 seconds.

**r/unixporn title**:
> My terminal now has a resident. Tamagotchi in tmux + Neovim [OC]

**Twitter/X launch tweet**:
> I added a Tamagotchi to my tmux status bar. Here's what it looks like when my Claude Code agent passes tests. [video] `brew install tamagotchi`

**Product Hunt tagline** (60 chars):
> Virtual pet for your terminal that watches your AI agent

**Discord opening line — Neovim**:
> Wrote a tmux plugin that puts a virtual pet in your status bar — it reacts to your Claude Code agent. Here's what it looks like in Neovim: [screenshot]

**Newsletter brief opening**:
> A developer built a virtual Tamagotchi that lives in the tmux status bar and reacts in real time to Claude Code, Aider, and Goose agent behavior. When the agent is shipping code, the pet dances. When it's stuck in a loop, it looks anxious. `brew install tamagotchi`. MIT, local-first.

---

*This document is owned by the founder and should be reviewed and updated at each monthly milestone. Every recommendation in this document is grounded in the USER_RESEARCH.md personas and journey map, the MARKETING.md campaigns and positioning analysis, and the PLAN.md product phases. When product phases ship, update the GTM phase targeting to match.*
