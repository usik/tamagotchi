# Terminal Tamagotchi — Marketing Toolkit

**Product**: `tamagotchi` — a virtual pet that lives in your CLI
**Status**: Pre-launch (alpha)
**Audience**: Developers who live in their terminal
**Distribution**: pip / npm / curl / brew — MIT, free forever
**Last updated**: 2026-04-03

---

## 1. Marketing Campaign Ideas

---

### Campaign 1 — "Show off your setup" thread bomb

**Channel**: Twitter/X, r/unixporn, terminal-aesthetics Discord servers
**Messaging angle**: Identity expression / terminal flex
**Effort**: S
**Expected impact**: High — taps an existing, high-engagement behaviour. Terminal setup screenshots are the #1 organic content format in this community.

**Execution steps**:
1. Run `tama share --gist` on your own setup (Mimitchi, Adult, full stats). Screenshot the card rendered inside a Neovim + tmux window.
2. Post to Twitter/X: *"Added a pet to my tmux status bar. Here's my setup — what's yours? `brew install tamagotchi` or `pip install tamagotchi`"* — include the screenshot, no thread, no markdown wall.
3. Post the same screenshot to r/unixporn with title: *"My terminal now has a resident. Tamagotchi in tmux. [OC]"* — include `tama share` card as the featured image.
4. Drop into 3–5 dev Discord servers (Neovim, dotfiles, CLI tools, Starship, AI coding) and post the screenshot + one-liner install in the `#show-and-tell` or `#tools` channel. No pitch — just the screenshot and the install command.
5. Reply to every comment. Pin the best pet screenshots as quote-tweets.
6. Track stars spiked per post. Double down on whichever platform drove the most.

---

### Campaign 2 — "Give your Claude Code agent a soul"

**Channel**: Twitter/X, Hacker News (Ask HN or Show HN), AI coding Discord servers (Claude, Cursor, Aider communities)
**Messaging angle**: AI agent ambient monitoring with emotional framing
**Effort**: M
**Expected impact**: High in a fast-growing segment. No analogous tool has this positioning. Likely to get picked up by AI tooling newsletters.

**Execution steps**:
1. Record a 45-second screen capture: three tmux panes side by side. Left pane — developer typing. Middle pane — Claude Code agent actively writing code, pet is dancing. Right pane — a second Claude Code agent in a loop, pet looks anxious and hungry.
2. Write a Twitter/X thread (3 tweets): Tweet 1: *"I gave my Claude Code agent a virtual pet. When it's shipping code, the pet is happy. When it's stuck in a loop, the pet gets anxious and hungry. I check on the pet instead of tailing the logs."* + video. Tweet 2: `tama install --claude-code` sets it all up. Tweet 3: *"What should the pet do when subagents spawn?"* (engagement hook).
3. Post the video to the Claude, Cursor, and Aider Discord servers under `#tools` or `#integrations`.
4. Submit to TLDR Dev, Pointer.io, and Bytes.dev newsletters as a brief — lead with the video, not the README.
5. File a `good first issue` on GitHub: *"Add Cursor plugin — behavioral classifier same as Claude Code"* — this pulls in AI-native contributors.

---

### Campaign 3 — GitHub README badge drop

**Channel**: GitHub (organic), developer Twitter/X
**Messaging angle**: Social proof embedded directly in the developer's identity surface
**Effort**: S
**Expected impact**: Medium-high compounding. Every README that embeds a live pet badge is a passive impression for the project.

**Execution steps**:
1. Make `tama share --gist` output a valid Markdown image embed: `![Pixel](https://gist.githubusercontent.com/you/abc123/raw/pixel_tamagotchi.txt)` — this already works per the README.
2. Write a one-paragraph GitHub Gist (not a blog post) titled *"How I added a live Tamagotchi to my GitHub profile README"* — show the three-line setup: install, `tama share --gist`, paste the embed snippet.
3. Share that Gist link on Twitter/X with: *"Your GitHub profile README can have a live terminal pet. Here's how."* Tag #GitHub #dotfiles.
4. Post the Gist to r/github and r/commandline.
5. Add the Gist link to the README's `tama share` section as the canonical setup guide.
6. Monitor GitHub profile READMEs that embed the badge via the Gist referrer log — reach out to early adopters directly and ask if they'd be willing to be featured on the project's social accounts.

