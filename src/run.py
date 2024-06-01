import pygame
from map import MapManager
from player import Player
from items import Icon

class Run:
  def __init__(self):
    """ Moteur du jeu:
    - création de la fenêtre, du joueur, et de la carte
    - boucle principale
    """
    # creation de la fenêtre de jeu + titre de la fenêtre
    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Jeu")
    pygame.font.init()
    self.ressources = {"xp":67, "hp":79, "faim":28, "en":34, "me":506, "mu":2, "do":597}

    self.icon = Icon(self.ressources)
    self.player = Player()  # mettre sur tiled un objet start

    self.map_manager = MapManager(self.screen, self.player) # appel de la classe mapManager

  def keyboard_input(self):
    """Déplacement du joueur avec les touches directionnelles"""
    press = pygame.key.get_pressed()

    # condition de déplacement
    if press[pygame.K_UP] and press[pygame.K_LEFT]: # pour se déplacer en diagonale
      self.player.haut(1.5)
      self.player.gauche(1.5)
    elif press[pygame.K_UP] and press[pygame.K_RIGHT]:
      self.player.haut(1.5)
      self.player.droite(1.5)
    elif press[pygame.K_DOWN] and press[pygame.K_RIGHT]:
      self.player.bas(1.5)
      self.player.droite(1.5)
    elif press[pygame.K_DOWN] and press[pygame.K_LEFT]:
      self.player.bas(1.5)
      self.player.gauche(1.5)
    elif press[pygame.K_UP]:        # pour se déplacer
      self.player.haut(1)
    elif press[pygame.K_DOWN]:
      self.player.bas(1)
    elif press[pygame.K_LEFT]:
      self.player.gauche(1)
    elif press[pygame.K_RIGHT]:
      self.player.droite(1)

  def update(self):
    """Rafraîchit la classe MapManager.update"""
    self.map_manager.update()

  def run(self):
    """Boucle principale, appelle les fonctions :
    - sauvegarde la position du joueur
    - détection des touches pressées
    - mise à jour
    - map_manager.draw
    """
    clock = pygame.time.Clock()
    run = True
    while run:
      self.player.save_location()
      self.keyboard_input()
      self.update()
      self.map_manager.draw()

      self.icon.get_bar(self.screen, "xp_bar", 20, 20, self.ressources["xp"])
      self.icon.get_bar(self.screen, "hp_bar", 20, 45, self.ressources["hp"])
      self.icon.get_bar(self.screen, "faim_bar", 20, 70, self.ressources["faim"])
      self.icon.get_icon(self.screen, "en_icon", 130, 100, 25, -3, 22, 20, self.ressources["en"])
      self.icon.get_icon(self.screen, "me_icon", 20, 100, 25, -3, 22, 20, self.ressources["me"])
      self.icon.get_icon(self.screen, "mu_icon", 134, 125, 21, 1, 15, 29, self.ressources["mu"])
      self.icon.get_icon(self.screen, "df_icon", 20, 127, 30, -1, 30, 21, self.ressources["do"])

      self.icon.ajout_ressource("en", 1)
      self.icon.ajout_ressource("me", 1)
      self.icon.ajout_ressource("mu", 1)
      self.icon.ajout_ressource("do", 1)


      pygame.display.flip()       # actualisation

      for event in pygame.event.get():  # détecte quand on quitte
        if event.type == pygame.QUIT:
          run = False

      clock.tick(60) # FPS

    pygame.quit() # fin du jeu