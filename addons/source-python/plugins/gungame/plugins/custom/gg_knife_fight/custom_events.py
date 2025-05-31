# ../gungame/plugins/custom/gg_knife_fight/custom_events.py

"""Events used by gg_knife_fight."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events.custom import CustomEvent
from events.variable import ShortVariable

# GunGame
from gungame.core.events.resource import GGResourceFile

# Plugin
from .info import info

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "GG_Knife_Fight",
)


# =============================================================================
# >> CLASSES
# =============================================================================
# ruff: noqa: N801
class GG_Knife_Fight(CustomEvent):
    """Called when a 1v1 knife fight begins."""

    variable = ShortVariable("Description of the variable")


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile(info.name, GG_Knife_Fight)
