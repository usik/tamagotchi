#!/usr/bin/env bash
# Outputs a compact pet status string for tmux status bar
# Example output: 🐱 Pixel ❤️❤️❤️❤️ 😊

TAMA_CMD="${TAMA_CMD:-tama}"

# Check tama is installed
if ! command -v "$TAMA_CMD" &>/dev/null; then
  echo "🥚 install tama"
  exit 0
fi

# Get status JSON
STATUS=$("$TAMA_CMD" status --json 2>/dev/null)
if [[ -z "$STATUS" ]]; then
  echo "🥚 no pet"
  exit 0
fi

NAME=$(echo "$STATUS"    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('name','?'))" 2>/dev/null)
MOOD=$(echo "$STATUS"    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('mood','?'))" 2>/dev/null)
HUNGER=$(echo "$STATUS"  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('hunger',0))" 2>/dev/null)
STAGE=$(echo "$STATUS"   | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('stage','?'))" 2>/dev/null)
ATTN=$(echo "$STATUS"    | python3 -c "import sys,json; d=json.load(sys.stdin); print('1' if d.get('needs_attention') else '')" 2>/dev/null)

# Mood emoji
case "$MOOD" in
  happy)    MOOD_ICON="😊" ;;
  hungry)   MOOD_ICON="😋" ;;
  unhappy)  MOOD_ICON="😢" ;;
  sick)     MOOD_ICON="🤒" ;;
  sleeping) MOOD_ICON="💤" ;;
  dead)     MOOD_ICON="💀" ;;
  *)        MOOD_ICON="😐" ;;
esac

# Hunger hearts
HEARTS=""
for i in $(seq 1 4); do
  if [[ $i -le $HUNGER ]]; then
    HEARTS="${HEARTS}♥"
  else
    HEARTS="${HEARTS}♡"
  fi
done

# Attention bell
BELL=""
[[ -n "$ATTN" ]] && BELL=" !"

echo "${MOOD_ICON} ${NAME} ${HEARTS}${BELL}"
