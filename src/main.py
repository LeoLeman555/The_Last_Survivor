print("------------------------- GO -------------------------")

from run import Run
from menu import *
from shop import Shop

running = True

while running == True:
  menu = MenuPrincipal()
  direction = menu.run()
  if direction == "game":
    run = Run()
    run.manager.start_run()
  elif direction == "shop":
    shop = Shop()
    shop.run()
  else:
    running = False

# run = Run()
# run.manager.start_run()

print("------------------------- END -------------------------")