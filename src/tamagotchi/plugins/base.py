"""
BasePlugin — all plugins extend this class.

Plugin lifecycle:
  on_load()         — called when plugin is registered
  on_tick(pet)      — called every game tick
  on_action(action, pet) — called when player takes an action
  on_evolve(pet, old_stage, new_stage) — called on evolution
  on_death(pet, cause) — called when pet dies
  on_agent_event(event_type, data) — called by AI agent plugins

To create a plugin:
  1. Subclass BasePlugin
  2. Override the methods you care about
  3. Register via entry_points or ~/.tamagotchi/plugins/
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from tamagotchi.core.pet import Pet


class BasePlugin:
    """Base class for all Tamagotchi plugins."""

    #: Unique plugin name (override in subclass)
    name: str = "unnamed_plugin"
    #: Human-readable description
    description: str = ""
    #: Version string
    version: str = "0.1.0"

    def on_load(self) -> None:
        """Called when plugin is registered. Do setup here."""

    def on_tick(self, pet: "Pet") -> None:
        """Called every game tick (~1s). Use for passive monitoring."""

    def on_action(self, action: str, pet: "Pet") -> None:
        """Called when player takes an action (feed, play, etc.)."""

    def on_evolve(self, pet: "Pet", old_stage: str, new_stage: str) -> None:
        """Called when pet evolves to a new life stage."""

    def on_death(self, pet: "Pet", cause: str) -> None:
        """Called when pet dies."""

    def on_agent_event(self, event_type: str, data: dict[str, Any]) -> None:
        """
        Called by AI agent integrations (Claude Code, Cursor, etc.)
        event_type examples:
          'tool_call'     — agent called a tool
          'tool_result'   — tool returned a result
          'task_complete' — agent finished a task
          'task_failed'   — agent hit an error
          'loop_detected' — agent seems to be looping
          'test_passed'   — test suite passed
          'test_failed'   — test suite failed
        """

    def on_peer_visit(self, visitor_pet: dict) -> None:
        """
        Called when a peer's pet visits (Phase 2: peer discovery).
        visitor_pet is a dict representation of the visiting pet.
        """
