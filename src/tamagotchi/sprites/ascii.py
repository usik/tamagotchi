"""
ASCII/Unicode sprites for all life stages and moods.
Each sprite is a list of strings (lines). All sprites are padded to SPRITE_WIDTH.

Animations are lists of frames (list[list[str]]).
"""
from __future__ import annotations
from tamagotchi.core.pet import PetCharacter, Mood

SPRITE_WIDTH  = 13
SPRITE_HEIGHT = 7


def _pad(lines: list[str], width: int = SPRITE_WIDTH, height: int = SPRITE_HEIGHT) -> list[str]:
    """Pad/trim sprite to fixed dimensions."""
    padded = [line.ljust(width)[:width] for line in lines]
    while len(padded) < height:
        padded.append(" " * width)
    return padded[:height]


# ---------------------------------------------------------------------------
# EGG
# ---------------------------------------------------------------------------
EGG_IDLE = _pad([
    "             ",
    "   .'''''.   ",
    "  / ~   ~ \\  ",
    " |  *   *  | ",
    "  \\  ~~~  /  ",
    "   '-----'   ",
    "             ",
])

EGG_WIGGLE = _pad([
    "             ",
    "  .'''''.    ",
    " / ~   ~ \\   ",
    "|  *   *  |  ",
    " \\  ~~~  /   ",
    "  '-----'    ",
    "             ",
])

EGG_HATCH = _pad([
    "    *   *    ",
    "  .'''''.    ",
    " /*~   ~*\\   ",
    "|  *   *  |  ",
    " \\* ~~~ */   ",
    "  '-----'    ",
    "    *   *    ",
])

# ---------------------------------------------------------------------------
# BABY  (marutchi-style round blob)
# ---------------------------------------------------------------------------
BABY_HAPPY = _pad([
    "             ",
    "   .-----.   ",
    "  ( ^   ^ )  ",
    "  (  ___  )  ",
    "   '-----'   ",
    "   _| | |_   ",
    "             ",
])

BABY_NEUTRAL = _pad([
    "             ",
    "   .-----.   ",
    "  ( -   - )  ",
    "  (  ---  )  ",
    "   '-----'   ",
    "   _| | |_   ",
    "             ",
])

BABY_SAD = _pad([
    "             ",
    "   .-----.   ",
    "  ( ;   ; )  ",
    "  (  ~~~  )  ",
    "   '-----'   ",
    "   _| | |_   ",
    "  .'     '.  ",
])

BABY_SICK = _pad([
    "   + + + +   ",
    "   .-----.   ",
    "  ( x   x )  ",
    "  (  ---  )  ",
    "   '-----'   ",
    "   _| | |_   ",
    "             ",
])

BABY_SLEEP = _pad([
    "             ",
    "   .-----.   ",
    "  ( -   - )  ",
    "  ( z z z )  ",
    "   '-----'   ",
    "   _| | |_   ",
    " Z z z       ",
])

BABY_EAT_1 = _pad([
    "             ",
    "   .-----.   ",
    "  ( ^   ^ )  ",
    "  ( o---o )  ",
    "   '-----'   ",
    "   _| | |_   ",
    "             ",
])

BABY_EAT_2 = _pad([
    "             ",
    "   .-----.   ",
    "  ( ^   ^ )  ",
    "  (  mmm  )  ",
    "   '-----'   ",
    "   _| | |_   ",
    "             ",
])

# ---------------------------------------------------------------------------
# CHILD  (rounder, bigger)
# ---------------------------------------------------------------------------
CHILD_GOOD_HAPPY = _pad([
    "             ",
    "  .-------.  ",
    " ( ^     ^ ) ",
    " (   ___   ) ",
    "  '-------'  ",
    "  /|     |\\ ",
    " / |     | \\ ",
])

CHILD_GOOD_SAD = _pad([
    "             ",
    "  .-------.  ",
    " ( ;     ; ) ",
    " (   ~~~   ) ",
    "  '-------'  ",
    "  /|     |\\ ",
    " .'         '.",
])

