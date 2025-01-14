import random
from src.game.enemies.enemy_events import *
from src.UI.scenes.end_screen import *


class RunManager:
    def __init__(self, run):
        self.run = run
        self.enemy_events = []  # list of generated events
        self.current_event_index = 0  # index to track events
        self.current_time = 0  # elapsed time

        self.enemies = {
            "shardsoul": {"id": 1.1, "max_health": 150, "speed": 2},
            "champo": {"id": 2.1, "max_health": 75, "speed": 3},
            "sprout": {"id": 3.1, "max_health": 40, "speed": 6},
            "flying_junk": {"id": 5.1, "max_health": 50, "speed": 4},
            "robot": {"id": 6.1, "max_health": 500, "speed": 1},
        }

    def start_run(self):
        self.run.resources["ammo"] = 500
        self.run.resources["health"] = 100
        self.run.resources["food"] = 100
        # generate enemy events for the game
        generator = EnemyEvent(self.enemies)
        self.enemy_events = generator.generate_enemy_events(self.run.difficulty)
        self.run.run()

    def manage_enemies(self):
        # update current time
        self.current_time += 1  # assume this method is called once a second

        # check if there are any events left to process
        if self.current_event_index < len(self.enemy_events):
            event = self.enemy_events[self.current_event_index]
            enemy_name, number_enemies, spawn_time = event

            # if the event time has arrived, trigger it
            if self.current_time >= spawn_time:
                for _ in range(number_enemies):
                    # add each enemy in play
                    enemy = self.run.random_enemy.random_enemy(
                        self.run.random_enemy.filter_by_exact_id(
                            self.run.data_enemies[enemy_name]["id"]
                        )
                    )
                    self.run.player.add_enemy(self.run.data_enemies, *enemy)
                    self.run.player.number_enemies += 1

                self.current_event_index += 1

    def new_weapon(self, name):
        if not self.run.current_weapon_dict["name"] == name:
            self.run.pause = True
            self.run.power_up_launch = True
            self.run.electrodes_manager.start()
            self.run.active_panel = "weapon"
            self.run.weapons_cards.launch_cards(
                [self.run.current_weapon_dict["name"], name]
            )

    def change_weapon(self, id):
        self.run.current_weapon_dict = self.run.data_weapons[f"{id}"]
        self.run.current_weapon_dict["position"][0] = 500 + (10 * self.run.zoom)
        self.run.current_weapon_dict["position"][1] = 300 + (5 * self.run.zoom)
        self.run.weapon.change_weapon(
            self.run.zoom, self.run.player, self.run.current_weapon_dict
        )

    def launch_power_up(self):
        self.run.pause = True
        self.run.power_up_launch = True
        self.run.electrodes_manager.start()
        self.unlocked_power_ups = [
            name
            for name, data in self.run.data_power_up.items()
            if not data.get("locked", False)
        ]
        self.unlocked_extras = [
            name
            for name, data in self.run.data_extras.items()
            if not data.get("locked", False)
        ]
        # ? Maybe add a other chance to get extras
        if (len(self.unlocked_power_ups) < 3 or random.random() < 0.15) and len(
            self.unlocked_extras
        ) >= 2:
            self.add_extras()
        else:
            self.run.active_panel = "power_up"
            self.run.power_up.launch_cards(random.sample(self.unlocked_power_ups, 3))

    def add_extras(self):
        self.run.active_panel = "extras"
        self.run.extras_cards.launch_cards(random.sample(self.unlocked_extras, 2))

    def new_extra(self, name):
        self.run.data_extras[name]["activate"] = True

    def change_max_xp(self, palier):
        self.run.index_threshold_xp = palier
        self.run.icon.change_threshold(
            "xp", self.run.threshold_xp[self.run.index_threshold_xp]
        )

    def change_zoom(self):
        self.run.map_manager.change_map_size(self.run.zoom)
        for enemy in self.run.player.enemies:
            enemy.change_zoom(self.run.zoom)
        for laser in self.run.player.lasers:
            laser.change_zoom(self.run.zoom)
        for missile in self.run.player.missiles:
            missile.change_zoom(self.run.zoom)
        for grenade in self.run.player.grenades:
            grenade.change_zoom(self.run.zoom)
        self.run.player.change_zoom()
        for objet in self.run.player.objects:
            objet.change_zoom(self.run.zoom)
        self.run.weapon.change_zoom(self.run.zoom)
        self.run.drone.change_zoom(self.run.zoom)
        self.run.rescue_ship.change_zoom()

    def end_game(self):
        win = "victory" if self.run.win else "defeat"
        extras_rewards = 6 if self.run.win else 3
        rewards = {
            "money": extras_rewards
            * (
                self.run.icon.resource["energy"]
                + self.run.icon.resource["metal"]
                + self.run.icon.resource["data"]
            ),
            "resource": {
                "energy": self.run.icon.resource["energy"],
                "metal": self.run.icon.resource["metal"],
                "data": self.run.icon.resource["data"],
            },
        }

        game_over_screen = GameOverScreen(
            self.run.WIDTH_SCREEN, self.run.HEIGHT_SCREEN, rewards, win
        )
        game_over_screen.run()

    def collision_sables(self, bool: bool):
        self.run.speed = self.run.speed_init / 2 if bool else self.run.speed_init

    def rock_collision(self, bool: bool):
        self.run.rock_collision = bool
