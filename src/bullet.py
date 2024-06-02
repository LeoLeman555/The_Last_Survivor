import pygame

class Bullet(pygame.sprite.Sprite):
  def __init__(self, player, goal):
    super().__init__()
    self.speed = 1
    self.player = player
    self.image = pygame.image.load("res/weapon/bullet.png")
    self.image = pygame.transform.scale(self.image, (50, 50))
    self.rect = self.image.get_rect()
    self.goal = goal
    self.rect.x = 500
    self.rect.y = 300
    self.vecteur = ((self.goal[0]-self.rect.x)/100, (self.goal[1]-self.rect.y)/100)  

  def delete(self):
    self.player.bullets.remove(self)

  def move(self):
    self.rect.x += self.vecteur[0]
    self.rect.y += self.vecteur[1]

    if self.rect.x > 900 or self.rect.x < 100 or self.rect.y > 500 or self.rect.y < 100:
      self.delete()