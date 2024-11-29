print("------------------------- GO -------------------------")

from menu import *
from introduction import *
from title import *
from run import *
from shop import *
from options import *
from load import *

running = True

read_data = ReadData()
game_data = read_data.read_params("data/game_save.txt", "game_save")

if __name__ == "__main__":
  pygame.init()
  screen = pygame.display.set_mode((1000, 600))
  pygame.display.set_caption("The Last Survivor - Title")

  title_screen = TitleScreen(screen)
  title_screen.run()

  if game_data["options"]["tutorial"] == "on":
    introduction = Introduction(screen)
    introduction.run()

  pygame.quit()

while running == True:
  menu = MenuPrincipal()
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

# run = Run()
# run.manager.start_run()

print("------------------------- END -------------------------")