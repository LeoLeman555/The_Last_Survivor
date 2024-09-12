import pygame

class CardManager:
  def __init__(self, run, data, image_folder):
    self.run = run
    self.cards = []
    self.positions = [(274, 200), (590, 200)]
    self.data = data
    self.image_folder = image_folder

  def get_image(self, name, level):
    image_path = f"res/power_up/level_{level}/{self.image_folder}/{name}.png"
    image = pygame.image.load(image_path)
    return self.run.load.split_image(image)

  def launch_cards(self, names: list):
    self.cards = []
    for i, name in enumerate(names):
      if name in self.data:
        card_data = self.data[name]
        left_image, right_image = self.get_image(name, card_data[1])
        position = self.positions[i]
        rect = left_image.get_rect(topleft=position)
        self.cards.append({
          'name': name,
          'left_image': left_image,
          'right_image': right_image,
          'current_image': left_image,
          'rect': rect,
          'id': card_data[0],
          'level': card_data[1]
        })

  def draw(self, screen: pygame.Surface):
    for card in self.cards:
      screen.blit(card['current_image'], card['rect'])

  def update(self, mouse_pos: tuple, mouse_click: bool):
    for card in self.cards[:]:
      if card['rect'].collidepoint(mouse_pos):
        card['current_image'] = card['right_image']
        if mouse_click:
          self.on_card_click(card)
          self.cards = []
          self.run.pause = False
      else:
        card['current_image'] = card['left_image']

  def on_card_click(self, card):
    """This method should be overridden by subclasses to handle specific actions when a card is clicked."""
    pass

class WeaponCard(CardManager):
  def __init__(self, run):
    super().__init__(run, {weapon["name"]: (weapon["id"], weapon["level"]) for weapon in run.data_weapons.values()}, "weapons")

  def on_card_click(self, card):
    self.run.manager.change_weapon(card["id"])

class ExtrasCard(CardManager):
  def __init__(self, run):
    super().__init__(run, {extras["name"]: (extras["id"], extras["level"]) for extras in run.data_extras.values()}, "extras")

  def on_card_click(self, card):
    self.run.manager.new_extra(card["name"])

class PowerUp(CardManager):
  def __init__(self, run, power_up_data):
    super().__init__(run, power_up_data, "")
    self.positions = [(274, 200), (432, 200), (590, 200)]

  def launch_cards(self, power_up_names: list):
    self.cards = []
    for i, name in enumerate(power_up_names):
      if name in self.data and not self.data[name].get('locked', False):
        card_data = self.data[name]
        left_image = card_data['left_image']
        right_image = card_data['right_image']
        position = self.positions[i]
        rect = left_image.get_rect(topleft=position)
        self.cards.append({
          'left_image': left_image,
          'right_image': right_image,
          'current_image': left_image,
          'rect': rect,
          'data': card_data
        })

  def on_card_click(self, card):
    card['data']['activate'] = True

class UsePowerUp:
  def __init__(self, run):
    self.run = run

  def use_power_up(self):
    if self.run.data_power_up["care_kit"]["activate"]:
      self.run.icon.resource["health"] += self.run.data_power_up["care_kit"]["value"]
      self.run.data_power_up["care_kit"]["activate"] = False

    if self.run.data_power_up["survival_ration"]["activate"]:
      self.run.icon.resource["food"] += self.run.data_power_up["survival_ration"]["value"]
      self.run.data_power_up["survival_ration"]["activate"] = False

    if self.run.data_power_up["critical_hit"]["activate"]:
      for weapon_id, weapon_data in self.run.data_weapons.items():
        if "critical" in weapon_data:
          weapon_data["critical"] *= self.run.data_power_up["critical_hit"]["value"]
      self.run.data_power_up["critical_hit"]["activate"] = False

    if self.run.data_power_up["2nd_life"]["activate"]:
      self.run.life = 2
      self.run.data_power_up["2nd_life"]["activate"] = False
    
    if self.run.data_power_up["expert"]["activate"]:
      self.run.xp_multiplier *= self.run.data_power_up["expert"]["value"]
      self.run.data_power_up["expert"]["activate"] = False

    if self.run.data_power_up["boost"]["activate"]:
      self.run.speed_init *= self.run.data_power_up["boost"]["value"]
      self.run.data_power_up["boost"]["activate"] = False

    if self.run.data_power_up["agile_fingers"]["activate"]:
      for weapon_id, weapon_data in self.run.data_weapons.items():
        if "recharge_time" in weapon_data:
          weapon_data["recharge_time"] *= self.run.data_power_up["agile_fingers"]["value"]
      self.run.data_power_up["agile_fingers"]["activate"] = False

    if self.run.data_power_up["extra_ammo"]["activate"]:
      for weapon_id, weapon_data in self.run.data_weapons.items():
        if "charger_capacity" in weapon_data:
          weapon_data["charger_capacity"] += self.run.data_power_up["extra_ammo"]["value"]
      self.run.data_power_up["extra_ammo"]["activate"] = False

    if self.run.data_power_up["large_range"]["activate"]:
      for weapon_id, weapon_data in self.run.data_weapons.items():
        if "range" in weapon_data:
          weapon_data["range"] *= self.run.data_power_up["large_range"]["value"]
      self.run.data_power_up["large_range"]["activate"] = False

    if self.run.data_power_up["magnetic"]["activate"]:
      self.run.range_obj *= self.run.data_power_up["magnetic"]["value"]
      self.run.data_power_up["magnetic"]["activate"] = False

    if self.run.data_power_up["rapid_fire"]["activate"]:
      for weapon_id, weapon_data in self.run.data_weapons.items():
        if "rate" in weapon_data:
          weapon_data["rate"] *= self.run.data_power_up["rapid_fire"]["value"]
      self.run.data_power_up["rapid_fire"]["activate"] = False

    if self.run.data_power_up["strong_stomach"]["activate"]:
      self.run.hunger_resistance *= self.run.data_power_up["strong_stomach"]["value"]
      self.run.data_power_up["strong_stomach"]["activate"] = False

    if self.run.data_power_up["zoom"]["activate"]:
      self.run.zoom = 1.5
      self.run.manager.change_zoom()
      self.run.data_power_up["zoom"]["activate"] = False

    if self.run.data_power_up["regeneration"]["activate"]:
      self.run.regeneration += self.run.data_power_up["regeneration"]["value"]
      self.run.data_power_up["regeneration"]["activate"] = False

    if self.run.data_power_up["piercing"]["activate"]:
      self.run.piercing += self.run.data_power_up["piercing"]["value"]
      self.run.data_power_up["piercing"]["activate"] = False
