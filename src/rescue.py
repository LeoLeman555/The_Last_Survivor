import pygame
import math
import random
from load import *

class RescueShip:
  def __init__(self, run):
    self.run = run
    self.original_image = Load.charge_image(self, self.run.zoom / 2, "rescue", "ship", "png", 1)
    self.image = self.original_image
    self.rect = self.image.get_rect()
    self.position = self.random_position(1000)
    self.target_position = self.random_position(-500)
    self.rect.center = self.position
    self.ladder_rect = pygame.Rect(0, 0, 30, 15)

    self.rescue = False
    self.move = False
    self.show_ladder = False
    self.float_counter = 0

    self.facing_right = True
    self.moving_right = True

    self.launch_rescue()

  def random_position(self, interval):
    x_ranges = {
      1: (-1000 - interval, 500 + interval),
      2: (500 + interval, 1000 + interval),
      3: (1000 + interval, 1500 + interval),
      4: (1500 + interval, 2000 + interval)
    }
    y_ranges = {
      1: (-1000 - interval, 1900 + interval),
      2: [(-1000 - interval, 500 + interval), (1100 + interval, 1700 + interval)],
      3: [(-1000 - interval, 500 + interval), (1100 + interval, 1700 + interval)],
      4: (-1000 - interval, 1700 + interval)
    }
    choice = random.choice(list(x_ranges.keys()))
    x = random.randint(*x_ranges[choice])
    if isinstance(y_ranges[choice], list):
      y_range = random.choice(y_ranges[choice])
    else:
      y_range = y_ranges[choice]
    y = random.randint(*y_range)
    return [x, y]

  def launch_rescue(self):
    self.rescue = True
    self.move = True

  def move_center(self):
    speed = 10
    delta_x = self.target_position[0] - self.position[0]
    delta_y = self.target_position[1] - self.position[1]

    if abs(delta_x) > speed:
      if delta_x > 0:
        self.position[0] += speed
        self.moving_right = True  # Va vers la droite
      else:
        self.position[0] -= speed
        self.moving_right = False  # Va vers la gauche
    else:
      self.position[0] = self.target_position[0]

    # Déplacement en Y
    if abs(delta_y) > speed:
      self.position[1] += speed if delta_y > 0 else -speed
    else:
      self.position[1] = self.target_position[1]  # Fixe à la position cible si proche

    # Mise à jour des coordonnées du rectangle
    self.rect.center = self.position

    # Condition pour vérifier si le vaisseau a atteint la cible
    if self.position == self.target_position:
      self.move = False
      print("ATTEINT")

  def update(self, x_var: int, y_var: int, player_rect: 'pygame.Rect'):
    x = (x_var / 2) * self.run.zoom
    y = (y_var / 2) * self.run.zoom

    self.position[0] += x
    self.position[1] += y
    self.target_position[0] += x
    self.target_position[1] += y
    
    if not self.move:
      self.float_counter += 0.3  # Incrémente plus rapidement pour accélérer le mouvement
      floating_offset = math.sin(self.float_counter) * 2  # Réduit l'amplitude (2 pixels)
      self.position[1] += floating_offset
    else:
      self.move_center()

    if not self.moving_right and self.facing_right:
      self.facing_right = False
      self.image = pygame.transform.flip(self.original_image, True, False)

    elif self.moving_right and self.facing_right:
      self.facing_right = True
      self.image = self.original_image

    self.rect.x = self.position[0]
    self.rect.y = self.position[1]

    self.check_collision(player_rect)

  def draw(self, screen):
    if self.rescue or self.move:
      if self.show_ladder and not self.move:
        self.draw_ladder(screen)

      # pygame.draw.rect(screen, (0, 0, 0), self.rect)
      screen.blit(self.image, self.rect)
      
  def draw_ladder(self, screen):
    if self.facing_right:
      ladder_x = self.rect.x + self.image.get_width() - 100 * self.run.zoom * 0.5
    else:
      ladder_x = self.rect.x + self.image.get_width() - 170 * self.run.zoom * 0.5

    ladder_y_start = self.rect.y + 60 * self.run.zoom * 0.5
    ladder_height = int(100 * self.run.zoom * 0.5)
    bar_spacing = int(20 * self.run.zoom * 0.5)
    ladder_color = (0, 0, 0)
    
    # Dessiner les barres de l'échelle
    pygame.draw.line(screen, ladder_color, (ladder_x, ladder_y_start), (ladder_x, ladder_y_start + ladder_height), int(3 * self.run.zoom * 0.5))
    pygame.draw.line(screen, ladder_color, (ladder_x + 10 * self.run.zoom * 0.5, ladder_y_start), (ladder_x + 10 * self.run.zoom * 0.5, ladder_y_start + ladder_height), int(3 * self.run.zoom * 0.5))
    for i in range(0, ladder_height // bar_spacing):
      y = ladder_y_start + i * bar_spacing
      pygame.draw.line(screen, ladder_color, (ladder_x, y), (ladder_x + 10 * self.run.zoom * 0.5, y), int(3 * self.run.zoom * 0.5))
    
    # Mise à jour de self.ladder_rect
    rectangle_width = 30 * self.run.zoom * 0.5
    rectangle_height = 15 * self.run.zoom * 0.5
    rectangle_x = ladder_x - 10 * self.run.zoom * 0.5
    rectangle_y = ladder_y_start + ladder_height  # Sous l'échelle
    self.ladder_rect.update(rectangle_x, rectangle_y, rectangle_width, rectangle_height)

    # pygame.draw.rect(screen, ladder_color, self.ladder_rect)

  def check_collision(self, player_rect: 'pygame.Rect'):
    if self.rect.colliderect(player_rect):
      self.show_ladder = True

    if self.ladder_rect.colliderect(player_rect):
      self.ladder_rect.center = 0, 0
      self.ladder_rect.width = 0
      self.ladder_rect.height = 0
      self.show_ladder = False
      self.rescue = False
      print("RESCUE")

  def change_zoom(self):
    self.speed = 10 * self.run.zoom * 0.5
    self.original_image = Load.charge_image(self, self.run.zoom / 2, "rescue", "ship", "png", 1)
    self.image = self.original_image
    if not self.facing_right:
      self.image = pygame.transform.flip(self.original_image, True, False)
    self.rect = self.image.get_rect()