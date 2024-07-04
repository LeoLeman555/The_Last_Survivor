import pygame, random
from update import Update
from items import Icon
from player import Player
from map import MapManager
from weapon import *
from lance_flamme import *
from extras import *

class Run:
  def __init__(self):
    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Jeu")
    pygame.font.init()

    self.index_palier_xp = 45
    self.palier_xp = self.get_paliers("paliers")
    self.ressources = {"xp_bar":0, "hp_bar":0, "faim_bar":0, "en":34, "me":506, "mu":2, "do":597}
    self.barres = {"xp":0, "hp":100, "faim":100, "xp_max":100, "hp_max":100, "faim_max":100}

    #?  numéro de l'arme:("nom de l'arme", (taille de l'arme), (position), portée, explosion?
    # TODO (type de mu, coût de mu, chargeur), (DPS, portée), (ME, EN, DF nécessaires))
    self.data_weapon = {
      1: ("pistol", (22, 17), (520, 310), 500, 0), 
      2: ("magnum", (36, 14), (520, 313), 700, 0), 
      3: ("shotgun", (42, 14), (520, 310), 300, 0), 
      4: ("sniper", (72, 21), (520, 310), 1000, 0), 
      5: ("ak", (45, 15), (520, 310), 600, 0), 
      6: ("rpg", (74, 20), (520, 310), 800, 1), 
      7: ("lance_flammes", (45, 18), (520, 310), 200, 0), 
      8: ("minigun", (48, 18), (520, 310), 500, 0), 
      9: ("lance_grenades", (48, 18), (520, 310), 600, 1),
      10: ("laser", (40, 20), (520, 310), 900, 1), 
      11: ("plasma", (43, 20), (520, 310), 800, 1),
      12: ("knife", (46, 12), (520, 310), 50, 0)
    }
    self.weapon_key = random.choice(list(self.data_weapon.keys()))
    self.weapon_key = 7
    self.weapon_name = self.data_weapon[self.weapon_key][0]
    self.weapon_taille = self.data_weapon[self.weapon_key][1]
    self.weapon_position = self.data_weapon[self.weapon_key][2]

    self.icon = Icon(self.ressources, self.barres)
    self.player = Player(self.screen)  # mettre sur tiled un objet start
    self.map_manager = MapManager(self.screen, self.player) # appel de la classe mapManager
    self.weapon = Weapon(self.player, self.weapon_name, self.weapon_taille, self.weapon_position)

    self.mouse_pressed = False
    self.shoot_delay = 100  # Délai entre les tirs en millisecondes
    self.last_shot_time = 0  # Temps du dernier tir

    self.explosions = pygame.sprite.Group()
    self.grenades = pygame.sprite.Group()

    self.particles = []

    self.drone = Drone(self.screen)
    self.lasers = []
    self.missile = []
    self.mouvement = [0, 0]

    self.update = Update(self.screen, self.map_manager, self.ressources, self.barres, self.icon, self.lasers, self.missile)

  def get_paliers(self, path):
    with open(f"data/{path}.txt", "r") as fichier:
        palier = tuple(int(num) for line in fichier for num in line.split(','))
    return palier

  def keyboard_input(self):
    """Déplacement du joueur avec les touches directionnelles"""
    press = pygame.key.get_pressed()

    # condition de déplacement
    if press[pygame.K_UP] and press[pygame.K_LEFT]: # pour se déplacer en diagonale
      self.player.haut(1.5)
      self.player.gauche(1.5)
      self.mouvement = [4, 4]
    elif press[pygame.K_UP] and press[pygame.K_RIGHT]:
      self.player.haut(1.5)
      self.player.droite(1.5)
      self.mouvement = [-4, 4]
    elif press[pygame.K_DOWN] and press[pygame.K_RIGHT]:
      self.player.bas(1.5)
      self.player.droite(1.5)
      self.mouvement = [-4, -4]
    elif press[pygame.K_DOWN] and press[pygame.K_LEFT]:
      self.player.bas(1.5)
      self.player.gauche(1.5)
      self.mouvement = [4, -4]
    elif press[pygame.K_UP]:        # pour se déplacer
      self.player.haut(1)
      self.mouvement = [0, 6]
    elif press[pygame.K_DOWN]:
      self.player.bas(1)
      self.mouvement = [0, -6]
    elif press[pygame.K_LEFT]:
      self.player.gauche(1)
      self.mouvement = [6, 0]
    elif press[pygame.K_RIGHT]:
      self.player.droite(1)
      self.mouvement = [-6, 0]
    else:
      self.mouvement = [0, 0]

    if press[pygame.K_r]:
      self.player.launch_grenade(-5)
    elif press[pygame.K_t]:
      self.player.launch_grenade(5)
  
  def change_max_xp(self, palier):
    self.index_palier_xp = palier
    self.icon.change_palier("xp", self.palier_xp[self.index_palier_xp])

  def ajout_particule(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - 500
    dy = mouse_y - 300
    distance = math.hypot(dx, dy)
    direction = (dx / distance, dy / distance)  # Normaliser le vecteur
    for _ in range(10):  # Ajouter plus de particules à la fois pour plus de diffusion
      self.particles.append(FireParticle(520, 310, direction))

  def update_weapon(self):
    if self.mouse_pressed:
      if self.weapon_key == 7: 
        self.ajout_particule()
      elif self.current_time - self.last_shot_time > self.shoot_delay:
          self.player.launch_bullet(self.cursor_pos, self.weapon_key, self.data_weapon)
          self.last_shot_time = self.current_time
      
    if self.weapon_key==7:
      for particle in self.particles:
        particle.update()
        particle.draw(self.screen)
      self.particles = [particle for particle in self.particles if particle.lifetime > 0 and particle.size > 0]
    else:
      self.player.bullets.draw(self.screen)
      for bullet in self.player.bullets:
        bullet.move()
        if bullet.distance_traveled > bullet.range:  # Si la balle atteint sa portée
          if bullet.explosive:  # Vérifiez si la balle est explosive
            explosion = Explosion(bullet.rect.center, bullet.images_explosion)
            self.explosions.add(explosion)
          bullet.delete()

    self.weapon.rotate_to_cursor(self.cursor_pos)
    self.weapon.display(self.screen)
    self.player.affiche_weapon(self.weapon_name, self.weapon_taille, self.weapon_position)

    self.player.grenades.update()
    self.player.grenades.draw(self.screen)

    self.player.explosions.update()
    self.player.explosions.draw(self.screen)

  def run(self):
    clock = pygame.time.Clock()
    run = True
    self.change_max_xp(5)
    while run:
      self.cursor_pos = pygame.mouse.get_pos()
      self.current_time = pygame.time.get_ticks()
      self.player.save_location()
      self.keyboard_input()
      self.map_manager.draw()

      self.icon.ajout_barres("xp", 1)
      self.icon.ajout_ressource("en", 1)

      self.update_class()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
          self.mouse_pressed = False

      clock.tick(60)

  def update_class(self):
    self.update.update_all(self.mouvement[0], self.mouvement[1])
    self.drone.update_drone()

    self.update_weapon()

    self.player.explosions.update()
    self.player.explosions.draw(self.screen)

    pygame.display.flip()