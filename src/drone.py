import pygame
import random

class Cible:
  def __init__(self, x, y):
    self.image = pygame.image.load("res/weapon/cible_drone.png")
    self.x = x
    self.y = y
    self.direction = 1
    self.speed = 3
    
  def update(self):
    self.x += self.direction * self.speed
    if self.x <= 150 or self.x >= 950 - self.image.get_width():
      self.direction *= -1  # Inverser la direction
    
  def draw(self, screen):
    if self.x <= 200 or self.x >= 800 - self.image.get_width() or 420 <= self.x <= 530:
      pass
    else:
      screen.blit(self.image, (self.x, self.y))

class Drone:
  def __init__(self, screen):
    self.screen = screen
    self.image_drone = pygame.image.load("res/weapon/drone.png")
    self.image_drone = pygame.transform.scale(self.image_drone, (81, 20))
    self.x_cible = 0
    self.cible = Cible(200, 315)
    
  def update_drone(self):
    self.screen.blit(self.image_drone, (460, 230))
    self.cible.update()
    self.cible.draw(self.screen)

class Laser():
  def __init__(self):
    if random.randint(1, 2) == 1:
      self.x = random.randint(100, 400)
    else:
      self.x = random.randint(600, 900)

    self.start_y = 0
    self.end_y = random.randint(200, 550)
    self.lifetime = 50

  def draw(self, screen):
    pygame.draw.line(screen, (255, 100, 100), (self.x, self.start_y), (self.x, self.end_y), 10)
    pygame.draw.line(screen, (255, 0, 0), (self.x, self.start_y), (self.x, self.end_y), 5)
    pygame.draw.circle(screen, (255, 0, 0), (self.x, self.end_y), 10)
    pygame.draw.circle(screen, (255, 100, 100), (self.x, self.end_y), 5)

  def update(self):
    self.lifetime -= 1