# ../gungame/plugins/custom/gg_knife_fight/configuration.py

"""Creates the gg_knife_fight configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import json
from warnings import warn

# Site-Package
from configobj import ConfigObj
from path import Path

# GunGame
from gungame.core.config.manager import GunGameConfigManager
from gungame.core.paths import GUNGAME_CFG_PATH

# Plugin
from .info import info

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "PLAYER_COUNT",
    "beacon_model",
    "locations",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
PLAYER_COUNT = 2

with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar(
        name="beacon_model",
        default="sprites/laser.vmt",
    ) as beacon_model,
):
    beacon_model.add_text()

_location_file = GUNGAME_CFG_PATH / f"{info.name}_locations.ini"
locations = ConfigObj(_location_file)
if locations:
    for _key, _values in locations.items():
        if len(_values) < PLAYER_COUNT:
            warn(
                message=(
                    f"Not enough locations for map '{_key}' found in "
                    f"{_location_file}, exactly 2 are required."
                ),
                stacklevel=2,
            )
        elif len(_values) > PLAYER_COUNT:
            warn(
                message=(
                    f"Too many locations for map '{_key}' found in "
                    f"{_location_file}, exactly 2 are required."
                ),
                stacklevel=2,
            )
else:
    _default_location_file = Path(__file__).parent / "default_locations.json"
    with _default_location_file.open() as _open_file:
        _data = json.load(_open_file)
    for _num, (_key, _value) in enumerate(_data.items()):
        locations[_key] = _value
        if _num:
            locations.comments[_key] = [""]
    locations.write()
