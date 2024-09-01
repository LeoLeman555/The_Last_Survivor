import random
from extras import *

class Update():
  def __init__(self, zoom: int, screen: 'pygame.surface.Surface', map_manager, player, weapon, ressources: dict, barres: dict, icon, weapon_dict: dict, mouvement :list, mouse: dict, data_extras: dict, power_up):
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

    self.power_up = power_up

    self.pause = False

  def change_zoom(self, new_zoom: float):
    self.zoom = new_zoom
    for enemy in self.player.enemies:
      enemy.change_zoom(new_zoom)
    for laser in self.player.lasers:
      laser.change_zoom(self.zoom)
    for missile in self.player.missiles:
      missile.change_zoom(self.zoom)
    for grenade in self.player.grenades:
      grenade.change_zoom(self.zoom)
    self.player.change_zoom()
    for objet in self.player.objects:
      objet.change_zoom(self.zoom)
    self.weapon.change_zoom(self.zoom)
    self.player.run.drone.change_zoom(self.zoom)

  def update_all(self, weapon_dict, mouvement, mouse, data_extras, pause):
    self.weapon_dict = weapon_dict
    self.mouvement = mouvement
    self.mouse = mouse
    self.data_extras = data_extras
    self.pause = pause

    if not self.pause:
      self.update_map()
      self.update_objects()
      if self.data_extras["missile"]["activate"] == True:
        self.update_missile()
      self.update_bullets()
      self.update_enemies()
      self.update_weapon()
      self.update_toxic()
      if self.data_extras["laser"]["activate"] == True:
        self.update_laser()
      if self.data_extras["drone"]["activate"] == True:
        self.update_drone()
      self.update_messages()
      
    self.draw()
    self.update_icon()
    self.update_cards()

  def draw(self):
    self.map_manager.draw()
    for objet in self.player.objects:
      objet.draw(self.screen)
    for missile in self.player.missiles:
      missile.draw(self.screen)
    for bullet in self.player.bullets:
        bullet.draw()
    for enemy in self.player.enemies:
      enemy.draw(self.screen)
    if self.weapon_dict["id"]==7:
      for particle in self.player.particles:
        particle.draw(self.screen)
    self.weapon.draw(self.screen)
    if self.data_extras["grenade"]["activate"] == True:
      self.player.grenades.draw(self.screen)
    for particle in self.particles_list:
      particle.draw(self.screen)
    self.player.explosions.draw(self.screen) 
    for laser in self.player.lasers:
      laser.draw(self.screen)
    if self.data_extras["grenade"]["activate"] == True:
      self.player.run.drone.draw(self.screen)
    for message in self.player.messages:
      message.draw(self.screen)

  def update_cards(self):
    self.power_up.update(self.mouse["position"], self.mouse["press"])
    self.power_up.draw(self.screen)
    self.player.run.weapons_cards.update(self.mouse["position"], self.mouse["press"])
    self.player.run.weapons_cards.draw(self.screen)

  def update_toxic(self):
    self.particles_list = list(self.player.toxic_particles)
    self.particles_list.sort(key=lambda p: p.creation_time, reverse=True)
    for particle in self.particles_list:
      particle.update(*self.mouvement)

  def update_weapon(self):
    self.weapon.rotate_to_cursor(self.mouse["position"])
    if self.data_extras["grenade"]["activate"] == True:
      self.player.grenades.update(*self.mouvement)
    self.player.explosions.update()

  def update_bullets(self):
    if self.weapon_dict["id"]==7:
      for particle in self.player.particles:
        particle.update()
    else:
      for bullet in self.player.bullets:
        bullet.update()

  def update_enemies(self):
    for enemy in self.player.enemies:
      enemy.follow(475, 281)
      enemy.update(0.05, *self.mouvement, self.player.rect_collision)

  def update_objects(self):
    for objet in self.player.objects:
      objet.update(*self.mouvement, self.player.rect_collision)

  def update_messages(self):
    for message in self.player.messages:
      message.update()

  def update_map(self):
    self.map_manager.update()

  def update_icon(self):
    self.icon.update()
    self.icon.draw(self.screen)

  def update_laser(self):
    if random.random() < self.data_extras["laser"]["rarity"]:
      self.player.add_laser()
    for laser in self.player.lasers:
      laser.update()

  def update_missile(self):
    if random.random() < self.data_extras["missile"]["rarity"]:
      self.player.add_missile()
    for missile in self.player.missiles:
      missile.update(*self.mouvement)

  def update_drone(self):
    self.player.run.drone.update()