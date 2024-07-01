import pygame

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
    self.x_cible = 0
    self.cible = Cible(200, 315)
    
  def update_drone(self):
    self.screen.blit(self.image_drone, (460, 230))
    self.cible.update()
    self.cible.draw(self.screen)