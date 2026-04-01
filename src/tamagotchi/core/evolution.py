"""
Evolution engine — describes the evolution tree and provides helpers.
"""
from __future__ import annotations

from dataclasses import dataclass
from tamagotchi.core.pet import PetCharacter, LifeStage


@dataclass
class EvolutionPath:
    good: PetCharacter
    normal: PetCharacter
    bad: PetCharacter
    good_threshold: int    # care_mistakes < this → good
    bad_threshold: int     # care_mistakes >= this → bad


EVOLUTION_TREE: dict[LifeStage, EvolutionPath] = {
    LifeStage.CHILD: EvolutionPath(
        good=PetCharacter.CHILD_GOOD,
        normal=PetCharacter.CHILD_NORMAL,
        bad=PetCharacter.CHILD_BAD,
        good_threshold=2,
        bad_threshold=5,
    ),
    LifeStage.TEEN: EvolutionPath(
        good=PetCharacter.TEEN_GOOD,
        normal=PetCharacter.TEEN_NORMAL,
        bad=PetCharacter.TEEN_BAD,
        good_threshold=3,
        bad_threshold=6,
    ),
    LifeStage.ADULT: EvolutionPath(
        good=PetCharacter.ADULT_GOOD,
        normal=PetCharacter.ADULT_NORMAL,
        bad=PetCharacter.ADULT_BAD,
        good_threshold=2,
        bad_threshold=5,
    ),
    LifeStage.ELDER: EvolutionPath(
        good=PetCharacter.ELDER_GOOD,
        normal=PetCharacter.ELDER_NORMAL,
        bad=PetCharacter.ELDER_BAD,
        good_threshold=3,
        bad_threshold=7,
    ),
}

# Human-readable names for display
CHARACTER_NAMES: dict[PetCharacter, str] = {
    PetCharacter.EGG:             "Egg",
    PetCharacter.BABY:            "Baby",
    PetCharacter.CHILD_GOOD:      "Marutchi",
    PetCharacter.CHILD_NORMAL:    "Tonmarutchi",
    PetCharacter.CHILD_BAD:       "Kuchitamatchi",
    PetCharacter.TEEN_GOOD:       "Tamatchi",
    PetCharacter.TEEN_NORMAL:     "Kuchitamatchi Jr.",
    PetCharacter.TEEN_BAD:        "Zuccitchi",
    PetCharacter.ADULT_GOOD:      "Mimitchi",
    PetCharacter.ADULT_NORMAL:    "Mametchi",
    PetCharacter.ADULT_BAD:       "Maskutchi",
    PetCharacter.ELDER_GOOD:      "Ojitchi",
    PetCharacter.ELDER_NORMAL:    "Otokitchi",
    PetCharacter.ELDER_BAD:       "Tarakotchi",
    PetCharacter.DEAD:            "Gone",
}

CHARACTER_DESCRIPTIONS: dict[PetCharacter, str] = {
    PetCharacter.EGG:          "Waiting to hatch...",
    PetCharacter.BABY:         "Newborn and tiny.",
    PetCharacter.CHILD_GOOD:   "A round, cheerful little thing.",
    PetCharacter.CHILD_NORMAL: "A bit chubby, but happy enough.",
    PetCharacter.CHILD_BAD:    "Looks a little rough around the edges.",
    PetCharacter.TEEN_GOOD:    "Growing up well! Very lively.",
    PetCharacter.TEEN_NORMAL:  "Moody teenager energy.",
    PetCharacter.TEEN_BAD:     "Has a bit of an attitude.",
    PetCharacter.ADULT_GOOD:   "Beautiful and healthy! You did great.",
    PetCharacter.ADULT_NORMAL: "A respectable adult. Could be worse.",
    PetCharacter.ADULT_BAD:    "A bit rough, but they're yours.",
    PetCharacter.ELDER_GOOD:   "A wise and elegant elder.",
    PetCharacter.ELDER_NORMAL: "Getting on in years, still ticking.",
    PetCharacter.ELDER_BAD:    "Weathered and grumpy, but alive.",
    PetCharacter.DEAD:         "You can visit them in the graveyard.",
}


class EvolutionEngine:
    @staticmethod
    def resolve(stage: LifeStage, care_mistakes: int) -> PetCharacter:
        path = EVOLUTION_TREE.get(stage)
        if path is None:
            return PetCharacter.EGG
        if care_mistakes < path.good_threshold:
            return path.good
        if care_mistakes >= path.bad_threshold:
            return path.bad
        return path.normal

    @staticmethod
    def name(character: PetCharacter) -> str:
        return CHARACTER_NAMES.get(character, character.value)

    @staticmethod
    def description(character: PetCharacter) -> str:
        return CHARACTER_DESCRIPTIONS.get(character, "")
