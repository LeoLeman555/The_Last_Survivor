import pygame
from weapon import *
from extras import *
from enemy import *
from load import Load

class Player(pygame.sprite.Sprite):
  def __init__(self, zoom:int, screen:'pygame.surface.Surface', icon :'items.Icon', name:str ="jim", x:int =0, y:int =0):
    super().__init__()
    self.zoom = zoom
    self.screen = screen
    self.icon = icon
    self.sprite_sheet = Load.charge_image(self, 1, "sprite", name, "png")
    self.animation_index = 0
    self.clock = 0
    self.images = {
      'right': self.get_images(0),
      'left': self.get_images(38)
    }
    self.speed = 0
    self.image = self.get_image(0, 0)
    self.image.set_colorkey((0, 0, 0))
    self.rect = self.image.get_rect()

    self.rect_collision = self.rect.copy()
    self.rect_collision.width = 17 * self.zoom
    self.rect_collision.height = 38 * self.zoom
    self.rect_collision.x = 500 - 8.5 * self.zoom
    self.rect_collision.y = 300 - 19 * self.zoom
    
    self.position = [x, y]
    self.feet = pygame.Rect(0, 0, self.rect.width * 0.4, 10)
    self.old_position = self.position.copy()
    self.attack = 10
    self.enemies = pygame.sprite.Group()
    self.bullets = pygame.sprite.Group()
    self.weapons = pygame.sprite.Group()
    self.grenades = pygame.sprite.Group()
    self.explosions = pygame.sprite.Group()
    self.particles = pygame.sprite.Group()
    self.lasers = pygame.sprite.Group()
    self.missiles = pygame.sprite.Group()

    self.ammo_images = {
      1: "ammo1",
      2: "ammo1",
      3: "ammo2",
      4: "ammo3",
      5: "ammo1",
      6: "ammo4",
      7: "lance_flammes",
      8: "ammo1",
      9: "ammo5",
      10: "ammo6",
      11: "ammo6",
      12: "ammo1",
    }

    self.enemy_dict = {
    "shardsoul": Shardsoul,
    "sprout": Sprout,
    "worm": Worm,
    "wolf": Wolf,
    "robot": Robot}

  def change_animation(self, name:str, speed:int):
    self.speed = speed
    self.image = self.images[name][self.animation_index]
    self.image.set_colorkey((0, 0, 0))
    self.clock += self.speed * 10

    if self.clock >= 100:
      self.animation_index = (self.animation_index + 1) % len(self.images[name])
      self.clock = 0

  def get_images(self, y:int):
    images = []
    for i in range(8):
      x = i * 17
      image = self.get_image(x, y)
      images.append(image)
    return images

  def get_image(self, x:int, y:int):
    image = pygame.Surface([17, 38], pygame.SRCALPHA)
    image.blit(self.sprite_sheet, (0, 0), (x, y, 17, 38))
    return image

  def save_location(self):
    self.old_position = self.position.copy()

  def move_right(self, diagonale:int, speed:int):
    self.change_animation('right', speed)
    self.position[0] += self.speed / diagonale

  def move_left(self, diagonale:int, speed:int):
    self.change_animation('left', speed)
    self.position[0] -= self.speed / diagonale

  def move_up(self, diagonale:int, speed:int):
    if diagonale == 1:
      self.change_animation('right', speed)
    self.position[1] -= self.speed / diagonale

  def move_down(self, diagonale:int, speed:int):
    if diagonale == 1:
      self.change_animation('left', speed)
    self.position[1] += self.speed / diagonale

  def update(self):
    # pygame.draw.rect(self.screen, (0, 0, 0), self.rect_collision)
    self.rect.topleft = self.position
    self.feet.midbottom = self.rect.midbottom

  def move_back(self):
    self.position = self.old_position
    self.rect.topleft = self.position
    self.feet.midbottom = self.rect.midbottom

  def launch_bullet(self, goal:tuple, weapon_id:int, data_weapon:dict):
    ammo_image = self.ammo_images.get(weapon_id)
    position = data_weapon[weapon_id][2]
    position = list(position)
    weapon_range = data_weapon[weapon_id][3]
    explosive = data_weapon[weapon_id][4] == 1
    distance = data_weapon[weapon_id][5]
    # speed bullet is not defined => default value
    self.bullets.add(Bullet(self.zoom, self.screen, self, self.enemies, goal, ammo_image, distance, position, weapon_range, explosive))

  def add_fire(self):
    x = 500 + 10 * self.zoom
    y = 300 + 5 * self.zoom
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - 500
    dy = mouse_y - 300
    distance = math.hypot(dx, dy)
    direction = (dx / distance, dy / distance)  # Normaliser le vecteur
    for _ in range(10):  # Ajouter plus de particules à la fois pour plus de diffusion
      self.particles.add(FireParticle(self.zoom, self.enemies, x, y, direction))

  def display_weapon(self, name:str, size:tuple, position:tuple):
    self.weapons.add(Weapon(self.zoom, self, name, size, position))

  def launch_grenade(self, speed:int):
    self.grenades.add(Grenade(self.zoom, self.screen, self.enemies, self, speed))

  def add_enemy(self, name:str, x:int=0, y:int=0):
    if name.lower() in self.enemy_dict:
      enemy_class = self.enemy_dict[name.lower()]
      self.enemies.add(enemy_class(self.zoom, self.screen, self.icon, x, y))

  def add_laser(self):
    self.lasers.add(Laser(self.zoom, self.enemies))

  def add_missile(self):
    self.missiles.add(Missile(self.zoom, self.enemies))