#!/usr/bin/env bash
# Tamagotchi tmux plugin
# Install via TPM: set -g @plugin 'usik/tamagotchi'
# Or manually: run-shell /path/to/tamagotchi.tmux

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default options (override in tmux.conf)
INTERVAL="${TAMAGOTCHI_INTERVAL:-30}"  # refresh every 30s

main() {
  # Register the status-right interpolation token #{tamagotchi}
  local status_right
  status_right=$(tmux show-option -gqv "status-right")

  if [[ "$status_right" == *"#{tamagotchi}"* ]]; then
    # User has #{tamagotchi} in their status-right — replace it
    tmux set-option -g status-right \
      "$(echo "$status_right" | sed 's/#{tamagotchi}/$('"$CURRENT_DIR"'\/scripts\/status.sh)/g')"
  else
    # Auto-prepend to status-right
    tmux set-option -g status-right \
      "#($CURRENT_DIR/scripts/status.sh) $status_right"
  fi

  # Set up refresh interval
  tmux set-option -g status-interval "$INTERVAL"
}

main
