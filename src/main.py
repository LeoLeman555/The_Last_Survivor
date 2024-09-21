print("------------------------- GO -------------------------")

import pygame
from run import Run
from menu import Menu_principal

pygame.init()

running = True

while running == True:
  if Menu_principal() == "jeu":

    run = Run()
    run.manager.start_run()
  else:
    running = False

# run = Run()
# run.manager.start_run()

print("------------------------- END -------------------------")