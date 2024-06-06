import pygame
from animation import AnimateSprite
from weapon import Bullet, Weapon

class Sprites(AnimateSprite):     # classe du joueur
  """Classe des sprites

  Args:
      AnimateSprite (classe mère): héritage
  """
  def __init__(self, name, x, y):
    super().__init__(name)
    self.image = self.get_image(0, 0)
    self.image.set_colorkey([0, 0 , 0])     # gère la transparence
    self.rect = self.image.get_rect()
    self.position = [x, y]  # position du joueur
    self.feet = pygame.Rect(0, 0, self.rect.width * 0.4, 10)  # taille des pieds du joueur
    self.old_position = self.position.copy()

  def save_location(self) :
    """Sauvegarde la position du joueur dans une variable old_position
    """
    self.old_position = self.position.copy()

  def droite(self, diagonale):
    """Déplacement du personnage à droite avec animation
    """
    self.change_animation('right')
    self.position[0] += self.speed / diagonale

  def gauche(self, diagonale):
    """Déplacement du personnage à gauche avec animation
    """
    self.change_animation('left')
    self.position[0] -= self.speed/ diagonale

  def haut(self, diagonale):
    """Déplacement du personnage en haut avec animation
    """
    if diagonale == 1:
      self.change_animation('right')
    self.position[1] -= self.speed / diagonale

  def bas(self, diagonale):
    """Déplacement du personnage en bas avec animation
    """
    if diagonale == 1:
      self.change_animation('left')
    self.position[1] += self.speed / diagonale

  def update(self):
    """Actualise le rectangle du joueur
    """
    self.rect.topleft = self.position
    self.feet.midbottom = self.rect.midbottom

  def move_back(self):
    """Permet de revenir en arrière si collision
    """
    self.position = self.old_position
    self.rect.topleft = self.position
    self.feet.midbottom = self.rect.midbottom

class Player(Sprites):
  """Sous classe de Sprite qui s'occupe du joueur
  """
  def __init__(self):
    super().__init__("jim", 0, 0)
    self.attack = 10
    self.bullets = pygame.sprite.Group()
    self.weapons = pygame.sprite.Group()

  def launch_bullet(self, goal):
    self.bullets.add(Bullet(self, goal))

  def affiche_weapon(self, name, taille, position):
    self.weapons.add(Weapon(self, name, taille, position))