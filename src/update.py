import random
from extras import *

class Update():
  def __init__(self, zoom: int, screen: 'pygame.surface.Surface', map_manager, player, weapon, ressources: dict, barres: dict, icon, weapon_dict: dict, mouvement :list, mouse: dict, data_extras: dict):
    self.zoom = zoom
    self.screen = screen
    self.map_manager = map_manager
    self.player = player
    self.weapon = weapon
    self.ressources = ressources
    self.barres = barres
    self.icon = icon
    self.enemies = self.player.enemies

    self.weapon_dict = weapon_dict
    self.mouvement = mouvement
    self.mouse = mouse

    self.data_extras = data_extras

  def update_all(self, weapon_dict, mouvement, mouse, data_extras):
    self.weapon_dict = weapon_dict
    self.mouvement = mouvement
    self.mouse = mouse
    self.data_extras = data_extras

    self.update_map()
    self.update_objects()
    if self.data_extras["missile"]["activate"] == True:
      self.update_missile()
    self.update_bullets()
    self.update_enemies()
    self.update_weapon()
    self.update_toxic()
    self.update_messages()
    if self.data_extras["laser"]["activate"] == True:
      self.update_laser()
    self.update_icon()

  def update_toxic(self):
    particles_list = list(self.player.toxic_particles)
    particles_list.sort(key=lambda p: p.creation_time, reverse=True)

    for particle in particles_list:
      particle.update(*self.mouvement)
      particle.draw(self.screen)

  def update_weapon(self):
    self.weapon.rotate_to_cursor(self.mouse["position"])
    self.weapon.draw(self.screen)

    if self.data_extras["grenade"]["activate"] == True:
      self.player.grenades.update(*self.mouvement)
      self.player.grenades.draw(self.screen)
    
    self.player.explosions.update()
    self.player.explosions.draw(self.screen) 

  def update_bullets(self):
    if self.weapon_dict["id"]==7:
      for particle in self.player.particles:
        particle.update()
        particle.draw(self.screen)
    else:
      for bullet in self.player.bullets:
        bullet.update()

  def update_enemies(self):
    for enemy in self.player.enemies:
      enemy.follow(475, 281)
      enemy.update(0.05, *self.mouvement, self.player.rect_collision)
      enemy.draw(self.screen)

  def update_objects(self):
    for objet in self.player.objects:
      objet.update(*self.mouvement, self.player.rect_collision)
      objet.draw(self.screen)

  def update_messages(self):
    for message in self.player.messages:
      message.update()
      message.draw(self.screen)

  def update_map(self):
    self.map_manager.update()

  def update_icon(self):
    self.icon.update()
    self.icon.draw(self.screen)

  def update_laser(self):
    if random.random() < 0.005:
      self.player.add_laser()
    for laser in self.player.lasers:
      laser.draw(self.screen)
      laser.update()

  def update_missile(self):
    if random.random() < 0.01:
      self.player.add_missile()
    for missile in self.player.missiles:
      missile.draw(self.screen)
      missile.update(*self.mouvement)