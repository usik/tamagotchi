"""
tama install — auto-detect AI coding agents and wire up tamagotchi hooks.

Usage:
    tama install              # detect everything, interactive
    tama install --all        # install all detected, no prompts
    tama install --claude-code
    tama install --aider
    tama install --goose
    tama install --starship
    tama install --tmux
    tama install --dry-run    # show what would be done, no changes
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

# ---------------------------------------------------------------------------
# Detection helpers
# ---------------------------------------------------------------------------

def _cmd_exists(name: str) -> bool:
    return shutil.which(name) is not None


def _detect() -> dict[str, bool]:
    return {
        "claude-code": _cmd_exists("claude"),
        "aider":       _cmd_exists("aider"),
        "goose":       _cmd_exists("goose"),
        "starship":    _cmd_exists("starship"),
        "tmux":        _cmd_exists("tmux"),
    }


# ---------------------------------------------------------------------------
# Installer: Claude Code
# ---------------------------------------------------------------------------

CLAUDE_SETTINGS = Path.home() / ".claude" / "settings.json"
CLAUDE_SKILLS_DIR = Path.home() / ".claude" / "skills" / "tamagotchi"

CLAUDE_HOOKS = {
    "PreToolUse": [{"matcher": "", "hooks": [
        {"type": "command", "command": "tama-hook pre-tool $CLAUDE_TOOL_NAME"}
    ]}],
    "PostToolUse": [{"matcher": "", "hooks": [
        {"type": "command", "command": "tama-hook post-tool $CLAUDE_TOOL_NAME $CLAUDE_TOOL_EXIT_CODE"}
    ]}],
    "Stop": [{"matcher": "", "hooks": [
        {"type": "command", "command": "tama-hook stop $CLAUDE_STOP_REASON"}
    ]}],
    "SubagentStart": [{"matcher": "", "hooks": [
        {"type": "command", "command": "tama-hook subagent-start"}
    ]}],
}


def install_claude_code(dry_run: bool = False) -> list[str]:
    actions = []

    # 1. Patch settings.json
    CLAUDE_SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    if CLAUDE_SETTINGS.exists():
        try:
            settings = json.loads(CLAUDE_SETTINGS.read_text())
        except json.JSONDecodeError:
            settings = {}
    else:
        settings = {}

    hooks = settings.setdefault("hooks", {})
    added: list[str] = []
    for event, entries in CLAUDE_HOOKS.items():
        existing = hooks.get(event, [])
        # Check if tama-hook already present
        already = any(
            "tama-hook" in h.get("command", "")
            for entry in existing
            for h in entry.get("hooks", [])
        )
        if not already:
            hooks.setdefault(event, []).extend(entries)
            added.append(event)

    if added:
        actions.append(f"  patch ~/.claude/settings.json — add hooks: {', '.join(added)}")
        if not dry_run:
            CLAUDE_SETTINGS.write_text(json.dumps(settings, indent=2))
    else:
        actions.append("  ~/.claude/settings.json — hooks already present, skipped")

    # 2. Copy skill file to ~/.claude/skills/tamagotchi/
    skill_src = Path(__file__).parent.parent.parent.parent / \
        "integrations" / "claude_code_skill" / "setup-tamagotchi-hooks.md"
    # Fallback: find relative to package install location
    if not skill_src.exists():
        # Installed package: skill lives alongside the package data
        import tamagotchi
        pkg_root = Path(tamagotchi.__file__).parent
        skill_src = pkg_root / "data" / "setup-tamagotchi-hooks.md"

    if skill_src.exists():
        dest = CLAUDE_SKILLS_DIR / "setup-tamagotchi-hooks.md"
        actions.append(f"  copy skill → {dest}")
        if not dry_run:
            CLAUDE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
            import shutil as _shutil
            _shutil.copy2(skill_src, dest)
    else:
        actions.append("  skill file not found — skipping (run from repo or reinstall)")

    return actions


# ---------------------------------------------------------------------------
# Installer: Aider
# ---------------------------------------------------------------------------

AIDER_CONF = Path.home() / ".aider.conf.yml"

AIDER_HOOKS_BLOCK = """
# tamagotchi hooks — added by `tama install`
pre-commit-cmd: tama-hook pre-tool bash
post-commit-cmd: tama-hook post-tool bash 0
"""


def install_aider(dry_run: bool = False) -> list[str]:
    actions = []

    if AIDER_CONF.exists():
        content = AIDER_CONF.read_text()
        if "tama-hook" in content:
            return ["  ~/.aider.conf.yml — hooks already present, skipped"]
    else:
        content = ""

    actions.append(f"  append tamagotchi hooks to {AIDER_CONF}")
    if not dry_run:
        with AIDER_CONF.open("a") as f:
            f.write(AIDER_HOOKS_BLOCK)

    # Also write an aider plugin event file marker
    event_dir = Path.home() / ".tamagotchi"
    event_dir.mkdir(parents=True, exist_ok=True)
    actions.append("  create ~/.tamagotchi/aider_events.jsonl")
    if not dry_run:
        (event_dir / "aider_events.jsonl").touch(exist_ok=True)

    return actions


# ---------------------------------------------------------------------------
# Installer: Goose (Block)
# ---------------------------------------------------------------------------

GOOSE_PROFILE = Path.home() / ".config" / "goose" / "profiles.yaml"
GOOSE_SHIM_DIR = Path.home() / ".local" / "bin"
GOOSE_SHIM = GOOSE_SHIM_DIR / "goose-tama-shim"

GOOSE_SHIM_CONTENT = """\
#!/usr/bin/env bash
# Tamagotchi shim for Goose — records session start/stop
# Installed by `tama install --goose`
TAMA_EVENTS=~/.tamagotchi/goose_events.jsonl
mkdir -p "$(dirname "$TAMA_EVENTS")"

