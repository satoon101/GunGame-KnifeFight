# ../gungame/plugins/custom/gg_knife_fight/gg_knife_fight.py

"""Plugin that allows the last 2 players to 1v1 in a knife fight."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from engines.precache import Model
from engines.server import global_vars
from effects.base import TempEntity
from events import Event
from filters.players import PlayerIter
from listeners.tick import Repeat
from mathlib import QAngle, Vector
from menus import SimpleMenu, SimpleOption, Text
from players.entity import Player
from players.helpers import userid_from_index
from players.teams import teams_by_name

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.plugins.manager import gg_plugin_manager
from gungame.core.status import GunGameMatchStatus, GunGameStatus

# Plugin
from .configuration import PLAYER_COUNT, beacon_model, locations
from .custom_events import GG_Knife_Fight_End, GG_Knife_Fight_Start

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
model = Model(str(beacon_model))

knife_fight_menu = SimpleMenu()
title = "1v1 Knife Fight?"
knife_fight_menu.append(Text(title))
knife_fight_menu.append("=" * len(title))
for num, (text, value) in enumerate((("Yes", True), ("No", False)), start=1):
    knife_fight_menu.append(
        SimpleOption(
            choice_index=num,
            text=text,
            value=value,
        ),
    )


# =============================================================================
# >> CLASSES
# =============================================================================
class _KnifeFightManager:

    accepted = {}
    in_knife_fight = False

    def reset(self):
        beacon.stop()
        self.accepted.clear()
        self.in_knife_fight = False

    @staticmethod
    def should_send_menu(userid, alive_players):
        if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
            return False

        if len(alive_players) != PLAYER_COUNT:
            return False

        if (
                len(
                    {
                        player.team_index for player in alive_players
                    },
                ) != PLAYER_COUNT and
                "gg_ffa" not in gg_plugin_manager
        ):
            return False

        if "gg_elimination" in gg_plugin_manager:
            from gungame.plugins.included.gg_elimination.gg_elimination import (
                eliminated_players,
            )
            if eliminated_players.get(userid):
                return False

        return True

    def send_menu(self, userid):
        alive_players = list(PlayerIter("alive"))
        if not self.should_send_menu(userid, alive_players):
            return

        knife_fight_menu.send([
            player for player in alive_players
            if not player.is_bot()
        ])
        for player in alive_players:
            if player.is_bot():
                self.menu_choice(
                    menu=knife_fight_menu,
                    index=player.index,
                    choice=SimpleOption(
                        choice_index=1,
                        text="",
                        value=True,
                    ),
                )
            else:
                knife_fight_menu.send([player.index])

    def menu_choice(self, menu, index, choice):
        if not choice.value:
            return

        self.accepted[index] = Player(index).team_index
        if len(self.accepted) == PLAYER_COUNT:
            self.start_knife_fight()

    def start_knife_fight(self):
        if global_vars.map_name not in locations:
            return

        map_locations = locations[global_vars.map_name].items()
        if set(self.accepted.values()) == set(teams_by_name.values()):
            team_users = {v: k for k, v in self.accepted.items()}
            index_1 = team_users[teams_by_name["ct"]]
            index_2 = team_users[teams_by_name["t"]]
        else:
            index_1, index_2 = self.accepted.keys()

        for n, index in enumerate((index_1, index_2)):
            player = player_dictionary.from_index(index)
            player.strip_weapons(remove_level_weapon=True)
            player.teleport(
                origin=Vector(*map(float, map_locations[n][0].split())),
                angle=QAngle(*map(float, map_locations[n][1].split())),
            )

        beacon.start(interval=1)
        self.in_knife_fight = True
        with GG_Knife_Fight_Start() as event:
            event.fighter_1 = userid_from_index(index_1)
            event.fighter_2 = userid_from_index(index_2)

    def end_knife_fight(self, attacker, userid):
        with GG_Knife_Fight_End() as event:
            event.winner = attacker
            event.loser = userid

        self.in_knife_fight = False


knife_fight_manager = _KnifeFightManager()
knife_fight_menu.select_callback = knife_fight_manager.menu_choice


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("player_death")
def _ask_knife_fight(game_event):
    userid = game_event["userid"]
    if knife_fight_manager.in_knife_fight:
        knife_fight_manager.end_knife_fight(game_event["attacker"], userid)
    else:
        knife_fight_manager.send_menu(userid)


@Event("round_end")
def _reset_knife_fight(game_event):
    knife_fight_manager.reset()


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
@Repeat
def beacon():
    """Create a beacon for both players in the knife fight."""
    for player in PlayerIter("alive"):
        gg_player = player_dictionary[player.userid]
        gg_player.emit_gg_sound(
            "knife_fight_beacon",
            *[
                other for other in PlayerIter() if other.index != player.index
            ],
        )
        center = Vector(*player.origin)
        center.z += 10
        entity = TempEntity(
            "BeamRingPoint",
            red=255 if player.team == teams_by_name["t"] else 0,
            green=0,
            blue=255 if player.team == teams_by_name["ct"] else 0,
            alpha=255,
            start_width=30,
            end_width=30,
            amplitude=0.0,
            life_time=1.0,
            flags=0,
            model_index=model.index,
            halo_index=model.index,
            center=center,
            start_radius=1,
            end_radius=200,
        )

        entity.create()
