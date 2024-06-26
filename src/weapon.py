import pygame
import math
from extras import Explosion

class Weapon(pygame.sprite.Sprite):
  def __init__(self, player, name, taille, position):
    super().__init__()
    self.player = player
    self.name = name
    self.taille = taille
    self.image = pygame.image.load(f"res/weapon/{self.name}.png")
    self.image = pygame.transform.scale(self.image, self.taille)
    self.rect = self.image.get_rect()
    self.rect.center = position  # Center of the screen
    self.original_image = self.image  # Stockage de l'image originale pour la rotation
    self.angle = 0

  def display(self, screen):
    """Affiche l'arme au centre de l'écran."""
    screen.blit(self.image, self.rect)

  def rotate_to_cursor(self, cursor_pos):
    """Tourne l'arme pour qu'elle pointe vers le curseur de la souris."""
    # Calcul de l'angle entre l'arme et le curseur
    dx, dy = cursor_pos[0] - self.rect.centerx, cursor_pos[1] - self.rect.centery
    self.angle = math.degrees(math.atan2(dy, dx))

    # Vérification de l'orientation pour éviter l'inversion
    if 90 < self.angle < 270 or -270 < self.angle < -90:
      self.image = pygame.transform.flip(self.original_image, False, True)
    else:
      self.image = self.original_image

    # Rotation de l'image
    self.image = pygame.transform.rotozoom(self.image, -self.angle, 1)
    self.rect = self.image.get_rect(center=self.rect.center)
    

class Bullet(pygame.sprite.Sprite):
  def __init__(self, screen, player, goal, image_path, range=500, speed=30, explosive=False):
    super().__init__()
    self.speed = speed
    self.player = player
    self.range = range / 2
    self.distance_traveled = 0
    self.image = pygame.image.load(image_path)
    self.rect = self.image.get_rect()
    self.goal = goal
    self.rect.x = 520
    self.rect.y = 310
    self.screen = screen
    self.explosive = explosive

    dx, dy = self.goal[0] - self.rect.x, self.goal[1] - self.rect.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    self.vecteur = (self.speed * dx / distance, self.speed * dy / distance)

    self.origin_image = self.image
    self.angle = 0

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

  def rotate(self):
    self.angle = math.atan2(-self.vecteur[1], self.vecteur[0]) * 180 / math.pi
    self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
    self.rect = self.image.get_rect(center=self.rect.center)

  def delete(self):
    self.player.bullets.remove(self)

  def move(self):
    self.rotate()
    self.rect.x += self.vecteur[0]
    self.rect.y += self.vecteur[1]
    self.distance_traveled += self.speed

    if self.rect.x > 1000 or self.rect.x < 0 or self.rect.y > 600 or self.rect.y < 0 or self.distance_traveled > self.range:
      self.delete()
      if self.explosive:  # Déclenche l'explosion uniquement si la balle est explosive
        explosion = Explosion(self.rect.center, self.images_explosion)
        self.player.screen.blit(explosion.image, explosion.rect)
      