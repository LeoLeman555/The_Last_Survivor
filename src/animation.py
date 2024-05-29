import pygame
from chargement import Chargement
class AnimateSprite(pygame.sprite.Sprite):
  def __init__(self, name):
    """Charge les différents personages

    Args:
        name (str): nom du perso a charger
    """
    super().__init__()
    self.sprite_sheet = Chargement.charge_image(self, chemin="sprite", name=name, extension="png")
    self.animation_index = 0
    self.clock = 0
    self.images = {
      'right': self.get_images(0), # recuperation des différentes images
      'left': self.get_images(38),}
    self.speed = 0    #int(input("Vitesse"))  #? valeur ronde sinon joueur flou
    
  def change_animation(self, name):
    """Permet d'afficher les différentes animations du personnage

    Args:
        name (str): nom de l'image a animer
    """
    self.image = self.images[name][self.animation_index]      # change de costume
    self.image.set_colorkey([0, 0 , 0])     # gère la transparence
    self.clock += self.speed * 10

    if self.clock >= 100:
      self.animation_index += 1 # passe a l'image suivante

      if self.animation_index >= len(self.images[name]):
        self.animation_index = 0

      self.clock = 0
    
  def get_images(self, y):
    """Cherche les différentes images du sprite sheet

    Args:
        y (int): axe y du sprite sheet

    Returns:
        liste images: contient toutes images du sprite sheet
    """
    images = []
    for i in range(0, 8):
      x = i*17
      image = self.get_image(x, y)
      images.append(image)
    
    return images
  
  def get_image(self, x, y):
    """_summary_

    Args:
        x (int): axe x
        y (int): axe y

    Returns:
        variable image: image a afficher
    """
    image = pygame.Surface([17, 38])
    image.blit(self.sprite_sheet, (0, 0), (x, y, 17, 38))
    return image
  
  def vitesse(self, speed):
    self.speed = speed