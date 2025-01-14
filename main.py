print("------------------------- GO -------------------------")

from src.data_handling.load import *
from src.data_handling.read_data import *
from src.game.controllers.run import *
from src.UI.scenes.title import *
from src.UI.scenes.introduction import *
from src.UI.scenes.menu import *
from src.UI.scenes.shop import *
from src.UI.scenes.options import *

# Initialize running state
running = True

# Load game data
read_data = ReadData()
game_data = read_data.read_params("data/game_save.txt", "game_save")

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Title")
    pygame.display.set_icon(pygame.image.load("res/menu/logo.jpg"))

    # Display title screen and run
    title_screen = TitleScreen(screen)
    title_screen.run()

    # Show introduction if the tutorial option is on
    if game_data["options"]["tutorial"] == "on":
        introduction = Introduction(screen)
        introduction.run()

# Main game loop
while running:
    # Display main menu
    menu = MainMenu()
    direction = menu.run()

    if direction == "play":
        # Start the game
        run = Run()
        run.manager.start_run()
    elif direction == "shop":
        # Open the shop
        shop = Shop()
        shop.run()
    elif direction == "options":
        # Open options menu
        options = Options()
        options.run()
    else:
        # Exit the game loop
        running = False

pygame.quit()

print("------------------------- END -------------------------")
