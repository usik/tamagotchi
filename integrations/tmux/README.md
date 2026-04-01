# Tamagotchi — tmux Plugin

Shows your pet's name, hunger hearts, and mood in the tmux status bar.

```
😊 Pixel ♥♥♥♡  [12:34]
```

## Install via TPM (recommended)

Add to `~/.tmux.conf`:

```tmux
set -g @plugin 'usik/tamagotchi'
```

Then press `prefix + I` to install.

## Manual install

```bash
git clone https://github.com/usik/tamagotchi ~/.tmux/plugins/tamagotchi
~/.tmux/plugins/tamagotchi/integrations/tmux/tamagotchi.tmux
```

## Options

Add to `~/.tmux.conf` before the plugin line:

```tmux
# Refresh interval in seconds (default: 30)
set -g @tamagotchi-interval 15
```

## Custom placement

Use `#{tamagotchi}` anywhere in your status line:

```tmux
set -g status-right "#{tamagotchi} | %H:%M"
```

## Requires

- `tama` installed and on your `$PATH` (`pip install tamagotchi`)
