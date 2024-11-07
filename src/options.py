import pygame
import time
from change_game_data import ChangeGameData
from load import *
from button import *

class Options:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Options")
    self.font = pygame.font.Font("res/texte/dialog_font.ttf", 18)

    # Initialisation des données du jeu et des commandes par défaut
    self.read_data = ReadData()
    self.load = Load()
    self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
    self.rewards = {"options": self.game_data["options"].copy()}

    self.dict_arrows = self.rewards["options"].copy()
    # Boutons d'interface
    self.button_return = ReturnButton(
      image_path="res/shop/button_return.png",
      click_image_path="res/shop/button_return_click.png",
      position=(975, 25)
    )
    self.button_arrow = pygame.image.load("res/options/button.png")
    self.button_arrow_click = pygame.image.load("res/options/button_click.png")

    # Variables de gestion des entrées
    self.mouse_pos = (0, 0)
    self.mouse_press = False
    self.option_step = 1
    self.last_click_times = [0] * 1
    self.cooldown = 0.5
    self.key_waiting_for_input = None  # Pour détecter quand une commande doit être modifiée

    self.error_message = ""
    self.error_message_start_time = 0
    self.error_display_duration = 3  # Durée d'affichage en secondes

  def display_error_message(self, message):
    """Affiche un message d'erreur en rouge pendant une durée limitée."""
    self.error_message = message
    self.error_message_start_time = time.time()

  def change_key(self, command_name, new_key):
    """Met à jour la touche pour une commande et sauvegarde le changement."""    
    self.rewards["options"][command_name] = new_key
    change_game_data = ChangeGameData(self.rewards, True)
    change_game_data.change_params(self.rewards, change_game_data.game_save_data)

  def handle_key_event(self, event):
    """Gestion du changement de touche clavier."""
    if self.key_waiting_for_input:
      if self.key_waiting_for_input != "shoot":
        new_key = pygame.key.name(event.key).upper()
        self.dict_arrows[self.key_waiting_for_input] = new_key
        self.change_key(self.key_waiting_for_input, new_key)
      else:
        self.display_error_message("MUST BE ASSIGNED TO A MOUSE BUTTON")
      
      self.key_waiting_for_input = None  

  def handle_mouse_event(self, event):
    """Gestion du changement de bouton de souris."""
    if self.key_waiting_for_input:
      if self.key_waiting_for_input == "shoot":
        if event.button == 1:
          new_key = "MOUSE1"
        elif event.button == 2:
          new_key = "MOUSE3"
        elif event.button == 3:
          new_key = "MOUSE2"
        else:
          new_key = f"MOUSE{event.button}"

        self.dict_arrows[self.key_waiting_for_input] = new_key
        self.change_key(self.key_waiting_for_input, new_key)
        self.key_waiting_for_input = None
      else:
        self.display_error_message("CAN'T BE ASSIGNED TO A MOUSE BUTTON")
        self.key_waiting_for_input = None

  def update(self):
    self.press_buttons()

  def press_buttons(self):
    current_time = time.time()
    return_button_index = 0
    if self.button_return.is_pressed(self.mouse_pos, self.mouse_press):
      if current_time - self.last_click_times[return_button_index] > self.cooldown:
        self.option_step = 0 if self.option_step == 1 else 1
        self.last_click_times[return_button_index] = current_time

  def draw(self):
    # Dessine les boutons et commandes
    self.button_return.draw(self.screen, self.mouse_pos)

    # Affiche les commandes
    rect_width = 100
    rect_height = 30
    x_offset = 50

    for i, name in enumerate(self.dict_arrows.keys(), start=0):
      element = self.dict_arrows[name]
      
      name_text = self.font.render(name.capitalize() + " :", True, (255, 255, 255))
      name_text_rect = name_text.get_rect()
      name_text_rect.topright = (200, 50 * i + 100)
      self.screen.blit(name_text, name_text_rect)

      key_display_text = "" if self.key_waiting_for_input == name else str(element)
      text = self.font.render(key_display_text, True, (255, 255, 255))
      text_rect = text.get_rect()
      
      button_rect = pygame.Rect(name_text_rect.right + x_offset, name_text_rect.top, rect_width, rect_height)
      text_rect.center = button_rect.center

      button_image = self.button_arrow_click if button_rect.collidepoint(self.mouse_pos) else self.button_arrow
      button_arrow = pygame.transform.scale(button_image, (rect_width, rect_height))
      
      self.screen.blit(button_arrow, button_rect)
      self.screen.blit(text, text_rect)

      if button_rect.collidepoint(self.mouse_pos) and self.mouse_press:
        self.key_waiting_for_input = name

    # Affiche le message d'erreur si nécessaire
    if self.error_message:
      elapsed_time = time.time() - self.error_message_start_time
      if elapsed_time < self.error_display_duration:
        error_text = self.font.render(self.error_message, True, (255, 0, 0))
        error_text_rect = error_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(error_text, error_text_rect)
      else:
        self.error_message = ""  # Réinitialise le message après la durée d'affichage


  def run(self):
    clock = pygame.time.Clock()
    running = True
    while running:
      self.mouse_pos = pygame.mouse.get_pos()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.mouse_press = True
          self.handle_mouse_event(event)  # Appel pour changement de bouton de souris
        elif event.type == pygame.MOUSEBUTTONUP:
          self.mouse_press = False
        elif event.type == pygame.KEYDOWN:
          self.handle_key_event(event)  # Appel pour changement de touche clavier

      self.update()
      self.screen.fill((0, 0, 0))
      self.draw()
      pygame.display.flip()
      if self.option_step <= 0:
        running = False
      clock.tick(60)

    pygame.quit()
