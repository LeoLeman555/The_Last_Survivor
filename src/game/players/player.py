import pygame
import math
from src.data_handling.load import *
from src.game.weapons.weapon import *
from src.game.weapons.extras import *
from src.game.weapons.grenade import *
from src.game.weapons.bullet import *
from src.game.weapons.fire_particle import *
from src.game.maps.gun_ground import *
from src.game.enemies.enemy import *
from src.game.maps.ground_objects import *
from src.UI.widgets.message import *


class Player(pygame.sprite.Sprite):
    """Represents the player with movement, animations, and interactions."""

    def __init__(self, run, name: str = "jim", x: int = 0, y: int = 0):
        super().__init__()
        self.run = run
        self.screen = run.screen
        self.icon = run.icon
        self.sprite_sheet = Load.charge_image(self, 1, "sprite", name, "png")
        self.animation_index = 0
        self.clock = 0
        self.images = {"right": self.get_images(0), "left": self.get_images(38)}
        self.image = self.get_image(0, 0)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        # Collision rect
        self.rect_collision = self.rect.copy()
        self.rect_collision.width = 17 * self.run.zoom
        self.rect_collision.height = 38 * self.run.zoom
        self.rect_collision.x = 500 - 8.5 * self.run.zoom
        self.rect_collision.y = 300 - 19 * self.run.zoom

        # Player attributes
        self.position = [x, y]
        self.old_position = self.position.copy()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.4, 10)
        self.attack = 10
        self.speed = 0
        self.number_enemies = 0

        # Groups for gameplay elements
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.grenades = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.messages = pygame.sprite.Group()
        self.toxic_particles = pygame.sprite.Group()

    def change_zoom(self):
        """Recalculate attributes based on zoom level."""
        self.rect_collision.width = 17 * self.run.zoom
        self.rect_collision.height = 38 * self.run.zoom
        self.rect_collision.x = 500 - 8.5 * self.run.zoom
        self.rect_collision.y = 300 - 19 * self.run.zoom

    def change_animation(self, name: str, speed: int):
        """Change player animation based on movement direction."""
        self.speed = speed
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey((0, 0, 0))
        self.clock += self.speed * 10
        if self.clock >= 100:
            self.animation_index = (self.animation_index + 1) % len(self.images[name])
            self.clock = 0

    def get_images(self, y: int):
        """Extract frames from the sprite sheet."""
        return [self.get_image(i * 17, y) for i in range(8)]

    def get_image(self, x: int, y: int):
        """Get a single image from the sprite sheet."""
        image = pygame.Surface([17, 38], pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, 17, 38))
        return image

    def save_location(self):
        """Save the current position for potential rollback."""
        self.old_position = self.position.copy()

    def move_right(self, diagonal: int, speed: int):
        """Move the player to the right."""
        self.change_animation("right", speed)
        self.position[0] += self.speed / diagonal

    def move_left(self, diagonal: int, speed: int):
        """Move the player to the left."""
        self.change_animation("left", speed)
        self.position[0] -= self.speed / diagonal

    def move_up(self, diagonal: int, speed: int):
        """Move the player upwards."""
        if diagonal == 1:
            self.change_animation("right", speed)
        self.position[1] -= self.speed / diagonal

    def move_down(self, diagonal: int, speed: int):
        """Move the player downwards."""
        if diagonal == 1:
            self.change_animation("left", speed)
        self.position[1] += self.speed / diagonal

    def update(self):
        """Update player state, including health and position."""
        # Check health and food levels
        if self.run.icon.resource["health"] <= 0 or self.run.icon.resource["food"] <= 0:
            self.run.life -= 1
            if self.run.life > 0:
                for enemy in self.enemies:
                    enemy.delete()
                self.run.icon.resource["health"] = 100
                self.run.icon.resource["food"] = 100
        if self.run.life == 0:
            self.die()

        # Update position and health regeneration
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.run.icon.resource["food"] -= 0.04 / self.run.hunger_resistance
        if not hasattr(self, "last_regeneration_time"):
            self.last_regeneration_time = pygame.time.get_ticks()
        if (
            pygame.time.get_ticks() - self.last_regeneration_time >= 1000
            and self.run.icon.resource["health"] < 100
        ):
            self.run.icon.resource["health"] += self.run.regeneration
            self.last_regeneration_time = pygame.time.get_ticks()

    def move_back(self):
        """Rollback player to previous position."""
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def launch_bullet(self, goal: tuple, weapon_dict: dict, delay: int = 0):
        """Fire a bullet."""
        self.bullets.add(
            Bullet(
                self.run.zoom,
                self.run.screen,
                self,
                self.enemies,
                goal,
                weapon_dict,
                delay,
                self.run.piercing,
            )
        )

    def add_fire(self, weapon_dict: dict):
        """Add fire particles."""
        x, y = 500 + 10 * self.run.zoom, 300 + 5 * self.run.zoom
        dx, dy = pygame.mouse.get_pos()[0] - 500, pygame.mouse.get_pos()[1] - 300
        distance = math.hypot(dx, dy)
        direction = (dx / distance, dy / distance)
        damage = weapon_dict["damage"] / 60
        for _ in range(10):
            self.particles.add(
                FireParticle(self.run.zoom, self.enemies, x, y, direction, damage)
            )

    def launch_grenade(self, speed: int, grenade_dict: dict):
        """Throw a grenade."""
        self.grenades.add(
            Grenade(
                self.run.zoom, self.run.screen, self.enemies, self, grenade_dict, speed
            )
        )

    def add_enemy(self, data: dict, name: str, x: int = 0, y: int = 0):
        """Spawn a new enemy."""
        if name.lower() in data:
            self.enemies.add(
                Enemy(
                    self.run.zoom,
                    self.run.screen,
                    name,
                    self,
                    self.run.icon,
                    x,
                    y,
                    data,
                )
            )

    def add_laser(self):
        """Add a laser attack."""
        self.lasers.add(
            Laser(self.run.zoom, self.enemies, self.run.data_extras["laser_probe"])
        )

    def add_missile(self):
        """Add a missile attack."""
        self.missiles.add(
            Missile(self.run.zoom, self, self.enemies, self.run.data_extras["missile"])
        )

    def add_object(self, name: str, value: int, x: int, y: int):
        """Add a new object to the world."""
        self.objects.add(
            GroundObjects(
                self.run.zoom, self.run.icon, name, value, x, y, self.run.range_obj
            )
        )

    def add_weapon(self, name: str, id: int, x: int, y: int):
        """Add a weapon to the world."""
        self.objects.add(
            GunGround(self.run.zoom, name, id, self, x, y, self.run.range_obj)
        )

    def add_message(
        self,
        text: str,
        start_position: tuple,
        end_position: tuple,
        color: tuple,
        font_size: int,
        duration: int,
    ):
        """Display a message on the screen."""
        self.messages.add(
            Message(
                self.run.zoom,
                text,
                start_position,
                end_position,
                color,
                font_size,
                duration,
            )
        )

    def die(self):
        """Handle player death."""
        self.run.running = False
