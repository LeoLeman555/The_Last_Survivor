print("------------------------- GO -------------------------")

from menu import *
from run import Run
from shop import Shop
from options import Options

running = True

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