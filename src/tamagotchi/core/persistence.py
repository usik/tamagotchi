"""
Save and load pet state as JSON.
Default save location: ~/.tamagotchi/<name>.pet.json
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from tamagotchi.core.pet import Pet, LifeStage, PetCharacter, Mood


SAVE_DIR = Path.home() / ".tamagotchi"
GRAVEYARD_DIR = SAVE_DIR / "graveyard"


def _save_path(name: str, dead: bool = False) -> Path:
    base = GRAVEYARD_DIR if dead else SAVE_DIR
    base.mkdir(parents=True, exist_ok=True)
    return base / f"{name.lower().replace(' ', '_')}.pet.json"


def save_pet(pet: Pet) -> Path:
    """Serialize and save a pet to disk. Returns save path."""
    data = asdict(pet)
    # Convert enums to strings
    data["stage"] = pet.stage.value
    data["character"] = pet.character.value
    
    path = _save_path(pet.name, dead=not pet.is_alive)
    
    # If pet just died, cleanup the old live save
    if not pet.is_alive:
        live_path = _save_path(pet.name, dead=False)
        if live_path.exists():
            live_path.unlink()

    path.write_text(json.dumps(data, indent=2))
    return path


def load_pet(name: str, dead: bool = False) -> Optional[Pet]:
    """Load a pet by name. Returns None if not found."""
    path = _save_path(name, dead=dead)
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    # Convert enum strings back
    data["stage"] = LifeStage(data["stage"])
    data["character"] = PetCharacter(data["character"])
    return Pet(**data)


def list_saved_pets() -> list[str]:
    """Return list of saved live pet names."""
    if not SAVE_DIR.exists():
        return []
    return [p.name.removesuffix(".pet.json").replace("_", " ").title()
            for p in SAVE_DIR.glob("*.pet.json") if p.is_file()]


def list_dead_pets() -> list[str]:
    """Return list of saved deceased pet names."""
    if not GRAVEYARD_DIR.exists():
        return []
    return [p.name.removesuffix(".pet.json").replace("_", " ").title()
            for p in GRAVEYARD_DIR.glob("*.pet.json")]


def delete_pet(name: str) -> bool:
    """Delete a pet save file. Returns True if deleted."""
    path = _save_path(name)
    if path.exists():
        path.unlink()
        return True
    return False
