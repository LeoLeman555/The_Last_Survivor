import pygame

class HealthBar(pygame.sprite.Sprite):
  def __init__(self, zoom: int, x: int, y: int, width: int, max_health: int):
    super().__init__()
    self.zoom = zoom
    self.x = x
    self.y = y
    self.width = width
    self.height = self.zoom
    self.max_health = max_health
    self.health = max_health
    self.image = pygame.Surface((self.width, self.height))
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y - 10)
    self.update(self.health)

  def update(self, health: int):
    self.health = health
    health_ratio = self.health / self.max_health
    self.image.fill((255, 0, 0))
    pygame.draw.rect(self.image, (0, 255, 0), (0, 0, self.width * health_ratio, self.height))