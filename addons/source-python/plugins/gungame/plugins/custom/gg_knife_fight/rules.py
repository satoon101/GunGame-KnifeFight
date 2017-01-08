# ../gungame/plugins/custom/gg_knife_fight/rules.py

"""Creates the gg_knife_fight rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules
from gungame.core.rules.strings import rules_translations

# Plugin
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
knife_fight_rules = GunGameRules(info.name)
