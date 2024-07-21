import pygame
import random
from load import Load

class Grenade(pygame.sprite.Sprite):
  def __init__(self, zoom: int, screen: pygame.Surface, player, speed: int):
    super().__init__()
    self.zoom = zoom
    self.screen = screen
    self.player = player
    self.image = Load.charge_image(self, self.zoom, "weapon", "ammo5", "png", 0.5)
    self.rect = self.image.get_rect()
    # Initial position of the grenade based on the player
    self.rect.centerx = player.rect.centerx - (player.rect.x - 500)
    self.rect.centery = player.rect.centery - (player.rect.y - 300)
    self.speed = speed * self.zoom
    self.gravity = 0.5
    self.velocity_y = -5 * self.zoom
    self.bounce_factor = 0.8
    self.rebound_height = self.screen.get_height() // 2
    self.lifetime = 25 * self.zoom

  def explode(self):
    """Trigger an explosion."""
    explosion = Explosion(self.zoom, self.rect.center)
    self.player.screen.blit(explosion.image, explosion.rect)
    self.player.explosions.add(explosion)

  def update(self, x: int = 0, y: int = 0):
    """Update the position of the grenade."""
    self.rect.x += self.speed + x
    self.velocity_y += self.gravity
    self.rect.y += self.velocity_y + y
    self.rebound_height += y

    if self.rect.bottom >= self.rebound_height:
      self.rect.bottom = self.rebound_height
      self.velocity_y = -self.velocity_y * self.bounce_factor
      if abs(self.velocity_y) < 1:
        self.velocity_y = 0

    self.lifetime -= 1
    
    if self.lifetime <= 0:
      self.explode()
      self.kill()

class Explosion(pygame.sprite.Sprite):
  def __init__(self, zoom: int, center: tuple):
    """Initialize an explosion at the given center point."""
    super().__init__()
    self.zoom = zoom
    self.images = self.get_images()
    self.image = self.images[0]
    self.rect = self.image.get_rect(center=center)
    self.index = 0
    self.clock = pygame.time.get_ticks()

  def get_images(self):
    """Load explosion images from a sprite sheet."""
    images_explosion = []
    sprite_sheet_explosion = Load.charge_image(self, self.zoom, "weapon", "explosion", "png", 0.5)
    sprite_width = int(34.5 * self.zoom)
    sprite_height = int(34.7 * self.zoom)
    for y in range(0, sprite_sheet_explosion.get_height(), sprite_height):
      for x in range(0, sprite_sheet_explosion.get_width(), sprite_width):
        img = self.get_image(sprite_sheet_explosion, x, y, sprite_width, sprite_height)
        images_explosion.append(img)
    return images_explosion

  def get_image(self, sprite_sheet: pygame.Surface, x: int, y: int, width: int, height: int):
    """Extract a single image from the sprite sheet."""
    image = pygame.Surface([width, height], pygame.SRCALPHA)
    image.blit(sprite_sheet, (0, 0), (x, y, width, height))
    return image

  def update(self):
    """Update the explosion animation."""
    now = pygame.time.get_ticks()
    if now - self.clock > 1:  # Change frame every 1ms
      self.index += 6
      if self.index < len(self.images):
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=self.rect.center)
        self.clock = now
      else:
        self.kill()

class Cible:
  def __init__(self, zoom: int, x: int, y: int):
    self.zoom = zoom
    self.image = Load.charge_image(self, self.zoom, "weapon", "cible_drone", "png", 0.5)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.x = x
    self.y = y
    self.direction = 1
    self.speed = 4
    
  def update(self):
    """Update the position of the target."""
    self.x += self.direction * self.speed
    self.rect.x = self.x
    if self.x <= 300 / self.zoom or self.x >= 550 + 150 * self.zoom - self.image.get_width():
      self.direction *= -1  # Invert direction
    
  def draw(self, screen: pygame.Surface):
    """Draw the target on the screen."""
    # pygame.draw.rect(screen, (0, 0, 0), self.rect)
    if not 460 - 40 * (self.zoom - 1) <= self.x <= 500 + 15 * self.zoom:
      screen.blit(self.image, (self.x, self.y))

class Drone:
  def __init__(self, zoom: int, screen: pygame.Surface):
    self.zoom = zoom
    self.screen = screen
    self.image = Load.charge_image(self, self.zoom, "weapon", "drone", "png", 0.4)
    self.x_cible = 0
    self.cible = Cible(self.zoom, 300 / self.zoom, 315)
    
  def update_drone(self):
    """Update the drone's position and draw it on the screen."""
    self.screen.blit(self.image, ((478 - 21 * (self.zoom - 1)), (260 - 30 * (self.zoom - 1))))
    self.cible.update()
    self.cible.draw(self.screen)

class Laser:
  def __init__(self, zoom: int):
    self.zoom = zoom
    self.x = random.choice([random.randint(100, 400), random.randint(600, 900)])
    self.start_y = 0
    self.end_y = random.randint(100, 550)
    self.lifetime = 50
    self.rect = pygame.Rect(self.x - 25 * self.zoom, self.end_y - 25 * self.zoom , 50 * self.zoom, 50 * self.zoom)

  def draw(self, screen: pygame.Surface):
    """Draw the laser on the screen."""
    # pygame.draw.rect(screen, (0, 0, 0), self.rect)
    pygame.draw.line(screen, (255, 100, 100), (self.x, self.start_y), (self.x, self.end_y), int(5 * self.zoom))
    pygame.draw.line(screen, (255, 0, 0), (self.x, self.start_y), (self.x, self.end_y), int(2.5 * self.zoom))
    pygame.draw.circle(screen, (255, 0, 0), (self.x, self.end_y), int(5 * self.zoom))
    pygame.draw.circle(screen, (255, 100, 100), (self.x, self.end_y), int(2.5 * self.zoom))

  def update(self):
    """Update the laser's lifetime."""
    self.lifetime -= 1

class Missile:
  def __init__(self, zoom: int):
    self.zoom = zoom
    self.cible_missile = Load.charge_image(self, self.zoom, "weapon", "cible_missile", "png", 0.5)
    self.x = random.randint(300, 700)
    self.y = random.randint(200, 400)
    self.rect = self.cible_missile.get_rect()
    self.lifetime = 50
  
  def draw(self, screen: pygame.Surface):
    """Draw the missile on the screen."""
    # pygame.draw.rect(screen, (0, 0, 0), self.rect)
    if self.lifetime % 2 == 0 or self.lifetime >= 40:
      screen.blit(self.cible_missile, (self.x, self.y))

  def update(self, x_var: int, y_var: int):
    """Update the missile's position and lifetime."""
    self.lifetime -= 1
    x = (x_var / 2) * self.zoom
    y = (y_var / 2) * self.zoom
    self.x += x
    self.y += y
    self.rect.x = self.x
    self.rect.y = self.y

  def get_rectangle(self):
    """Return the missile's rectangle."""
    return self.rect
