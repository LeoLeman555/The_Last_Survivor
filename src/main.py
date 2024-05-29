print("------------------------- GO -------------------------")

import pygame
import math
from run import Run

# menu principal
pygame.init()

def Menu_principal():
  direction = None
  screen = pygame.display.set_mode((1000, 600))
  pygame.display.set_caption("The Last Survivor - Menu principal")

  # importe les images
  background = pygame.image.load("res/menu/background.jpg")
  b_jeu = pygame.image.load("res/menu/jeu.png")
  b_intro = pygame.image.load("res/menu/intro.png")
  b_boutique = pygame.image.load("res/menu/boutique.png")
  b_elements = pygame.image.load("res/menu/elements.png")
  b_options = pygame.image.load("res/menu/options.png")

  b_width = b_jeu.get_width()
  b_height = b_jeu.get_height()

  # transforme et affiche les images
  b_jeu = pygame.transform.scale(b_jeu, (b_width + 20, b_height))
  b_jeu_rect = b_jeu.get_rect()
  b_intro = pygame.transform.scale(b_intro, (b_width + 20, b_height))
  b_intro_rect = b_intro.get_rect()
  b_boutique = pygame.transform.scale(b_boutique, (b_width + 20, b_height))
  b_boutique_rect = b_boutique.get_rect()
  b_elements = pygame.transform.scale(b_elements, (b_width + 20, b_height))
  b_elements_rect = b_elements.get_rect()
  b_options = pygame.transform.scale(b_options, (b_width + 20, b_height))
  b_options_rect = b_options.get_rect()

  # placement correct
  b_jeu_rect.x = math.ceil((screen.get_width() / 2) - b_width / 2 - 5)
  b_jeu_rect.y = math.ceil((screen.get_height() / 2) - b_height / 2 - b_height - 20)
  b_intro_rect.x = math.ceil((screen.get_width() / 2) - b_width / 2 - 5)
  b_intro_rect.y = math.ceil((screen.get_height() / 2) - b_height / 2 - 10)
  b_boutique_rect.x = math.ceil((screen.get_width() / 2) - b_width / 2 - 5)
  b_boutique_rect.y = math.ceil((screen.get_height()/ 2) - b_height / 2 + b_height)
  b_elements_rect.x = math.ceil((screen.get_width() / 2) - b_width / 2 - 5)
  b_elements_rect.y = math.ceil((screen.get_height() / 2) - b_height / 2 + b_height * 2 + 10)
  b_options_rect.x = math.ceil((screen.get_width() / 2) - b_width / 2 - 5)
  b_options_rect.y = math.ceil((screen.get_height() / 2) - b_height / 2 + b_height * 3 + 20)

  # affichage a l’écran
  screen.blit(background, (0, 0))
  screen.blit(b_jeu, b_jeu_rect)
  screen.blit(b_intro, b_intro_rect)
  screen.blit(b_boutique, b_boutique_rect)
  screen.blit(b_elements, b_elements_rect)
  screen.blit(b_options, b_options_rect)

  running = True

  while running:
    pygame.display.flip()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if b_jeu_rect.collidepoint(event.pos):  # verification si la souris est en collision avec bouton
          direction = "jeu" # lance le jeu
          running = False
        elif b_intro_rect.collidepoint(event.pos): 
          direction = "intro"
          running = False
        elif b_boutique_rect.collidepoint(event.pos): 
          direction = "boutique"
          running = False
        elif b_elements_rect.collidepoint(event.pos): 
          direction = "elements"
          running = False
        elif b_options_rect.collidepoint(event.pos): 
          direction = "options"
          running = False

  pygame.quit()

  # decide quel direction prendre
  if direction == "jeu":
    start = Run() # appel classe Run
    start.run()
    Menu_principal()
    print("------------------------- FIN -------------------------")
  elif direction == "intro":
    pass
  elif direction == "boutique":
    pass
  elif direction == "elements":
    pass
  elif direction == "options":
    pass

# Menu_principal()
start = Run()
start.run()