import pygame
import random
from items import Icon
from player import Player
from weapon import *
from map import MapManager

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

    #?  numéro de l'arme:("nom de l'arme", (taille de l'arme), (position), (type de mu, coût de mu, chargeur), (DPS, portée), (ME, EN, DF nécessaires))
    self.data_weapon = {
      1: ("pistol", (22, 17), (520, 310), 500), 
      2: ("magnum", (36, 14), (520, 313), 700), 
      3: ("shotgun", (42, 14), (520, 310), 300), 
      4: ("sniper", (72, 21), (520, 310), 1000), 
      5: ("ak", (45, 15), (520, 310), 600), 
      6: ("rpg", (74, 20), (520, 310), 800), 
      7: ("lance_flammes", (45, 18), (520, 310), 200), 
      8: ("minigun", (48, 18), (520, 310), 500), 
      9: ("lance_grenades", (48, 18), (520, 310), 600),
      10: ("laser", (40, 20), (520, 310), 900), 
      11: ("plasma", (43, 20), (520, 310), 800),
      12: ("knife", (46, 12), (520, 310), 50)
    }
    self.weapon_key = random.choice(list(self.data_weapon.keys()))
    self.weapon_name, self.weapon_taille, self.weapon_position, self.id_munition = self.data_weapon[self.weapon_key]

    self.icon = Icon(self.ressources, self.barres)
    self.player = Player()  # mettre sur tiled un objet start
    self.map_manager = MapManager(self.screen, self.player) # appel de la classe mapManager
    self.weapon = Weapon(self.player, self.weapon_name, self.weapon_taille, self.weapon_position)

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

    if press[pygame.K_SPACE]:
      self.player.launch_bullet(pygame.mouse.get_pos(), self.weapon_key, self.data_weapon)
      self.icon.ajout_ressource("mu", -2)

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

      # Rotation de l'arme vers le curseur
      cursor_pos = pygame.mouse.get_pos()
      self.weapon.rotate_to_cursor(cursor_pos)

      self.player.bullets.draw(self.screen)

      self.weapon.display(self.screen)  # Affiche l'arme

      self.player.affiche_weapon(self.weapon_name, self.weapon_taille, self.weapon_position)

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
          self.player.launch_bullet(cursor_pos, self.weapon_key, self.data_weapon)
          self.icon.ajout_ressource("mu", -5)

      clock.tick(60)  # FPS