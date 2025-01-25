import pygame
from src.data_handling.load import *
from src.data_handling.read_data import *
from src.game.animations.electrodes import *
from src.game.controllers.draw import *
from src.game.controllers.keyboard_input import *
from src.game.controllers.manager import *
from src.game.controllers.shooter import *
from src.game.controllers.update import *
from src.game.mechanics.items import *
from src.game.mechanics.countdown import *
from src.game.mechanics.pause_panel import *
from src.game.players.player import *
from src.game.maps.map import *
from src.game.weapons.weapon import *
from src.game.weapons.extras import *
from src.game.power_ups.cards import *
from src.game.power_ups.effects import *
from src.game.enemies.enemy import *
from src.game.enemies.enemy_selector import *
from src.game.rescue.rescue import *
from src.game.rescue.arrow_indicator import *
from src.UI.scenes.end_screen import *
from src.UI.scenes.tutorial import *


class Run:
    def __init__(self):
        pygame.font.init()

        self.WIDTH_SCREEN = 1000
        self.HEIGHT_SCREEN = 600
        self.screen = pygame.display.set_mode((self.WIDTH_SCREEN, self.HEIGHT_SCREEN))
        pygame.display.set_caption("The Last Survivor - Game")
        self.load = Load()
        self.read_data = ReadData()

        self.initialize_data()
        self.initialize_game_variables()
        self.initialize_weapons_extras_power_up()
        self.update_weapons_with_levels()
        self.update_extras_with_levels()
        self.initialize_components()

        self.manager.change_weapon(1)
        self.manager.change_max_xp(1)

    def initialize_game_variables(self):
        self.zoom = 2
        self.life = 1
        self.xp_multiplier = 1
        self.range_obj = 25
        self.regeneration = 0
        self.hunger_resistance = 1
        self.piercing = 1
        self.speed_init = 3
        self.speed = self.speed_init
        self.pause = False
        self.movement = [0, 0]
        self.rock_collision = False
        self.current_shot = 0
        self.time = 0
        self.index_threshold_xp = 1
        self.weapon_id = 1
        self.win = False
        self.time_left = 180
        self.power_up_launch = False
        self.active_panel = None  # Can be "power_up", "extras" or "weapon"
        self.cooldown = 0.5

    def initialize_data(self):
        self.thresholds = self.read_data.read_json(
            "data/configurations/thresholds.json"
        )
        self.threshold_xp = self.thresholds["xp_thresholds"]
        self.player_stats = self.read_data.read_yaml("data/player_stats.yaml")
        self.bars = self.player_stats["bars"]
        self.resources = self.player_stats["resources"]
        self.data_enemies = self.read_data.read_json("data/configurations/enemies.json")
        self.data_weapons = self.read_data.read_json("data/configurations/weapons.json")
        self.data_weapons_levels = self.read_data.read_json(
            "data/configurations/weapons_levels.json"
        )
        self.data_extras_levels = self.read_data.read_json(
            "data/configurations/extras_levels.json"
        )
        self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
        self.data_power_up = self.read_data.read_json(
            "data/configurations/power_up.json"
        )
        self.data_extras = self.read_data.read_json("data/configurations/extras.json")
        self.commands = self.game_data["options"]
        self.FPS = int(self.game_data["options"]["fps"])
        self.difficulty = int(self.game_data["options"]["difficulty"])
        self.mouse_mappings = self._map_mouse_buttons()

    def _map_mouse_buttons(self):
        mouse_map = {}
        for action, button in self.commands.items():
            if button == "MOUSE1":
                mouse_map[action] = 1
            elif button == "MOUSE2":
                mouse_map[action] = 3
            elif button == "MOUSE3":
                mouse_map[action] = 2
            elif button == "MOUSE4":
                mouse_map[action] = 4
            elif button == "MOUSE5":
                mouse_map[action] = 5
        return mouse_map

    def update_extras_with_levels(self):
        for extra_id, extra_data in self.data_extras.items():
            extra_name = extra_data["name"]
            extra_level = extra_data["level"]
            if extra_level > 0:
                level_upgrades = self.data_extras_levels.get(extra_name, {})
                for stat, upgrade_value in level_upgrades.items():
                    if stat in extra_data:
                        extra_data[stat] += upgrade_value * (extra_level - 1)

    def update_weapons_with_levels(self):
        for weapon_id, weapon_data in self.data_weapons.items():
            weapon_name = weapon_data["name"]
            weapon_level = weapon_data["level"]
            if weapon_level > 0:
                level_upgrades = self.data_weapons_levels.get(weapon_name, {})
                for stat, upgrade_value in level_upgrades.items():
                    if stat in weapon_data:
                        if stat == "critical":
                            weapon_data[stat] += upgrade_value * (weapon_level - 1)
                        else:
                            weapon_data[stat] += int(upgrade_value * (weapon_level - 1))

    def initialize_weapons_extras_power_up(self):
        self.data_weapons = self.load.process_data(
            self.game_data, "weapon_level", self.data_weapons
        )
        self.current_weapon_dict = self.data_weapons[f"{self.weapon_id}"]
        self.position_weapon()

        self.data_extras = self.load.process_data(
            self.game_data, "extras_level", self.data_extras
        )

        self.data_power_up = self.load.process_data(
            self.game_data, "power_up_level", self.data_power_up
        )
        self.load.load_power_up(self.data_power_up)

    def position_weapon(self):
        self.current_weapon_dict["position"][0] = 500 + (10 * self.zoom)
        self.current_weapon_dict["position"][1] = 300 + (5 * self.zoom)

    def initialize_components(self):
        self.mouse = self.initialize_mouse()
        self.last_shot_time = self.mouse["current_time"]

        self.countdown = CountDown(self, self.time_left)
        self.random_enemy = EnemySelector(self.data_enemies)
        self.manager = RunManager(self)
        self.power_up = PowerUpCard(self, self.data_power_up)
        self.use_power_up = UsePowerUp(self)
        self.icon = Icon(self, self.resources, self.bars)
        self.player = Player(self, "jim")
        self.map_manager = MapManager(self, self.screen, self.player, self.zoom)
        self.weapon = Weapon(self.zoom, self.player, self.current_weapon_dict)
        self.drone = Drone(
            self.zoom, self.screen, self.player.enemies, self.data_extras["drone"]
        )
        self.update = Update(self)
        self.draw = Draw(self)
        self.weapons_cards = WeaponCard(self)
        self.extras_cards = ExtrasCard(self)
        self.shooter = Shooter(self)
        self.keyboard_input = KeyboardInput(self)
        self.rescue_ship = RescueShip(self)
        self.arrow_indicator = ArrowIndicator(self, self.rescue_ship)
        self.tutorial = Tutorial()
        self.pause_panel = PausePanel(self)
        self.electrodes_manager = ElectrodesManager(self)

        self.filtered_weapons = {
            key: weapon
            for key, weapon in self.data_weapons.items()
            if weapon.get("level", 0) > 0
        }

    def initialize_mouse(self):
        return {
            "press": False,
            "position": pygame.mouse.get_pos(),
            "current_time": pygame.time.get_ticks(),
            "shoot_delay": self.current_weapon_dict["rate"],
            "active_click": True,
            "cooldown_active_click": 0,
        }

    def run(self):
        clock = pygame.time.Clock()
        last_enemy_update = 0
        self.running = True
        while self.running:
            current_time = pygame.time.get_ticks()
            self.mouse["position"] = pygame.mouse.get_pos()
            self.mouse["current_time"] = pygame.time.get_ticks()
            self.mouse["shoot_delay"] = self.current_weapon_dict["rate"]
            if not self.pause:
                self.player.save_location()  #! Don't change this line...
                self.keyboard_input.check_input()  #! ...with this one (bad collision manager)
                if current_time - last_enemy_update >= 1000:  # 1000 ms = 1 seconde
                    self.manager.manage_enemies()
                    last_enemy_update = current_time  # Update last call
                self.use_power_up.use_power_up()

            self.keyboard_input.get_pause()
            self.draw.draw_all()

            if self.pause:
                if not self.power_up_launch:
                    self.pause_panel.draw()
            else:
                self.pause_panel.press_pause()

            self.update_class()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (
                        event.button == self.mouse_mappings.get("shoot")
                        and self.mouse["active_click"]
                    ):
                        self.mouse["press"] = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == self.mouse_mappings.get("shoot"):
                        self.mouse["press"] = False

            if not self.mouse["active_click"]:
                self.mouse["press"] = False
                current_time = pygame.time.get_ticks() / 1000  # Current time in seconds
                if current_time - self.mouse["cooldown_active_click"] > self.cooldown:
                    self.mouse["active_click"] = True

            clock.tick(self.FPS)

        self.manager.end_game()

    def update_class(self):
        self.update.update_all()
        if not self.pause:
            self.shooter.test_shooting()  #! Don't move this line (otherwise reloading does not work)
        pygame.display.flip()
