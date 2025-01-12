from src.game.power_ups.card_manager import *

class WeaponCard(CardManager):
  def __init__(self, run):
    super().__init__(run, "choose_weapon", {weapon["name"]: (weapon["id"], weapon["level"]) for weapon in run.data_weapons.values()}, "weapons")

  def draw(self, screen: pygame.Surface):
    if self.run.active_panel != "weapon":
      return
    super().draw(screen)

  def on_card_click(self, card):
    self.run.manager.change_weapon(card["id"])
    self.run.active_panel = None

class ExtrasCard(CardManager):
  def __init__(self, run):
    super().__init__(run, "choose_extra", {extras["name"]: (extras["id"], extras["level"]) for extras in run.data_extras.values()}, "extras")

  def draw(self, screen: pygame.Surface):
    if self.run.active_panel != "extras":
      return
    super().draw(screen)

  def on_card_click(self, card):
    self.run.manager.new_extra(card["name"])
    self.run.active_panel = None

class PowerUpCard(CardManager):
  def __init__(self, run, power_up_data):
    super().__init__(run, "choose_power_up", power_up_data, "power_up")
    self.positions = [(274, 200), (432, 200), (590, 200)]  # Trois positions

  def draw(self, screen: pygame.Surface):
    if self.run.active_panel != "power_up":
      return
    super().draw(screen)

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

    self.cooldown_start_time = pygame.time.get_ticks() / 1000

  def on_card_click(self, card):
    card['data']['activate'] = True
    self.run.active_panel = None
