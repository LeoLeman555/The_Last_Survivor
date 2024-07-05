import pygame
from chargement import Chargement
class AnimateSprite(pygame.sprite.Sprite):
  def __init__(self, name):
    super().__init__()
    self.sprite_sheet = Chargement.charge_image(self, chemin="sprite", name=name, extension="png")
    self.animation_index = 0
    self.clock = 0
    self.images = {
      'right': self.get_images(0), # recuperation des différentes images
      'left': self.get_images(38),}
    self.speed = 0    #int(input("Vitesse"))  #? valeur ronde sinon joueur flou
    
  def change_animation(self, name, speed):
    self.speed = speed
    self.image = self.images[name][self.animation_index]      # change de costume
    self.image.set_colorkey([0, 0 , 0])     # gère la transparence
    self.clock += self.speed * 10

    if self.clock >= 100:
      self.animation_index += 1 # passe a l'image suivante

      if self.animation_index >= len(self.images[name]):
        self.animation_index = 0

      self.clock = 0
    
  def get_images(self, y):
    images = []
    for i in range(0, 8):
      x = i*17
      image = self.get_image(x, y)
      images.append(image)
    
    return images
  
  def get_image(self, x, y):
    image = pygame.Surface([17, 38])
    image.blit(self.sprite_sheet, (0, 0), (x, y, 17, 38))
    return image