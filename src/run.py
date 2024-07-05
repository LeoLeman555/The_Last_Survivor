import pygame, random
from update import Update
from items import Icon
from player import Player
from map import MapManager
from weapon import *
from lance_flamme import *
from extras import *
from read_data import ReadData

class Run:
  def __init__(self):
    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Jeu")
    pygame.font.init()

    self.read_data = ReadData()

    self.index_palier_xp = 45
    self.palier_xp = self.read_data.get_paliers("data/paliers.txt")
    self.ressources = self.read_data.read_ressources_data("data/ressources.txt")
    self.barres = self.read_data.read_barres_data("data/barres.txt")

    self.data_weapon = self.read_data.read_weapon_data('data/weapons.txt')

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