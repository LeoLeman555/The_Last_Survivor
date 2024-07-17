import pygame, math, player, random
from extras import Explosion
from load import *

class Weapon(pygame.sprite.Sprite):
  def __init__(self, zoom:int, player:'player.Player', name:str, taille:tuple, position:list):
    super().__init__()
    self.zoom = zoom
    self.player = player
    self.name = name
    self.taille = taille
    self.image = Load.charge_image(self, self.zoom/2, "weapon", self.name, "png", 0.85)
    self.rect = self.image.get_rect()
    self.position = position

    self.rect.center = self.position  # Center of the screen
    self.original_image = self.image  # Stockage de l'image originale pour la rotation
    self.angle = 0

  def display(self, screen:'pygame.surface.Surface'):
    """Affiche l'arme au centre de l'écran."""
    screen.blit(self.image, self.rect)

  def rotate_to_cursor(self, cursor_pos:tuple):
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
  def __init__(self, zoom:int, screen:'pygame.surface.Surface', player:'player.Player', goal:tuple, name:str, distance_weapon:int, position:list, range:int =500, explosive:bool =False, speed:int =15):
    super().__init__()
    self.zoom = zoom
    self.speed = speed * self.zoom
    self.player = player
    self.name = name
    self.range = range * self.zoom
    self.distance_weapon = distance_weapon * self.zoom
    self.distance_traveled = 0
    self.image = Load.charge_image(self, self.zoom/2, "weapon", self.name, "png", 1)
    self.rect = self.image.get_rect()
    self.goal = goal
    self.position = position
    self.position[0] += 10 * self.zoom
    self.position[1] += 5 * self.zoom
    self.rect.center = self.position
    self.screen = screen
    self.explosive = explosive

    dx, dy = self.goal[0] - self.rect.x, self.goal[1] - self.rect.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    self.vecteur = (self.speed * dx / distance, self.speed * dy / distance)

    self.origin_image = self.image
    self.angle = 0

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

    # pygame.draw.rect(self.screen, (0, 0, 0), self.rect)
    if self.distance_traveled > self.distance_weapon:
      self.screen.blit(self.image, self.rect)

    if self.distance_traveled > self.range:
      self.delete()
      self.explode()

  def explode(self):
    if self.explosive:  # Déclenche l'explosion uniquement si la balle est explosive
      explosion = Explosion(self.rect.center)
      self.player.screen.blit(explosion.image, explosion.rect)
      self.player.explosions.add(explosion)

class FireParticle:
  def __init__(self, zoom:int, x:int, y:int, direction:tuple):
    self.zoom = zoom
    self.x = x
    self.y = y
    self.size = random.randint(3*self.zoom, 5*self.zoom)  # Augmenter la taille initiale des particules
    self.color = (random.randint(200, 255), random.randint(100, 150), 0)
    self.lifetime = random.randint(10*self.zoom, 12*self.zoom)
    self.direction = (direction[0] + random.uniform(-0.1, 0.1), direction[1] + random.uniform(-0.1, 0.1))
    self.speed = random.uniform(6*self.zoom, 8*self.zoom)  # Augmenter la vitesse des particules
    
  def update(self):
    self.x += self.direction[0] * self.speed
    self.y += self.direction[1] * self.speed
    self.size -= 0.2  # Les particules rétrécissent plus lentement
    self.lifetime -= 1
    
  def draw(self, screen:'pygame.surface.Surface'):
    if self.lifetime < 8 * self.zoom:
      pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))