---

### Campaign 4 — "Your pet reflects how you actually code" developer identity angle

**Channel**: dev.to, Hashnode, personal blog cross-posts
**Messaging angle**: Developer identity / care-driven evolution as a proxy for coding style
**Effort**: M
**Expected impact**: Medium — longer tail. Dev.to posts surface in Google for "terminal tools" and "developer setup" queries. This campaign seeds SEO and positions the product in the "tools that reflect who you are" category rather than "toy."

**Execution steps**:
1. Write a 600-word dev.to post titled *"My terminal pet judged my coding style — and it was right"*. Narrative arc: installed the pet, raised a Maskutchi (Poor path, 5+ care mistakes), realized it mapped exactly to how I actually shipped that week — fast, messy, too many loops. Include a screenshot of the evolution result with `tama share` card.
2. End the post with: "The Good path is Mimitchi. I'm trying again." This creates a sequel hook and encourages readers to share their own evolution results.
3. Cross-post to Hashnode and personal blog (canonical on dev.to for SEO).
4. Share the post in r/programming and r/devops. Title on Reddit: *"I wrote about what my terminal Tamagotchi's evolution path revealed about how I code"* — Reddit hates product pitches; frame it as a personal story.
5. Reply to every comment on every platform within 24 hours.
6. Pitch the topic as a 5-minute lightning talk at a local devtools or CLI meetup.

---

### Campaign 5 — Show HN + Product Hunt coordinated double-launch

**Channel**: Hacker News (Show HN), Product Hunt
**Messaging angle**: The demo and the hook. Show, don't tell.
**Effort**: L
**Expected impact**: Very high if executed well. A Show HN front-page run generates a permanent, credible inbound link and drives a spike in GitHub stars. Product Hunt extends the window to 24 hours and pulls in a non-HN audience.

**Execution steps**:
1. Pre-launch (7 days before): post in `#show-and-tell` of 3–5 dev Discords to warm up early supporters who can upvote on launch day. Do not post the HN link yet.
2. Launch day timing: post Show HN at 9am ET on a Tuesday or Wednesday (historically highest HN engagement for Show HN posts).
3. Show HN title format: *"Show HN: Terminal Tamagotchi — a virtual pet that reacts to your Claude Code agent"* — the AI agent hook differentiates it from "another terminal toy."
4. First comment (post immediately after submission): paste the full demo terminal screenshot, `brew install tamagotchi` one-liner, and the three most interesting pet reactions to agent states (tests pass → Happy +2, stuck in loop → anxious animation). This becomes the de facto landing page for skimmers.
5. Product Hunt: launch the same day, 12:01am PT. Prepare a 60-second Loom demo video showing the tmux status bar integration and `tama share` card generation — embed it as the primary media. Write a maker comment explaining the AI agent hook and tagging the Claude/Aider/Goose communities.
6. DM or email 20 developer friends and newsletter authors the Product Hunt link at 7am PT. Ask specifically for a comment, not just an upvote — comments drive algorithmic placement.
7. Post the Product Hunt link to all relevant Discords and the project's Twitter/X at 8am PT.

---

## 2. Positioning Options

---

### Option A — vs. GitHub profile pets / static README decorations

**Frame**: "The one that's actually alive"
**One-liner**: Unlike static GitHub shields or profile-README widgets, your terminal Tamagotchi has real-time stats that decay when you're away, evolves based on how you work, and reacts live to your AI coding agent.
**Why it wins this comparison**: Static decorations are passive. This is interactive and ambient. The "it ages in real time even when the app is closed" mechanic is a genuine differentiator that no badge can replicate.
**Risk**: Developers who only want a visual flair may not value the added complexity.

---

### Option B — vs. WakaTime / coding metrics dashboards

**Frame**: "Developer identity you didn't have to fill out a form for"
**One-liner**: WakaTime tracks your hours and shows them in a dashboard you have to remember to check. Your terminal Tamagotchi lives in your tmux status bar and its evolution path reflects how you actually coded — no dashboard, no login, no data leaving your machine.
**Why it wins this comparison**: WakaTime requires opt-in self-surveillance and a web dashboard. This is ambient, local-first, and emotionally engaging rather than analytical. No Jira-badge energy.
**Risk**: Power users who want raw metrics will still prefer WakaTime for reporting. Position as complementary, not a replacement.

