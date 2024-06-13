import pygame

class Grenade(pygame.sprite.Sprite):
  def __init__(self, screen, player, image_path, speed):
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

    self.sprite_sheet_explosion = pygame.image.load("res/weapon/explosion.png")
    self.images_explosion = self.get_images()

  def get_images(self):
    images_explosion = []
    sprite_width = 69
    sprite_height = int(69.4)
    for y in range(0, self.sprite_sheet_explosion.get_height(), sprite_height):
      for x in range(0, self.sprite_sheet_explosion.get_width(), sprite_width):
        img = self.get_image(x, y, sprite_width, sprite_height)
        images_explosion.append(img)
    return images_explosion
  
  def get_image(self, x, y, width, height):
    image = pygame.Surface([width, height], pygame.SRCALPHA)
    image.blit(self.sprite_sheet_explosion, (0, 0), (x, y, width, height))
    return image

  def explode(self):
    explosion = Explosion(self.rect.center, self.images_explosion)
    self.player.screen.blit(explosion.image, explosion.rect)
    self.player.explosions.add(explosion)  # Add explosion to the player's explosion group

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
    if self.rect.right > 900 or self.rect.left < 100:
      self.explode()  # Déclenche l'explosion
      self.kill()

class Explosion(pygame.sprite.Sprite):
  def __init__(self, center, images):
    super().__init__()
    self.images = images
    self.image = self.images[0]
    self.rect = self.image.get_rect(center=center)
    self.index = 0
    self.clock = pygame.time.get_ticks()

  def update(self):
    now = pygame.time.get_ticks()
    if now - self.clock > 1:  # changer de frame toutes les 50ms
      self.index += 6
      if self.index < 18:
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=self.rect.center)
        self.clock = now
      else:
        self.kill()  # supprimer l'explosion après la dernière frame