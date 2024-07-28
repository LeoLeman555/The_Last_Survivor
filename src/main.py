print("------------------------- GO -------------------------")

import pygame
from run import Run
from menu import Menu_principal

pygame.init()

run = Run(2)

# Lancer le jeu directement
if Menu_principal() == "jeu":
  run.run()
  pygame.quit()

# run.run()

print("------------------------- FIN -------------------------")