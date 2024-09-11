import pygame

class WeaponCard:
  def __init__(self, run):
    self.run = run
    self.cards = []
    self.positions =[(274, 200), (590, 200)]
    self.data_weapon_card  = {weapon["name"]: (weapon["id"], weapon["level"]) for weapon in self.run.data_weapons.values()}

  def get_image(self, name):
    image_path = f"res/power_up/level_{self.data_weapon_card[name][1]}/weapons/{name}.png"
    image = pygame.image.load(image_path)
    return self.run.load.split_image(image)

  def launch_cards(self, weapons_names: list):
    self.cards = []
    for i, name in enumerate(weapons_names):
      if name in self.data_weapon_card:
        card_data = self.data_weapon_card[name]
        left_image, right_image = self.get_image(name)
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
          print(f"New weapon : {card["name"]}, ID : {card["id"]}")
          self.run.manager.change_weapon(card["id"])
          self.cards = []
          self.run.pause = False
      else:
        card['current_image'] = card['left_image']

class ExtrasCard:
  def __init__(self, run):
    self.run = run
    self.cards = []
    self.positions = [(274, 200), (590, 200)]
    self.data_extras_card  = {extras["name"]: (extras["id"], extras["level"]) for extras in self.run.data_extras.values()}

  def get_image(self, name):
    image_path = f"res/power_up/level_{self.data_extras_card[name][1]}/extras/{name}.png"
    image = pygame.image.load(image_path)
    return self.run.load.split_image(image)

  def launch_cards(self, extras_names: list):
    self.cards = []
    for i, name in enumerate(extras_names):
      if name in self.data_extras_card:
        card_data = self.data_extras_card[name]
        left_image, right_image = self.get_image(name)
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
          print(f"New extras : {card["name"]}")
          self.run.manager.new_extra(card["name"])
          self.cards = []
          self.run.pause = False
      else:
        card['current_image'] = card['left_image']

class PowerUp:
  def __init__(self, run, power_up_data: dict):
    self.run = run
    self.cards = []
    self.positions = [(274, 200), (432, 200), (590, 200)]
    self.power_up_data = power_up_data

  def launch_cards(self, power_up_names: list):
    self.cards = []
    for i, name in enumerate(power_up_names):
      if name in self.power_up_data:
        card_data = self.power_up_data[name]
        # Vérifie si la carte est verrouillée (locked == False)
        if not card_data.get('locked', False):  
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

  def draw(self, screen: pygame.Surface):
    for card in self.cards:
      screen.blit(card['current_image'], card['rect'])

  def update(self, mouse_pos: tuple, mouse_click: bool):
    for card in self.cards[:]:
      if card['rect'].collidepoint(mouse_pos):
        card['current_image'] = card['right_image']
        if mouse_click:
          card['data']['activate'] = True
          print(f"Power-Up {card['data']['name']}")
          self.cards = []
          self.run.pause = False
      else:
        card['current_image'] = card['left_image']

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
      self.run.map_manager.change_map_size(self.run.zoom)
      self.run.update.change_zoom(self.run.zoom)
      self.run.drone.change_zoom(self.run.zoom)
      self.run.data_power_up["zoom"]["activate"] = False

    if self.run.data_power_up["regeneration"]["activate"]:
      self.run.regeneration += self.run.data_power_up["regeneration"]["value"]
      self.run.data_power_up["regeneration"]["activate"] = False

    if self.run.data_power_up["piercing"]["activate"]:
      self.run.piercing += self.run.data_power_up["piercing"]["value"]
      self.run.data_power_up["piercing"]["activate"] = False
