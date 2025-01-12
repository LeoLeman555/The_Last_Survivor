import pygame
import random
import math
from src.data_handling.load import *
from src.game.animations.explosion import *

class Bullet(pygame.sprite.Sprite):
  def __init__(self, zoom: int, screen: 'pygame.surface.Surface', player, enemies, goal: tuple, weapon_dict: dict, delay, piercing):
    super().__init__()
    self.zoom = zoom
    self.data = weapon_dict
    self.speed = self.data["bullet_speed"] * self.zoom
    self.player = player
    self.enemies = enemies

    self.critical = 0
    self.damage = self.data["damage"]
    if random.random() < self.data["critical"]:
      self.damage *= 2
      self.critical = 1
    self.piercing = piercing
    self.ammo_name = self.data["ammo_name"]
    self.range = self.data["range"] * self.zoom
    self.distance_weapon = self.data["distance_bullet"] * self.zoom
    self.distance_traveled = 0
    self.image = Load.charge_image(self, self.zoom / 2, "weapon", self.ammo_name, "png", 1)
    self.rect = self.image.get_rect()
    self.goal = goal
    self.position = self.data["position"]
    self.rect.center = self.position
    self.screen = screen
    self.explosive = self.data["explosion"]

    self.delay = delay

    dx, dy = self.goal[0] - self.rect.x, self.goal[1] - self.rect.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    self.vector = (self.speed * dx / distance, self.speed * dy / distance)

    self.origin_image = self.image
    self.angle = 0

  def rotate(self):
    """Rotates the bullet image based on its direction vector."""
    self.angle = math.atan2(-self.vector[1], self.vector[0]) * 180 / math.pi
    self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
    self.rect = self.image.get_rect(center=self.rect.center)

  def delete(self):
    """Removes the bullet from the player's bullets list."""
    self.player.bullets.remove(self)

  def update(self):
    """Moves the bullet and handles collisions."""
    if self.delay == 0:
      self.rotate()
      self.rect.x += self.vector[0]
      self.rect.y += self.vector[1]
      self.distance_traveled += self.speed

      if self.distance_traveled > self.range:
        self.delete()
        self.explode()
      else:
        self.check_collision()
    else:
      self.delay -= 1

  def draw(self, screen):
    if self.distance_traveled > self.distance_weapon:
      screen.blit(self.image, self.rect)

  def check_collision(self):
    """Checks for collisions with enemies."""
    hit_enemy = pygame.sprite.spritecollideany(self, self.enemies)
    if hit_enemy:
      self.piercing -= 1
      hit_enemy.damage(self.damage)
      self.rect.x += self.vector[0]
      self.rect.y += self.vector[1]
      if self.critical == 1:
        self.player.add_message("CRITICAL!!!", (self.rect.center[0], self.rect.center[1]), (self.rect.center[0], self.rect.center[1]-50*self.zoom), (255, 0, 0), 8*self.zoom, 1000)
      if self.piercing == 0:
        self.delete()
        self.explode()

  def explode(self):
    """Triggers an explosion if the bullet is explosive."""
    if self.explosive:
      explosion = Explosion(self.zoom, self.rect.center, self.damage, self.enemies)
      self.player.screen.blit(explosion.image, explosion.rect)
      self.player.explosions.add(explosion)