---

### Option C — vs. classic Tamagotchi / nostalgia toys

**Frame**: "The Tamagotchi that grew up with you"
**One-liner**: The original Tamagotchi was a toy you carried in your pocket. This one lives in the terminal you never leave, reacts to the AI agent you run instead of writing all the code yourself, and its evolution path is a record of how you shipped.
**Why it wins this comparison**: Nostalgia is the acquisition hook, but the AI agent awareness is the retentive differentiator. Every developer 25–45 understands the Tamagotchi reference instantly. The payoff — "but this one watches your Claude Code agent" — is the surprise.
**Risk**: Nostalgia framing risks making the product feel like a novelty rather than a tool. Mitigate by leading with the tmux integration screenshot first, nostalgia reference second.

---

### Option D — vs. CodeStreaks / habit-tracking tools

**Frame**: "Habit tracking with emotional stakes"
**One-liner**: CodeStreaks shows you a streak counter. Your terminal Tamagotchi shows you a living creature that gets hungry when you stop shipping and celebrates when your tests pass — stakes that a number cannot replicate.
**Why it wins this comparison**: Streak counters are cold. An animated ASCII creature that looks anxious when your Claude Code agent is looping creates genuine emotional engagement. The evolutionary arc (Egg to Adult) is a visible, shareable record of consistency.
**Risk**: Users who want unambiguous daily habit data will find the pet mechanic too abstract. Offer `tama status --json` for those users and let it coexist.

---

### Option E — vs. no tool (the default: nothing in the terminal)

**Frame**: "Your terminal has never been this alive" (beachhead positioning, recommended)
**One-liner**: Most developer terminals are a black rectangle with white text. Yours can have a pet that reacts to your code, evolves based on how well you care for it, and looks anxious when your AI agent gets stuck.
**Why it wins this comparison**: No displacement required. The emotional hook ("your terminal is alive") works for a developer who has never used any analogous product. This is the largest addressable audience.
**Risk**: No competitive contrast means the product has to sell itself on pure novelty. The demo must do the work.

**Recommended positioning: Option E (vs. nothing) as the primary frame, with Option C (nostalgia) as the acquisition hook.**

Rationale: Most developers have not used a terminal gamification tool. Framing against "nothing" means the product only has to beat the status quo (a blank terminal). The Tamagotchi nostalgia reference gets immediate recognition from the core demographic (25–45 year old developers) and primes the correct mental model before the AI agent hook lands as a surprise differentiator. Option B (vs. WakaTime) is useful for PR pitches and developer newsletter blurbs where you need a credible "vs." frame.

---

## 3. Value Prop Copy

---

### Tagline (8 words or fewer)

> **Your terminal finally has something to live for.**

Alternative (harder edge):

> **The pet your terminal has been missing.**

---

### Elevator pitch (2–3 sentences)

Terminal Tamagotchi is a virtual pet that lives in your tmux status bar and evolves based on how you code. It reacts in real time to your AI coding agent — happy when your tests pass, anxious when Claude Code gets stuck in a loop, celebratory when a task completes. It's the one developer tool that gets sadder the less you ship.

---

### Landing page hero

**Headline**:
> Your AI agent now has a pet.

**Subheading**:
> Terminal Tamagotchi lives in your tmux status bar and reacts to everything your Claude Code, Aider, or Goose agent does — shipping, looping, passing tests, failing builds. Raise it well and it evolves. Neglect it and it sulks. One command to install. No data leaves your machine.

---

### Sales one-liner

> A virtual pet that lives in your terminal, evolves based on how you code, and reacts live to your AI coding agent — `brew install tamagotchi`.

---

### Show HN opening line

> I built a Tamagotchi that lives in your tmux status bar and gets anxious when your Claude Code agent is stuck in a loop. It evolves based on how well you maintain your coding habits. One-line install, MIT, local-only.

---

### Twitter/X bio line (160 characters or fewer)

> Virtual pet for your terminal. Lives in tmux, reacts to Claude Code/Aider/Goose, evolves with your coding habits. pip/npm/brew. MIT, local-first.

---

## 4. Messaging Matrix

