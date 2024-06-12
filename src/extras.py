import pygame

class Grenade(pygame.sprite.Sprite):
  def __init__(self, screen, player, image_path, speed=5):
    super().__init__()
    self.screen = screen
    self.player = player
    self.image = pygame.image.load(image_path).convert_alpha()
    self.rect = self.image.get_rect()
    # Position initiale de la grenade en fonction du joueur
    self.rect.centerx = player.rect.centerx - (player.rect.x - 500)
    self.rect.centery = player.rect.centery - (player.rect.y - 300)
    self.speed = speed
    self.gravity = 0.4
    self.velocity_y = -10
    self.bounce_factor = 0.8
    self.rebound_height = self.screen.get_height() // 2

  def update(self):
    # Mise à jour de la position horizontale
    self.rect.x += self.speed
    
    # Mise à jour de la position verticale avec la gravité
    self.velocity_y += self.gravity
    self.rect.y += self.velocity_y

    # Vérifier si la grenade touche la position de rebond
    if self.rect.bottom >= self.rebound_height:
      self.rect.bottom = self.rebound_height
      self.velocity_y = -self.velocity_y * self.bounce_factor
      if abs(self.velocity_y) < 1:  # Arrêter la grenade après quelques rebonds
        self.velocity_y = 0
    
    # Vérifier si la grenade sort de l'écran
    if self.rect.right > self.screen.get_width() or self.rect.left < 0:
      print("Grenade hors de l'écran, suppression.")
      self.kill()