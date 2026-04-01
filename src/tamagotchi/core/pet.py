"""
Core pet model — stats, lifecycle, actions.

Faithfully replicates original Tamagotchi mechanics:
  Hunger, Happiness, Weight, Age, Discipline, Health
  Life stages: Egg → Baby → Child → Teen → Adult → Elder → Dead
  Care mistakes drive evolution path (good / normal / bad)
  Real-time aging — pet lives on even when game is closed
"""
from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class LifeStage(Enum):
    EGG    = "egg"
    BABY   = "baby"
    CHILD  = "child"
    TEEN   = "teen"
    ADULT  = "adult"
    ELDER  = "elder"
    DEAD   = "dead"


class PetCharacter(Enum):
    """
    Character name encodes the evolution path.
    Format: <stage>_<path>   path = good | normal | bad
    """
    # Egg (always the same)
    EGG         = "egg"

    # Baby (always the same — too young to diverge)
    BABY        = "baby"

    # Child
    CHILD_GOOD   = "marutchi"    # well-cared
    CHILD_NORMAL = "tonmarutchi" # average care
    CHILD_BAD    = "kuchitamatchi"  # neglected

    # Teen
    TEEN_GOOD    = "tamatchi"
    TEEN_NORMAL  = "kuchitamatchi_teen"
    TEEN_BAD     = "zuccitchi"

    # Adult
    ADULT_GOOD   = "mimitchi"    # best care (<2 care mistakes)
    ADULT_NORMAL = "mametchi"    # decent  (2–4)
    ADULT_BAD    = "maskutchi"   # neglected (5+)

    # Elder
    ELDER_GOOD   = "ojitchi"
    ELDER_NORMAL = "otokitchi"
    ELDER_BAD    = "tarakotchi"

    # Dead
    DEAD        = "dead"


class Mood(Enum):
    HAPPY    = "happy"
    NEUTRAL  = "neutral"
    HUNGRY   = "hungry"
    UNHAPPY  = "unhappy"
    SICK     = "sick"
    SLEEPING = "sleeping"
    DEAD     = "dead"


# ---------------------------------------------------------------------------
# Timing constants (seconds) — tune these for playability
# ---------------------------------------------------------------------------

STAGE_DURATIONS: dict[LifeStage, float] = {
    LifeStage.EGG:   60 * 5,        #  5 min
    LifeStage.BABY:  60 * 60,       #  1 hour
    LifeStage.CHILD: 60 * 60 * 8,   #  8 hours
    LifeStage.TEEN:  60 * 60 * 24,  # 24 hours
    LifeStage.ADULT: 60 * 60 * 72,  # 72 hours
    LifeStage.ELDER: 60 * 60 * 48,  # 48 hours then dies of old age
    LifeStage.DEAD:  float("inf"),
}

HUNGER_DECAY_INTERVAL  = 60 * 30   # lose 1 hunger every 30 min
HAPPY_DECAY_INTERVAL   = 60 * 30   # lose 1 happy  every 30 min
DISCIPLINE_DECAY_INTERVAL = 60 * 60 * 6  # lose 5% discipline every 6h
POOP_INTERVAL          = 60 * 60 * 3     # poop every ~3h (randomised)
SICK_CHANCE_PER_TICK   = 0.002           # per-tick chance of random sickness
SICK_HUNGER_THRESHOLD  = 0              # sick if hunger hits 0 and untreated


