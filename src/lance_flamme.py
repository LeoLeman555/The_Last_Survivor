import pygame
import random
import math

class FireParticle:
  def __init__(self, x, y, direction):
    self.x = x
    self.y = y
    self.size = random.randint(6, 10)  # Augmenter la taille initiale des particules
    self.color = (random.randint(200, 255), random.randint(100, 150), 0)
    self.lifetime = random.randint(20, 25)
    self.direction = (direction[0] + random.uniform(-0.1, 0.1), direction[1] + random.uniform(-0.1, 0.1))
    self.speed = random.uniform(12, 16)  # Augmenter la vitesse des particules
    
  def update(self):
    self.x += self.direction[0] * self.speed
    self.y += self.direction[1] * self.speed
    self.size -= 0.2  # Les particules rétrécissent plus lentement
    self.lifetime -= 1
    
  def draw(self, screen):
    if self.lifetime < 18:
      pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))