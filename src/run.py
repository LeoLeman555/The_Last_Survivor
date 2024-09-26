import pygame
from update import *
from items import *
from player import *
from map import *
from weapon import *
from extras import *
from load import *
from enemy import *
from enemy_selector import *
from power_up import *
from shooter import *
from keyboard_input import *
from run_manager import *
from end_screen import *

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
    self.initialize_weapons_and_extras()
    self.update_weapons_with_levels()
    self.update_extras_with_levels()
    self.initialize_components()

    self.manager.change_weapon(2)
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
    self.mouvement = [0, 0]
    self.collision_caillou = False
    self.current_shot = 0
    self.time = 0
    self.index_palier_xp = 1
    self.weapon_id = 1

  def initialize_data(self):
    self.palier_xp = self.read_data.get_thresholds("data/paliers.txt")
    self.barres = self.read_data.read_bars_data("data/barres.txt")
    self.ressources = self.read_data.read_resources_data("data/ressources.txt")
    self.data_enemies = self.read_data.read_params("data/enemies.txt", "enemies")
    self.data_weapons = self.read_data.read_params("data/weapons.txt", "weapons")
    self.data_weapons_levels = self.read_data.read_params("data/weapons_level.txt", "weapons_level")
    self.data_extras_levels = self.read_data.read_params("data/extras_level.txt", "extras_level")
    self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
    self.data_power_up = self.read_data.read_params("data/power_up.txt", "power_up")
    self.data_extras = self.read_data.read_params("data/extras.txt", "extras")

  def update_extras_with_levels(self):
    for extra_id, extra_data in self.data_extras.items():
      extra_name = extra_data["name"]
      extra_level = extra_data["level"]
      if extra_level > 0:
        level_upgrades = self.data_extras_levels.get(extra_name, {})
        for stat, upgrade_value in level_upgrades.items():
          if stat in extra_data:
            extra_data[stat] += upgrade_value * (extra_level - 1)
    # print(self.data_extras)

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

  def initialize_weapons_and_extras(self):
    self.data_weapons = self.load_and_process_data("weapon_level", self.data_weapons)
    self.current_weapon_dict = self.data_weapons[f"{self.weapon_id}"]
    self.position_weapon()

    self.data_extras = self.load_and_process_data("extras_level", self.data_extras)
    
    self.load.load_power_up(self.data_power_up)

  def load_and_process_data(self, level_key, data):
    for name, level in self.game_data[level_key].items():
      for item_id, item_info in data.items():
        if item_info["name"] == name:
          item_info["level"] = level
          item_info["locked"] = (level == 0)
          break
    return {key: value for key, value in data.items()}

  def position_weapon(self):
    self.current_weapon_dict["position"][0] = 500 + (10 * self.zoom)
    self.current_weapon_dict["position"][1] = 300 + (5 * self.zoom)

  def initialize_components(self):
    self.mouse = self.initialize_mouse()
    self.last_shot_time = self.mouse["current_time"]

    self.random_enemy = EnemySelector(self.data_enemies)
    self.manager = RunManager(self)
    self.power_up = PowerUp(self, self.data_power_up)
    self.use_power_up = UsePowerUp(self)
    self.icon = Icon(self, self.ressources, self.barres)
    self.player = Player(self, "jim")
    self.map_manager = MapManager(self, self.screen, self.player, self.zoom)
    self.weapon = Weapon(self.zoom, self.player, self.current_weapon_dict)
    self.drone = Drone(self.zoom, self.screen, self.player.enemies, self.data_extras["drone"])
    self.update = Update(self)
    self.weapons_cards = WeaponCard(self)
    self.extras_cards = ExtrasCard(self)
    self.shooter = Shooter(self)
    self.keyboard_input = KeyboardInput(self)

  def initialize_mouse(self):
    return {
      "press": False,
      "position": pygame.mouse.get_pos(),
      "current_time": pygame.time.get_ticks(),
      "shoot_delay": self.current_weapon_dict["rate"]
    }

  def run(self):
    clock = pygame.time.Clock()
    self.running = True
    while self.running:
      self.mouse["position"] = pygame.mouse.get_pos()
      self.mouse["current_time"] = pygame.time.get_ticks()
      self.mouse["shoot_delay"] = self.current_weapon_dict["rate"]
      if not self.pause:
        self.player.save_location() #! Don't change this line...
        self.keyboard_input.check_input() #! ...with this one (bad collision manager)
        self.manage_enemies()
        self.use_power_up.use_power_up()

      self.keyboard_input.get_pause()
      self.update_class()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.mouse["press"] = True
        elif event.type == pygame.MOUSEBUTTONUP:
          self.mouse["press"] = False
      clock.tick(60)

    pygame.quit()
    
    self.end_game()

  def end_game(self):
    rewards = {
    "resource": {
      "energy": self.icon.resource["energy"],
      "metal": self.icon.resource["metal"],
      "data": self.icon.resource["data"]
      }
    }
    game_over_screen = GameOverScreen(self.WIDTH_SCREEN, self.HEIGHT_SCREEN, rewards)
    game_over_screen.run()

  def manage_enemies(self):
    # ? maybe change the difficulty
    if random.random() <= 0.005 or self.player.number_enemies < 5:
      for loop in range(0, 10):
        enemy = self.random_enemy.random_enemy(self.random_enemy.filter_by_exact_id(1.1))
        self.player.add_enemy(self.data_enemies, *enemy)
        self.player.number_enemies += 1

  def update_class(self):
    self.update.update_all()
    if not self.pause:
      self.shooter.test_shooting()
    pygame.display.flip()

  def collision_sables(self, bool: bool):
    self.speed = self.speed_init / 2 if bool else self.speed_init

  def collision(self, bool: bool):
    self.collision_caillou = bool
