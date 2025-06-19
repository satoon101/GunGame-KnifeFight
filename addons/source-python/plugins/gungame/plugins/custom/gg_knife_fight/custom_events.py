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
    "GG_Knife_Fight_End",
    "GG_Knife_Fight_Start",
)


# =============================================================================
# >> CLASSES
# =============================================================================
# ruff: noqa: N801
class GG_Knife_Fight_Start(CustomEvent):
    """Called when a 1v1 knife fight begins."""

    fighter_1 = ShortVariable("Userid of the first fighter.")
    fighter_2 = ShortVariable("Userid of the second fighter.")


class GG_Knife_Fight_End(CustomEvent):
    """Called when a 1v1 knife fight begins."""

    winner = ShortVariable("Userid of the winner.")
    loser = ShortVariable("Userid of the loser.")


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile(info.name, GG_Knife_Fight_Start, GG_Knife_Fight_End)
