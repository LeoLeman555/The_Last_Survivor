import pygame
import math
import random
from extras import Explosion
from load import Load
import player

class Weapon(pygame.sprite.Sprite):
  def __init__(self, zoom: int, player: 'player.Player', name: str, size: tuple, position: list):
    super().__init__()
    self.zoom = zoom
    self.player = player
    self.name = name
    self.size = size
    self.image = Load.charge_image(self, self.zoom / 2, "weapon", self.name, "png", 0.85)
    self.rect = self.image.get_rect()
    self.position = position
    self.rect.center = self.position
    self.original_image = self.image
    self.angle = 0

  def draw(self, screen: 'pygame.surface.Surface'):
    """Draws the weapon on the screen."""
    screen.blit(self.image, self.rect)

  def rotate_to_cursor(self, cursor_pos: tuple):
    """Rotates the weapon to point towards the mouse cursor."""
    dx, dy = cursor_pos[0] - self.rect.centerx, cursor_pos[1] - self.rect.centery
    self.angle = math.degrees(math.atan2(dy, dx))

    # Flip image if needed
    if 90 < self.angle < 270 or -270 < self.angle < -90:
      self.image = pygame.transform.flip(self.original_image, False, True)
    else:
      self.image = self.original_image

    # Rotate the image
    self.image = pygame.transform.rotozoom(self.image, -self.angle, 1)
    self.rect = self.image.get_rect(center=self.rect.center)


class Bullet(pygame.sprite.Sprite):
  def __init__(self, zoom: int, screen: 'pygame.surface.Surface', player: 'player.Player', enemies, goal: tuple,
              name: str, distance_weapon: int, position: list, range: int = 500, explosive: bool = False, speed: int = 15, damage: int = 100):
    super().__init__()
    self.zoom = zoom
    self.speed = speed * self.zoom
    self.player = player
    self.enemies = enemies
    self.damage = damage
    self.name = name
    self.range = range * self.zoom
    self.distance_weapon = distance_weapon * self.zoom
    self.distance_traveled = 0
    self.image = Load.charge_image(self, self.zoom / 2, "weapon", self.name, "png", 1)
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
    self.vector = (self.speed * dx / distance, self.speed * dy / distance)

    self.origin_image = self.image
    self.angle = 0

  def rotate(self):
    """Rotates the bullet image based on its direction vector."""
    self.angle = math.atan2(-self.vector[1], self.vector[0]) * 180 / math.pi
    self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
    self.rect = self.image.get_rect(center=self.rect.center)

  def delete(self):
    """Removes the bullet from the player's bullets list."""
    self.player.bullets.remove(self)

  def move(self):
    """Moves the bullet and handles collisions."""
    self.rotate()
    self.rect.x += self.vector[0]
    self.rect.y += self.vector[1]
    self.distance_traveled += self.speed

    if self.distance_traveled > self.range:
      self.delete()
      self.explode()
    else:
      self.check_collision()

    if self.distance_traveled > self.distance_weapon:
      self.screen.blit(self.image, self.rect)

  def check_collision(self):
    """Checks for collisions with enemies."""
    hit_enemy = pygame.sprite.spritecollideany(self, self.enemies)
    if hit_enemy:
      self.delete()
      hit_enemy.damage(self.damage)
      self.explode()

  def explode(self):
    """Triggers an explosion if the bullet is explosive."""
    if self.explosive:
      explosion = Explosion(self.zoom, self.rect.center)
      self.player.screen.blit(explosion.image, explosion.rect)
      self.player.explosions.add(explosion)

  def get_rectangle(self):
    """Returns the bullet's rectangle."""
    return self.rect


class FireParticle:
  def __init__(self, zoom: int, x: int, y: int, direction: tuple):
    self.zoom = zoom
    self.x = x
    self.y = y
    self.size = random.randint(3 * self.zoom, 5 * self.zoom)
    self.color = (random.randint(200, 255), random.randint(100, 150), 0)
    self.lifetime = random.randint(10 * self.zoom, 12 * self.zoom)
    self.direction = (direction[0] + random.uniform(-0.1, 0.1), direction[1] + random.uniform(-0.1, 0.1))
    self.speed = random.uniform(6 * self.zoom, 8 * self.zoom)

  def update(self):
    """Updates the particle's position and properties."""
    self.x += self.direction[0] * self.speed
    self.y += self.direction[1] * self.speed
    self.size -= 0.2
    self.lifetime -= 1

  def draw(self, screen: 'pygame.surface.Surface'):
    """Draws the particle on the screen."""
    if self.lifetime > 0:
      pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
