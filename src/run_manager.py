import random

class RunManager:
  def __init__(self, run):
    self.run = run

  def start_run(self):
    self.run.ressources["ammo"] = 500
    self.run.ressources["health"] = 100
    self.run.ressources["food"] = 100
    self.run.run()

  def new_weapon(self, name):
    if not self.run.current_weapon_dict["name"] == name:
      self.run.pause = True
      self.run.weapons_cards.launch_cards([self.run.current_weapon_dict["name"], name])

  def add_extras(self):
    unlocked_extras = [name for name, data in self.run.data_extras.items() if not data.get('locked', False)]
    self.run.pause = True
    self.run.extras_cards.launch_cards(random.sample(unlocked_extras, 2))

  def new_extra(self, name):
    self.run.data_extras[name]["activate"] = True

  def change_weapon(self, id):
    self.run.current_weapon_dict = self.run.data_weapons[f"{id}"]
    self.run.current_weapon_dict["position"][0] = 500 + (10 * self.run.zoom)
    self.run.current_weapon_dict["position"][1] = 300 + (5 * self.run.zoom)
    self.run.weapon.change_weapon(self.run.zoom, self.run.player, self.run.current_weapon_dict)

  def launch_power_up(self):
    unlocked_power_ups = [name for name, data in self.run.data_power_up.items() if not data.get('locked', False)]
    #? Maybe add a other chance to get extras
    if len(unlocked_power_ups) < 3 or random.random() < 0.15:
      self.add_extras()
      return
    self.run.pause = True
    self.run.power_up.launch_cards(random.sample(unlocked_power_ups, 3))

  def change_max_xp(self, palier):
    self.run.index_palier_xp = palier
    self.run.icon.change_threshold("xp", self.run.palier_xp[self.run.index_palier_xp])