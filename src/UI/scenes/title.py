import pygame
import time


class TitleScreen:
    def __init__(self, screen):
        """Initialization with screen sharing."""
        self.screen = screen

        # Font settings
        self.base_font_size = 100  # Initial size for separate words
        self.impact_font_size = 150  # Size during impact
        self.impact_color = (38, 255, 186)  # Impact color
        self.bg_color = (0, 0, 0)  # Background color

        self.words = ["THE", "LAST", "SURVIVOR"]  # The three words to display

    def draw_text(self, text, font_size, position, color):
        """Draw text centered at the given position."""
        font = pygame.font.Font("res/fonts/futurist_font.ttf", font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)

    def hammer_effect(self, word, position):
        """Hammer effect: quick appearance with a strong impact."""
        # Quick impact (large and green)
        self.screen.fill(self.bg_color)
        self.draw_text(word, self.impact_font_size, position, self.impact_color)
        pygame.display.flip()
        time.sleep(0.1)  # Pause for the effect

        # Reduce to normal size
        self.screen.fill(self.bg_color)
        self.draw_text(word, self.base_font_size, position, (255, 255, 255))
        pygame.display.flip()
        time.sleep(0.6)  # Pause to stay displayed

        # Disappear
        self.screen.fill(self.bg_color)
        pygame.display.flip()
        time.sleep(0.2)

    def display_title(self):
        """Display words sequentially with hammer effect."""
        center_position = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        for word in self.words[:-1]:
            self.hammer_effect(word, center_position)

        self.hammer_effect(self.words[-1], center_position)

    def run(self):
        """Main loop to run the animation."""
        self.display_title()
