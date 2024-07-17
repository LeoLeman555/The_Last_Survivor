import pygame, random

class FireParticle:
  def __init__(self, zoom:int, x:int, y:int, direction:tuple):
    self.zoom = zoom
    self.x = x
    self.y = y
    self.size = random.randint(3*self.zoom, 5*self.zoom)  # Augmenter la taille initiale des particules
    self.color = (random.randint(200, 255), random.randint(100, 150), 0)
    self.lifetime = random.randint(10*self.zoom, 12*self.zoom)
    self.direction = (direction[0] + random.uniform(-0.1, 0.1), direction[1] + random.uniform(-0.1, 0.1))
    self.speed = random.uniform(6*self.zoom, 8*self.zoom)  # Augmenter la vitesse des particules
    
  def update(self):
    self.x += self.direction[0] * self.speed
    self.y += self.direction[1] * self.speed
    self.size -= 0.2  # Les particules rétrécissent plus lentement
    self.lifetime -= 1
    
  def draw(self, screen:'pygame.surface.Surface'):
    if self.lifetime < 8 * self.zoom:
      pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))