import pygame
import math

class Bullet(pygame.sprite.Sprite):
  def __init__(self, player, goal):
    super().__init__()
    self.speed = 1
    self.player = player
    self.image = pygame.image.load("res/weapon/munition.png")
    self.image = pygame.transform.scale(self.image, (28, 9))
    self.rect = self.image.get_rect()
    self.goal = goal
    self.rect.x = 500
    self.rect.y = 300
    self.vecteur = ((self.goal[0]-self.rect.x)/50, (self.goal[1]-self.rect.y)/50)
    self.origin_image = self.image
    self.angle = 0

  def rotate(self):
    # Calcul de l'angle en degrés
    self.angle = math.atan2(-self.vecteur[1], self.vecteur[0]) * 180 / math.pi
    # Rotation de l'image
    self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
    self.rect = self.image.get_rect(center = self.rect.center)

  def delete(self):
    self.player.bullets.remove(self)

  def move(self):
    self.rotate()
    self.rect.x += self.vecteur[0]
    self.rect.y += self.vecteur[1]
    self.rotate()

    if self.rect.x > 900 or self.rect.x < 100 or self.rect.y > 500 or self.rect.y < 100:
      self.delete()