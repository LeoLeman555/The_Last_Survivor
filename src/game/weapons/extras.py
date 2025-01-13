import pygame
import random
from src.game.weapons.grenade import *
from src.data_handling.load import *
from src.game.animations.explosion import *


class Cible:
    def __init__(self, zoom: int, enemies, x: int, y: int, damage: int = 10):
        self.zoom = zoom
        self.enemies = enemies
        self.image = Load.charge_image(
            self, self.zoom, "weapon", "cible_drone", "png", 0.5
        )
        self.rect = self.image.get_rect()
        self.rect.x = x / self.zoom
        self.rect.y = y
        self.x = x / self.zoom
        self.y = y
        self.direction = 1
        self.speed = 4
        self.damage = damage
        self.visual = False

    def change_zoom(self, new_zoom: int):
        """Change the zoom and adjust target properties."""
        self.zoom = new_zoom
        self.image = Load.charge_image(
            self, self.zoom, "weapon", "cible_drone", "png", 0.5
        )
        self.rect = self.image.get_rect()
        self.x = 300 / self.zoom
        self.direction = 1
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """Update the position of the target."""
        self.x += self.direction * self.speed
        self.rect.x = self.x
        if (
            self.x <= 300 / self.zoom
            or self.x >= 550 + 150 * self.zoom - self.image.get_width()
        ):
            self.direction *= -1  # Invert direction

        if self.visual:
            self.check_collision()

    def draw(self, screen: pygame.Surface):
        """Draw the target on the screen."""
        if not 460 - 40 * (self.zoom - 1) <= self.x <= 500 + 15 * self.zoom:
            screen.blit(self.image, (self.x, self.y))
            self.visual = True
        else:
            self.visual = False

    def check_collision(self):
        """Checks for collisions with enemies."""
        hit_enemy = pygame.sprite.spritecollideany(self, self.enemies)
        if hit_enemy:
            hit_enemy.damage(self.damage)


class Drone:
    def __init__(self, zoom: int, screen: pygame.Surface, enemies, data):
        self.zoom = zoom
        self.screen = screen
        self.enemies = enemies
        self.data = data
        self.image = Load.charge_image(self, self.zoom, "weapon", "drone", "png", 0.4)
        self.x_cible = 0
        self.cible = Cible(self.zoom, self.enemies, 300, 315, self.data["damage"])

    def change_zoom(self, new_zoom: int):
        """Change the zoom and adjust drone properties."""
        self.zoom = new_zoom
        self.image = Load.charge_image(self, self.zoom, "weapon", "drone", "png", 0.4)
        self.cible.change_zoom(self.zoom)

    def update(self):
        """Update the drone's position and draw it on the screen."""
        self.cible.update()

    def draw(self, screen):
        screen.blit(
            self.image, ((478 - 21 * (self.zoom - 1)), (260 - 30 * (self.zoom - 1)))
        )
        self.cible.draw(screen)


class Laser(pygame.sprite.Sprite):
    def __init__(self, zoom: int, enemies, data):
        super().__init__()
        self.zoom = zoom
        self.enemies = enemies
        self.data = data
        self.damage = self.data["damage"]
        self.x = random.choice([random.randint(100, 400), random.randint(600, 900)])
        self.start_y = 0
        self.end_y = random.randint(100, 550)
        self.lifetime = self.data["lifetime"]
        self.rect = pygame.Rect(
            self.x - 25 * self.zoom,
            self.end_y - 25 * self.zoom,
            50 * self.zoom,
            50 * self.zoom,
        )

    def change_zoom(self, new_zoom: int):
        """Change the zoom and adjust laser properties."""
        self.zoom = new_zoom
        self.rect = pygame.Rect(
            self.x - 25 * self.zoom,
            self.end_y - 25 * self.zoom,
            50 * self.zoom,
            50 * self.zoom,
        )

    def draw(self, screen: pygame.Surface):
        """Draw the laser on the screen."""
        pygame.draw.line(
            screen,
            (255, 100, 100),
            (self.x, self.start_y),
            (self.x, self.end_y),
            int(5 * self.zoom),
        )
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (self.x, self.start_y),
            (self.x, self.end_y),
            int(2.5 * self.zoom),
        )
        pygame.draw.circle(
            screen, (255, 0, 0), (self.x, self.end_y), int(5 * self.zoom)
        )
        pygame.draw.circle(
            screen, (255, 100, 100), (self.x, self.end_y), int(2.5 * self.zoom)
        )

    def update(self):
        """Update the laser's lifetime."""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        self.check_collision()

    def check_collision(self):
        """Checks for collisions with enemies."""
        hit_enemy = pygame.sprite.spritecollideany(self, self.enemies)
        if hit_enemy:
            hit_enemy.damage(self.damage)


class Missile(pygame.sprite.Sprite):
    def __init__(self, zoom: int, player, enemies, data):
        super().__init__()
        self.zoom = zoom
        self.player = player
        self.enemies = enemies
        self.data = data
        self.damage = self.data["damage"]
        self.cible_missile = Load.charge_image(
            self, self.zoom, "weapon", "cible_missile", "png", 0.5
        )
        self.x = random.randint(300, 700)
        self.y = random.randint(200, 400)
        self.rect = self.cible_missile.get_rect()
        self.lifetime = 50

    def change_zoom(self, new_zoom: int):
        """Change the zoom and adjust missile properties."""
        self.zoom = new_zoom
        self.cible_missile = Load.charge_image(
            self, self.zoom, "weapon", "cible_missile", "png", 0.5
        )
        self.rect = self.cible_missile.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen: pygame.Surface):
        """Draw the missile on the screen."""
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

        if self.lifetime <= 0:
            explosion = Explosion(
                self.zoom, self.rect.center, self.damage, self.enemies
            )
            self.player.screen.blit(explosion.image, explosion.rect)
            self.player.explosions.add(explosion)
            self.kill()
