import pygame
import math
from src.data_handling.load import *
from src.game.weapons.grenade import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, zoom: int, player, weapon_dict: dict):
        super().__init__()
        self.zoom = zoom
        self.player = player
        self.current_weapon_dict_origin = weapon_dict
        self.current_weapon_dict = self.current_weapon_dict_origin
        self.level = self.current_weapon_dict["level"]
        self.image = Load.charge_image(
            self,
            self.zoom / 2,
            f"weapon/{self.current_weapon_dict["name"]}",
            f"level_{self.level}",
            "png",
            0.85,
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.current_weapon_dict["position"]
        self.original_image = self.image
        self.angle = 0

    def change_zoom(self, new_zoom: int):
        self.zoom = new_zoom
        self.current_weapon_dict["position"][0] = 500 + (10 * self.zoom)
        self.current_weapon_dict["position"][1] = 300 + (5 * self.zoom)
        self.image = Load.charge_image(
            self,
            self.zoom / 2,
            f"weapon/{self.current_weapon_dict["name"]}",
            f"level_{self.level}",
            "png",
            0.85,
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.current_weapon_dict["position"]
        self.original_image = self.image

    def draw(self, screen: "pygame.surface.Surface"):
        """Draws the weapon on the screen."""
        screen.blit(self.image, self.rect)

    def rotate_to_cursor(self, cursor_pos: tuple):
        """Rotates the weapon to point towards the mouse cursor or flips it if the id is 9."""
        dx, dy = cursor_pos[0] - self.rect.centerx, cursor_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))

        if 90 < self.angle < 270 or -270 < self.angle < -90:
            self.image = pygame.transform.flip(self.original_image, False, True)
        else:
            self.image = self.original_image

        self.image = pygame.transform.rotozoom(self.image, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def change_weapon(self, zoom: int, player, current_weapon_dict: dict):
        self.zoom = zoom
        self.player = player
        self.current_weapon_dict = current_weapon_dict
        self.level = self.current_weapon_dict["level"]
        self.image = Load.charge_image(
            self,
            self.zoom / 2,
            f"weapon/{self.current_weapon_dict["name"]}",
            f"level_{self.level}",
            "png",
            0.85,
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.current_weapon_dict["position"]
        self.original_image = self.image
        self.angle = 0
