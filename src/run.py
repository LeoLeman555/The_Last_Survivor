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

class Run:
  def __init__(self):
    pygame.font.init()

    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Game")
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

    self.load = Load()
    self.read_data = ReadData()

    self.index_palier_xp = 1
    self.palier_xp = self.read_data.get_thresholds("data/paliers.txt")
    self.barres = self.read_data.read_bars_data("data/barres.txt")

    self.ressources = self.read_data.read_resources_data("data/ressources.txt")

    self.data_enemies = self.read_data.read_enemy_params("data/enemies.txt")
    self.random_enemy = EnemySelector(self.data_enemies)

    self.game_data = self.read_data.read_game_params("data/game_save.txt")
    self.manager = RunManager(self)

    self.data_weapons = self.read_data.read_weapon_params("data/weapons.txt")
    for weapon_name, level in self.game_data["weapon_level"].items():
      for weapon_id, weapon_info in self.data_weapons.items():
        if weapon_info["name"] == weapon_name:
          weapon_info["level"] = level
          if level == 0:
            weapon_info["locked"] = True
          else:
            weapon_info["locked"] = False
          break
    self.data_weapons = {key: value for key, value in self.data_weapons.items() if not value.get("locked", False)}

    self.weapon_id = 1
    self.current_weapon_dict = self.data_weapons[f"{self.weapon_id}"]
    self.current_weapon_dict["position"][0] = 500 + (10 * self.zoom)
    self.current_weapon_dict["position"][1] = 300 + (5 * self.zoom)
    self.mouse = {
      "press": False,
      "position": pygame.mouse.get_pos(),
      "current_time": pygame.time.get_ticks(),
      "shoot_delay": self.current_weapon_dict["rate"]
    }
    self.last_shot_time = self.mouse["current_time"]

    self.data_extras = self.read_data.read_extras_params("data/extras.txt")
    for extras_name, level in self.game_data["extras_level"].items():
      for extras_id, extras_info in self.data_extras.items():
        if extras_info["name"] == extras_name:
          extras_info["level"] = level
          if level == 0:
            extras_info["locked"] = True
          else:
            extras_info["locked"] = False
          break

    self.data_power_up = self.read_data.read_power_up_params("data/power_up.txt")
    self.load.load_power_up(self.data_power_up)
    self.power_up = PowerUp(self, self.data_power_up)
    self.use_power_up = UsePowerUp(self)

    self.icon = Icon(self, self.ressources, self.barres)
    self.player = Player(self, "jim")  #! Don't forget on Tiled to add a start object on the center of the map
    self.map_manager = MapManager(self, self.screen, self.player, self.zoom)
    self.weapon = Weapon(self.zoom, self.player, self.current_weapon_dict)
    self.drone = Drone(self.zoom, self.screen, self.player.enemies, self.data_extras["drone"])
    self.update = Update(self.zoom, self.screen, self.map_manager, self.player, self.weapon, self.ressources, self.barres, self.icon, self.current_weapon_dict, self.mouvement, self.mouse, self.data_extras, self.power_up)
    self.weapons_cards = WeaponCard(self)
    self.extras_cards = ExtrasCard(self)
    self.shooter = Shooter(self)
    self.keyboard_input = KeyboardInput(self)

    self.manager.change_max_xp(1)

  def run(self):
    clock = pygame.time.Clock()
    self.running = True
    while self.running:
      self.mouse["position"] = pygame.mouse.get_pos()
      self.mouse["current_time"] = pygame.time.get_ticks()
      self.mouse["shoot_delay"] = self.current_weapon_dict["rate"]
      if not self.pause:
        self.player.save_location() #! Don't move this line
        self.keyboard_input.check_input() #! With this one !!!

        #TODO add a enemy manager in a separate class
        if random.random() <= 0.005 or self.player.number_enemies < 5:
          for loop in range(0, 10):
            enemy = self.random_enemy.random_enemy(self.random_enemy.filter_by_exact_id(2.1))
            self.player.add_enemy(self.data_enemies, *enemy)
            self.player.number_enemies += 1

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

  def update_class(self):
    self.update.update_all(self.current_weapon_dict, self.mouvement, self.mouse, self.data_extras, self.pause)
    if not self.pause:
      self.shooter.test_shooting()
    pygame.display.flip()

  #TODO add a collision manager in a separate class
  def collision_sables(self, bool:bool):
    if bool:
      self.speed = self.speed_init/2
    else:
      self.speed = self.speed_init

  def collision(self, bool:bool):
    self.collision_caillou = bool