import pygame
from load import *
import items

class Objects(pygame.sprite.Sprite):
  def __init__(self, zoom: int, icon: 'items.Icon', x: int, y: int):
    super().__init__()
    self.zoom = zoom
    # self.image = Load.charge_image(self, self.zoom, "weapon", "cible_missile", "png", 0.5)
    self.x = x
    self.y = y
    self.rect = pygame.Rect(self.x, self.y, 5 * self.zoom, 5 * self.zoom)
    self.lifetime = 1000
    self.icon = icon
  
  def draw(self, screen: pygame.Surface):
    """Draw the missile on the screen."""
    pygame.draw.rect(screen, (0, 0, 0), self.rect)
    # screen.blit(self.cible_missile, (self.x, self.y))

  def update(self, x_var: int, y_var: int, player_rect: 'pygame.Rect'):
    """Update the missile's position and lifetime."""
    self.lifetime -= 1
    x = (x_var / 2) * self.zoom
    y = (y_var / 2) * self.zoom
    self.x += x
    self.y += y
    self.rect.x = self.x
    self.rect.y = self.y

    self.check_collision(player_rect)

    if self.lifetime <= 0:
      self.kill()

  def check_collision(self, player_rect: 'pygame.Rect'):
    """Checks for collisions with enemies."""
    if self.rect.colliderect(player_rect):
      self.icon.add_resource("do", 5)
      self.icon.add_resource("en", 50)
      self.kill()