echo '{"type":"session_start","ts":'$(date +%s)'}' >> "$TAMA_EVENTS"
goose "$@"
EXIT=$?
if [ $EXIT -eq 0 ]; then
  echo '{"type":"stop","reason":"success","ts":'$(date +%s)'}' >> "$TAMA_EVENTS"
else
  echo '{"type":"stop","reason":"error","ts":'$(date +%s)'}' >> "$TAMA_EVENTS"
fi
exit $EXIT
"""


def install_goose(dry_run: bool = False) -> list[str]:
    actions = []

    # Write shim
    actions.append(f"  write Goose shim → {GOOSE_SHIM}")
    if not dry_run:
        GOOSE_SHIM_DIR.mkdir(parents=True, exist_ok=True)
        GOOSE_SHIM.write_text(GOOSE_SHIM_CONTENT)
        GOOSE_SHIM.chmod(0o755)

    # Suggest alias
    alias_line = f'alias goose="{GOOSE_SHIM}"'
    actions.append(f"  add to your shell rc: {alias_line}")
    if not dry_run:
        _append_shell_alias(alias_line, "goose")

    return actions


# ---------------------------------------------------------------------------
# Installer: Starship
# ---------------------------------------------------------------------------

STARSHIP_CONFIG = Path(os.environ.get("STARSHIP_CONFIG", Path.home() / ".config" / "starship.toml"))

# The [custom.tamagotchi] block to append
_STARSHIP_BLOCK_MARKER = "[custom.tamagotchi]"

# Source: integrations/starship/tamagotchi.toml — embedded inline for pip install
STARSHIP_MODULE = r"""
# tamagotchi — added by `tama install`
[custom.tamagotchi]
description = "Tamagotchi pet status"
command = """
STATUS=$(tama status --json 2>/dev/null)
if [ -z "$STATUS" ]; then echo "🥚"; exit 0; fi
NAME=$(echo "$STATUS"   | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('name','?'))" 2>/dev/null)
MOOD=$(echo "$STATUS"   | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('mood','?'))" 2>/dev/null)
HUNGER=$(echo "$STATUS" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('hunger',0))" 2>/dev/null)
ATTN=$(echo "$STATUS"   | python3 -c "import sys,json; d=json.load(sys.stdin); print('!' if d.get('needs_attention') else '')" 2>/dev/null)
case "$MOOD" in happy) ICON="😊";; hungry) ICON="😋";; unhappy) ICON="😢";; sick) ICON="🤒";; sleeping) ICON="💤";; dead) ICON="💀";; *) ICON="😐";; esac
HEARTS=""; for i in 1 2 3 4; do [ "$i" -le "$HUNGER" ] && HEARTS="${HEARTS}♥" || HEARTS="${HEARTS}♡"; done
BELL=""; [ -n "$ATTN" ] && BELL=" !"
echo "${ICON} ${NAME} ${HEARTS}${BELL}"
"""
when = "command -v tama > /dev/null"
shell = ["bash", "--norc", "--noprofile"]
format = "[$output]($style) "
style = "bold cyan"
"""


def install_starship(dry_run: bool = False) -> list[str]:
    actions = []

    if STARSHIP_CONFIG.exists():
        content = STARSHIP_CONFIG.read_text()
        if _STARSHIP_BLOCK_MARKER in content:
            return [f"  {STARSHIP_CONFIG} — [custom.tamagotchi] already present, skipped"]
    else:
        content = ""

    actions.append(f"  append [custom.tamagotchi] to {STARSHIP_CONFIG}")
    if not dry_run:
        STARSHIP_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        with STARSHIP_CONFIG.open("a") as f:
            f.write(STARSHIP_MODULE)

    actions.append("  note: add $custom.tamagotchi to your prompt format if not using 'add_newline'")
    return actions


# ---------------------------------------------------------------------------
# Installer: tmux
# ---------------------------------------------------------------------------

TMUX_CONF = Path.home() / ".tmux.conf"
TMUX_PLUGIN_LINE = "set -g @plugin 'usik/tamagotchi'"


def install_tmux(dry_run: bool = False) -> list[str]:
    actions = []

    if TMUX_CONF.exists():
        content = TMUX_CONF.read_text()
        if "tamagotchi" in content:
            return [f"  {TMUX_CONF} — tamagotchi already configured, skipped"]
    else:
        content = ""

    has_tpm = "tpm" in content

    if has_tpm:
        actions.append(f"  append plugin line to {TMUX_CONF}: {TMUX_PLUGIN_LINE}")
        if not dry_run:
            with TMUX_CONF.open("a") as f:
                f.write(f"\n# tamagotchi — added by `tama install`\n{TMUX_PLUGIN_LINE}\n")
        actions.append("  then press prefix + I inside tmux to install")
    else:
        # No TPM — wire status bar directly
        tama_hook = shutil.which("tama") or "tama"
        status_line = f'set -g status-right "#({tama_hook} status --json | python3 -c \\"import sys,json; d=json.load(sys.stdin); h=d.get(\'hunger\',0); m=d.get(\'mood\',\'?\'); n=d.get(\'name\',\'?\'); icons={{\'happy\':\'😊\',\'hungry\':\'😋\',\'unhappy\':\'😢\',\'sick\':\'🤒\',\'sleeping\':\'💤\',\'dead\':\'💀\'}}; print(icons.get(m,\'😐\')+\' \'+n+\' \'+\'♥\'*h+\'♡\'*(4-h))\\")" | %%H:%%M"'
        actions.append(f"  append status-right to {TMUX_CONF}")
        if not dry_run:
            with TMUX_CONF.open("a") as f:
                f.write(f"\n# tamagotchi — added by `tama install`\nset -g status-interval 30\n{status_line}\n")
        actions.append("  note: TPM not detected — used direct status-right instead")

    return actions


# ---------------------------------------------------------------------------
# Shell alias helper
# ---------------------------------------------------------------------------

def _append_shell_alias(alias_line: str, marker: str) -> None:
    """Append an alias to the user's shell rc file if not already present."""
    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        rc = Path.home() / ".zshrc"
    elif "fish" in shell:
        rc = Path.home() / ".config" / "fish" / "config.fish"
        alias_line = f"alias {marker}='{alias_line.split(\"=\", 1)[1].strip(chr(34))}'"
    else:
        rc = Path.home() / ".bashrc"

    if rc.exists() and alias_line in rc.read_text():
        return
    with rc.open("a") as f:
        f.write(f"\n# tamagotchi — added by `tama install`\n{alias_line}\n")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

