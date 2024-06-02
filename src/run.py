import pygame
from map import MapManager
from player import Player
from items import Icon
from bullet import Bullet

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
    self.index_palier_xp = 45
    self.palier_xp = (100, 250, 500, 800, 1200, 1700, 2300, 3000, 3800, 4700, 5700, 6800, 8000, 9300, 10700, 12200, 13800, 15500, 17300, 19200, 21200, 23300, 25500, 27800, 30200, 32700, 35300, 38000, 40800, 43700, 46700, 49800, 53000, 56300, 59700, 63200, 66800, 70500, 74300, 78200, 82200, 86300, 90500, 94800, 99200, 103700, 108300, 113000, 117800, 122700, 127700, 132800, 138000, 143300, 148700, 154200, 159800, 165500, 171300, 180000)
    self.ressources = {"xp_bar":0, "hp_bar":0, "faim_bar":0, "en":34, "me":506, "mu":2, "do":597}
    self.barres = {"xp":0, "hp":100, "faim":100, "xp_max":100, "hp_max":100, "faim_max":100}

    self.icon = Icon(self.ressources, self.barres)
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

  def update_icon(self):
    self.ressources["xp_bar"] =  round(self.barres["xp"] * 79 / self.barres["xp_max"])
    self.ressources["hp_bar"] =  round(self.barres["hp"] * 79 / self.barres["hp_max"])
    self.ressources["faim_bar"] =  round(self.barres["faim"] * 79 / self.barres["faim_max"])
    self.icon.get_bar(self.screen, "xp_bar", 20, 20, self.ressources["xp_bar"])
    self.icon.get_bar(self.screen, "hp_bar", 20, 45, self.ressources["hp_bar"])
    self.icon.get_bar(self.screen, "faim_bar", 20, 70, self.ressources["faim_bar"])
    self.icon.get_icon(self.screen, "en_icon", 130, 100, 25, -3, 22, 20, self.ressources["en"])
    self.icon.get_icon(self.screen, "me_icon", 20, 100, 25, -3, 22, 20, self.ressources["me"])
    self.icon.get_icon(self.screen, "mu_icon", 134, 125, 21, 1, 15, 29, self.ressources["mu"])
    self.icon.get_icon(self.screen, "df_icon", 20, 127, 30, -1, 30, 21, self.ressources["do"])
  
  def change_max_xp(self, palier):
    self.index_palier_xp = palier
    self.icon.change_palier("xp", self.palier_xp[self.index_palier_xp])

  def run(self):
    """Boucle principale, appelle les fonctions :
    - sauvegarde la position du joueur
    - détection des touches pressées
    - mise à jour
    - map_manager.draw
    - gestion des icons
    """
    clock = pygame.time.Clock()
    run = True
    self.change_max_xp(5)
    while run:
      self.player.save_location()
      self.keyboard_input()
      self.update()
      self.map_manager.draw()

      self.player.bullets.draw(self.screen)

      for bullet in self.player.bullets:
        bullet.move()

      self.update_icon()

      self.icon.ajout_barres("xp", 1)
      self.icon.ajout_ressource("en", 1)
      self.icon.ajout_ressource("me", 1)
      self.icon.ajout_ressource("mu", 1)
      self.icon.ajout_ressource("do", 1)

      pygame.display.flip()       # actualisation

      for event in pygame.event.get():  # détecte quand on quitte
        if event.type == pygame.QUIT:
          run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.player.launch_bullet(event.pos)

      clock.tick(60) # FPS