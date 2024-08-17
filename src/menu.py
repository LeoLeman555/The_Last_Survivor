import pygame

def Menu_principal():
  direction = None
  screen = pygame.display.set_mode((1000, 600))
  pygame.display.set_caption("The Last Survivor - Menu principal")

  # Noms des boutons à afficher
  # buttons = ["jeu", "intro", "boutique", "elements", "options"]
  buttons = ["jeu"]

  # Charger et redimensionner les images des boutons
  images = {
    name: pygame.transform.scale(
      pygame.image.load(f"res/menu/{name}.png"), 
      (pygame.image.load(f"res/menu/{name}.png").get_width() + 20, pygame.image.load(f"res/menu/{name}.png").get_height())
    ) for name in buttons
  }

  # Obtenir les rectangles des images pour les positionner
  rects = {name: images[name].get_rect() for name in buttons}

  # Positionner les images des boutons au centre de l'écran avec des espacements
  for i, name in enumerate(buttons):
    rects[name].x = (screen.get_width() - rects[name].width) // 2
    rects[name].y = (screen.get_height() // 2) - rects[name].height // 2 + i * (rects[name].height + 20) - 2 * rects[name].height

  # Afficher l'arrière-plan et les boutons à l'écran
  screen.blit(pygame.image.load("res/menu/background.jpg"), (0, 0))
  for name in buttons:
    screen.blit(images[name], rects[name])

  running = True

  # Boucle principale du menu
  while running:
    pygame.display.flip()  # Mettre à jour l'affichage
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        # Vérifier si un bouton a été cliqué
        for name in buttons:
          if rects[name].collidepoint(event.pos):
            direction = name
            running = False
            break
  return direction