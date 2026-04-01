"""
Plugin system for Tamagotchi.

Plugins register via pyproject.toml entry_points:
  [project.entry-points."tamagotchi.plugins"]
  my_plugin = "my_package.plugin:MyPlugin"

Or placed in ~/.tamagotchi/plugins/<name>.py as a standalone module.

Built-in plugins live in tamagotchi/plugins/builtin/.
"""
from __future__ import annotations

import importlib
import importlib.metadata
from pathlib import Path
from typing import TYPE_CHECKING

from tamagotchi.plugins.base import BasePlugin

if TYPE_CHECKING:
    from tamagotchi.core.pet import Pet


class PluginManager:
    """Loads and manages all active plugins."""

    def __init__(self) -> None:
        self._plugins: list[BasePlugin] = []

    def discover(self) -> None:
        """Auto-discover plugins from entry_points and ~/.tamagotchi/plugins/."""
        self._load_entry_point_plugins()
        self._load_local_plugins()

    def _load_entry_point_plugins(self) -> None:
        try:
            eps = importlib.metadata.entry_points(group="tamagotchi.plugins")
            for ep in eps:
                try:
                    cls = ep.load()
                    plugin = cls()
                    self._plugins.append(plugin)
                    plugin.on_load()
                except Exception as e:
                    print(f"[plugin] Failed to load {ep.name}: {e}")
        except Exception:
            pass

    def _load_local_plugins(self) -> None:
        plugin_dir = Path.home() / ".tamagotchi" / "plugins"
        if not plugin_dir.exists():
            return
        for py_file in plugin_dir.glob("*.py"):
            try:
                spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    for attr in dir(mod):
                        obj = getattr(mod, attr)
                        if (isinstance(obj, type)
                                and issubclass(obj, BasePlugin)
                                and obj is not BasePlugin):
                            plugin = obj()
                            self._plugins.append(plugin)
                            plugin.on_load()
            except Exception as e:
                print(f"[plugin] Failed to load {py_file.name}: {e}")

    def register(self, plugin: BasePlugin) -> None:
        """Manually register a plugin instance."""
        self._plugins.append(plugin)
        plugin.on_load()

    def emit(self, event: str, **kwargs) -> None:
        """Fire an event on all registered plugins."""
        for plugin in self._plugins:
            try:
                handler = getattr(plugin, event, None)
                if callable(handler):
                    handler(**kwargs)
            except Exception as e:
                print(f"[plugin:{plugin.name}] Error in {event}: {e}")

    @property
    def plugins(self) -> list[BasePlugin]:
        return list(self._plugins)


# Global singleton
plugin_manager = PluginManager()
