# ../gungame/plugins/custom/gg_knife_fight/configuration.py

"""Creates the gg_knife_fight configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-Package
from configobj import ConfigObj

# Source.Python
from core import GAME_NAME

# Site-package
from configobj import ConfigObj

# GunGame
from gungame.core.config.manager import GunGameConfigManager
from gungame.core.paths import GUNGAME_DATA_PATH

# Plugin
from .info import info

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "beacon_model",
    "locations",
    "plugin_data",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
plugin_data = ConfigObj(GUNGAME_DATA_PATH / info.name + '.ini')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar(
        name="beacon_model",
        default="sprites/laser.vmt",
    ) as beacon_model,
):
    beacon_model.add_text()

_location_file = GUNGAME_DATA_PATH / "knife_fight_locations.ini"
locations = ConfigObj(_location_file)
if not _location_file.is_file():
    locations["map"] = [
        ("16.031250 -1507.522217 640.031250", "0.000000 33.458862 0.000000"),
        ("274.396454 -1526.880249 640.031250", "0.000000 7.745361 0.000000"),
    ]
    locations["map2"] = [
        ("16.031250 -1507.522217 640.031250", "0.000000 33.458862 0.000000"),
        ("274.396454 -1526.880249 640.031250", "0.000000 7.745361 0.000000"),
    ]
    locations.write()
