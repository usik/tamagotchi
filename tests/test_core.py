"""Tests for the core pet engine."""
import time
import pytest
from tamagotchi.core.pet import Pet, LifeStage, PetCharacter, Mood
from tamagotchi.core.evolution import EvolutionEngine, CHARACTER_NAMES
from tamagotchi.core.persistence import save_pet, load_pet, delete_pet, list_saved_pets


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

def test_pet_mood_dead():
    pet = Pet()
    pet.stage = LifeStage.DEAD
    assert pet.mood == Mood.DEAD
    assert not pet.is_alive

def test_age_display_hours():
    pet = Pet()
    pet.age_days = 0.5
    assert "h" in pet.age_display

def test_age_display_days():
    pet = Pet()
    pet.age_days = 3.0
    assert "d" in pet.age_display

# ---------------------------------------------------------------------------
# Actions — happy path
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

def test_feed_meal_clears_attention():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.hunger = 0
    pet.needs_attention = True
    pet.attention_reason = "hungry"
    pet.feed_meal()
    assert not pet.needs_attention

def test_feed_snack_increases_happy():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.happy = 2
    pet.feed_snack()
    assert pet.happy == 3

def test_feed_snack_increases_weight():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    w = pet.weight
    pet.feed_snack()
    assert pet.weight == w + 3

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

def test_play_blocked_when_sleeping():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.lights_on = False
    result = pet.play()
    assert "sleeping" in result.lower()

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

def test_flush_poop_nothing_to_clean():
    pet = Pet(name="T")
    pet.poop_count = 0
    result = pet.flush_poop()
    assert "nothing" in result.lower()

def test_toggle_lights():
    pet = Pet(name="T")
    pet.lights_on = True
    pet.toggle_lights()
    assert not pet.lights_on
    pet.toggle_lights()
    assert pet.lights_on

def test_scold_when_not_needed_is_mistake():
    pet = Pet(name="T")
    pet.stage = LifeStage.CHILD
    pet.needs_attention = False
    mistakes = pet.care_mistakes
    pet.scold()
    assert pet.care_mistakes == mistakes + 1

def test_scold_increases_discipline():
    pet = Pet(name="T")
    pet.stage = LifeStage.CHILD
    pet.needs_attention = True
    d = pet.discipline
    pet.scold()
    assert pet.discipline == min(100, d + 25)
    assert not pet.needs_attention

# ---------------------------------------------------------------------------
# Actions on dead/egg pet
# ---------------------------------------------------------------------------

def test_dead_pet_actions_return_ellipsis():
    pet = Pet(name="T")
    pet.stage = LifeStage.DEAD
    pet.character = PetCharacter.DEAD
    for action in [pet.feed_meal, pet.feed_snack, pet.play,
                   pet.give_medicine, pet.flush_poop, pet.scold]:
        assert action() == "..."

def test_egg_cannot_eat():
    pet = Pet(name="T")
    pet.stage = LifeStage.EGG
    result = pet.feed_meal()
    assert "egg" in result.lower()

# ---------------------------------------------------------------------------
# Decay mechanics
# ---------------------------------------------------------------------------

def test_hunger_decays_over_time():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.lights_on = True
    pet.hunger = 4
    pet._last_hunger_decay -= 1800  # 30 min ago
    pet.tick()
    assert pet.hunger == 3

def test_happy_decays_over_time():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.lights_on = True
    pet.happy = 4
    pet._last_happy_decay -= 1800
    pet.tick()
    assert pet.happy == 3

def test_poop_appears_over_time():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.lights_on = True
    pet._next_poop_at = time.time() - 1
    events = pet.tick()
    assert "poop" in events
    assert pet.poop_count == 1

def test_too_much_poop_causes_sickness():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.lights_on = True
    pet.poop_count = 3
    pet._next_poop_at = time.time() - 1
    events = pet.tick()
    assert "sick" in events
    assert pet.sick

def test_sleeping_blocks_decay():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.lights_on = False
    pet.hunger = 4
    pet._last_hunger_decay -= 1800
    pet.tick()
    assert pet.hunger == 4  # no decay while sleeping

def test_egg_tick_does_not_decay():
    pet = Pet(name="T")
    pet.stage = LifeStage.EGG
    pet.hunger = 4
    pet._last_hunger_decay -= 1800
    pet.tick()
    assert pet.hunger == 4

# ---------------------------------------------------------------------------
# Death
# ---------------------------------------------------------------------------

def test_death_from_neglect():
    pet = Pet(name="T")
    pet.stage = LifeStage.BABY
    pet.lights_on = True
    pet.hunger = 0
    pet.sick = True
    events = pet.tick()
    assert any("died" in e for e in events)
    assert pet.stage == LifeStage.DEAD

def test_dead_pet_tick_returns_empty():
    pet = Pet(name="T")
    pet.stage = LifeStage.DEAD
    assert pet.tick() == []

# ---------------------------------------------------------------------------
# Evolution
# ---------------------------------------------------------------------------