| Audience | Key Message | Proof Point | CTA |
|---|---|---|---|
| **Solo devs (Terminal Aesthetes)** | Your terminal is the most personal surface you have — it deserves something alive in it. Your pet lives in your tmux status bar, evolves through 6 stages based on your care, and generates a shareable ASCII card you can put in your GitHub README or drop in Discord. | `tama share` card embeds directly in GitHub profile READMEs. Integrates with Starship prompt and tmux status bar in one command: `tama install --tmux`. | `brew install tamagotchi` — first pet hatches in under 60 seconds. |
| **AI agent operators (Claude Code, Aider, Goose users)** | You kick off an agent run and then what — tail the logs? Your terminal Tamagotchi is an ambient mood indicator for your agent. Happy pet = agent is shipping. Anxious pet = agent is looping. Sad pet = something failed. One glance instead of a log tail. | Pet state maps directly to agent behavioral states (SHIPPING, LOOPING, BLOCKED, DONE) via hooks into Claude Code, Aider, and Goose. Works across multiple tmux windows — each agent can have a named pet. | `tama install --claude-code` — one command wires up all Claude Code hooks. |
| **Team leads / engineering managers** | You want your team to enjoy shipping, not just celebrate the outcome. Drop this in Slack, let engineers install it themselves, and watch the `#tools` channel light up with pet screenshots. No admin rollout, no IT approval, no subscription, nothing tracked or reported to you. | MIT, local-first — no server, no telemetry, no data leaving the machine. A single manager mention drives 5–10 organic installs. Phase 3 (peer discovery) brings optional team rooms for LAN or Tailscale setups. | Share the README link in Slack or the team `#dev` channel. One sentence: "it's a terminal pet that reacts to your AI agent." |
| **Open source contributors** | The evolution tree needs your sprites. The plugin system needs your agent integrations. The peer discovery layer needs your WebSocket protocol design. This is a project where your contribution — a new ASCII character, a Cursor plugin, a hibernation mechanic — ships to everyone who installs it. | Clean architecture (`core/`, `ui/`, `plugins/` separated), 52 passing tests, `BasePlugin` with documented lifecycle hooks, `good first issue` tags on GitHub. Plugin drop-in requires zero install: drop a `.py` in `~/.tamagotchi/plugins/`. | `git clone` + `uv sync --dev` + pick an open issue. The `CONTRIBUTING.md` has a good first contributions table. |

---

## 5. Launch Checklist

---

### Show HN

- [ ] Confirm the pet hatches in under 60 seconds from `brew install tamagotchi` — run the install cold on a fresh shell and time it.
- [ ] Take the canonical screenshot: Neovim + tmux + Starship on macOS with the pet visible in the status bar. This is the image you paste as the first comment.
- [ ] Draft the Show HN title. Test two versions: (A) *"Show HN: Terminal Tamagotchi — virtual pet that reacts to your Claude Code agent"* vs. (B) *"Show HN: I put a Tamagotchi in my terminal — it gets anxious when my AI agent loops"*. Version B has a stronger personal story hook.
- [ ] Write the first comment in advance (paste into the submission immediately after posting). Include: screenshot, one-liner install, top 3 pet reactions to agent events, link to `tama share` example. Under 150 words — HN readers skim.
- [ ] Prepare answers to the most likely HN pushback: "why not just WakaTime?" / "isn't this a distraction?" / "what data does it collect?" — answer each in under two sentences.
- [ ] Do not post on a Monday or Friday. Post at 9am ET on a Tuesday or Wednesday.
- [ ] Have 5 people ready to leave substantive early comments (not upvotes) — early comment velocity affects HN ranking.

---

### Product Hunt

- [ ] Create the product page 48 hours before launch day. Set go-live to 12:01am PT.
- [ ] Product tagline (60 chars max): *"The virtual pet that lives in your terminal and watches your AI agent"*
- [ ] Record a 60-second Loom: open tmux, show the pet in the status bar, run `tama share`, paste the ASCII card. Show the agent plugin reacting (agent writes files → pet dances). No voiceover required — terminal is self-explanatory with on-screen annotations.
- [ ] Write the maker comment before launch. Lead with the AI agent hook, end with the Phase 3 peer discovery roadmap — gives readers something to look forward to. Mention the MIT license and local-only data explicitly.
- [ ] Upload 3–4 screenshots: (1) tmux status bar with the pet, (2) full TUI with stats, (3) `tama share` card output, (4) agent plugin diagram showing pet reactions.
- [ ] Line up at least 10 people to comment on launch day. Reach out the day before via DM. Ask specifically for a comment, not just a vote.
- [ ] Post the Product Hunt link to Twitter/X at 8am PT on launch day. Post to relevant Discord servers at the same time.
- [ ] Respond to every Product Hunt comment within 2 hours on launch day.

