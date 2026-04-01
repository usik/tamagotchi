# Tamagotchi — Starship Module

Shows your pet's mood, name, and hunger hearts in your shell prompt.

```
😊 Pixel ♥♥♥♡ ❯
```

## Install

1. Install tamagotchi:

   ```bash
   pip install tamagotchi
   ```

2. Add the module to your `~/.config/starship.toml`:

   ```bash
   cat integrations/starship/tamagotchi.toml >> ~/.config/starship.toml
   ```

   Or copy-paste the `[custom.tamagotchi]` block manually.

3. Add `$custom.tamagotchi` to your prompt `format`:

   ```toml
   format = """
   $custom.tamagotchi\
   $directory\
   $git_branch\
   $character"""
   ```

## Status indicators

| Symbol | Meaning |
|--------|---------|
| 😊 | Happy |
| 😋 | Hungry |
| 😢 | Unhappy |
| 🤒 | Sick |
| 💤 | Sleeping |
| 💀 | Dead |
| ♥ | Full hunger heart |
| ♡ | Empty hunger heart |
| ! | Needs attention |
| 🥚 | No pet yet |

## Performance note

Starship runs the command on every prompt render. `tama status --json` is a fast
local read (~20ms). If you're on a slow machine, wrap the command with a file-based
cache (write to `/tmp/tama_status` every 30s via a background job).

## Requires

- `tama` installed and on your `$PATH`
- Starship `>= 1.0`
