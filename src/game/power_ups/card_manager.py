import pygame
import time

class CardManager:
  def __init__(self, run, data, image_folder):
    self.run = run
    self.cards = []
    self.positions = [(274, 200), (590, 200)]
    self.data = data
    self.image_folder = image_folder

    self.last_click_times = 0
    self.cooldown = 0.5

  def get_image(self, name, level):
    image_path = f"res/power_up/{self.image_folder}/{name}_{level}.png"
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
        
        current_time = time.time()
        if mouse_click:
          if current_time - self.last_click_times > self.cooldown:
            self.last_click_times = current_time
            self.on_card_click(card)
            self.cards = []
            self.run.pause = False
            self.run.power_up_launch = False
            self.run.electrodes_manager.stop()
      else:
        card['current_image'] = card['left_image']

  def on_card_click(self, card):
    """This method should be overridden by subclasses to handle specific actions when a card is clicked."""
    pass