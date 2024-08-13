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

class Run:
  def __init__(self, zoom:int):
    pygame.font.init()

    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Game")
    
    self.zoom = zoom

    self.read_data = ReadData()

    self.index_palier_xp = 1
    self.palier_xp = self.read_data.get_thresholds("data/paliers.txt")
    self.barres = self.read_data.read_bars_data("data/barres.txt")

    self.ressources = self.read_data.read_resources_data("data/ressources.txt")

    self.data_enemies = self.read_data.read_enemy_params("data/enemies.txt")
    self.random_enemy = EnemySelector(self.data_enemies)
    # print(list(self.data_enemies.keys()))

    self.data_weapons = self.read_data.read_weapon_params("data/weapons.txt")
    self.weapon_id = random.choice(list(self.data_weapons.keys()))
    self.weapon_id = 2
    self.weapon_dict = self.data_weapons[f"{self.weapon_id}"]
    self.weapon_dict["position"][0] += 10 * self.zoom
    self.weapon_dict["position"][1] += 5 * self.zoom
    # print(self.weapon_dict)

    self.data_extras = self.read_data.read_extras_params("data/extras.txt")
    print(self.data_extras)

    self.icon = Icon(self, self.ressources, self.barres)
    
    self.speed_init = 3
    self.speed = self.speed_init

    self.player = Player(self.zoom, self.screen, self, self.icon, "jim")  # mettre sur tiled un objet start
    self.map_manager = MapManager(self, self.screen, self.player, self.zoom)
    self.weapon = Weapon(self.zoom, self.player, self.weapon_dict)

    self.mouse = {
      "press": False,
      "position": pygame.mouse.get_pos(),
      "current_time": pygame.time.get_ticks(),
      "shoot_delay": self.weapon_dict["rate"]
    }

    self.last_shot_time = self.mouse["current_time"]

    self.drone = Drone(self.zoom, self.screen, self.player.enemies)

    self.mouvement = [0, 0]

    self.update = Update(self.zoom, self.screen, self.map_manager, self.player, self.weapon, self.ressources, self.barres, self.icon, self.weapon_dict, self.mouvement, self.mouse, self.data_extras)

    self.collision_caillou = False

    self.current_shot = 0
    self.time = 0

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

    if press[pygame.K_SPACE] and self.mouse["current_time"] - self.last_shot_time > 750 and self.data_extras["grenade"]["activate"] == True:
      if self.mouse["position"][0] > 500:
        self.player.launch_grenade(3/self.zoom)
      else:
        self.player.launch_grenade(-3/self.zoom)

      self.last_shot_time = self.mouse["current_time"]
  
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
          self.player.launch_grenade(10/self.zoom)
        else:
          self.player.launch_grenade(-10/self.zoom)

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
      self.player.save_location()
      self.keyboard_input()
      self.map_manager.draw()

      if random.random() <= 0.005 or self.player.number_enemies < 5:
        for loop in range(0, 10):
          enemy = self.random_enemy.random_enemy(self.random_enemy.filter_by_exact_id(1.1))
          self.player.add_enemy(self.data_enemies, *enemy)
          self.player.number_enemies += 1

      self.update_class()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.mouse["press"] = True
        elif event.type == pygame.MOUSEBUTTONUP:
          self.mouse["press"] = False

      clock.tick(60)

  def update_class(self):
    self.update.update_all(self.weapon_dict, self.mouvement, self.mouse, self.data_extras)

    self.test_shooting()

    if self.data_extras["drone"]["activate"] == True:
      self.drone.update_drone()

    pygame.display.flip()

  def collision_sables(self, bool:bool):
    if bool:
      self.speed = self.speed_init/2
    else:
      self.speed = self.speed_init

  def collision(self, bool:bool):
    self.collision_caillou = bool
