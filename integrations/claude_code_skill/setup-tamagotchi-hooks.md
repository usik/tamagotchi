# /setup-tamagotchi-hooks — Wire Tamagotchi to Claude Code

Connect your tamagotchi pet to Claude Code so it reacts to your coding sessions.
Your pet gets hungry, happy, or moody based on how your coding is going.

## What it does

- **You're shipping** → pet gets happier
- **You're in a loop** (same tools repeatedly) → pet gets hungry / unhappy
- **You're exploring** (grep, read) → pet stays neutral
- **You're blocked** (errors, retries) → pet mood drops
- **Session ends** → pet gets a small treat

## Invocation

```
/setup-tamagotchi-hooks
```

## Workflow

### Step 1: Check prerequisites

Verify `tama` is installed and a pet exists:

```bash
tama --version
tama status
```

If not installed: `pip install tamagotchi`

### Step 2: Find the hooks event file path

The Claude Code hooks write events to `~/.tamagotchi/claude_events.jsonl`.
The tamagotchi app polls this file every tick.

### Step 3: Add hooks to Claude Code settings

Add the following to `~/.claude/settings.json` (or `settings.local.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "tama-hook pre-tool $CLAUDE_TOOL_NAME"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "tama-hook post-tool $CLAUDE_TOOL_NAME $CLAUDE_TOOL_EXIT_CODE"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "tama-hook stop"
          }
        ]
      }
    ]
  }
}
```

### Step 4: Verify

Run a Claude Code session, then check pet status:

```bash
tama status
```

Your pet's mood and hunger should reflect your coding session.

## Hook commands reference

| Command | When fired | Pet effect |
|---------|-----------|------------|
| `tama-hook pre-tool <tool>` | Before any tool call | Logs tool to classifier |
| `tama-hook post-tool <tool> <exit>` | After tool returns | Updates behavioral state |
| `tama-hook stop` | Session ends | Awards treat if good session |
| `tama-hook subagent-start` | Subagent spawned | Logged as exploration |

## Behavioral states

The plugin classifies your session into one of:

- **SHIPPING** — consecutive write/edit/bash calls → pet happiness +1
- **LOOPING** — same tool called 3+ times → hunger +1
- **EXPLORING** — mostly reads/greps → neutral
- **BLOCKED** — tool errors repeatedly → mood −1
- **DONE** — stop event → small treat

## Requires

- `tama` and `tama-hook` on `$PATH` (`pip install tamagotchi`)
- Claude Code `>= 1.0`
- An existing pet (`tama` to hatch one)
