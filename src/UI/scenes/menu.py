import pygame
import time
from src.data_handling.game_data_manager import *
from src.data_handling.load import *
from src.data_handling.read_data import *
from src.UI.scenes.tutorial import *
from src.UI.widgets.button import *


class MainMenu:
    def __init__(self):
        """Initialize the main menu."""
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("The Last Survivor - Main Menu")
        pygame.display.set_icon(pygame.image.load("res/icons/official_logo.png"))

        self.font = pygame.font.Font("res/fonts/futurist_font.ttf", 18)
        self.title_font = pygame.font.Font("res/fonts/futurist_font.ttf", 25)

        self.direction: str | None = None
        self.read_data = ReadData()
        self.game_data_manager = GameDataManager()
        self.tutorial = Tutorial()

        self.button_return = Button("button_return", (975, 25))

        self.buttons = ["play", "shop", "options"]
        self.icon_names = ["energy", "metal", "data"]
        self.running = True

        self.images = [
            {name: self.load_button_image(name) for name in self.buttons},
            {name: self.load_button_image(f"{name}_click") for name in self.buttons},
        ]
        self.rects = {name: self.images[0][name].get_rect() for name in self.buttons}

        # Position the button images
        for i, name in enumerate(self.buttons):
            self.rects[name].centerx = self.screen.get_width() // 2
            self.rects[name].centery = (
                self.screen.get_height() // 2
                + i * (self.rects[name].height + 20)
                - 2 * self.rects[name].height
            )

        # Load game data and icons
        self.game_data = self.game_data_manager.game_data
        self.icon_numbers = [
            self.game_data["resource"]["energy"],
            self.game_data["resource"]["metal"],
            self.game_data["resource"]["data"],
        ]
        self.icons = {
            name: pygame.image.load(f"res/sprite/{name}_icon.png")
            for name in self.icon_names
        }
        self.icon_rects = {
            name: self.icons[name].get_rect() for name in self.icon_names
        }

        # Position the icons
        for i, name in enumerate(self.icon_names):
            self.icon_rects[name].x = 15
            self.icon_rects[name].y = 20 + i * 30

        # Animation setup
        self.menu_step = 1
        self.mouse_pos = 0
        self.mouse_press = False
        self.last_click_times = [0] * 1
        self.cooldown = 0.5

    def load_button_image(self, name: str) -> pygame.Surface:
        """Load and resize a button image."""
        image = pygame.image.load(f"res/menu/{name}.png")
        return pygame.transform.scale(
            image, (image.get_width() + 20, image.get_height())
        )

    def update(self) -> None:
        """Update the screen and handle user inputs."""
        self.press_buttons()

    def press_buttons(self) -> None:
        """Handle button presses with cooldown."""
        current_time = time.time()
        return_button_index = 0
        if self.button_return.is_pressed(self.mouse_pos, self.mouse_press):
            if (
                current_time - self.last_click_times[return_button_index]
                > self.cooldown
            ):
                self.menu_step = 0
                self.last_click_times[return_button_index] = current_time

    def draw(self):
        """Draw the main menu elements."""
        self.screen.blit(pygame.image.load("res/menu/background.jpg"), (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        self.button_return.draw(self.screen, self.mouse_pos)

        # Display title
        title = self.title_font.render("THE LAST SURVIVOR", True, (255, 255, 255))
        title_rect = title.get_rect(center=(500, 50))
        self.screen.blit(title, title_rect)
        pygame.draw.line(self.screen, (255, 255, 255), (450, 65), (650, 65))

        # Display buttons
        for name in self.buttons:
            if self.rects[name].collidepoint(mouse_pos):
                self.screen.blit(self.images[1][name], self.rects[name])
                if self.game_data["options"]["tutorial"] == "on":
                    self.tutorial.draw_main_menu(self.screen, name)
            else:
                self.screen.blit(self.images[0][name], self.rects[name])

        # Display icons with numbers
        for i, name in enumerate(self.icon_names):
            self.screen.blit(self.icons[name], self.icon_rects[name])
            number_text = self.font.render(
                str(self.icon_numbers[i]), True, (255, 255, 255)
            )
            self.screen.blit(
                number_text, (self.icon_rects[name].x + 30, self.icon_rects[name].y - 2)
            )

        pygame.display.flip()

    def run(self) -> str | None:
        """Run the main menu loop."""
        while self.running:
            self.mouse_pos = pygame.mouse.get_pos()
            # Handle key press
            if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                self.delete_data()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.menu_step <= 0:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_press = True
                    for name in self.buttons:
                        if self.rects[name].collidepoint(event.pos):
                            self.direction = name
                            self.running = False
                            break
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_press = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            self.update()
            self.draw()

        return self.direction

    def delete_data(self):
        """Handle data deletion."""
        self.running = False
        pygame.quit()
        question = (
            input("Are you sure you want to delete your progress? (Yes / No) -- ")
            .strip()
            .upper()
        )
        if question == "YES":
            self.game_data_manager.reset_game_save()
            print("-------- Your progress has been reinitialized ---------")
            time.sleep(0.5)
        else:
            print("Action cancelled.")
        pygame.init()
        self.__init__()
        self.run()
