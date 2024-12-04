import pygame
from src.data_handling.load import *

class Explosion(pygame.sprite.Sprite):
  def __init__(self, zoom: int, center: tuple, damage: int, enemies):
    """Initialize an explosion at the given center point."""
    super().__init__()
    self.zoom = zoom * 2
    self.enemies = enemies
    self.images = self.get_images()
    self.image = self.images[0]
    self.rect = self.image.get_rect(center=center)
    self.index = 0
    self.clock = pygame.time.get_ticks()

    self.damage = damage

  def change_zoom(self, new_zoom: int):
    """Adjust zoom level."""
    self.zoom = new_zoom * 2
    self.images = self.get_images()  # Recharger les images en fonction du nouveau zoom
    self.image = self.images[0]
    self.rect = self.image.get_rect(center=self.rect.center)

  def get_images(self):
    """Load explosion images from a sprite sheet."""
    images_explosion = []
    sprite_sheet_explosion = Load.charge_image(self, self.zoom, "weapon", "explosion", "png", 0.5)
    sprite_width = int(34.5 * self.zoom)
    sprite_height = int(34.7 * self.zoom)
    for y in range(0, sprite_sheet_explosion.get_height(), sprite_height):
      for x in range(0, sprite_sheet_explosion.get_width(), sprite_width):
        img = self.get_image(sprite_sheet_explosion, x, y, sprite_width, sprite_height)
        images_explosion.append(img)
    return images_explosion

  def get_image(self, sprite_sheet: pygame.Surface, x: int, y: int, width: int, height: int):
    """Extract a single image from the sprite sheet."""
    image = pygame.Surface([width, height], pygame.SRCALPHA)
    image.blit(sprite_sheet, (0, 0), (x, y, width, height))
    return image

  def update(self):
    """Update the explosion animation."""
    self.check_collision()
    now = pygame.time.get_ticks()
    if now - self.clock > 1:  # Change frame every 1ms
      self.index += 6
      if self.index < len(self.images):
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=self.rect.center)
        self.clock = now
      else:
        self.kill()

  def check_collision(self):
    """Checks for collisions with enemies."""
    hit_enemy = pygame.sprite.spritecollideany(self, self.enemies)
    if hit_enemy:
      hit_enemy.damage(self.damage)