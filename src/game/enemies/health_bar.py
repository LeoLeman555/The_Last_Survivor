import pygame


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, zoom: int, x: int, y: int, width: int, max_health: int):
        """Initialize the health bar with position, size, and max health."""
        super().__init__()
        self.zoom = zoom
        self.x = x
        self.y = y
        self.width = width
        self.width_zoom = self.width
        self.height = self.zoom
        self.max_health = max_health
        self.health = max_health
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y - 10)
        self.update(self.health)  # Initialize the visual representation of health.

    def change_zoom(self, new_zoom: float):
        """Update the zoom level and resize the health bar."""
        self.zoom = new_zoom
        if self.width != self.width_zoom:  # Ensure original width is preserved.
            self.width = self.width_zoom
        self.width = round(self.width * self.zoom / 2)  # Adjust width for zoom level.
        self.height = round(self.zoom)
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y - 10)
        self.update(self.health)  # Refresh the health bar display.

    def update(self, health: int):
        """Update the health bar display based on current health."""
        self.health = health
        health_ratio = self.health / self.max_health
        self.image.fill((255, 0, 0))  # Background color: red.
        pygame.draw.rect(
            self.image, (0, 255, 0), (0, 0, self.width * health_ratio, self.height)
        )  # Green bar.
