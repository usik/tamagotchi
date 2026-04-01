#!/usr/bin/env sh
# Tamagotchi — universal installer
# Usage: curl -fsSL https://raw.githubusercontent.com/usik/tamagotchi/main/install.sh | sh
set -e

REPO="usik/tamagotchi"
PKG="tamagotchi"

echo "👾 Installing tamagotchi..."

# Helper: check if a command exists
has() { command -v "$1" >/dev/null 2>&1; }

# ---------------------------------------------------------------------------
# Try installers in order of preference
# ---------------------------------------------------------------------------

if has pipx; then
  echo "→ Using pipx"
  pipx install "$PKG"

elif has uv; then
  echo "→ Using uv"
  uv tool install "$PKG"

elif has pip3; then
  echo "→ Using pip3"
  pip3 install --user "$PKG"

elif has pip; then
  echo "→ Using pip"
  pip install --user "$PKG"

elif has brew; then
  echo "→ Using Homebrew"
  brew tap "$REPO" 2>/dev/null || true
  brew install "$PKG"

elif has npm; then
  echo "→ Using npm (wrapper only — Python still required for the TUI)"
  npm install -g "$PKG"

else
  echo ""
  echo "⚠️  Could not find pip, pipx, uv, brew, or npm."
  echo ""
  echo "Install Python 3.12+ first:"
  echo "  https://python.org/downloads"
  echo ""
  echo "Then run:"
  echo "  pip install tamagotchi"
  exit 1
fi

# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------
if has tama; then
  echo ""
  echo "✅ Done! Run: tama"
else
  echo ""
  echo "✅ Installed! You may need to reload your shell:"
  echo "   source ~/.zshrc   # or ~/.bashrc"
  echo ""
  echo "Then run: tama"
fi
