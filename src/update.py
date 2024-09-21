import random
from extras import *

class Update():
  def __init__(self, run):
    self.run = run

  def update_all(self):
    if not self.run.pause:
      self.update_map()
      self.update_objects()
      if self.run.data_extras["missile"]["activate"] == True:
        self.update_missile()
      self.update_bullets()
      self.update_enemies()
      self.update_weapon()
      self.update_toxic()
      if self.run.data_extras["laser_probe"]["activate"] == True:
        self.update_laser()
      if self.run.data_extras["drone"]["activate"] == True:
        self.update_drone()
      self.update_messages()
      
    self.draw()
    self.update_icon()
    self.update_cards()

  def draw(self):
    self.run.map_manager.draw()
    for objet in self.run.player.objects:
      objet.draw(self.run.screen)
    for missile in self.run.player.missiles:
      missile.draw(self.run.screen)
    for bullet in self.run.player.bullets:
        bullet.draw()
    for enemy in self.run.player.enemies:
      enemy.draw(self.run.screen)
    if self.run.current_weapon_dict["id"]==7:
      for particle in self.run.player.particles:
        particle.draw(self.run.screen)
    self.run.weapon.draw(self.run.screen)
    self.run.player.grenades.draw(self.run.screen)
    for particle in self.particles_list:
      particle.draw(self.run.screen)
    self.run.player.explosions.draw(self.run.screen) 
    for laser in self.run.player.lasers:
      laser.draw(self.run.screen)
    if self.run.data_extras["drone"]["activate"] == True:
      self.run.drone.draw(self.run.screen)
    for message in self.run.player.messages:
      message.draw(self.run.screen)

  def update_cards(self):
    self.run.power_up.update(self.run.mouse["position"], self.run.mouse["press"])
    self.run.power_up.draw(self.run.screen)
    self.run.weapons_cards.update(self.run.mouse["position"], self.run.mouse["press"])
    self.run.weapons_cards.draw(self.run.screen)
    self.run.extras_cards.update(self.run.mouse["position"], self.run.mouse["press"])
    self.run.extras_cards.draw(self.run.screen)

  def update_toxic(self):
    self.particles_list = list(self.run.player.toxic_particles)
    self.particles_list.sort(key=lambda p: p.creation_time, reverse=True)
    for particle in self.particles_list:
      particle.update(*self.run.mouvement)

  def update_weapon(self):
    self.run.weapon.rotate_to_cursor(self.run.mouse["position"])
    self.run.player.grenades.update(*self.run.mouvement)
    self.run.player.explosions.update()

  def update_bullets(self):
    if self.run.current_weapon_dict["id"]==7:
      for particle in self.run.player.particles:
        particle.update()
    else:
      for bullet in self.run.player.bullets:
        bullet.update()

  def update_enemies(self):
    for enemy in self.run.player.enemies:
      enemy.follow(475, 281)
      enemy.update(0.05, *self.run.mouvement, self.run.player.rect_collision)

  def update_objects(self):
    for objet in self.run.player.objects:
      objet.update(*self.run.mouvement, self.run.player.rect_collision)

  def update_messages(self):
    for message in self.run.player.messages:
      message.update()

  def update_map(self):
    self.run.map_manager.update()

  def update_icon(self):
    self.run.icon.update()
    self.run.icon.draw(self.run.screen)

  def update_laser(self):
    if random.random() < self.run.data_extras["laser_probe"]["rarity"]:
      self.run.player.add_laser()
    for laser in self.run.player.lasers:
      laser.update()

  def update_missile(self):
    if random.random() < self.run.data_extras["missile"]["rarity"]:
      self.run.player.add_missile()
    for missile in self.run.player.missiles:
      missile.update(*self.run.mouvement)

  def update_drone(self):
    self.run.drone.update()