# ---------------------------------------------------------------------------
# Pet dataclass
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    # Identity
    name: str = "Tama"
    character: PetCharacter = PetCharacter.EGG

    # Life stage & age
    stage: LifeStage = LifeStage.EGG
    age_days: float = 0.0          # displayed age in "years" (1 day = 1 year)
    born_at: float = field(default_factory=time.time)
    last_tick_at: float = field(default_factory=time.time)

    # Core stats (0–4 scale like original, except weight & discipline)
    hunger: int = 4        # 4=full, 0=starving
    happy: int = 4         # 4=very happy, 0=sad
    weight: int = 10       # arbitrary units; ideal ~10–20
    discipline: int = 50   # 0–100 %

    # Health
    sick: bool = False
    poop_count: int = 0    # 0–4; ≥4 triggers sickness
    lights_on: bool = True

    # Care quality tracking (drives evolution)
    care_mistakes: int = 0     # increments when attention ignored or needs unmet

    # Attention system — a flag requiring player action
    needs_attention: bool = False
    attention_reason: str = ""

    # Session tracking (useful for plugins)
    total_feedings: int = 0
    total_plays: int = 0
    total_medicines: int = 0
    times_disciplined: int = 0

    # Timestamps for interval tracking
    _last_hunger_decay: float = field(default_factory=time.time)
    _last_happy_decay: float = field(default_factory=time.time)
    _last_discipline_decay: float = field(default_factory=time.time)
    _next_poop_at: float = field(default_factory=lambda: time.time() + POOP_INTERVAL + random.uniform(-900, 900))

    # ---------------------------------------------------------------------------
    # Computed properties
    # ---------------------------------------------------------------------------

    @property
    def mood(self) -> Mood:
        if self.stage == LifeStage.DEAD:
            return Mood.DEAD
        if not self.lights_on:
            return Mood.SLEEPING
        if self.sick:
            return Mood.SICK
        if self.hunger == 0:
            return Mood.HUNGRY
        if self.happy == 0:
            return Mood.UNHAPPY
        if self.hunger <= 1 or self.happy <= 1:
            return Mood.NEUTRAL
        return Mood.HAPPY

    @property
    def is_alive(self) -> bool:
        return self.stage != LifeStage.DEAD

    @property
    def age_display(self) -> str:
        if self.age_days < 1:
            hours = int(self.age_days * 24)
            return f"{hours}h"
        return f"{int(self.age_days)}d"

    # ---------------------------------------------------------------------------
    # Actions
    # ---------------------------------------------------------------------------

    def feed_meal(self) -> str:
        """Feed a full meal — increases hunger, increases weight."""
        if not self.is_alive:
            return "..."
        if self.stage == LifeStage.EGG:
            return "It's still an egg!"
        if self.hunger >= 4:
            self.care_mistakes += 1  # overfeeding is a care mistake
            self.weight += 2
            return f"{self.name} is already full! (care mistake)"
        self.hunger = min(4, self.hunger + 2)
        self.weight += 2
        self.total_feedings += 1
        if self.needs_attention and self.attention_reason == "hungry":
            self._clear_attention()
        return f"{self.name} ate a meal! Yum! 🍱"

    def feed_snack(self) -> str:
        """Feed a snack — increases happy, increases weight more."""
        if not self.is_alive:
            return "..."
        if self.stage == LifeStage.EGG:
            return "It's still an egg!"
        self.happy = min(4, self.happy + 1)
        self.weight += 3
        self.total_feedings += 1
        return f"{self.name} loved the snack! 🍬"

    def play(self) -> str:
        """Play a mini-game — increases happy, decreases weight."""
        if not self.is_alive:
            return "..."
        if self.stage == LifeStage.EGG:
            return "It's still an egg!"
        if not self.lights_on:
            return f"{self.name} is sleeping. Turn the lights on first."
        self.happy = min(4, self.happy + 2)
        self.weight = max(1, self.weight - 1)
        self.total_plays += 1
        if self.needs_attention and self.attention_reason == "unhappy":
            self._clear_attention()
        return f"{self.name} had fun playing! ⭐"

    def give_medicine(self) -> str:
        """Administer medicine — cures sickness."""
        if not self.is_alive:
            return "..."
        if not self.sick:
            self.care_mistakes += 1  # unnecessary medicine is a mistake
            return f"{self.name} isn't sick! (care mistake)"
        self.sick = False
        self.total_medicines += 1
        if self.needs_attention and self.attention_reason == "sick":
            self._clear_attention()
        return f"{self.name} feels better! 💊"

    def discipline(self) -> str:
        """Scold the pet when it calls for attention needlessly."""
        if not self.is_alive:
            return "..."
        if self.stage in (LifeStage.EGG, LifeStage.BABY):
            return "Too young to discipline."
        if not self.needs_attention:
            self.care_mistakes += 1
            return f"{self.name} didn't need disciplining! (care mistake)"
        # Only discipline when pet called without real need
        self.discipline = min(100, self.discipline + 25)
        self.times_disciplined += 1
        self._clear_attention()
        return f"{self.name} was disciplined. 📣"

    def flush_poop(self) -> str:
        """Clean up poop."""
        if not self.is_alive:
            return "..."
        if self.poop_count == 0:
            return "Nothing to clean!"
        self.poop_count = 0
        if self.needs_attention and self.attention_reason == "dirty":
            self._clear_attention()
        return f"Cleaned up! ✨"

    def toggle_lights(self) -> str:
        """Turn lights on/off — pet sleeps with lights off."""
        if not self.is_alive:
            return "..."
        self.lights_on = not self.lights_on
        state = "on" if self.lights_on else "off"
        return f"Lights turned {state}. {'💡' if self.lights_on else '🌙'}"

    # ---------------------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------------------

    def _clear_attention(self) -> None:
        self.needs_attention = False
        self.attention_reason = ""

    def _request_attention(self, reason: str) -> None:
        if not self.needs_attention:
            self.needs_attention = True
            self.attention_reason = reason

    # ---------------------------------------------------------------------------
    # Tick — call this regularly (every game loop iteration)
    # Returns a list of events that happened this tick
    # ---------------------------------------------------------------------------

    def tick(self) -> list[str]:
        """Advance pet state. Returns list of event strings."""
        if not self.is_alive:
            return []

        now = time.time()
        elapsed = now - self.last_tick_at
        self.last_tick_at = now
        events: list[str] = []

        # Age
        self.age_days += elapsed / (60 * 60 * 24)

        # Stage progression
        stage_event = self._check_stage_progression(now)
        if stage_event:
            events.append(stage_event)

        if self.stage == LifeStage.EGG:
            return events  # egg doesn't have stat decay

        if not self.lights_on:
            # Pet is sleeping — no decay, no poop
            return events

        # Hunger decay
        if now - self._last_hunger_decay >= HUNGER_DECAY_INTERVAL:
            self._last_hunger_decay = now
            if self.hunger > 0:
                self.hunger -= 1
            if self.hunger <= 1:
                self._request_attention("hungry")
                events.append("hungry")
            if self.hunger == 0:
                self._check_starvation_death(events)

        # Happy decay
        if now - self._last_happy_decay >= HAPPY_DECAY_INTERVAL:
            self._last_happy_decay = now
            if self.happy > 0:
                self.happy -= 1
            if self.happy <= 1:
                self._request_attention("unhappy")
                events.append("unhappy")

        # Discipline decay
        if now - self._last_discipline_decay >= DISCIPLINE_DECAY_INTERVAL:
            self._last_discipline_decay = now
            self.discipline = max(0, self.discipline - 5)

        # Poop
        if now >= self._next_poop_at:
            self.poop_count = min(4, self.poop_count + 1)
            self._next_poop_at = now + POOP_INTERVAL + random.uniform(-900, 900)
            events.append("poop")
            if self.poop_count >= 3:
                self._request_attention("dirty")
            if self.poop_count >= 4:
                if not self.sick:
                    self.sick = True
                    events.append("sick")

        # Random sickness
        if not self.sick and random.random() < SICK_CHANCE_PER_TICK:
            self.sick = True
            self._request_attention("sick")
            events.append("sick")

        # Sick death check
        if self.sick and self.hunger == 0:
            self._die(events, cause="neglect")

        return events

    def _check_stage_progression(self, now: float) -> Optional[str]:
        """Advance to next life stage if time is up."""
        if self.stage == LifeStage.DEAD:
            return None
        stage_age = now - self.born_at
        # Cumulative thresholds
        thresholds = {
            LifeStage.EGG:   STAGE_DURATIONS[LifeStage.EGG],
            LifeStage.BABY:  STAGE_DURATIONS[LifeStage.EGG] + STAGE_DURATIONS[LifeStage.BABY],
            LifeStage.CHILD: (STAGE_DURATIONS[LifeStage.EGG] + STAGE_DURATIONS[LifeStage.BABY]
                              + STAGE_DURATIONS[LifeStage.CHILD]),
            LifeStage.TEEN:  (STAGE_DURATIONS[LifeStage.EGG] + STAGE_DURATIONS[LifeStage.BABY]
                              + STAGE_DURATIONS[LifeStage.CHILD] + STAGE_DURATIONS[LifeStage.TEEN]),
            LifeStage.ADULT: (STAGE_DURATIONS[LifeStage.EGG] + STAGE_DURATIONS[LifeStage.BABY]
                              + STAGE_DURATIONS[LifeStage.CHILD] + STAGE_DURATIONS[LifeStage.TEEN]
                              + STAGE_DURATIONS[LifeStage.ADULT]),
            LifeStage.ELDER: float("inf"),  # elder → dead via old age timer
        }
        next_stage_map = {
            LifeStage.EGG:   LifeStage.BABY,
            LifeStage.BABY:  LifeStage.CHILD,
            LifeStage.CHILD: LifeStage.TEEN,
            LifeStage.TEEN:  LifeStage.ADULT,
            LifeStage.ADULT: LifeStage.ELDER,
        }
        # Elder death by old age
        if self.stage == LifeStage.ELDER:
            elder_start = (STAGE_DURATIONS[LifeStage.EGG] + STAGE_DURATIONS[LifeStage.BABY]
                           + STAGE_DURATIONS[LifeStage.CHILD] + STAGE_DURATIONS[LifeStage.TEEN]
                           + STAGE_DURATIONS[LifeStage.ADULT])
            if stage_age > elder_start + STAGE_DURATIONS[LifeStage.ELDER]:
                events: list[str] = []
                self._die(events, cause="old age")
                return "died_old_age"
            return None

        threshold = thresholds.get(self.stage)
        if threshold and stage_age >= threshold:
            next_stage = next_stage_map[self.stage]
            self.stage = next_stage
            self.character = self._resolve_character(next_stage)
            return f"evolved:{next_stage.value}"
        return None

    def _resolve_character(self, stage: LifeStage) -> PetCharacter:
        """Determine character based on care mistake count."""
        m = self.care_mistakes
        if stage == LifeStage.BABY:
            return PetCharacter.BABY
        if stage == LifeStage.CHILD:
            return PetCharacter.CHILD_GOOD if m < 2 else (PetCharacter.CHILD_NORMAL if m < 5 else PetCharacter.CHILD_BAD)
        if stage == LifeStage.TEEN:
            return PetCharacter.TEEN_GOOD if m < 3 else (PetCharacter.TEEN_NORMAL if m < 6 else PetCharacter.TEEN_BAD)
        if stage == LifeStage.ADULT:
            return PetCharacter.ADULT_GOOD if m < 2 else (PetCharacter.ADULT_NORMAL if m < 5 else PetCharacter.ADULT_BAD)
        if stage == LifeStage.ELDER:
            return PetCharacter.ELDER_GOOD if m < 3 else (PetCharacter.ELDER_NORMAL if m < 7 else PetCharacter.ELDER_BAD)
        return PetCharacter.EGG

    def _check_starvation_death(self, events: list[str]) -> None:
        # Starving for too long = death (give a grace period handled in calling code)
        # For now, starving + sick = instant death (handled by caller)
        pass

    def _die(self, events: list[str], cause: str = "neglect") -> None:
        self.stage = LifeStage.DEAD
        self.character = PetCharacter.DEAD
        self.needs_attention = False
        events.append(f"died:{cause}")
