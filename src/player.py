import pygame
import time
from weapon import *
from extras import *
from enemy import *
from load import *
from objects import *
from message import *
from grenade import *

class Player(pygame.sprite.Sprite):
  def __init__(self, run, name: str ="jim", x: int =0, y: int =0):
    super().__init__()
    self.run = run
    self.screen = self.run.screen
    self.icon = self.run.icon
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
    self.rect_collision.width = 17 * self.run.zoom
    self.rect_collision.height = 38 * self.run.zoom
    self.rect_collision.x = 500 - 8.5 * self.run.zoom
    self.rect_collision.y = 300 - 19 * self.run.zoom
    
    self.position = [x, y]
    self.feet = pygame.Rect(0, 0, self.rect.width * 0.4, 10)
    self.old_position = self.position.copy()
    self.attack = 10
    self.enemies = pygame.sprite.Group()
    self.bullets = pygame.sprite.Group()
    self.grenades = pygame.sprite.Group()
    self.explosions = pygame.sprite.Group()
    self.particles = pygame.sprite.Group()
    self.lasers = pygame.sprite.Group()
    self.missiles = pygame.sprite.Group()
    self.objects = pygame.sprite.Group()
    self.messages = pygame.sprite.Group()
    self.toxic_particles = pygame.sprite.Group()

    self.number_enemies = 0

  def change_zoom(self):
    self.rect_collision = self.rect.copy()
    self.rect_collision.width = 17 * self.run.zoom
    self.rect_collision.height = 38 * self.run.zoom
    self.rect_collision.x = 500 - 8.5 * self.run.zoom
    self.rect_collision.y = 300 - 19 * self.run.zoom

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
    if self.run.icon.resource["health"] <= 0 or self.run.icon.resource["food"] <= 0:
      self.run.life -= 1
      if self.run.life:
        print("Alive")
        for enemy in self.enemies:
          enemy.delete()
        self.run.icon.resource["health"] = 100
        self.run.icon.resource["food"] = 100
    if self.run.life == 0:
      print("DEATH")
      self.die()
    self.rect.topleft = self.position
    self.feet.midbottom = self.rect.midbottom
    self.run.icon.resource["food"] -= 0.04 / self.run.hunger_resistance

    if not hasattr(self, 'last_regeneration_time'):
      self.last_regeneration_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    time_elapsed = current_time - self.last_regeneration_time
    if time_elapsed >= 1000 and self.run.icon.resource["health"] < 100:
        self.run.icon.resource["health"] += self.run.regeneration
        self.last_regeneration_time = current_time

  def move_back(self):
    self.position = self.old_position
    self.rect.topleft = self.position
    self.feet.midbottom = self.rect.midbottom

  def launch_bullet(self, goal:tuple, weapon_dict: dict, delay: int =0):
    self.bullets.add(Bullet(self.run.zoom, self.run.screen, self, self.enemies, goal, weapon_dict, delay, self.run.piercing))

  def add_fire(self, weapon_dict: dict):
    x = 500 + 10 * self.run.zoom
    y = 300 + 5 * self.run.zoom
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - 500
    dy = mouse_y - 300
    distance = math.hypot(dx, dy)
    direction = (dx / distance, dy / distance)  # Normaliser le vecteur
    damage = weapon_dict["damage"] / 60
    for _ in range(10):
      self.particles.add(FireParticle(self.run.zoom, self.enemies, x, y, direction, damage))

  def launch_grenade(self, speed: int, grenade_dict: dict):
    print("launch grenade", grenade_dict["type"])
    self.grenades.add(Grenade(self.run.zoom, self.run.screen, self.enemies, self, grenade_dict, speed))

  def add_enemy(self, data: dict, name: str, x: int = 0, y: int = 0):
    if name.lower() in data:
      enemy = Enemy(self.run.zoom, self.run.screen, name, self, self.run.icon, x, y, data)
      self.enemies.add(enemy)

  def add_laser(self):
    self.lasers.add(Laser(self.run.zoom, self.enemies, self.run.data_extras["laser"]))

  def add_missile(self):
    self.missiles.add(Missile(self.run.zoom, self, self.enemies, self.run.data_extras["missile"]))

  def add_object(self, name: str, value: int, x: int, y: int):
    self.objects.add(Objects(self.run.zoom, self.run.icon, name, value, x, y, self.run.range_obj))

  def add_weapon(self, name: str, id: int, x: int, y: int):
    self.objects.add(GunGround(self.run.zoom, name, id, self,x, y, self.run.range_obj))

  def change_weapon(self, id:int):
    self.run.change_weapon(id)

  def add_message(self, text: str, start_position: tuple, end_position: tuple, color: tuple, font_size: int, duration: int):
    self.messages.add((Message(self.run.zoom, text, start_position, end_position, color, font_size, duration)))

  def die(self):
    self.run.running = False