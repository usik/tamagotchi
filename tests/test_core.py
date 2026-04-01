"""Tests for the core pet engine."""
import time
import pytest
from tamagotchi.core.pet import Pet, LifeStage, PetCharacter, Mood
from tamagotchi.core.evolution import EvolutionEngine, CHARACTER_NAMES
from tamagotchi.core.persistence import save_pet, load_pet, delete_pet


# ---------------------------------------------------------------------------
# Pet basics
# ---------------------------------------------------------------------------

def test_pet_defaults():
    pet = Pet(name="TestPet")
    assert pet.name == "TestPet"
    assert pet.stage == LifeStage.EGG
    assert pet.hunger == 4
    assert pet.happy == 4
    assert pet.is_alive

def test_pet_mood_happy():
    pet = Pet()
    pet.stage = LifeStage.BABY
    pet.hunger = 4
    pet.happy = 4
    pet.sick = False
    pet.lights_on = True
    assert pet.mood == Mood.HAPPY

def test_pet_mood_hungry():
    pet = Pet()
    pet.stage = LifeStage.BABY
    pet.hunger = 0
    assert pet.mood == Mood.HUNGRY

def test_pet_mood_sick():
    pet = Pet()
    pet.stage = LifeStage.BABY
    pet.sick = True
    assert pet.mood == Mood.SICK

def test_pet_mood_sleeping():
    pet = Pet()
    pet.stage = LifeStage.BABY
    pet.lights_on = False
    assert pet.mood == Mood.SLEEPING

# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

def test_feed_meal_increases_hunger():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.hunger = 2
    result = pet.feed_meal()
    assert pet.hunger == 4
    assert "meal" in result.lower()

def test_feed_meal_full_is_mistake():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.hunger = 4
    mistakes_before = pet.care_mistakes
    pet.feed_meal()
    assert pet.care_mistakes == mistakes_before + 1

def test_feed_snack_increases_happy():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.happy = 2
    pet.feed_snack()
    assert pet.happy == 3

def test_play_increases_happy():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.happy = 2
    pet.lights_on = True
    pet.play()
    assert pet.happy == 4

def test_play_decreases_weight():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.weight = 15
    pet.play()
    assert pet.weight == 14

def test_medicine_cures_sick():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.sick = True
    result = pet.give_medicine()
    assert not pet.sick
    assert "better" in result.lower()

def test_medicine_when_healthy_is_mistake():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.sick = False
    mistakes = pet.care_mistakes
    pet.give_medicine()
    assert pet.care_mistakes == mistakes + 1

def test_flush_poop():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.poop_count = 3
    pet.flush_poop()
    assert pet.poop_count == 0

def test_toggle_lights():
    pet = Pet(name="T")
    pet.lights_on = True
    pet.toggle_lights()
    assert not pet.lights_on
    pet.toggle_lights()
    assert pet.lights_on

def test_attention_cleared_on_feed():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.hunger = 0
    pet.needs_attention = True
    pet.attention_reason = "hungry"
    pet.feed_meal()
    assert not pet.needs_attention

# ---------------------------------------------------------------------------
# Evolution
# ---------------------------------------------------------------------------

def test_evolution_good_path():
    pet = Pet(name="T")
    pet.care_mistakes = 0
    char = EvolutionEngine.resolve(LifeStage.ADULT, pet.care_mistakes)
    assert char == PetCharacter.ADULT_GOOD

def test_evolution_bad_path():
    pet = Pet(name="T")
    pet.care_mistakes = 10
    char = EvolutionEngine.resolve(LifeStage.ADULT, pet.care_mistakes)
    assert char == PetCharacter.ADULT_BAD

def test_evolution_normal_path():
    pet = Pet(name="T")
    pet.care_mistakes = 3
    char = EvolutionEngine.resolve(LifeStage.ADULT, pet.care_mistakes)
    assert char == PetCharacter.ADULT_NORMAL

def test_character_names_complete():
    for char in PetCharacter:
        assert char in CHARACTER_NAMES, f"Missing name for {char}"

# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def test_save_and_load_pet(tmp_path, monkeypatch):
    import tamagotchi.core.persistence as p
    monkeypatch.setattr(p, "SAVE_DIR", tmp_path)

    pet = Pet(name="SaveTest")
    pet.stage = LifeStage.BABY
    pet.hunger = 3
    pet.happy = 2
    pet.care_mistakes = 1

    save_pet(pet)
    loaded = load_pet("SaveTest")

    assert loaded is not None
    assert loaded.name == "SaveTest"
    assert loaded.stage == LifeStage.BABY
    assert loaded.hunger == 3
    assert loaded.happy == 2
    assert loaded.care_mistakes == 1

def test_load_nonexistent_returns_none(tmp_path, monkeypatch):
    import tamagotchi.core.persistence as p
    monkeypatch.setattr(p, "SAVE_DIR", tmp_path)
    assert load_pet("DoesNotExist") is None

def test_dead_pet_stays_dead():
    pet = Pet(name="T")
    pet.stage = LifeStage.DEAD
    pet.character = PetCharacter.DEAD
    result = pet.feed_meal()
    assert "..." in result
    assert pet.stage == LifeStage.DEAD
