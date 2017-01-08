# ../gungame/plugins/custom/gg_knife_fight/info.py

"""Provides/stores information about the plugin."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from cvars.public import PublicConVar
from plugins.info import PluginInfo


# =============================================================================
# >> PLUGIN INFO
# =============================================================================
info = PluginInfo()
info.title = 'GunGame Knife Fight'
info.author = ''
info.version = '1.0'
info.name = 'gg_knife_fight'
info.variable = info.name + '_version'
info.url = ''
info.convar = PublicConVar(
    info.variable, info.version, info.title + ' Version',
)
