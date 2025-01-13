import pygame
import random
from src.data_handling.load import *


class GunGround(pygame.sprite.Sprite):
    def __init__(
        self,
        zoom: int,
        name: str,
        id: int,
        player,
        x: int,
        y: int,
        range_obj: int,
        speed_obj: int = 4,
    ):
        """Initialize a dropped weapon on the ground."""
        super().__init__()
        self.zoom = zoom
        self.name = name
        self.id = id
        self.player = player
        for weapon in self.player.run.data_weapons.values():
            if weapon["name"] == self.name:
                self.level = weapon["level"]
        self.image = Load.charge_image(
            self, self.zoom, f"weapon/{self.name}", f"level_{self.level}", "png", 0.45
        )
        self.x = x + random.randint(round(-10 * self.zoom), round(10 * self.zoom))
        self.y = y + random.randint(round(-10 * self.zoom), round(10 * self.zoom))

        self.range_obj = range_obj
        self.speed_obj = speed_obj
        self.range = self.range_obj * self.zoom
        self.speed = self.speed_obj * self.zoom
        self.rect = self.image.get_rect()
        self.lifetime = 200

    def change_zoom(self, new_zoom: int) -> None:
        """Update zoom level and recalculate attributes."""
        self.zoom = new_zoom
        for weapon in self.player.run.data_weapons.values():
            if weapon["name"] == self.name:
                self.level = weapon["level"]
        self.image = Load.charge_image(
            self, self.zoom, f"weapon/{self.name}", f"level_{self.level}", "png", 0.45
        )
        self.rect = self.image.get_rect()
        self.range = self.range_obj * self.zoom
        self.speed = self.speed * self.zoom

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the weapon on the screen."""
        screen.blit(self.image, (self.x, self.y))

    def update(self, x_var: int, y_var: int, player_rect: "pygame.Rect") -> None:
        """Update position, proximity checks, and lifetime."""
        self.lifetime -= 1
        self.x += (x_var / 2) * self.zoom
        self.y += (y_var / 2) * self.zoom
        self.rect.x = self.x
        self.rect.y = self.y

        # Check proximity to player
        player_center = player_rect.center
        obj_center = self.rect.center
        distance = (
            (player_center[0] - obj_center[0]) ** 2
            + (player_center[1] - obj_center[1]) ** 2
        ) ** 0.5

        if distance <= self.range:
            if distance != 0:
                move_x = (
                    (player_center[0] - obj_center[0])
                    / distance
                    * min(self.speed, distance)
                )
                move_y = (
                    (player_center[1] - obj_center[1])
                    / distance
                    * min(self.speed, distance)
                )
                self.x += move_x
                self.y += move_y
                self.rect.x = int(self.x)
                self.rect.y = int(self.y)

        self.check_collision(player_rect)
        if self.lifetime <= 0:
            self.kill()

    def check_collision(self, player_rect: "pygame.Rect") -> None:
        """Check for collision with the player."""
        if self.rect.colliderect(player_rect):
            self.player.run.manager.new_weapon(self.name)
            self.kill()
