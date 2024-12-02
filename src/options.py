import pygame
import time
from itertools import islice
from change_game_data import ChangeGameData
from load import *
from button import *
from reset import *
from slider import *
from tutorial import *

class Options:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Options")
    self.font = pygame.font.Font("res/texte/dialog_font.ttf", 18)
    self.title_font = pygame.font.Font("res/texte/dialog_font.ttf", 25)

    # Initialisation des données du jeu et des commandes par défaut
    self.read_data = ReadData()
    self.load = Load()
    self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
    self.rewards = {"options": self.game_data["options"].copy()}
    self.data_options = self.rewards["options"].copy()
    self.dict_arrows = dict(islice(self.data_options.items(), 7))
    self.dict_options = dict(islice(self.data_options.items(), 7, None))

    self.FPS = int(self.game_data["options"]["fps"])

    self.tutorial = Tutorial()

    #? maybe add new language
    self.possibilities_language = ["english"]
    self.possibilities_fps = ["30", "40", "50", "60"]
    #? maybe implement different screen size => "1024x768", "1280x720", "1920x1080", "2560x1440", "3840x2160"
    self.possibilities_size_screen = ["1000x600"]

    # Slider
    self.slider = Slider(680, 405, 150, 1, 100, int(self.game_data["options"]["difficulty"]))

    # Boutons d'interface
    self.button_return = ReturnButton(
      image_path="res/shop/button_return.png",
      click_image_path="res/shop/button_return_click.png",
      position=(975, 25)
    )
    self.button_arrow = pygame.image.load("res/options/button.png")
    self.button_arrow_click = pygame.image.load("res/options/button_click.png")

    self.button_arrow_red = pygame.image.load("res/options/button_red.png")
    self.button_arrow_red_click = pygame.image.load("res/options/button_red_click.png")

    self.button_arrow_green = pygame.image.load("res/options/button_green.png")
    self.button_arrow_green_click = pygame.image.load("res/options/button_green_click.png")

    # Variables de gestion des entrées
    self.mouse_pos = (0, 0)
    self.mouse_press = False
    self.option_step = 1
    self.last_click_times = [0] * 1
    self.cooldown = 0.5
    self.key_waiting_for_input = None  # Pour détecter quand une commande doit être modifiée
    self.option_waiting_for_input = None

    self.error_message = ""
    self.error_message_start_time = 0
    self.error_display_duration = 3  # Durée d'affichage en secondes

  def display_error_message(self, message):
    self.error_message = message
    self.error_message_start_time = time.time()

  def change_key(self, command_name, new_key):
    self.rewards["options"][command_name] = new_key
    change_game_data = ChangeGameData(self.rewards, True)
    change_game_data.change_params(self.rewards, change_game_data.game_save_data)
    self.update_data()

  def change_option(self):
    change_game_data = ChangeGameData(self.rewards, True)
    change_game_data.change_params(self.rewards, change_game_data.game_save_data)
    self.update_data()

  def handle_key_event(self, event):
    if self.key_waiting_for_input:
      if self.key_waiting_for_input != "shoot":
        new_key = pygame.key.name(event.key).upper()
        self.dict_arrows[self.key_waiting_for_input] = new_key
        self.change_key(self.key_waiting_for_input, new_key)
      else:
        self.display_error_message("MUST BE ASSIGNED TO A MOUSE BUTTON")
      self.key_waiting_for_input = None

  def handle_mouse_event(self, event):
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

  def change_options(self):
    if self.option_waiting_for_input:    
      if self.option_waiting_for_input == "sound" or self.option_waiting_for_input == "music" or self.option_waiting_for_input == "tutorial":
        if self.dict_options[self.option_waiting_for_input] == "off":
          new_key = "on"
        else:
          new_key = "off"

      elif self.option_waiting_for_input == "fps":
        current_fps = self.dict_options[self.option_waiting_for_input]
        current_index = self.possibilities_fps.index(current_fps)
        next_index = (current_index + 1) % len(self.possibilities_fps)
        new_key = self.possibilities_fps[next_index]

      elif self.option_waiting_for_input == "language":
        current_language = self.dict_options[self.option_waiting_for_input]
        current_index = self.possibilities_language.index(current_language)
        next_index = (current_index + 1) % len(self.possibilities_language)
        new_key = self.possibilities_language[next_index]

      elif self.option_waiting_for_input == "screen size":
        current_size_screen = self.dict_options[self.option_waiting_for_input]
        current_index = self.possibilities_size_screen.index(current_size_screen)
        next_index = (current_index + 1) % len(self.possibilities_size_screen)
        new_key = self.possibilities_size_screen[next_index]
      
      self.change_key(self.option_waiting_for_input, new_key)
      self.option_waiting_for_input = None

    # Mise à jour de la difficulté en fonction du slider
    new_difficulty = self.slider.get_value()  # Récupère la nouvelle valeur
    if str(self.dict_options["difficulty"]) != str(new_difficulty):
        self.dict_options["difficulty"] = str(new_difficulty)  # Met à jour localement
        self.rewards["options"]["difficulty"] = str(new_difficulty)  # Met à jour les données sauvegardées
        self.change_key("difficulty", str(new_difficulty))  # Sauvegarde la modification

  def update(self):
    self.press_buttons()

  def press_buttons(self):
    current_time = time.time()
    return_button_index = 0
    if self.button_return.is_pressed(self.mouse_pos, self.mouse_press):
      if current_time - self.last_click_times[return_button_index] > self.cooldown:
        self.option_step = 0 if self.option_step == 1 else 1
        self.last_click_times[return_button_index] = current_time

  def reset_button(self):
    rect_width = 175
    rect_height = 35

    button1_image = self.button_arrow_red_click if self.get_button_rect((875, 550), rect_width, rect_height).collidepoint(self.mouse_pos) else self.button_arrow_red
    button1 = pygame.transform.scale(button1_image, (rect_width, rect_height))
    button1_rect = button1.get_rect(center=(875, 550))
    self.screen.blit(button1, button1_rect)

    text1 = self.font.render("RESET GAME", True, (255, 255, 255))
    text1_rect = text1.get_rect(center=(875, 550))
    self.screen.blit(text1, text1_rect)

    current_time = time.time()
    if self.mouse_press and button1_rect.collidepoint(self.mouse_pos):
      if current_time - self.last_click_times[0] > self.cooldown:
        self.last_click_times[0] = current_time
        self.delete_data()

  def delete_data(self):
    # Variables pour gérer l'état de confirmation
    confirmation_visible = True

    while confirmation_visible:
      self.mouse_pos = pygame.mouse.get_pos()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          confirmation_visible = False  # Fermer la fenêtre
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.mouse_press = True
        elif event.type == pygame.MOUSEBUTTONUP:
          self.mouse_press = False

      # Dessiner l'écran de confirmation
      self.screen.fill((0, 0, 0))  # Fond noir

      message_text = self.font.render("ARE YOU SURE YOU WANT TO RESET YOUR PROGRESS?", True, (255, 255, 255))
      message_rect = message_text.get_rect(center=(500, 250))
      self.screen.blit(message_text, message_rect)

      yes_rect = self.get_button_rect((400, 350), 150, 50)
      yes_image = self.button_arrow_green_click if yes_rect.collidepoint(self.mouse_pos) else self.button_arrow_green
      yes_button = pygame.transform.scale(yes_image, (150, 50))
      self.screen.blit(yes_button, yes_rect)
      yes_text = self.font.render("YES", True, (255, 255, 255))
      yes_text_rect = yes_text.get_rect(center=yes_rect.center)
      self.screen.blit(yes_text, yes_text_rect)

      no_rect = self.get_button_rect((600, 350), 150, 50)
      no_image = self.button_arrow_red_click if no_rect.collidepoint(self.mouse_pos) else self.button_arrow_red
      no_button = pygame.transform.scale(no_image, (150, 50))
      self.screen.blit(no_button, no_rect)
      no_text = self.font.render("NO", True, (255, 255, 255))
      no_text_rect = no_text.get_rect(center=no_rect.center)
      self.screen.blit(no_text, no_text_rect)

      if self.mouse_press:
        if yes_rect.collidepoint(self.mouse_pos):
          reset_game_save(self.game_data)  # Reset les données
          time.sleep(0.5)
          self.update_data()
          print("-------- Your progress has been reinitialized ---------")
          confirmation_visible = False
        elif no_rect.collidepoint(self.mouse_pos):
          print("Action cancelled.")
          confirmation_visible = False

      pygame.display.flip()
      pygame.time.Clock().tick(self.FPS)

  def get_button_rect(self, center, width, height):
    button_rect = pygame.Rect(0, 0, width, height)
    button_rect.center = center
    return button_rect

  def draw(self):
    self.button_return.draw(self.screen, self.mouse_pos)

    self.slider.draw(self.screen)

    title_text = self.title_font.render("SETTINGS", True, (255, 255, 255))
    title_text_rect = title_text.get_rect()
    title_text_rect.center = (500, 30)
    self.screen.blit(title_text, title_text_rect)
    pygame.draw.line(self.screen, (255, 255, 255), (450, 45), (575, 45))

    self.draw_arrow_command()
    self.draw_options()

    # Affiche le message d'erreur si nécessaire
    if self.error_message:
      elapsed_time = time.time() - self.error_message_start_time
      if elapsed_time < self.error_display_duration:
        error_text = self.font.render(self.error_message, True, (255, 0, 0))
        error_text_rect = error_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(error_text, error_text_rect)
      else:
        self.error_message = ""  # Réinitialise le message après la durée d'affichage

  def draw_options(self):
    rect_width = 130
    rect_height = 30
    x_offset = 10

    text = self.font.render("OPTIONS", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (700, 100)
    self.screen.blit(text, text_rect)
    pygame.draw.line(self.screen, (255, 255, 255), (665, 110), (750, 110))

    for i, name in enumerate(self.dict_options.keys(), start=0):
      element = self.dict_options[name]
      name_text = self.font.render(name.upper() + " :", True, (255, 255, 255))
      name_text_rect = name_text.get_rect()
      name_text_rect.topright = (670, 50 * i + 150)
      self.screen.blit(name_text, name_text_rect)

      key_display_text = "" if self.option_waiting_for_input == name else str(element)
      text = self.font.render(key_display_text.upper(), True, (255, 255, 255))
      text_rect = text.get_rect()
      button_rect = pygame.Rect(name_text_rect.right + x_offset, name_text_rect.top - 2, rect_width, rect_height)
      text_rect.center = button_rect.center

      if name == "music" or name == "sound" or name == "tutorial":
        if element == "on":
          button_image = self.button_arrow_green_click if button_rect.collidepoint(self.mouse_pos) else self.button_arrow_green
          
          if name != "tutorial":
            text_error = self.font.render("SOUND AND MUSIC NOT YET IMPLEMENTED", True, (0, 255, 0))
            text_error_rect = text_error.get_rect()
            text_error_rect.center = (500, 550)
            self.screen.blit(text_error, text_error_rect)

        elif element == "off":
          button_image = self.button_arrow_red_click if button_rect.collidepoint(self.mouse_pos) else self.button_arrow_red
      
      else:
          button_image = self.button_arrow_click if button_rect.collidepoint(self.mouse_pos) else self.button_arrow

      button_arrow = pygame.transform.scale(button_image, (rect_width, rect_height))
      
      if name == "difficulty":
        pass

      else:
        self.screen.blit(button_arrow, button_rect)
        self.screen.blit(text, text_rect)
      
        current_time = time.time()
        if current_time - self.last_click_times[0] > self.cooldown:
          if button_rect.collidepoint(self.mouse_pos) and self.mouse_press:
            self.option_waiting_for_input = name
            self.last_click_times[0] = current_time

  def draw_arrow_command(self):
    rect_width = 130
    rect_height = 30
    x_offset = 10

    text = self.font.render("CONTROLS", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (300, 100)
    self.screen.blit(text, text_rect)
    pygame.draw.line(self.screen, (255, 255, 255), (265, 110), (355, 110))

    for i, name in enumerate(self.dict_arrows.keys(), start=0):
      element = self.dict_arrows[name]
      name_text = self.font.render(name.upper() + " :", True, (255, 255, 255))
      name_text_rect = name_text.get_rect()
      name_text_rect.topright = (250, 50 * i + 150)
      self.screen.blit(name_text, name_text_rect)

      key_display_text = "" if self.key_waiting_for_input == name else str(element)
      text = self.font.render(key_display_text, True, (255, 255, 255))
      text_rect = text.get_rect()
      button_rect = pygame.Rect(name_text_rect.right + x_offset, name_text_rect.top - 2, rect_width, rect_height)
      text_rect.center = button_rect.center
      button_image = self.button_arrow_click if button_rect.collidepoint(self.mouse_pos) else self.button_arrow
      button_arrow = pygame.transform.scale(button_image, (rect_width, rect_height))
      self.screen.blit(button_arrow, button_rect)
      self.screen.blit(text, text_rect)
      if button_rect.collidepoint(self.mouse_pos) and self.mouse_press:
        self.key_waiting_for_input = name

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
          if self.key_waiting_for_input:
            self.handle_mouse_event(event)  # Appel pour changement de bouton de souris
        elif event.type == pygame.MOUSEBUTTONUP:
          self.mouse_press = False
        elif event.type == pygame.KEYDOWN:
          if self.key_waiting_for_input:
            self.handle_key_event(event)

        self.slider.update(event)

      self.update()

      self.change_options()
      
      self.screen.fill((0, 0, 0))
      self.reset_button()
      self.draw()
      if self.game_data["options"]["tutorial"] == "on":
        self.tutorial.draw_options(self.screen)
      pygame.display.flip()

      if self.option_step <= 0:
        running = False

      clock.tick(self.FPS)

    pygame.quit()

  def update_data(self):
    self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
    self.rewards = {"options": self.game_data["options"].copy()}
    self.data_options = self.rewards["options"].copy()
    self.dict_arrows = dict(islice(self.data_options.items(), 7))
    self.dict_options = dict(islice(self.data_options.items(), 7, None))

    self.FPS = int(self.game_data["options"]["fps"])