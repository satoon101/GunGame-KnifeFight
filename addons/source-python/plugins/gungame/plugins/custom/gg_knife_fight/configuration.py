# ../gungame/plugins/included/gg_knife_fight/configuration.py

"""Creates the gg_knife_fight configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-Package
from configobj import ConfigObj

# Source.Python
from core import GAME_NAME

# GunGame
from gungame.core.config.manager import GunGameConfigManager
from gungame.core.paths import GUNGAME_DATA_PATH

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'beacon_model',
    'plugin_data',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
plugin_data = ConfigObj(GUNGAME_DATA_PATH / info.name + '.ini')
_default = plugin_data['default_model'].get(GAME_NAME, 'sprites/laser.vmt')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar(
        name='beacon_model',
        default=_default,
    ) as beacon_model:
        beacon_model.add_text()