INSTALLERS: dict[str, Callable[[bool], list[str]]] = {
    "claude-code": install_claude_code,
    "aider":       install_aider,
    "goose":       install_goose,
    "starship":    install_starship,
    "tmux":        install_tmux,
}

LABELS = {
    "claude-code": "Claude Code",
    "aider":       "Aider",
    "goose":       "Goose (Block)",
    "starship":    "Starship prompt",
    "tmux":        "tmux status bar",
}


def run_install(args: list[str]) -> None:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()

    dry_run = "--dry-run" in args
    install_all = "--all" in args

    # Which targets to install
    explicit = [k for k in INSTALLERS if f"--{k}" in args]
    detected = _detect()

    if explicit:
        targets = explicit
    elif install_all:
        targets = list(INSTALLERS.keys())
    else:
        # Interactive: show detected, ask which to install
        console.print(Panel("[bold]tama install[/] — wire tamagotchi to your tools",
                             border_style="bright_cyan", width=52))
        console.print()
        console.print("[bold]Detected:[/]")
        for k, label in LABELS.items():
            icon = "[green]✓[/]" if detected[k] else "[dim]✗[/]"
            console.print(f"  {icon}  {label}")
        console.print()

        found = [k for k, v in detected.items() if v]
        if not found:
            console.print("[yellow]No supported tools detected. Install aider, goose, starship, or tmux first.[/]")
            return

        console.print(f"[bold]Install hooks for:[/] {', '.join(LABELS[k] for k in found)}")
        answer = input("Proceed? [Y/n] ").strip().lower()
        if answer in ("n", "no"):
            console.print("[dim]Aborted.[/]")
            return
        targets = found

    if dry_run:
        console.print("[dim](dry run — no changes will be made)[/]\n")

    success = []
    failed = []

    for target in targets:
        label = LABELS.get(target, target)
        console.print(f"[bold cyan]{label}[/]")
        try:
            actions = INSTALLERS[target](dry_run=dry_run)
            for action in actions:
                console.print(f"[green]  {action}[/]" if "skipped" not in action else f"[dim]{action}[/]")
            success.append(label)
        except Exception as e:
            console.print(f"[red]  ✗ failed: {e}[/]")
            failed.append(label)
        console.print()

    # Summary
    if success:
        console.print(f"[bold green]✓ Done:[/] {', '.join(success)}")
    if failed:
        console.print(f"[bold red]✗ Failed:[/] {', '.join(failed)}")

    if not dry_run and success:
        console.print()
        console.print("[dim]Run [bold]tama status[/] to verify, or [bold]tama[/] to open the TUI.[/]")
