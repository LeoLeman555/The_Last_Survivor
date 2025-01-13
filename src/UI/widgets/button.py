import pygame


class Button:
    def __init__(self, name: str, position: tuple[int, int]):
        """Initialize the button with position and resources."""
        self.name = name
        self.image = pygame.image.load(f"res/widgets/{name}.png").convert_alpha()
        self.click_image = pygame.image.load(
            f"res/widgets/{name}_click.png"
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.original_pos = self.rect.topleft
        self.is_clicked = False

    def draw(self, screen: pygame.Surface, mouse_pos: tuple[int, int]) -> None:
        """Draw the button on the screen based on mouse position."""
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.click_image, (self.rect.x + 1, self.rect.y + 1))
        else:
            screen.blit(self.image, self.rect)

    def is_pressed(self, mouse_pos: tuple[int, int], press_mouse: bool) -> bool:
        """Check if the button is pressed."""
        return self.rect.collidepoint(mouse_pos) and press_mouse