CHILD_NORMAL_HAPPY = _pad([
    "             ",
    "  .-------.  ",
    " ( o     o ) ",
    " (   ___   ) ",
    "  '-------'  ",
    "  /|     |\\ ",
    "             ",
])

CHILD_BAD_HAPPY = _pad([
    "             ",
    "  .-------.  ",
    " ( >     < ) ",
    " (  _____  ) ",
    "  '-------'  ",
    "  /|     |\\ ",
    "             ",
])

# ---------------------------------------------------------------------------
# TEEN
# ---------------------------------------------------------------------------
TEEN_GOOD_HAPPY = _pad([
    "    (^ ^)    ",
    "   /|   |\\   ",
    "   | o o |   ",
    "   |  w  |   ",
    "   \\ ___ /   ",
    "    |   |    ",
    "   /|   |\\   ",
])

TEEN_NORMAL_HAPPY = _pad([
    "    (- -)    ",
    "   /|   |\\   ",
    "   | - - |   ",
    "   |  -  |   ",
    "   \\ ___ /   ",
    "    |   |    ",
    "   /|   |\\   ",
])

TEEN_BAD_HAPPY = _pad([
    "    (> <)    ",
    "   /|   |\\   ",
    "   | > < |   ",
    "   | ___ |   ",
    "   \\_____/   ",
    "    |   |    ",
    "   /|   |\\   ",
])

# ---------------------------------------------------------------------------
# ADULT
# ---------------------------------------------------------------------------
ADULT_GOOD_HAPPY = _pad([
    "   /\\ /\\     ",
    "  ( ^ . ^ )  ",
    "  (  ___  )  ",
    "   \\_____/   ",
    "    |   |    ",
    "   /     \\   ",
    "  /       \\  ",
])

ADULT_GOOD_SAD = _pad([
    "   /\\ /\\     ",
    "  ( ; . ; )  ",
    "  (  ~~~  )  ",
    "   \\_____/   ",
    "    |   |    ",
    "   /     \\   ",
    "  .'     '.  ",
])

ADULT_NORMAL_HAPPY = _pad([
    "   .------.  ",
    "  ( o   o )  ",
    "  ( / _ \\ )  ",
    "  (  ---  )  ",
    "   '------'  ",
    "    |   |    ",
    "   /     \\   ",
])

ADULT_BAD_HAPPY = _pad([
    "  .-  -  -.  ",
    " ( >     < ) ",
    " ( |     | ) ",
    " (  -----  ) ",
    "  '---------'",
    "    |   |    ",
    "   /     \\   ",
])

# ---------------------------------------------------------------------------
# ELDER
# ---------------------------------------------------------------------------
ELDER_GOOD_HAPPY = _pad([
    "    ~~~~~    ",
    "  ( ^   ^ )  ",
    "  ( \\___/ )  ",
    "   '-----'   ",
    "     | |     ",
    "    /   \\    ",
    "   (     )   ",
])

ELDER_NORMAL_HAPPY = _pad([
    "             ",
    "  ( -   - )  ",
    "  ( \\___/ )  ",
    "   '-----'   ",
    "     | |     ",
    "    /   \\    ",
    "   (     )   ",
])

ELDER_BAD_HAPPY = _pad([
    "             ",
    "  ( x   x )  ",
    "  ( -___- )  ",
    "   '-----'   ",
    "     | |     ",
    "    /   \\    ",
    "   (     )   ",
])

# ---------------------------------------------------------------------------
# DEAD
# ---------------------------------------------------------------------------
DEAD_SPRITE = _pad([
    "             ",
    "   .-----.   ",
    "   | R I P|  ",
    "   |      |  ",
    "   |      |  ",
    "   '------'  ",
    "  /////////  ",
])

# ---------------------------------------------------------------------------
# POOP  (shown alongside pet)
# ---------------------------------------------------------------------------
POOP = [" 💩 ", "    "]

