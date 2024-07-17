import pygame, random, math
from update import *
from items import *
from player import *
from map import *
from weapon import *
from extras import *
from read_data import *
from enemy import *

class Run:
  def __init__(self, zoom:int):
    pygame.font.init()
    self.zoom = zoom

    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Jeu")

    self.read_data = ReadData()

    self.index_palier_xp = 45
    self.palier_xp = self.read_data.get_paliers("data/paliers.txt")
    self.ressources = self.read_data.read_ressources_data("data/ressources.txt")
    self.barres = self.read_data.read_barres_data("data/barres.txt")

    self.data_weapon = self.read_data.read_weapon_data('data/weapons.txt')
    self.weapon_key = random.choice(list(self.data_weapon.keys()))
    self.weapon_key = 1
    self.weapon_name = self.data_weapon[self.weapon_key][0]
    self.weapon_taille = self.data_weapon[self.weapon_key][1]
    self.weapon_position = self.data_weapon[self.weapon_key][2]
    self.weapon_position = list(self.weapon_position)
    self.weapon_position[0] += 10 * self.zoom
    self.weapon_position[1] += 5 * self.zoom

    self.icon = Icon(self.ressources, self.barres)
    
    self.speed_init = 3
    self.speed = self.speed_init

    self.player = Player(self.zoom, self.screen, "jim")  # mettre sur tiled un objet start
    self.map_manager = MapManager(self, self.screen, self.player, self.zoom) # appel de la classe mapManager

    self.weapon = Weapon(self.zoom, self.player, self.weapon_name, self.weapon_taille, self.weapon_position)

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

    self.collision_caillou = False

    self.enemy = pygame.sprite.Group()

  def keyboard_input(self):
    """Déplacement du joueur avec les touches directionnelles"""
    press = pygame.key.get_pressed()

    # condition de déplacement
    if press[pygame.K_w] and press[pygame.K_a]: # pour se déplacer en diagonale
      self.player.move_up(1.5, self.speed)
      self.player.move_left(1.5, self.speed)
      self.mouvement = [math.ceil(self.speed*1.33), math.ceil(self.speed*1.33)]
    elif press[pygame.K_w] and press[pygame.K_d]:
      self.player.move_up(1.5, self.speed)
      self.player.move_right(1.5, self.speed)
      self.mouvement = [math.ceil(self.speed*1.33)*-1, math.ceil(self.speed*1.33)]
    elif press[pygame.K_s] and press[pygame.K_d]:
      self.player.move_down(1.5, self.speed)
      self.player.move_right(1.5, self.speed)
      self.mouvement = [math.ceil(self.speed*1.33)*-1, math.ceil(self.speed*1.33)*-1]
    elif press[pygame.K_s] and press[pygame.K_a]:
      self.player.move_down(1.5, self.speed)
      self.player.move_left(1.5, self.speed)
      self.mouvement = [math.ceil(self.speed*1.33), math.ceil(self.speed*1.33)*-1]
    elif press[pygame.K_w]:        # pour se déplacer
      self.player.move_up(1, self.speed)
      self.mouvement = [0, self.speed*2]
    elif press[pygame.K_s]:
      self.player.move_down(1, self.speed)
      self.mouvement = [0, self.speed*-2]
    elif press[pygame.K_a]:
      self.player.move_left(1, self.speed)
      self.mouvement = [self.speed*2, 0]
    elif press[pygame.K_d]:
      self.player.move_right(1, self.speed)
      self.mouvement = [self.speed*-2, 0]
    else:
      self.mouvement = [0, 0]
    
    if self.collision_caillou:
      self.mouvement = [0, 0]

    if press[pygame.K_r]:
      self.player.launch_grenade(-1.5)
    elif press[pygame.K_t]:
      self.player.launch_grenade(1.5)
  
  def change_max_xp(self, palier):
    self.index_palier_xp = palier
    self.icon.change_palier("xp", self.palier_xp[self.index_palier_xp])

  def ajout_particule(self):
    x = 500 + 10 * self.zoom
    y = 300 + 5 * self.zoom
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - 500
    dy = mouse_y - 300
    distance = math.hypot(dx, dy)
    direction = (dx / distance, dy / distance)  # Normaliser le vecteur
    for _ in range(10):  # Ajouter plus de particules à la fois pour plus de diffusion
      self.particles.append(FireParticle(self.zoom, x, y, direction))

  def update_weapon(self):
    if self.mouse_pressed:
      self.tir()

    self.update_bullet()

    self.weapon.rotate_to_cursor(self.cursor_pos)
    self.weapon.display(self.screen)
    self.player.display_weapon(self.weapon_name, self.weapon_taille, self.weapon_position)

    self.player.grenades.update(self.mouvement[0], self.mouvement[1])
    self.player.grenades.draw(self.screen)
    
    self.player.explosions.update()
    self.player.explosions.draw(self.screen)

  def tir(self):
    if self.weapon_key == 7: 
      self.ajout_particule()
    elif self.current_time - self.last_shot_time > self.shoot_delay:
      if self.weapon_key == 9:
        # self.player.launch_grenade(3)
        pass
      else:
        self.player.launch_bullet(self.cursor_pos, self.weapon_key, self.data_weapon)
      self.last_shot_time = self.current_time

  def update_bullet(self):
    if self.weapon_key==7:
      for particle in self.particles:
        particle.update()
        particle.draw(self.screen)
      self.particles = [particle for particle in self.particles if particle.lifetime > 0 and particle.size > 0]
    else:
      for bullet in self.player.bullets:
        bullet.move()

  def update_enemy(self):
    for enemy in self.enemy:
      enemy.follow(475, 281)
      # enemy.attack()
      # enemy.die()
      enemy.update(0.05, self.mouvement[0], self.mouvement[1], self.player.rect_collision)
      enemy.draw(self.screen)

  def run(self):
    clock = pygame.time.Clock()
    run = True
    self.change_max_xp(5)
    # self.enemy.add(Shardsoul(self.screen, 0, 0))
    self.enemy.add(Sprout(self.screen, 100, 0))
    # self.enemy.add(Worm(self.screen, 100, 100))
    # self.enemy.add(Wolf(self.screen, 200, 100))
    # self.enemy.add(Robot(self.screen, 100, 100))

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
    self.update_enemy()
    self.update.update_all(self.mouvement[0], self.mouvement[1])
    self.drone.update_drone()

    self.update_weapon()

    self.player.explosions.update()
    self.player.explosions.draw(self.screen)

    pygame.display.flip()

  def collision_sables(self, bool:bool):
    if bool:
      self.speed = self.speed_init/2
    else:
      self.speed = self.speed_init

  def collision(self, bool:bool):
    self.collision_caillou = bool
