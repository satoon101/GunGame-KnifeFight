# ../gungame/plugins/included/gg_knife_fight/configuration.py

"""Creates the gg_knife_fight configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from core import GAME_NAME

# GunGame
from gungame.core.config.manager import GunGameConfigManager

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'beacon_model',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar(
        name='beacon_model',
        default=(
            'sprites/laserbeam.vmt' if GAME_NAME == 'csgo'
            else 'sprites/laser.vmt'
        ),
    ) as beacon_model:
        beacon_model.add_text()
