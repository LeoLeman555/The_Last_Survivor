import pygame
from src.data_handling.load import *
from src.data_handling.read_data import *


class Introduction:
    def __init__(self, screen: pygame.Surface):
        """Initialize the introduction screen with fonts and data."""
        pygame.font.init()

        self.screen = screen
        pygame.display.set_caption("The Last Survivor - Introduction")
        pygame.display.set_icon(pygame.image.load("res/menu/logo.jpg"))

        self.font = pygame.font.Font("res/texte/dialog_font.ttf", 18)
        self.title_font = pygame.font.Font("res/texte/dialog_font.ttf", 25)  # Bold font

        self.read_data = ReadData()
        self.load = Load()
        self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
        self.tutorial = self.read_data.read_params("data/tutorial.txt", "tutorial")

        self.FPS = int(self.game_data["options"]["fps"])
        self.text_lines = self.split_text_to_lines(
            list(self.tutorial["introduction"].values()), 900
        )  # Split text to fit the width
        self.current_line = 0
        self.displayed_text = ""
        self.text_timer = 0
        self.text_speed = 50  # Display speed (letters per second)
        self.line_pause_timer = 0  # Timer for automatic pause
        self.line_pause_duration = self.FPS  # 1-second pause (based on FPS)

        self.pause_lines = [
            2,
            4,
            9,
            12,
        ]  # Indices of lines requiring a pause (1-indexed)
        self.pause_timer = 0
        self.is_paused = False
        self.finished_text = False  # Indicator for when text is fully displayed

    def split_text_to_lines(self, text_list: list[str], max_width: int) -> list[str]:
        """Split text into lines fitting the specified width."""
        lines = []
        for text in text_list:
            words = text.split(" ")
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())
        return lines

    def update(self):
        """Update the text display or manage pauses."""
        if self.is_paused:
            self.pause_timer += 1
            if self.pause_timer >= self.FPS:  # 1-second pause
                self.is_paused = False
                self.pause_timer = 0
                self.current_line += 1
                self.displayed_text = ""
        else:
            if self.current_line < len(self.text_lines):
                current_text = self.text_lines[self.current_line]
                if len(self.displayed_text) < len(current_text):
                    self.text_timer += 1
                    if self.text_timer >= self.FPS / self.text_speed:
                        self.text_timer = 0
                        self.displayed_text += current_text[len(self.displayed_text)]
                else:
                    # Pause after specific lines
                    if (self.current_line + 1) in self.pause_lines:
                        self.is_paused = True
                    else:
                        self.current_line += 1
                        self.displayed_text = ""

        # Mark text as finished when all lines are displayed
        if self.current_line >= len(self.text_lines):
            self.finished_text = True

    def draw(self):
        """Render the introduction text on the screen."""
        self.screen.fill((0, 0, 0))

        # Draw title
        title = self.title_font.render("THE LAST SURVIVOR", True, (255, 255, 255))
        title_rect = title.get_rect(center=(500, 50))
        self.screen.blit(title, title_rect)
        pygame.draw.line(self.screen, (255, 255, 255), (450, 65), (650, 65))

        # Draw text lines
        y_offset = 100  # Starting vertical position
        line_height = self.font.size("A")[1] + 5  # Line height with spacing

        for i in range(self.current_line):  # Display previous lines
            text_surface = self.font.render(self.text_lines[i], True, (255, 255, 255))
            self.screen.blit(text_surface, (50, y_offset + i * line_height))

        if self.current_line < len(
            self.text_lines
        ):  # Display current line progressively
            text_surface = self.font.render(self.displayed_text, True, (255, 255, 255))
            self.screen.blit(
                text_surface, (50, y_offset + self.current_line * line_height)
            )

        # Display skip/continue message at the bottom-right corner
        message = (
            "PRESS SPACE TO CONTINUE" if self.finished_text else "PRESS SPACE TO SKIP"
        )
        message_surface = self.font.render(message, True, (255, 0, 0))  # Red text
        self.screen.blit(
            message_surface,
            (
                self.screen.get_width() - message_surface.get_width() - 20,
                self.screen.get_height() - 40,
            ),
        )

    def run(self):
        """Run the introduction loop."""
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if (
                            self.finished_text
                        ):  # If text is finished, close the introduction
                            running = False
                        else:
                            self.finished_text = True  # Skip remaining text
                            running = False

            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(self.FPS)