# ---------------------------------------------------------------------------
# Attention indicator
# ---------------------------------------------------------------------------
ATTENTION_ICON = "❗"
SLEEP_ICON     = "💤"

# ---------------------------------------------------------------------------
# Sprite registry
# ---------------------------------------------------------------------------

# Map (character, mood) → sprite lines
_SPRITES: dict[tuple[PetCharacter, Mood], list[str]] = {
    # Egg
    (PetCharacter.EGG, Mood.HAPPY):    EGG_IDLE,
    (PetCharacter.EGG, Mood.NEUTRAL):  EGG_IDLE,
    (PetCharacter.EGG, Mood.HUNGRY):   EGG_WIGGLE,
    (PetCharacter.EGG, Mood.UNHAPPY):  EGG_WIGGLE,
    (PetCharacter.EGG, Mood.SICK):     EGG_WIGGLE,
    (PetCharacter.EGG, Mood.SLEEPING): EGG_IDLE,
    (PetCharacter.EGG, Mood.DEAD):     DEAD_SPRITE,

    # Baby
    (PetCharacter.BABY, Mood.HAPPY):    BABY_HAPPY,
    (PetCharacter.BABY, Mood.NEUTRAL):  BABY_NEUTRAL,
    (PetCharacter.BABY, Mood.HUNGRY):   BABY_SAD,
    (PetCharacter.BABY, Mood.UNHAPPY):  BABY_SAD,
    (PetCharacter.BABY, Mood.SICK):     BABY_SICK,
    (PetCharacter.BABY, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.BABY, Mood.DEAD):     DEAD_SPRITE,

    # Child good
    (PetCharacter.CHILD_GOOD, Mood.HAPPY):    CHILD_GOOD_HAPPY,
    (PetCharacter.CHILD_GOOD, Mood.NEUTRAL):  CHILD_NORMAL_HAPPY,
    (PetCharacter.CHILD_GOOD, Mood.HUNGRY):   CHILD_GOOD_SAD,
    (PetCharacter.CHILD_GOOD, Mood.UNHAPPY):  CHILD_GOOD_SAD,
    (PetCharacter.CHILD_GOOD, Mood.SICK):     BABY_SICK,
    (PetCharacter.CHILD_GOOD, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.CHILD_GOOD, Mood.DEAD):     DEAD_SPRITE,

    # Child normal
    (PetCharacter.CHILD_NORMAL, Mood.HAPPY):    CHILD_NORMAL_HAPPY,
    (PetCharacter.CHILD_NORMAL, Mood.NEUTRAL):  CHILD_NORMAL_HAPPY,
    (PetCharacter.CHILD_NORMAL, Mood.HUNGRY):   CHILD_GOOD_SAD,
    (PetCharacter.CHILD_NORMAL, Mood.UNHAPPY):  CHILD_GOOD_SAD,
    (PetCharacter.CHILD_NORMAL, Mood.SICK):     BABY_SICK,
    (PetCharacter.CHILD_NORMAL, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.CHILD_NORMAL, Mood.DEAD):     DEAD_SPRITE,

    # Child bad
    (PetCharacter.CHILD_BAD, Mood.HAPPY):    CHILD_BAD_HAPPY,
    (PetCharacter.CHILD_BAD, Mood.NEUTRAL):  CHILD_BAD_HAPPY,
    (PetCharacter.CHILD_BAD, Mood.HUNGRY):   CHILD_GOOD_SAD,
    (PetCharacter.CHILD_BAD, Mood.UNHAPPY):  CHILD_GOOD_SAD,
    (PetCharacter.CHILD_BAD, Mood.SICK):     BABY_SICK,
    (PetCharacter.CHILD_BAD, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.CHILD_BAD, Mood.DEAD):     DEAD_SPRITE,

    # Teen
    (PetCharacter.TEEN_GOOD, Mood.HAPPY):    TEEN_GOOD_HAPPY,
    (PetCharacter.TEEN_GOOD, Mood.NEUTRAL):  TEEN_NORMAL_HAPPY,
    (PetCharacter.TEEN_GOOD, Mood.HUNGRY):   TEEN_NORMAL_HAPPY,
    (PetCharacter.TEEN_GOOD, Mood.UNHAPPY):  TEEN_NORMAL_HAPPY,
    (PetCharacter.TEEN_GOOD, Mood.SICK):     BABY_SICK,
    (PetCharacter.TEEN_GOOD, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.TEEN_GOOD, Mood.DEAD):     DEAD_SPRITE,

    (PetCharacter.TEEN_NORMAL, Mood.HAPPY):    TEEN_NORMAL_HAPPY,
    (PetCharacter.TEEN_NORMAL, Mood.NEUTRAL):  TEEN_NORMAL_HAPPY,
    (PetCharacter.TEEN_NORMAL, Mood.HUNGRY):   TEEN_NORMAL_HAPPY,
    (PetCharacter.TEEN_NORMAL, Mood.UNHAPPY):  TEEN_NORMAL_HAPPY,
    (PetCharacter.TEEN_NORMAL, Mood.SICK):     BABY_SICK,
    (PetCharacter.TEEN_NORMAL, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.TEEN_NORMAL, Mood.DEAD):     DEAD_SPRITE,

    (PetCharacter.TEEN_BAD, Mood.HAPPY):    TEEN_BAD_HAPPY,
    (PetCharacter.TEEN_BAD, Mood.NEUTRAL):  TEEN_BAD_HAPPY,
    (PetCharacter.TEEN_BAD, Mood.HUNGRY):   TEEN_BAD_HAPPY,
    (PetCharacter.TEEN_BAD, Mood.UNHAPPY):  TEEN_BAD_HAPPY,
    (PetCharacter.TEEN_BAD, Mood.SICK):     BABY_SICK,
    (PetCharacter.TEEN_BAD, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.TEEN_BAD, Mood.DEAD):     DEAD_SPRITE,

    # Adult
    (PetCharacter.ADULT_GOOD, Mood.HAPPY):    ADULT_GOOD_HAPPY,
    (PetCharacter.ADULT_GOOD, Mood.NEUTRAL):  ADULT_NORMAL_HAPPY,
    (PetCharacter.ADULT_GOOD, Mood.HUNGRY):   ADULT_GOOD_SAD,
    (PetCharacter.ADULT_GOOD, Mood.UNHAPPY):  ADULT_GOOD_SAD,
    (PetCharacter.ADULT_GOOD, Mood.SICK):     BABY_SICK,
    (PetCharacter.ADULT_GOOD, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.ADULT_GOOD, Mood.DEAD):     DEAD_SPRITE,

    (PetCharacter.ADULT_NORMAL, Mood.HAPPY):    ADULT_NORMAL_HAPPY,
    (PetCharacter.ADULT_NORMAL, Mood.NEUTRAL):  ADULT_NORMAL_HAPPY,
    (PetCharacter.ADULT_NORMAL, Mood.HUNGRY):   ADULT_GOOD_SAD,
    (PetCharacter.ADULT_NORMAL, Mood.UNHAPPY):  ADULT_GOOD_SAD,
    (PetCharacter.ADULT_NORMAL, Mood.SICK):     BABY_SICK,
    (PetCharacter.ADULT_NORMAL, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.ADULT_NORMAL, Mood.DEAD):     DEAD_SPRITE,

    (PetCharacter.ADULT_BAD, Mood.HAPPY):    ADULT_BAD_HAPPY,
    (PetCharacter.ADULT_BAD, Mood.NEUTRAL):  ADULT_BAD_HAPPY,
    (PetCharacter.ADULT_BAD, Mood.HUNGRY):   ADULT_GOOD_SAD,
    (PetCharacter.ADULT_BAD, Mood.UNHAPPY):  ADULT_GOOD_SAD,
    (PetCharacter.ADULT_BAD, Mood.SICK):     BABY_SICK,
    (PetCharacter.ADULT_BAD, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.ADULT_BAD, Mood.DEAD):     DEAD_SPRITE,

    # Elder
    (PetCharacter.ELDER_GOOD, Mood.HAPPY):    ELDER_GOOD_HAPPY,
    (PetCharacter.ELDER_GOOD, Mood.NEUTRAL):  ELDER_NORMAL_HAPPY,
    (PetCharacter.ELDER_GOOD, Mood.HUNGRY):   ELDER_NORMAL_HAPPY,
    (PetCharacter.ELDER_GOOD, Mood.UNHAPPY):  ELDER_NORMAL_HAPPY,
    (PetCharacter.ELDER_GOOD, Mood.SICK):     BABY_SICK,
    (PetCharacter.ELDER_GOOD, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.ELDER_GOOD, Mood.DEAD):     DEAD_SPRITE,

    (PetCharacter.ELDER_NORMAL, Mood.HAPPY):    ELDER_NORMAL_HAPPY,
    (PetCharacter.ELDER_NORMAL, Mood.NEUTRAL):  ELDER_NORMAL_HAPPY,
    (PetCharacter.ELDER_NORMAL, Mood.HUNGRY):   ELDER_NORMAL_HAPPY,
    (PetCharacter.ELDER_NORMAL, Mood.UNHAPPY):  ELDER_NORMAL_HAPPY,
    (PetCharacter.ELDER_NORMAL, Mood.SICK):     BABY_SICK,
    (PetCharacter.ELDER_NORMAL, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.ELDER_NORMAL, Mood.DEAD):     DEAD_SPRITE,

    (PetCharacter.ELDER_BAD, Mood.HAPPY):    ELDER_BAD_HAPPY,
    (PetCharacter.ELDER_BAD, Mood.NEUTRAL):  ELDER_NORMAL_HAPPY,
    (PetCharacter.ELDER_BAD, Mood.HUNGRY):   ELDER_NORMAL_HAPPY,
    (PetCharacter.ELDER_BAD, Mood.UNHAPPY):  ELDER_NORMAL_HAPPY,
    (PetCharacter.ELDER_BAD, Mood.SICK):     BABY_SICK,
    (PetCharacter.ELDER_BAD, Mood.SLEEPING): BABY_SLEEP,
    (PetCharacter.ELDER_BAD, Mood.DEAD):     DEAD_SPRITE,

    # Dead
    (PetCharacter.DEAD, Mood.DEAD): DEAD_SPRITE,
}

