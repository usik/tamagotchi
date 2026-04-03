"""
tama share --gist — upload pet card to GitHub Gist and return embed URL.

Uses `gh gist create` (GitHub CLI) — no API token needed if gh is authed.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def upload_gist(card: str, pet_name: str) -> str | None:
    """Upload card to a GitHub Gist, return raw URL. Returns None on failure."""
    # Check gh is available
    if not _has_gh():
        print("⚠️  GitHub CLI (gh) not found. Install: https://cli.github.com")
        return None

    filename = f"{pet_name.lower()}_tamagotchi.txt"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                     prefix=f"{pet_name}_", delete=False) as f:
        f.write(card)
        f.write(f"\n\nRaise your own: github.com/usik/tamagotchi\n")
        tmp_path = f.name

    try:
        result = subprocess.run(
            ["gh", "gist", "create", tmp_path,
             "--filename", filename,
             "--desc", f"{pet_name}'s tamagotchi card — github.com/usik/tamagotchi",
             "--public"],
            capture_output=True, text=True, check=True,
        )
        gist_url = result.stdout.strip()
        # Convert gist URL to raw URL for embedding
        # https://gist.github.com/user/abc123 → https://gist.githubusercontent.com/user/abc123/raw/
        raw_url = _to_raw_url(gist_url, filename)
        return gist_url, raw_url
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Gist upload failed: {e.stderr.strip()}")
        return None
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def _has_gh() -> bool:
    import shutil
    return shutil.which("gh") is not None


def _to_raw_url(gist_url: str, filename: str) -> str:
    """Convert gist page URL to raw content URL."""
    # gist_url: https://gist.github.com/usik/abc123def456
    parts = gist_url.rstrip("/").split("/")
    if len(parts) >= 2:
        user = parts[-2]
        gist_id = parts[-1]
        return f"https://gist.githubusercontent.com/{user}/{gist_id}/raw/{filename}"
    return gist_url


def print_embed_instructions(pet_name: str, gist_url: str, raw_url: str) -> None:
    """Print copy-paste instructions for embedding in GitHub README."""
    print()
    print("─" * 52)
    print(f"  Gist: {gist_url}")
    print()
    print("  Embed in your GitHub README:")
    print()
    print(f"  ![{pet_name}]({raw_url})")
    print()
    print("  Or as a code block link:")
    print()
    print(f"  [{pet_name}'s tamagotchi]({gist_url})")
    print("─" * 52)
    print()
