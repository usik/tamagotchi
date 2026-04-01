"""Core pet engine."""
from tamagotchi.core.pet import Pet, LifeStage, PetCharacter
from tamagotchi.core.evolution import EvolutionEngine
from tamagotchi.core.persistence import save_pet, load_pet

__all__ = ["Pet", "LifeStage", "PetCharacter", "EvolutionEngine", "save_pet", "load_pet"]