# ---------------------------------------------------------------------------
# Animation frames (list of sprite frames for each mood/character)
# ---------------------------------------------------------------------------
_ANIMATIONS: dict[tuple[PetCharacter, Mood], list[list[str]]] = {
    (PetCharacter.EGG, Mood.HAPPY):    [EGG_IDLE, EGG_WIGGLE],
    (PetCharacter.EGG, Mood.NEUTRAL):  [EGG_IDLE, EGG_WIGGLE],
    (PetCharacter.EGG, Mood.HUNGRY):   [EGG_WIGGLE, EGG_HATCH],
    (PetCharacter.BABY, Mood.HAPPY):   [BABY_HAPPY, BABY_NEUTRAL],
    (PetCharacter.BABY, Mood.HUNGRY):  [BABY_SAD, BABY_NEUTRAL],
    (PetCharacter.BABY, Mood.SLEEPING):[BABY_SLEEP, BABY_SLEEP],
}


def get_sprite(character: PetCharacter, mood: Mood) -> list[str]:
    """Return the sprite lines for a given character and mood."""
    key = (character, mood)
    sprite = _SPRITES.get(key)
    if sprite:
        return sprite
    # Fallback: try happy mood, then first available
    fallback = _SPRITES.get((character, Mood.HAPPY))
    if fallback:
        return fallback
    return DEAD_SPRITE


def get_animation_frames(character: PetCharacter, mood: Mood) -> list[list[str]]:
    """Return animation frames. Falls back to single static sprite."""
    key = (character, mood)
    frames = _ANIMATIONS.get(key)
    if frames:
        return frames
    return [get_sprite(character, mood), get_sprite(character, mood)]
