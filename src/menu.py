import pygame
import ast
import time
from reset import *

class MenuPrincipal:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Main Menu")
    self.direction = None
    # ["jeu", "intro", "boutique", "elements", "options"]
    self.buttons = ["jeu"]
    self.icon_names = ["energy", "metal", "data"]
    self.running = True

    # Charger les images des boutons et obtenir leurs rectangles
    self.images = {name: self.load_button_image(name) for name in self.buttons}
    self.rects = {name: self.images[name].get_rect() for name in self.buttons}

    # Positionner les images des boutons
    for i, name in enumerate(self.buttons):
      self.rects[name].centerx = self.screen.get_width() // 2
      self.rects[name].centery = self.screen.get_height() // 2 + i * (self.rects[name].height + 20) - 2 * self.rects[name].height

    # Charger les données du jeu et les icônes
    self.game_data = self.read_params("data/game_save.txt", "game_save")
    self.icon_numbers = [self.game_data["resource"]["energy"], self.game_data["resource"]["metal"], self.game_data["resource"]["data"]]
    self.icons = {name: pygame.image.load(f"res/sprite/{name}_icon.png") for name in self.icon_names}
    self.icon_rects = {name: self.icons[name].get_rect() for name in self.icon_names}

    # Positionner les icônes
    for i, name in enumerate(self.icon_names):
      self.icon_rects[name].x = 15
      self.icon_rects[name].y = 20 + i * 30

    # Initialiser la police pour les nombres
    self.font = pygame.font.Font("res/texte/dialog_font.ttf", 18)

  def load_button_image(self, name):
    image = pygame.image.load(f"res/menu/{name}.png")
    return pygame.transform.scale(image, (image.get_width() + 20, image.get_height()))

  def read_params(self, filepath: str, prefix: str):
    """Méthode générique pour lire tout fichier de paramètres."""
    with open(filepath, 'r') as file:
      content = file.read()
    real_prefix = prefix.upper()
    content = content.replace(f"{real_prefix}_PARAMS = ", "", 1)
    return ast.literal_eval(content)

  def afficher_menu(self):
    # Afficher l'arrière-plan
    self.screen.blit(pygame.image.load("res/menu/background.jpg"), (0, 0))

    # Afficher les boutons
    for name in self.buttons:
      self.screen.blit(self.images[name], self.rects[name])

    # Afficher les icônes avec les nombres à côté
    for i, name in enumerate(self.icon_names):
      self.screen.blit(self.icons[name], self.icon_rects[name])
      number_text = self.font.render(str(self.icon_numbers[i]), True, (255, 255, 255))
      self.screen.blit(number_text, (self.icon_rects[name].x + 30, self.icon_rects[name].y - 2))

    pygame.display.flip()  # Mise à jour de l'affichage

  def run(self):
    # Boucle principale du menu
    while self.running:
      self.afficher_menu()

      press = pygame.key.get_pressed()
      if press[pygame.K_BACKSPACE]:
        self.delete_data()

      # Gestion des événements
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          # Vérifier si un bouton a été cliqué
          for name in self.buttons:
            if self.rects[name].collidepoint(event.pos):
              self.direction = name
              self.running = False
              break

    return self.direction
  
  def delete_data(self):
    self.running = False
    pygame.quit()
    question = input("Are you sure you want to delete your progress? (Yes / No) -- ").upper()
    if question == "YES":
      reset_game_save(self.game_data)  # Reset les données
      time.sleep(0.5)
      print("-------- Your progress has been reinitialized ---------")

    self.game_data = self.read_params("data/game_save.txt", "game_save")  # Recharger les nouvelles données
    self.icon_numbers = [self.game_data["resource"]["energy"], self.game_data["resource"]["metal"], self.game_data["resource"]["data"]]
      
    self.running = True
    self.__init__()
    self.run()
