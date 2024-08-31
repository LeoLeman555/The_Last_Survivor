import pygame, random, math
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
    # TODO self.time in Player for regeneration => sends a signal when 1 second has elapsed
    self.hunger_resistance = 1
    self.piercing = 1
    # TODO implement piercing in bullet and in ennemi => later?
    self.speed_init = 3
    self.pause = False
    self.mouvement = [0, 0]

    self.load = Load()
    self.read_data = ReadData()

    self.index_palier_xp = 1
    self.palier_xp = self.read_data.get_thresholds("data/paliers.txt")
    self.barres = self.read_data.read_bars_data("data/barres.txt")

    self.ressources = self.read_data.read_resources_data("data/ressources.txt")

    self.data_enemies = self.read_data.read_enemy_params("data/enemies.txt")
    self.random_enemy = EnemySelector(self.data_enemies)

    self.data_weapons = self.read_data.read_weapon_params("data/weapons.txt")
    self.weapon_id = random.choice(list(self.data_weapons.keys()))
    self.weapon_id = 1

    self.weapon_dict = self.data_weapons[f"{self.weapon_id}"]
    self.weapon_dict["position"][0] = 500 + (10 * self.zoom)
    self.weapon_dict["position"][1] = 300 + (5 * self.zoom)

    self.data_extras = self.read_data.read_extras_params("data/extras.txt")

    self.data_power_up = self.read_data.read_power_up_params("data/power_up.txt")
    self.load_power_up()
    self.power_up = PowerUp(self.data_power_up, self.cards_positions, self)

    self.icon = Icon(self, self.ressources, self.barres)
    
    self.speed = self.speed_init

    self.player = Player(self, "jim")  # mettre sur tiled un objet start
    self.map_manager = MapManager(self, self.screen, self.player, self.zoom)
    self.weapon = Weapon(self.zoom, self.player, self.weapon_dict)

    self.mouse = {
      "press": False,
      "position": pygame.mouse.get_pos(),
      "current_time": pygame.time.get_ticks(),
      "shoot_delay": self.weapon_dict["rate"]
    }

    self.last_shot_time = self.mouse["current_time"]

    self.drone = Drone(self.zoom, self.screen, self.player.enemies, self.data_extras["drone"])

    self.update = Update(self.zoom, self.screen, self.map_manager, self.player, self.weapon, self.ressources, self.barres, self.icon, self.weapon_dict, self.mouvement, self.mouse, self.data_extras, self.power_up)

    self.collision_caillou = False

    self.current_shot = 0
    self.time = 0

    self.change_weapon(5)

  def start_run(self):
    self.ressources["ammo"] = 500
    self.ressources["health"] = 100
    self.ressources["food"] = 100
    self.run()

  def load_power_up(self):
    for power_up_name, power_up_data in self.data_power_up.items():
      image_path = f"res/power_up/{power_up_name}.png"
      resized_image = self.load.load_and_resize_image(image_path, 268, 189)
      left_image, right_image = self.load.split_image(resized_image)
      power_up_data["left_image"] = left_image
      power_up_data["right_image"] = right_image
    self.cards_positions = [(274, 200), (432, 200), (590, 200)]

  def change_weapon(self, id):
    self.weapon_dict = self.data_weapons[f"{id}"]
    self.weapon_dict["position"][0] = 500 + (10 * self.zoom)
    self.weapon_dict["position"][1] = 300 + (5 * self.zoom)
    self.weapon.change_weapon(self.zoom, self.player, self.weapon_dict)

  def keyboard_input(self):
    """Déplacement du joueur avec les touches directionnelles"""
    press = pygame.key.get_pressed()

    # condition de déplacement
    if press[pygame.K_w] and press[pygame.K_a]: # pour se déplacer en diagonale
      self.player.move_up(1.5, self.speed)
      self.player.move_left(1.5, self.speed)
      self.mouvement = [math.ceil(self.speed*1.33), math.ceil(self.speed*1.33)]
    elif press[pygame.K_w] and press[pygame.K_d]:
      self.player.move_up(1.5, self.speed)
      self.player.move_right(1.5, self.speed)
      self.mouvement = [math.ceil(self.speed*1.33)*-1, math.ceil(self.speed*1.33)]
    elif press[pygame.K_s] and press[pygame.K_d]:
      self.player.move_down(1.5, self.speed)
      self.player.move_right(1.5, self.speed)
      self.mouvement = [math.ceil(self.speed*1.33)*-1, math.ceil(self.speed*1.33)*-1]
    elif press[pygame.K_s] and press[pygame.K_a]:
      self.player.move_down(1.5, self.speed)
      self.player.move_left(1.5, self.speed)
      self.mouvement = [math.ceil(self.speed*1.33), math.ceil(self.speed*1.33)*-1]
    elif press[pygame.K_w]:        # pour se déplacer
      self.player.move_up(1, self.speed)
      self.mouvement = [0, self.speed*2]
    elif press[pygame.K_s]:
      self.player.move_down(1, self.speed)
      self.mouvement = [0, self.speed*-2]
    elif press[pygame.K_a]:
      self.player.move_left(1, self.speed)
      self.mouvement = [self.speed*2, 0]
    elif press[pygame.K_d]:
      self.player.move_right(1, self.speed)
      self.mouvement = [self.speed*-2, 0]
    else:
      self.mouvement = [0, 0]
    
    if self.collision_caillou:
      self.mouvement = [0, 0]

    if press[pygame.K_g]:
      unlocked_power_ups = [name for name, data in self.data_power_up.items() if not data.get('locked', False)]
      self.power_up.launch_cards(random.sample(unlocked_power_ups, 3))
      self.pause = True

    if press[pygame.K_z]:
      if self.zoom != 2:
        self.zoom = 2
      else:
        self.zoom = 1.5
      self.map_manager.change_map_size(self.zoom)
      self.update.change_zoom(self.zoom)
      time.sleep(0.1)

    if press[pygame.K_SPACE] and self.mouse["current_time"] - self.data_extras["grenade"]["last_shot_time"] > self.data_extras["grenade"]["rate"] and self.data_extras["grenade"]["activate"] == True:
      if self.mouse["position"][0] > 500:
        self.player.launch_grenade(self.data_extras["grenade"]["speed"]*self.zoom, self.data_extras["grenade"])
      else:
        self.player.launch_grenade(-self.data_extras["grenade"]["speed"]*self.zoom, self.data_extras["grenade"])

      self.data_extras["grenade"]["last_shot_time"] = self.mouse["current_time"]

  def get_pause(self):
    press = pygame.key.get_pressed()
    if press[pygame.K_p]:
      if self.pause:
        self.pause = False
        time.sleep(1)
      else:
        self.pause = True  
        time.sleep(0.1)
  
  def change_max_xp(self, palier):
    self.index_palier_xp = palier
    self.icon.change_threshold("xp", self.palier_xp[self.index_palier_xp])

  def test_shooting(self):
    if self.mouse["press"] and self.current_shot < self.weapon_dict["charger_capacity"] and self.mouse["current_time"] - self.last_shot_time > self.mouse["shoot_delay"]:
      self.shoot()
      self.current_shot += self.weapon_dict["number_shoot"]
      self.last_shot_time = self.mouse["current_time"]
    elif not self.current_shot < self.weapon_dict["charger_capacity"]:
      if self.time >= self.weapon_dict["recharge_time"]:
        self.current_shot = 0
        self.icon.resource["ammo"] -= self.weapon_dict["charger_capacity"]
        self.time = 0
      else:
        self.time += 1
        self.draw_reload_bar()

  def draw_reload_bar(self):
    bar_width = 50 * self.zoom
    bar_height = 2 * self.zoom
    
    bar_x = 500 - bar_width/2
    bar_y = 300 + bar_width/2
    
    reload_progress = self.time / self.weapon_dict["recharge_time"]
    fill_width = int(bar_width * reload_progress)
    pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, fill_width, bar_height))

  def shoot(self):
    if self.weapon_dict["type"] == "flamethrower":
      self.player.add_fire(self.weapon_dict)

    elif self.mouse["current_time"] - self.last_shot_time > self.mouse["shoot_delay"]:
      if self.weapon_dict["type"] == "grenade_launcher":
        if self.mouse["position"][0] > 500:
          self.player.launch_grenade(1*self.zoom, self.data_extras["grenade"])
        else:
          self.player.launch_grenade(-1*self.zoom, self.data_extras["grenade"])

      else:
        if self.weapon_dict["delay"] == 0:
          for position in range(-30, 10, 3):
            self.player.launch_bullet((list(self.mouse["position"])[0] + position, (list(self.mouse["position"])[1] + position)), self.weapon_dict)
        else:
          for delay in range(0, self.weapon_dict["number_shoot"], self.weapon_dict["delay"]):
            self.player.launch_bullet(((list(self.mouse["position"])[0] + random.randint(-self.weapon_dict["precision"], self.weapon_dict["precision"])), (list(self.mouse["position"])[1] + random.randint(-self.weapon_dict["precision"], self.weapon_dict["precision"]))), self.weapon_dict, delay)
      self.last_shot_time = self.mouse["current_time"]

  def run(self):
    clock = pygame.time.Clock()
    self.running = True
    self.change_max_xp(1)

    while self.running:
      self.mouse["position"] = pygame.mouse.get_pos()
      self.mouse["current_time"] = pygame.time.get_ticks()
      self.mouse["shoot_delay"] = self.weapon_dict["rate"]
      if not self.pause:
        self.keyboard_input()
        self.player.save_location()

        if random.random() <= 0.005 or self.player.number_enemies < 5:
          for loop in range(0, 10):
            enemy = self.random_enemy.random_enemy(self.random_enemy.filter_by_exact_id(1.1))
            self.player.add_enemy(self.data_enemies, *enemy)
            self.player.number_enemies += 1

        self.use_power_up()
      self.get_pause()
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
    self.update.update_all(self.weapon_dict, self.mouvement, self.mouse, self.data_extras, self.pause)

    if not self.pause:
      self.test_shooting()

    pygame.display.flip()

  def collision_sables(self, bool:bool):
    if bool:
      self.speed = self.speed_init/2
    else:
      self.speed = self.speed_init

  def collision(self, bool:bool):
    self.collision_caillou = bool

  def use_power_up(self):
    if self.data_power_up["care_kit"]["activate"]:
      self.icon.resource["health"] += self.data_power_up["care_kit"]["value"]
      self.data_power_up["care_kit"]["activate"] = False

    if self.data_power_up["survival_ration"]["activate"]:
      self.icon.resource["food"] += self.data_power_up["survival_ration"]["value"]
      self.data_power_up["survival_ration"]["activate"] = False

    if self.data_power_up["critical_hit"]["activate"]:
      for weapon_id, weapon_data in self.data_weapons.items():
        if "critical" in weapon_data:
          weapon_data["critical"] *= self.data_power_up["critical_hit"]["value"]
      self.data_power_up["critical_hit"]["activate"] = False

    if self.data_power_up["2nd_life"]["activate"]:
      self.life = 2
      self.data_power_up["2nd_life"]["activate"] = False
    
    if self.data_power_up["expert"]["activate"]:
      self.xp_multiplier *= self.data_power_up["expert"]["value"]
      self.data_power_up["expert"]["activate"] = False

    if self.data_power_up["boost"]["activate"]:
      self.speed_init *= self.data_power_up["boost"]["value"]
      self.data_power_up["boost"]["activate"] = False

    if self.data_power_up["agile_fingers"]["activate"]:
      for weapon_id, weapon_data in self.data_weapons.items():
        if "recharge_time" in weapon_data:
          weapon_data["recharge_time"] *= self.data_power_up["agile_fingers"]["value"]
      self.data_power_up["agile_fingers"]["activate"] = False

    if self.data_power_up["extra_ammo"]["activate"]:
      for weapon_id, weapon_data in self.data_weapons.items():
        if "charger_capacity" in weapon_data:
          weapon_data["charger_capacity"] += self.data_power_up["extra_ammo"]["value"]
      self.data_power_up["extra_ammo"]["activate"] = False

    if self.data_power_up["large_range"]["activate"]:
      for weapon_id, weapon_data in self.data_weapons.items():
        if "range" in weapon_data:
          weapon_data["range"] *= self.data_power_up["large_range"]["value"]
      self.data_power_up["large_range"]["activate"] = False

    if self.data_power_up["magnetic"]["activate"]:
      self.range_obj *= self.data_power_up["magnetic"]["value"]
      self.data_power_up["magnetic"]["activate"] = False

    if self.data_power_up["rapid_fire"]["activate"]:
      for weapon_id, weapon_data in self.data_weapons.items():
        if "rate" in weapon_data:
          weapon_data["rate"] *= self.data_power_up["rapid_fire"]["value"]
      self.data_power_up["rapid_fire"]["activate"] = False

    if self.data_power_up["strong_stomach"]["activate"]:
      self.hunger_resistance *= self.data_power_up["strong_stomach"]["value"]
      self.data_power_up["strong_stomach"]["activate"] = False

    if self.data_power_up["zoom"]["activate"]:
      self.zoom = 1.5
      self.map_manager.change_map_size(self.zoom)
      self.update.change_zoom(self.zoom)
      self.drone.change_zoom(self.zoom)
      self.data_power_up["zoom"]["activate"] = False