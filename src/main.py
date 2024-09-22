print("------------------------- GO -------------------------")

from run import Run
from menu import *

running = True

while running == True:
  menu = MenuPrincipal()
  direction = menu.run()
  if direction == "jeu":

    run = Run()
    run.manager.start_run()
  else:
    running = False

# run = Run()
# run.manager.start_run()

print("------------------------- END -------------------------")