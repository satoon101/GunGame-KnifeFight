# ../gungame/plugins/custom/gg_knife_fight/gg_knife_fight.py

"""Plugin that allows the last 2 players to 1v1 in a knife fight."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-package
from configobj import ConfigObj

# Source.Python
from engines.server import global_vars
from events import Event
from filters.players import PlayerIter
from mathlib import Vector
from players.entity import Player

# GunGame
from gungame.core.paths import GUNGAME_DATA_PATH
from gungame.core.plugins.manager import gg_plugin_manager
from gungame.core.status import GunGameMatchStatus, GunGameStatus


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
locations = ConfigObj(GUNGAME_DATA_PATH / 'knife_fight_locations.ini')


# =============================================================================
# >> CLASSES
# =============================================================================
class _KnifeFightManager(object):
    userid_1 = None
    userid_2 = None
    accepted_1 = False
    accepted_2 = False
    has_chicken = False

    def reset(self):
        self.userid_1 = None
        self.userid_2 = None
        self.accepted_1 = False
        self.accepted_2 = False
        self.has_chicken = False

    def _menu_choice(self, menu, index, choice):
        if self.has_chicken:
            return

        player = Player(index)
        if not choice.value:
            self.chicken_player(player)
            self.has_chicken = True
            return

        if player.userid == self.userid_1:
            self.accepted_1 = True

        elif player.userid == self.userid_2:
            self.accepted_2 = True

        if self.accepted_1 and self.accepted_2:
            self.start_knife_fight()

    def start_knife_fight(self):
        # TODO: ping / beacon players prior to moving
        if global_vars.map_name not in locations:
            return

        map_locations = locations[global_vars.map_name].items()
        count = len(map_locations)
        if count < 2:
            # TODO: print a warning
            return

        if count > 2:
            # TODO: print a warning
            return

        player_1 = Player.from_userid(self.userid_1)
        player_1.origin = Vector(map_locations[0][0])
        # TODO: test for type
        player_1.angle = Vector(map_locations[0][1])

        player_2 = Player.from_userid(self.userid_2)
        player_2.origin = Vector(map_locations[1][0])
        # TODO: test for type
        player_2.angle = Vector(map_locations[1][1])

    @staticmethod
    def chicken_player(player):
        pass

knife_fight_manager = _KnifeFightManager()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _ask_knife_fight(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    players = list(PlayerIter('alive'))
    if len(players) != 2:
        return

    if len({player.team for player in players}) != 2:
        if 'gg_ffa' not in gg_plugin_manager:
            return

    if 'gg_elimination' in gg_plugin_manager:
        from gungame.plugins.included.gg_elimination.gg_elimination import (
            eliminated_players
        )
        userid = game_event['userid']
        if userid in eliminated_players and eliminated_players[userid]:
            return

    # TODO: send menu


@Event('round_end')
def _reset_knife_fight(game_event):
    knife_fight_manager.reset()
