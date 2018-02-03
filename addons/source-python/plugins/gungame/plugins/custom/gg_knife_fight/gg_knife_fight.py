# ../gungame/plugins/custom/gg_knife_fight/gg_knife_fight.py

"""Plugin that allows the last 2 players to 1v1 in a knife fight."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from engines.server import global_vars
from events import Event
from filters.players import PlayerIter
from mathlib import Vector
from players.entity import Player

# GunGame
from gungame.core.plugins.manager import gg_plugin_manager
from gungame.core.status import GunGameMatchStatus, GunGameStatus

# Plugin
from .configuration import beacon_model, plugin_data


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
locations = plugin_data['locations']


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

    if len({player.team_index for player in players}) != 2:
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

'''
from random import randrange

from colors import Color
from effects.base import TempEntity
from engines.precache import Model
from events import Event
from filters.players import PlayerIter
from listeners.tick import Repeat, RepeatStatus


model = Model('sprites/laser.vmt')
# model = Model('sprites/laserbeam.vmt')


@Repeat
def beacon():
    for player in PlayerIter('human'):
        break
    else:
        return
    center = player.origin
    center.z += 10
    entity = TempEntity(
        'BeamRingPoint',
        red=randrange(256),
        green=randrange(256),
        blue=randrange(256),
        alpha=255,
        start_width=5,
        end_width=5,
        amplitude=1.0,
        life_time=1.0,
        flags=0,
        model_index=model.index,
        halo_index=model.index,
        center=center,
        start_radius=10,
        end_radius=150,
    )

    entity.create()


@Event('player_say')
def _stuff(game_event):
    if beacon.status is RepeatStatus.RUNNING:
        beacon.stop()
    else:
        beacon.start(0.5, execute_on_start=True)
'''