def test_evolution_good_path():
    char = EvolutionEngine.resolve(LifeStage.ADULT, 0)
    assert char == PetCharacter.ADULT_GOOD

def test_evolution_bad_path():
    char = EvolutionEngine.resolve(LifeStage.ADULT, 10)
    assert char == PetCharacter.ADULT_BAD

def test_evolution_normal_path():
    char = EvolutionEngine.resolve(LifeStage.ADULT, 3)
    assert char == PetCharacter.ADULT_NORMAL

def test_evolution_all_stages():
    for stage in [LifeStage.CHILD, LifeStage.TEEN, LifeStage.ADULT, LifeStage.ELDER]:
        for mistakes in [0, 3, 10]:
            char = EvolutionEngine.resolve(stage, mistakes)
            assert char is not None

def test_character_names_complete():
    for char in PetCharacter:
        assert char in CHARACTER_NAMES, f"Missing name for {char}"

def test_evolution_name_not_empty():
    for char in PetCharacter:
        assert EvolutionEngine.name(char) != ""

def test_evolution_description_not_empty():
    for char in PetCharacter:
        assert EvolutionEngine.description(char) != ""

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
    pet.discipline = 60

    save_pet(pet)
    loaded = load_pet("SaveTest")

    assert loaded is not None
    assert loaded.name == "SaveTest"
    assert loaded.stage == LifeStage.BABY
    assert loaded.hunger == 3
    assert loaded.happy == 2
    assert loaded.care_mistakes == 1
    assert loaded.discipline == 60

def test_load_nonexistent_returns_none(tmp_path, monkeypatch):
    import tamagotchi.core.persistence as p
    monkeypatch.setattr(p, "SAVE_DIR", tmp_path)
    assert load_pet("DoesNotExist") is None

def test_list_saved_pets(tmp_path, monkeypatch):
    import tamagotchi.core.persistence as p
    monkeypatch.setattr(p, "SAVE_DIR", tmp_path)

    save_pet(Pet(name="Alpha"))
    save_pet(Pet(name="Beta"))
    names = list_saved_pets()
    assert len(names) == 2

def test_delete_pet(tmp_path, monkeypatch):
    import tamagotchi.core.persistence as p
    monkeypatch.setattr(p, "SAVE_DIR", tmp_path)

    save_pet(Pet(name="Temp"))
    assert load_pet("Temp") is not None
    delete_pet("Temp")
    assert load_pet("Temp") is None

def test_save_all_stages(tmp_path, monkeypatch):
    """Ensure every life stage round-trips through JSON without error."""
    import tamagotchi.core.persistence as p
    monkeypatch.setattr(p, "SAVE_DIR", tmp_path)

    for stage in LifeStage:
        pet = Pet(name=f"Stage_{stage.value}")
        pet.stage = stage
        save_pet(pet)
        loaded = load_pet(f"Stage_{stage.value}")
        assert loaded.stage == stage

# ---------------------------------------------------------------------------
# Plugin system
# ---------------------------------------------------------------------------

def test_plugin_receives_events():
    from tamagotchi.plugins import PluginManager, BasePlugin

    class TrackPlugin(BasePlugin):
        name = "track"
        log: list = []
        def on_tick(self, pet): self.log.append("tick")
        def on_action(self, action, pet): self.log.append(f"action:{action}")
        def on_evolve(self, pet, old_stage, new_stage): self.log.append(f"evolve:{new_stage}")
        def on_death(self, pet, cause): self.log.append(f"death:{cause}")

    mgr = PluginManager()
    plugin = TrackPlugin()
    mgr.register(plugin)

    pet = Pet(name="T")
    mgr.emit("on_tick", pet=pet)
    mgr.emit("on_action", action="feed_meal", pet=pet)
    mgr.emit("on_evolve", pet=pet, old_stage="baby", new_stage="child")
    mgr.emit("on_death", pet=pet, cause="neglect")

    assert plugin.log == ["tick", "action:feed_meal", "evolve:child", "death:neglect"]

def test_plugin_error_does_not_crash_game():
    from tamagotchi.plugins import PluginManager, BasePlugin

    class BrokenPlugin(BasePlugin):
        name = "broken"
        def on_tick(self, pet): raise RuntimeError("I am broken")

    mgr = PluginManager()
    mgr.register(BrokenPlugin())
    pet = Pet(name="T")
    # Should not raise
    mgr.emit("on_tick", pet=pet)

# ---------------------------------------------------------------------------
# Sprites
# ---------------------------------------------------------------------------

def test_all_sprites_load():
    from tamagotchi.sprites.ascii import get_sprite, get_animation_frames, SPRITE_WIDTH, SPRITE_HEIGHT
    for char in PetCharacter:
        for mood in Mood:
            sprite = get_sprite(char, mood)
            assert len(sprite) == SPRITE_HEIGHT
            for line in sprite:
                assert len(line) == SPRITE_WIDTH

def test_animation_frames_have_two_frames():
    from tamagotchi.sprites.ascii import get_animation_frames
    frames = get_animation_frames(PetCharacter.EGG, Mood.HAPPY)
    assert len(frames) >= 2
