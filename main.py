print("------------------------- GO -------------------------")

import pygame
from src.data_handling.game_data_manager import *
from src.data_handling.load import *
from src.data_handling.read_data import *
from src.game.controllers.run import *
from src.UI.scenes.title import *
from src.UI.scenes.introduction import *
from src.UI.scenes.menu import *
from src.UI.scenes.shop import *
from src.UI.scenes.options import *


def initialize_pygame():
    """Initialize Pygame and the display."""
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Title")
    pygame.display.set_icon(pygame.image.load("res/icons/official_logo.png"))
    return screen


def load_game_data():
    """Load and return game data."""
    game_data_manager = GameDataManager()
    current_data = game_data_manager.game_data
    return current_data


def run_title_and_intro(screen, game_data):
    """Run the title screen and introduction if needed."""
    try:
        title_screen = TitleScreen(screen)
        title_screen.run()

        if game_data["options"]["tutorial"] == "on":
            introduction = Introduction(screen)
            introduction.run()
    except Exception as e:
        print(f"Error during title or introduction: {e}")
        return False
    return True


def main_game_loop():
    """Main game loop to manage menus and game state."""
    running = True
    while running:
        try:
            menu = MainMenu()
            direction = menu.run()

            if direction == "play":
                run = Run()
                run.manager.start_run()
            elif direction == "shop":
                shop = Shop()
                shop.run()
            elif direction == "options":
                options = Options()
                options.run()
            else:
                running = False
        except Exception as e:
            print(f"Error in main game loop: {e}")
            running = False


def main():
    """Main entry point of the program."""
    screen = initialize_pygame()
    game_data = load_game_data()

    try:
        if run_title_and_intro(screen, game_data):
            main_game_loop()
    except KeyboardInterrupt:
        print("Game stopped by the user")
    except Exception as e:
        print(f"Unhandled exception: {e}")
    finally:
        # Ensure Pygame resources are released
        pygame.quit()
        print("------------------------- END -------------------------")


if __name__ == "__main__":
    main()
