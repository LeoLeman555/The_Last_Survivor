import pygame
import random
from load import *
import items

class Objects(pygame.sprite.Sprite):
  def __init__(self, zoom: int, icon: 'items.Icon', name: str, value: int, x: int, y: int):
    super().__init__()
    self.zoom = zoom
    self.name = name
    self.value = value
    self.image = Load.charge_image(self, self.zoom, "token", self.name, "png", 0.25)
    self.x = x + random.randint(-5 * self.zoom, 5 * self.zoom)
    self.y = y + random.randint(-5 * self.zoom, 5 * self.zoom)

    self.range = 25 * self.zoom
    self.speed = 4 * self.zoom
    self.rect = self.image.get_rect()
    self.lifetime = 500
    self.icon = icon
  
  def draw(self, screen: pygame.Surface):
    """Draw the missile on the screen."""
    # pygame.draw.rect(screen, (0, 0, 0), self.rect)
    screen.blit(self.image, (self.x, self.y))

  def update(self, x_var: int, y_var: int, player_rect: 'pygame.Rect'):
    """Update the object's position and lifetime."""
    self.lifetime -= 1
    x = (x_var / 2) * self.zoom
    y = (y_var / 2) * self.zoom
    self.x += x
    self.y += y
    self.rect.x = self.x
    self.rect.y = self.y

    # Vérification de la proximité avec le joueur
    player_center = player_rect.center
    obj_center = self.rect.center
    distance_x = player_center[0] - obj_center[0]
    distance_y = player_center[1] - obj_center[1]
    distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

    if distance <= self.range:
      # Calcul de la direction vers le joueur
      if distance != 0:
        move_x = (distance_x / distance) * min(self.speed, distance)
        move_y = (distance_y / distance) * min(self.speed, distance)
      else:
        move_x, move_y = 0, 0

      # Déplacement vers le joueur
      self.x += move_x
      self.y += move_y
      self.rect.x = int(self.x)
      self.rect.y = int(self.y)

    self.check_collision(player_rect)

    if self.lifetime <= 0:
      self.kill()

  def check_collision(self, player_rect: 'pygame.Rect'):
    """Checks for collisions with enemies."""
    if self.rect.colliderect(player_rect):
      self.icon.add_resource(self.name, self.value)
      self.kill()