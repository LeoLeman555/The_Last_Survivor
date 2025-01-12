import pygame
from src.data_handling.load import *
from src.game.animations.explosion import *
from src.game.weapons.toxic_particle import *

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

    self.image = Load.charge_image(self, self.zoom, "weapon", self.name, "png", 0.5)
    self.rect = self.image.get_rect()
    # Initial position of the grenade based on the player
    self.rect.centerx = player.rect.centerx - (player.rect.x - 500)
    self.rect.centery = player.rect.centery - (player.rect.y - 300)
    self.speed = speed * self.zoom
    self.gravity = 0.4
    self.velocity_y = -5 * self.zoom
    self.bounce_factor = 0.8
    self.rebound_height = self.screen.get_height() // 2
    self.lifetime = self.data["lifetime"] * self.zoom
    self.damage = self.data["damage"]

  def change_zoom(self, new_zoom: int):
    """Adjust zoom level."""
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
    """Toxic explosion."""
    self.toxic["number"] += 1
    for _ in range(15):
      self.player.toxic_particles.add(ToxicParticle(self.zoom, self.rect.centerx, self.rect.centery, self.enemies, self.damage/200))

    if self.toxic["number"] >= 100:
      self.kill()

  def update(self, x_var: int, y_var: int):
    """Update the position of the grenade."""
    x = (x_var / 2) * self.zoom
    y = (y_var / 2) * self.zoom
    self.rect.x += x
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