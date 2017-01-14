# ../gungame/plugins/custom/gg_knife_fight/rules.py

"""Creates the gg_knife_fight rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules

# Plugin
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
knife_fight_rules = GunGameRules(info.name)
knife_fight_rules.register_all_rules()
