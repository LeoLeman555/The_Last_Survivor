import pygame
import random
import time
import math
from src.data_handling.load import *

PALETTE = [  # Palette for toxic particles
    (34, 139, 34), # Forest green
    (0, 100, 0), # Dark green
    (50, 205, 50), # Lime green
    (0, 255, 0), # Light green
    (0, 128, 0) # Medium green
]

class ToxicParticle(pygame.sprite.Sprite):
  def __init__(self, zoom: int, x: int, y: int, enemies, damage):
    super().__init__()
    self.zoom = zoom
    self.x = x
    self.y = y
    self.size_origin = random.randint(2, 4)
    self.size = round(self.size_origin * self.zoom)
    angle = random.uniform(0, 2 * math.pi)
    speed = random.uniform(1, round(2*self.zoom))
    self.speed_x = speed * math.cos(angle)
    self.speed_y = speed * math.sin(angle)
    self.color = random.choice(PALETTE)
    self.creation_time = time.time()
    self.life_duration_origin = 25
    self.life_duration = round(self.life_duration_origin*self.zoom)
    self.alpha = 255
    self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    self.enemies = enemies
    self.damage = damage

  def change_zoom(self, new_zoom: int):
    """Adjust zoom level."""
    self.zoom = new_zoom
    self.size = round(self.size_origin * self.zoom)
    self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    self.life_duration = round(self.life_duration_origin*self.zoom)

  def update(self, x_var: int, y_var: int):
    """Update grenade position."""
    x = (x_var / 2) * self.zoom
    y = (y_var / 2) * self.zoom
    self.x += self.speed_x + x
    self.y += self.speed_y + y
    self.speed_x *= 0.99
    self.speed_y *= 0.99

    self.rect.topleft = (self.x - self.size // 2, self.y - self.size // 2)
    self.rect.size = (self.size, self.size)
    
    elapsed_time = time.time() - self.creation_time
    if elapsed_time > self.life_duration:
      self.alpha = 0
    else:
      self.alpha = max(0, 255 - int((elapsed_time / self.life_duration) * 255))

    self.life_duration -= 1

    if self.life_duration <= 0:
      self.kill()

    self.check_collision()
    
  def check_collision(self):
    """Checks for collisions with enemies."""
    hit_enemy = pygame.sprite.spritecollideany(self, self.enemies)
    if hit_enemy:
      hit_enemy.damage(self.damage)

  def draw(self, screen):
    """Draw grenade."""
    particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
    pygame.draw.circle(particle_surface, (*self.color, self.alpha), (self.size, self.size), self.size)
    screen.blit(particle_surface, (self.x - self.size, self.y - self.size))