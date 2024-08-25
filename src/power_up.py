import pygame
import random

class PowerUp:
  def __init__(self, power_up_data: dict, positions: list, run) -> None:
    self.power_up_data = power_up_data
    self.positions = positions
    self.run = run
    self.cards: list = []

  def launch_cards(self, power_up_names: list) -> None:
    self.cards = []
    for i, name in enumerate(power_up_names):
      if name in self.power_up_data:
        card_data = self.power_up_data[name]
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

  def draw(self, screen: pygame.Surface) -> None:
    for card in self.cards:
      screen.blit(card['current_image'], card['rect'])

  def update(self, mouse_pos: tuple, mouse_click: bool) -> None:
    for card in self.cards[:]:
      if card['rect'].collidepoint(mouse_pos):
        card['current_image'] = card['right_image']
        if mouse_click:
          card['data']['activate'] = True
          print(f"Power-Up {card['data']['effect']} activé !")
          self.cards = []
          self.run.pause = False
      else:
        card['current_image'] = card['left_image']

  def get_activated_power_ups(self) -> list:
    return [card for card in self.cards if card['data']['activate']]
