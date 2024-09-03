import pygame
import math
import random
import time
from load import *

PALETTE = [
    (34, 139, 34), # Forest green
    (0, 100, 0), # Dark green
    (50, 205, 50), # Lime green
    (0, 255, 0), # Light green
    (0, 128, 0) # Medium green
]
class Grenade(pygame.sprite.Sprite):
  def __init__(self, zoom: int, screen: pygame.Surface, enemies, player, data: dict, speed: int):
    super().__init__()
    self.zoom = zoom
    self.data = data
    self.screen = screen
    self.enemies = enemies
    self.player = player
    self.type = self.data["type"]
    if self.type == "toxic":
      self.name = "toxic_grenade"
      self.toxic = {
        "toxic": True,
        "explode": False,
        "number": 0,
      }
    else:
      self.name = "grenade"
      self.toxic = {
        "toxic": False,
      }
    print(self.toxic["toxic"])

    self.image = Load.charge_image(self, self.zoom, "weapon", self.name, "png", 0.5)
    self.rect = self.image.get_rect()
    # Initial position of the grenade based on the player
    self.rect.centerx = player.rect.centerx - (player.rect.x - 500)
    self.rect.centery = player.rect.centery - (player.rect.y - 300)
    self.speed = speed* self.zoom
    self.gravity = 0.4
    self.velocity_y = -5 * self.zoom
    self.bounce_factor = 0.8
    self.rebound_height = self.screen.get_height() // 2
    self.lifetime = self.data["lifetime"] * self.zoom
    self.damage = self.data["damage"]

  def change_zoom(self, new_zoom: int):
    """Change le zoom et ajuste les propriétés de la grenade."""
    self.zoom = new_zoom
    self.image = Load.charge_image(self, self.zoom, "weapon", self.name, "png", 0.5)
    self.rect = self.image.get_rect(center=self.rect.center)
    self.speed = self.speed / self.zoom  # Ajustement de la vitesse en fonction du zoom
    self.velocity_y = -5 * self.zoom
    self.rebound_height = self.screen.get_height() // 2
    self.lifetime = self.data["lifetime"] * self.zoom

  def explode(self):
    """Trigger an explosion."""
    explosion = Explosion(self.zoom, self.rect.center, self.damage, self.enemies)
    self.player.screen.blit(explosion.image, explosion.rect)
    self.player.explosions.add(explosion)

  def explode_toxic(self):
    self.toxic["number"] += 1
    for _ in range(15):
      self.player.toxic_particles.add(ToxicParticle(self.zoom, self.rect.centerx, self.rect.centery, self.enemies, self.damage/200))

    if self.toxic["number"] >= 100:
      self.kill()

  def update(self, x_var: int, y_var: int):
    """Update the position of the grenade."""
    x = (x_var / 2) * self.zoom
    y = (y_var / 2) * self.zoom
    self.rect.x +=  x
    self.rebound_height += y
    self.rect.y += y

    if self.lifetime <= 0:
      if self.toxic["toxic"]:
        self.explode_toxic()
        return
      else:
        self.explode()
        self.kill()

    self.rect.x += self.speed
    self.velocity_y += self.gravity
    self.rect.y += self.velocity_y

    if self.rect.bottom >= self.rebound_height:
      self.rect.bottom = self.rebound_height
      self.velocity_y = -self.velocity_y * self.bounce_factor
      if abs(self.velocity_y) < 1:
        self.velocity_y = 0

    self.lifetime -= 1

class ToxicParticle(pygame.sprite.Sprite):
  def __init__(self, zoom: int, x: int, y: int, enemies, damage):
    super().__init__()
    self.zoom = zoom
    self.x = x
    self.y = y
    self.size_origin = random.randint(2, 4)
    self.size = round(self.size_origin * self.zoom)
    angle = random.uniform(0, 2 * math.pi)
    speed = random.uniform(1, round(2*self.zoom))
    self.speed_x = speed * math.cos(angle)
    self.speed_y = speed * math.sin(angle)
    self.color = random.choice(PALETTE)
    self.creation_time = time.time()
    self.life_duration_origin = 25
    self.life_duration = round(self.life_duration_origin*self.zoom)
    self.alpha = 255
    self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    self.enemies = enemies
    self.damage = damage

  def change_zoom(self, new_zoom: int):
    """Change le zoom et ajuste les propriétés des particules toxiques."""
    self.zoom = new_zoom
    self.size = round(self.size_origin * self.zoom)
    self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    self.life_duration = round(self.life_duration_origin*self.zoom)

  def update(self, x_var: int, y_var: int):
    x = (x_var / 2) * self.zoom
    y = (y_var / 2) * self.zoom
    self.x += self.speed_x + x
    self.y += self.speed_y + y
    self.speed_x *= 0.99
    self.speed_y *= 0.99

    self.rect.topleft = (self.x - self.size // 2, self.y - self.size // 2)
    self.rect.size = (self.size, self.size)
    
    elapsed_time = time.time() - self.creation_time
    if elapsed_time > self.life_duration:
      self.alpha = 0
    else:
      self.alpha = max(0, 255 - int((elapsed_time / self.life_duration) * 255))

    self.life_duration -= 1

    if self.life_duration <= 0:
      self.kill()

    self.check_collision()
    
  def check_collision(self):
    """Checks for collisions with enemies."""
    hit_enemy = pygame.sprite.spritecollideany(self, self.enemies)
    if hit_enemy:
      hit_enemy.damage(self.damage)

  def draw(self, screen):
    particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
    pygame.draw.circle(particle_surface, (*self.color, self.alpha), (self.size, self.size), self.size)
    screen.blit(particle_surface, (self.x - self.size, self.y - self.size))

class Explosion(pygame.sprite.Sprite):
  def __init__(self, zoom: int, center: tuple, damage: int, enemies):
    """Initialize an explosion at the given center point."""
    super().__init__()
    self.zoom = zoom * 2
    self.enemies = enemies
    self.images = self.get_images()
    self.image = self.images[0]
    self.rect = self.image.get_rect(center=center)
    self.index = 0
    self.clock = pygame.time.get_ticks()

    self.damage = damage

  def change_zoom(self, new_zoom: int):
    """Change le zoom et ajuste les propriétés de l'explosion."""
    self.zoom = new_zoom * 2
    self.images = self.get_images()  # Recharger les images en fonction du nouveau zoom
    self.image = self.images[0]
    self.rect = self.image.get_rect(center=self.rect.center)

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
    self.check_collision()
    now = pygame.time.get_ticks()
    if now - self.clock > 1:  # Change frame every 1ms
      self.index += 6
      if self.index < len(self.images):
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=self.rect.center)
        self.clock = now
      else:
        self.kill()

  def check_collision(self):
    """Checks for collisions with enemies."""
    hit_enemy = pygame.sprite.spritecollideany(self, self.enemies)
    if hit_enemy:
      hit_enemy.damage(self.damage)