import pygame
import random

class FireParticle(pygame.sprite.Sprite):
  def __init__(self, zoom: int, enemies, x: int, y: int, direction: tuple, damage: float):
    super().__init__()
    self.zoom = zoom
    self.x = x
    self.y = y
    self.enemies = enemies
    self.damage = damage
    self.size_origin = random.randint(3, 5)
    self.size = round(self.size_origin * self.zoom)
    self.color = (random.randint(200, 255), random.randint(100, 150), 0)
    self.lifetime_origin = random.randint(10, 12)
    self.lifetime = round(self.lifetime_origin * self.zoom)
    self.direction = (direction[0] + random.uniform(-0.1, 0.1), direction[1] + random.uniform(-0.1, 0.1))
    self.speed = random.uniform(6 * self.zoom, 8 * self.zoom)
    self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

  def update(self):
    """Updates the particle's position and properties."""
    self.x += self.direction[0] * self.speed
    self.y += self.direction[1] * self.speed
    self.size -= 0.2
    self.lifetime -= 1
    if self.lifetime <= 0:
      self.kill()
    self.rect.topleft = (self.x - self.size // 2, self.y - self.size // 2)
    self.rect.size = (self.size, self.size)
    self.check_collision()

  def draw(self, screen: 'pygame.surface.Surface'):
    """Draws the particle on the screen."""
    if 8 * self.zoom > self.lifetime > 0:
      pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

  def check_collision(self):
    """Checks for collisions with enemies."""
    hit_enemy = pygame.sprite.spritecollideany(self, self.enemies)
    if hit_enemy:
      hit_enemy.damage(self.damage)