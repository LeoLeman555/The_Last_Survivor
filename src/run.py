import pygame, random, math
from update import *
from items import *
from player import *
from map import *
from weapon import *
from extras import *
from load import *
from enemy import *

class Run:
  def __init__(self, zoom:int):
    pygame.font.init()

    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Jeu")
    
    self.zoom = zoom

    self.read_data = ReadData()

    self.index_palier_xp = 1
    self.palier_xp = self.read_data.get_thresholds("data/paliers.txt")
    self.ressources = self.read_data.read_resources_data("data/ressources.txt")
    self.barres = self.read_data.read_bars_data("data/barres.txt")

    self.data_weapons = self.read_data.read_weapon_data("data/weapons.txt")
    self.data_enemies = self.read_data.read_enemy_params("data/enemies.txt")

    self.weapon_id = random.choice(list(self.data_weapons.keys()))
    self.weapon_id = 10

    self.weapon_dict = self.get_weapon(self.weapon_id, self.data_weapons)
    print(self.weapon_dict)

    self.icon = Icon(self.ressources, self.barres)
    
    self.speed_init = 3
    self.speed = self.speed_init

    self.player = Player(self.zoom, self.screen, self.icon, "jim")  # mettre sur tiled un objet start
    self.map_manager = MapManager(self, self.screen, self.player, self.zoom) # appel de la classe mapManager
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

    self.update = Update(self.zoom, self.screen, self.map_manager, self.player, self.weapon, self.ressources, self.barres, self.icon, self.weapon_dict, self.mouvement, self.mouse)

    self.collision_caillou = False

  def get_weapon(self, id: int, data: dict):
    weapon_dict = {
      "id": self.weapon_id,
      "name": data[id][0],
      "size": data[id][1],
      "position": list(data[id][2]),
      "range": data[id][3],
      "explosive": data[id][4],
      "rate": data[id][6],
      "precision": data[id][7],
      "number_shoot": data[id][8],
      "delay": data[id][9],
      "dps": data[id][10],
      # "speed": data[id][11]
    }
    weapon_dict["position"][0] += 10 * self.zoom
    weapon_dict["position"][1] += 5 * self.zoom
    return weapon_dict

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

    if press[pygame.K_r] and self.mouse["current_time"] - self.last_shot_time > 750:
      if self.mouse["position"][0] > 500:
        self.player.launch_grenade(3/self.zoom)
      else:
        self.player.launch_grenade(-3/self.zoom)

      self.last_shot_time = self.mouse["current_time"]
  
  def change_max_xp(self, palier):
    self.index_palier_xp = palier
    self.icon.change_threshold("xp", self.palier_xp[self.index_palier_xp])

  def random_enemy(self):
    names = list(self.data_enemies.keys())
    random_name = random.choice(names)
    x_ranges = {
        1: (-100, 0),
        2: (0, 500),
        3: (500, 1000),
        4: (1000, 1100)}
    y_ranges = {
        1: (-100, 700),
        2: [(-100, 0), (600, 700)],
        3: [(-100, 0), (600, 700)],
        4: (-100, 700)}
    choice = random.choice([1, 2, 3, 4])
    x = random.randint(*x_ranges[choice])
    
    if choice in [2, 3]:
        y_range = random.choice(y_ranges[choice])
        y = random.randint(*y_range)
    else:
        y = random.randint(*y_ranges[choice])
    return random_name, x, y
  
  def shoot(self):
    if self.weapon_id == 7:
      self.player.add_fire(0.25)
    elif self.mouse["current_time"] - self.last_shot_time > self.mouse["shoot_delay"]:
      if self.weapon_id == 9:
        if self.mouse["position"][0] > 500:
          self.player.launch_grenade(10/self.zoom)
        else:
          self.player.launch_grenade(-10/self.zoom)

      else:
        if self.weapon_dict["delay"] == 0:
          for position in range(-30, self.weapon_dict["number_shoot"], int(30/self.weapon_dict["number_shoot"])):
            self.player.launch_bullet((list(self.mouse["position"])[0] + position, (list(self.mouse["position"])[1] + position)), self.weapon_id, self.data_weapons)
        else:
          for delay in range(0, self.weapon_dict["number_shoot"], self.weapon_dict["delay"]):
            self.player.launch_bullet(((list(self.mouse["position"])[0] + random.randint(-self.weapon_dict["precision"], self.weapon_dict["precision"])), (list(self.mouse["position"])[1] + random.randint(-self.weapon_dict["precision"], self.weapon_dict["precision"]))), self.weapon_id, self.data_weapons, delay)
      self.last_shot_time = self.mouse["current_time"]

  def run(self):
    clock = pygame.time.Clock()
    run = True
    self.change_max_xp(5)
    self.player.add_enemy(self.data_enemies, "worm", 0, 0)

    self.player.add_object(0, 0)

    while run:
      self.mouse["position"] = pygame.mouse.get_pos()
      self.mouse["current_time"] = pygame.time.get_ticks()
      self.player.save_location()
      self.keyboard_input()
      self.map_manager.draw()

      if random.random() <= 0.05:
          enemy = self.random_enemy()
          self.player.add_enemy(self.data_enemies, *enemy)

      # self.icon.add_bars("xp", 1)
      # self.icon.add_resource("en", 1)

      self.update_class()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.mouse["press"] = True
        elif event.type == pygame.MOUSEBUTTONUP:
          self.mouse["press"] = False

      clock.tick(60)

  def update_class(self):
    self.update.update_all(self.weapon_dict, self.mouvement, self.mouse)

    if self.mouse["press"]:
      self.shoot()

    self.drone.update_drone()

    pygame.display.flip()

  def collision_sables(self, bool:bool):
    if bool:
      self.speed = self.speed_init/2
    else:
      self.speed = self.speed_init

  def collision(self, bool:bool):
    self.collision_caillou = bool
