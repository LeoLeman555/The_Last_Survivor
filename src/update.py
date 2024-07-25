import random
from extras import *

class Update():
  def __init__(self, zoom:int, screen:'pygame.surface.Surface', map_manager, player, weapon, ressources:dict, barres:dict, icon, data_weapon, weapon_key: int, weapon_name, weapon_taille, weapon_position, mouvement, mouse):
    self.zoom = zoom
    self.screen = screen
    self.map_manager = map_manager
    self.player = player
    self.weapon = weapon
    self.ressources = ressources
    self.barres = barres
    self.icon = icon
    self.enemies = self.player.enemies

    self.mouvement = mouvement
    self.data_weapon = data_weapon
    self.weapon_key = weapon_key
    self.weapon_name = weapon_name
    self.weapon_taille = weapon_taille
    self.weapon_position = weapon_position

    self.mouse = mouse

    self.last_shot_time = self.mouse["current_time"]

  def update_all(self, mouvement, mouse):
    self.mouvement = mouvement

    self.mouse = mouse

    self.update_map()
    self.update_laser()
    self.update_missile()
    self.update_weapon()
    self.update_enemies()
    self.update_bullets()
    self.update_icon()

  def update_weapon(self):

    self.weapon.rotate_to_cursor(self.mouse["position"])
    self.weapon.draw(self.screen)
    self.player.display_weapon(self.weapon_name, self.weapon_taille, self.weapon_position)

    self.player.grenades.update(*self.mouvement)
    self.player.grenades.draw(self.screen)
    
    self.player.explosions.update()
    self.player.explosions.draw(self.screen) 

  def update_bullets(self):
    if self.weapon_key==7:
      for particle in self.player.particles:
        particle.update()
        particle.draw(self.screen)
    else:
      for bullet in self.player.bullets:
        bullet.update()

  def update_enemies(self):
    for enemy in self.player.enemies:
      enemy.follow(475, 281)
      enemy.update(0.05, self.mouvement[0], self.mouvement[1], self.player.rect_collision)
      enemy.draw(self.screen)

  def update_map(self):
    self.map_manager.update()

  def update_icon(self):
    self.ressources["xp_bar"] =  round(self.barres["xp"] * 79 / self.barres["xp_max"])
    self.ressources["hp_bar"] =  round(self.barres["hp"] * 79 / self.barres["hp_max"])
    self.ressources["faim_bar"] =  round(self.barres["faim"] * 79 / self.barres["faim_max"])
    self.icon.draw_bar(self.screen, "xp_bar", 20, 20, self.ressources["xp_bar"])
    self.icon.draw_bar(self.screen, "hp_bar", 20, 45, self.ressources["hp_bar"])
    self.icon.draw_bar(self.screen, "faim_bar", 20, 70, self.ressources["faim_bar"])
    self.icon.draw_icon(self.screen, "en_icon", 130, 100, 25, -3, 22, 20, self.ressources["en"])
    self.icon.draw_icon(self.screen, "me_icon", 20, 100, 25, -3, 22, 20, self.ressources["me"])
    self.icon.draw_icon(self.screen, "mu_icon", 134, 125, 21, 1, 15, 29, self.ressources["mu"])
    self.icon.draw_icon(self.screen, "df_icon", 20, 127, 30, -1, 30, 21, self.ressources["do"])

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