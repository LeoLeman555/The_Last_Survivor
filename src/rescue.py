import pygame
import math
import random
from load import *

class RescueShip:
  def __init__(self, run):
    self.run = run
    self.original_image = Load.charge_image(self, self.run.zoom / 2, "rescue", "ship", "png", 1)
    
    # Load movement images
    self.move_images_right = [
      Load.charge_image(self, self.run.zoom / 2, "rescue", "ship_move1", "png", 1),
      Load.charge_image(self, self.run.zoom / 2, "rescue", "ship_move2", "png", 1),
      Load.charge_image(self, self.run.zoom / 2, "rescue", "ship_move3", "png", 1)
    ]
    # Pre-flip images for left
    self.move_images_left = [pygame.transform.flip(img, True, False) for img in self.move_images_right]
    
    self.current_move_frame = 0  # Current image index
    self.animation_delay = 75  # Delay in milliseconds between image changes
    self.last_update = pygame.time.get_ticks()  # Time of the last animation update
    
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
        self.moving_right = True  # Moving to the right
      else:
        self.position[0] -= speed
        self.moving_right = False  # Moving to the left
    else:
      self.position[0] = self.target_position[0]

    # Movement in Y
    if abs(delta_y) > speed:
      self.position[1] += speed if delta_y > 0 else -speed
    else:
      self.position[1] = self.target_position[1]  # Set to target position if close

    # Update rectangle coordinates
    self.rect.center = self.position

    if self.position == self.target_position:
      self.move = False
  
  def update(self, x_var: int, y_var: int, player_rect: 'pygame.Rect'):
    x = (x_var / 2) * self.run.zoom
    y = (y_var / 2) * self.run.zoom

    self.position[0] += x
    self.position[1] += y
    self.target_position[0] += x
    self.target_position[1] += y
    
    if not self.move:
      self.float_counter += 0.3  # Increment faster to accelerate movement
      floating_offset = math.sin(self.float_counter) * 2  # Reduce amplitude (2 pixels)
      self.position[1] += floating_offset
    else:
      self.move_center()

    # Handle animation
    current_time = pygame.time.get_ticks()
    if self.move:
      if current_time - self.last_update > self.animation_delay:
        self.last_update = current_time
        self.current_move_frame = (self.current_move_frame + 1) % len(self.move_images_right)
        if self.facing_right:
          self.image = self.move_images_right[self.current_move_frame]
        else:
          self.image = self.move_images_left[self.current_move_frame]
    else:
      # If the ship is not moving, display the base image
      if self.facing_right:
        self.image = self.original_image
      else:
        self.image = pygame.transform.flip(self.original_image, True, False)

    # Handle direction
    if not self.moving_right and self.facing_right:
      self.facing_right = False
      # Switch to the first image of the left sequence
      self.current_move_frame = 0
      self.image = self.move_images_left[self.current_move_frame]

    elif self.moving_right and not self.facing_right:
      self.facing_right = True
      # Switch to the first image of the right sequence
      self.current_move_frame = 0
      self.image = self.move_images_right[self.current_move_frame]

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
    
    # Draw the ladder bars
    pygame.draw.line(screen, ladder_color, (ladder_x, ladder_y_start), (ladder_x, ladder_y_start + ladder_height), int(3 * self.run.zoom * 0.5))
    pygame.draw.line(screen, ladder_color, (ladder_x + 10 * self.run.zoom * 0.5, ladder_y_start), (ladder_x + 10 * self.run.zoom * 0.5, ladder_y_start + ladder_height), int(3 * self.run.zoom * 0.5))
    for i in range(0, ladder_height // bar_spacing):
      y = ladder_y_start + i * bar_spacing
      pygame.draw.line(screen, ladder_color, (ladder_x, y), (ladder_x + 10 * self.run.zoom * 0.5, y), int(3 * self.run.zoom * 0.5))
    
    # Update self.ladder_rect
    rectangle_width = 30 * self.run.zoom * 0.5
    rectangle_height = 15 * self.run.zoom * 0.5
    rectangle_x = ladder_x - 10 * self.run.zoom * 0.5
    rectangle_y = ladder_y_start + ladder_height  # Below the ladder
    self.ladder_rect.update(rectangle_x, rectangle_y, rectangle_width, rectangle_height)
  
  def check_collision(self, player_rect: 'pygame.Rect'):
    if self.rect.colliderect(player_rect):
      self.show_ladder = True

    if self.ladder_rect.colliderect(player_rect):
      self.ladder_rect.center = 0, 0
      self.ladder_rect.width = 0
      self.ladder_rect.height = 0
      self.show_ladder = False
      self.rescue = False

      self.run.win = True
      self.run.player.die()

      print("RESCUE")
  
  def change_zoom(self):
    self.speed = 10 * self.run.zoom * 0.5
    self.original_image = Load.charge_image(self, self.run.zoom / 2, "rescue", "ship", "png", 1)
    # Reload movement images with the new zoom
    self.move_images_right = [
      Load.charge_image(self, self.run.zoom / 2, "rescue", "ship_move1", "png", 1),
      Load.charge_image(self, self.run.zoom / 2, "rescue", "ship_move2", "png", 1),
      Load.charge_image(self, self.run.zoom / 2, "rescue", "ship_move3", "png", 1)
    ]
    self.move_images_left = [pygame.transform.flip(img, True, False) for img in self.move_images_right]
    
    self.image = self.original_image
    if not self.facing_right:
      self.image = pygame.transform.flip(self.original_image, True, False)
    self.rect = self.image.get_rect()

class ArrowIndicator:
  def __init__(self, run, rescue_ship):
    self.run = run
    self.rescue_ship = rescue_ship
    self.original_arrow_image = Load.charge_image(self, 1, "rescue", "arrow_ship", "png", 1)
    self.arrow_image = self.original_arrow_image
    self.arrow_rect = self.arrow_image.get_rect()

    self.arrow_rect.center = 500, 50
    
  def update(self):
    delta_x = self.rescue_ship.rect.centerx - self.arrow_rect.centerx
    delta_y = self.rescue_ship.rect.centery - self.arrow_rect.centery
    angle = math.atan2(delta_y, delta_x)
    self.arrow_image = pygame.transform.rotate(self.original_arrow_image, -math.degrees(angle) + 90)
  
  def draw(self, screen):
    if self.rescue_ship.rescue or self.rescue_ship.move:
      screen.blit(self.arrow_image, self.arrow_rect)
