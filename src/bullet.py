import pygame

class Bullet(pygame.sprite.Sprite):
  def __init__(self, player):
    super().__init__()
    self.speed = 5
    self.player = player
    self.image = pygame.image.load("res/weapon/bullet.png")
    self.image = pygame.transform.scale(self.image, (50, 50))
    self.rect = self.image.get_rect()
    self.rect.x = 500
    self.rect.y = 300

  def delete(self):
    self.player.bullets.remove(self)

  def move(self):
    self.rect.x += self.speed

    if self.rect.x > 900:
      self.delete()