---

### Twitter/X

- [ ] Three tweets ready to go before launch day, scheduled at: 9am ET (Show HN link + screenshot), 1pm ET (quote-tweet of the best early reply), 5pm ET (Product Hunt link + day-1 stats: stars, installs if trackable).
- [ ] Record a sub-30-second screen recording of the pet reacting to a test suite passing — no voiceover. This is your pinned tweet for launch week.
- [ ] Write the tweet that goes with the Show HN post. Do not just paste the HN link. Lead with the visual: "I added a Tamagotchi to my tmux status bar. Here's what it looks like when my Claude Code agent passes tests." + screen recording. HN link in the second tweet of the thread.
- [ ] Follow and prep @-mentions for developer influencers in the CLI/terminal tools space who are likely to reshare. Do not cold DM — reply to their existing tweets about terminal setup / AI agents.
- [ ] Use hashtags: #terminal #devtools #ClaudeAI #tmux — use at most 3 per tweet. Do not use #Tamagotchi (wrong audience).
- [ ] Pin the screen recording tweet for the first two weeks post-launch.

---

### Dev Discord servers (priority order)

- [ ] **Neovim Discord** — `#plugins` or `#random`. Post the tmux + Neovim screenshot. Most relevant audience.
- [ ] **Claude.ai / Anthropic Discord** (if publicly accessible) — post in `#tools` or `#community`. The AI agent hook is the most differentiated feature here.
- [ ] **Aider Discord** — `#general` or `#tools`. Post the `tama install --aider` one-liner.
- [ ] **Goose Discord** (Block) — same approach as Aider.
- [ ] **Starship Discord** — post the Starship integration screenshot. The Starship community cares about terminal aesthetics specifically.
- [ ] **r/unixporn** — post the canonical tmux screenshot. Title: *"Finally added something alive to my terminal. Terminal Tamagotchi in tmux + Neovim [OC]"*. Do not mention it's your own project in the title. Mention it in the top comment.
- [ ] **r/commandline** and **r/programming** — post the dev.to narrative post (Campaign 4), not a direct product link. Reddit tolerates personal stories, not launch pitches.
- [ ] For each server: post once, do not re-post. Reply to every response. Do not cross-post the exact same message — write a unique first line for each community.

---

### Pre-launch checklist (complete before any public post)

- [ ] `brew install tamagotchi` works end-to-end on macOS (fresh shell, no prior install).
- [ ] `pip install tamagotchi` works on Python 3.12+ on macOS and Linux.
- [ ] `npx tamagotchi` works without any global install.
- [ ] `tama install --claude-code` succeeds and the hook fires on the next Claude Code session.
- [ ] `tama share` generates a valid ASCII card and copies to clipboard.
- [ ] README has: a GIF or screenshot at the very top (above the fold), a one-line install command visible without scrolling, and an explicit "no data leaves your machine" statement.
- [ ] GitHub repo has: a description set, a topic list (`terminal`, `tamagotchi`, `cli-tool`, `claude-code`, `tmux`, `developer-tools`), and at least 5 `good first issue` labels on open issues.
- [ ] `tama --version` returns a valid semver string.
- [ ] The pet does not crash or render broken characters in: iTerm2 (macOS), Alacritty (macOS), Windows Terminal (WSL2), and VS Code integrated terminal.
- [ ] CONTRIBUTING.md exists and has a "good first contributions" table.
- [ ] LICENSE file is present (MIT).

---

*This document is a living toolkit. Update the messaging after seeing which angle drives the most engagement in the first two weeks. The AI agent hook is the most differentiated claim — lead with it on Hacker News and AI-focused communities. The nostalgia + terminal aesthetics hook is the faster grab on Twitter/X and r/unixporn.*
