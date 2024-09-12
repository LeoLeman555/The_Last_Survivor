import pygame
import random
from load import *
import items

class Objects(pygame.sprite.Sprite):
  def __init__(self, zoom: int, icon: 'items.Icon', name: str, value: int, x: int, y: int, range_obj: int, speed_obj: int=4):
    super().__init__()
    self.zoom = zoom
    self.name = name
    self.value = value
    self.image = Load.charge_image(self, self.zoom, "token", self.name, "png", 0.25)
    self.x = x + random.randint(round(-10 * self.zoom), round(10 * self.zoom))
    self.y = y + random.randint(round(-10 * self.zoom), round(10 * self.zoom))

    self.range_obj = range_obj
    self.speed_obj = speed_obj

    self.range = range_obj * self.zoom
    self.speed = speed_obj * self.zoom
    self.rect = self.image.get_rect()
    self.lifetime = 1000
    self.icon = icon

  def change_zoom(self, new_zoom: int):
    self.zoom = new_zoom
    self.image = Load.charge_image(self, self.zoom, "token", self.name, "png", 0.25)
    self.rect = self.image.get_rect()
    self.range = self.range_obj * self.zoom
    self.speed = self.speed * self.zoom
  
  def draw(self, screen: pygame.Surface):
    """Draw on the screen."""
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

class GunGround(pygame.sprite.Sprite):
  def __init__(self, zoom: int, name: str, id: int, player, x: int, y: int, range_obj: int, speed_obj: int=4):
    super().__init__()
    self.zoom = zoom
    self.name = name
    self.id = id
    self.player = player
    self.image = Load.charge_image(self, self.zoom, "weapon", self.name, "png", 0.45)
    self.x = x + random.randint(round(-10 * self.zoom), round(10 * self.zoom))
    self.y = y + random.randint(round(-10 * self.zoom), round(10 * self.zoom))

    self.range_obj = range_obj
    self.speed_obj = speed_obj

    self.range = self.range_obj * self.zoom
    self.speed = self.speed_obj * self.zoom
    self.rect = self.image.get_rect()
    self.lifetime = 200

  def change_zoom(self, new_zoom: int):
    self.zoom = new_zoom
    self.image = Load.charge_image(self, self.zoom, "weapon", self.name, "png", 0.45)
    self.rect = self.image.get_rect()
    self.range = self.range_obj * self.zoom
    self.speed = self.speed * self.zoom
  
  def draw(self, screen: pygame.Surface):
    """Draw on the screen."""
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
      self.player.run.manager.new_weapon(self.name)
      self.kill()