import random
from extras import *

class Update():
  def __init__(self, screen, map_manager, ressources, barres, icon, lasers, missile):
    self.screen = screen
    self.map_manager = map_manager
    self.ressources = ressources
    self.barres = barres
    self.icon = icon
    self.lasers = lasers
    self.missile = missile

  def update_all(self, x=0, y=0):
    self.update_map()
    self.update_laser()
    self.update_missile(x, y)
    self.update_icon()

  def update_map(self):
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

  def update_laser(self):
    if random.random() < 0.01:
      self.lasers.append(Laser())
    for laser in self.lasers:
      laser.draw(self.screen)
      laser.update()
    self.lasers = [laser for laser in self.lasers if laser.lifetime > 0]

  def update_missile(self, x, y):
    if random.random() < 0.05:
      self.missile.append(Missile())
      # self.missile.append(Missile())
      # self.missile.append(Missile())
    for mis in self.missile:
      mis.draw(self.screen)
      mis.update(x, y)
    self.missile = [mis for mis in self.missile if mis.lifetime > 0]