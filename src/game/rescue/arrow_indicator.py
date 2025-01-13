import pygame
import math
from src.data_handling.load import *


class ArrowIndicator:
    """Shows an arrow pointing to the rescue ship."""

    def __init__(self, run, rescue_ship):
        self.run = run
        self.rescue_ship = rescue_ship
        self.original_arrow_image = Load.charge_image(
            self, 1, "rescue", "arrow_ship", "png", 1
        )
        self.arrow_image = self.original_arrow_image
        self.arrow_rect = self.arrow_image.get_rect()
        self.arrow_rect.center = 500, 50

    def update(self) -> None:
        """Updates the arrow's angle to point at the rescue ship."""
        delta_x = self.rescue_ship.rect.centerx - self.arrow_rect.centerx
        delta_y = self.rescue_ship.rect.centery - self.arrow_rect.centery
        angle = math.atan2(delta_y, delta_x)
        self.arrow_image = pygame.transform.rotate(
            self.original_arrow_image, -math.degrees(angle) + 90
        )

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the arrow on the screen."""
        if self.rescue_ship.rescue or self.rescue_ship.move:
            screen.blit(self.arrow_image, self.arrow_rect)
