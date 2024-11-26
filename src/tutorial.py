import pygame
from load import *

class Introduction:
  def __init__(self):
    pygame.init()
    pygame.font.init()

    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Introduction")
    self.font = pygame.font.Font("res/texte/dialog_font.ttf", 18)
    self.bold_font = pygame.font.Font("res/texte/dialog_font.ttf", 18)  # Police en gras

    self.read_data = ReadData()
    self.load = Load()
    self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
    self.tutorial = self.read_data.read_params("data/tutorial.txt", "tutorial")

    self.FPS = int(self.game_data["options"]["fps"])
    self.text_lines = self.split_text_to_lines(
      list(self.tutorial["introduction"].values()), 900
    )  # Découpe des textes pour tenir dans le cadre
    self.current_line = 0
    self.displayed_text = ""
    self.text_timer = 0
    self.text_speed = 50  # Vitesse d'affichage (lettres par seconde)
    self.line_pause_timer = 0  # Chronomètre pour la pause automatique
    self.line_pause_duration = self.FPS  # 1 seconde de pause (en fonction de la FPS)

    self.pause_lines = [2, 4, 9, 12]  # Indices des lignes où une pause est nécessaire (1-indexé pour correspondre au texte)
    self.pause_timer = 0  # Timer pour la pause
    self.is_paused = False  # Indique si une pause est en cours
    self.finished_text = False  # Indicateur que le texte est complètement affiché

  def split_text_to_lines(self, text_list, max_width):
    """Découpe les textes pour qu'ils tiennent dans la largeur donnée."""
    lines = []
    for text in text_list:
      words = text.split(" ")
      current_line = ""
      for word in words:
        test_line = current_line + word + " "
        if self.font.size(test_line)[0] <= max_width:
          current_line = test_line
        else:
          lines.append(current_line.strip())
          current_line = word + " "
      if current_line:
        lines.append(current_line.strip())
    return lines

  def update(self):
    # Avancer dans l'affichage du texte ou gérer la pause
    if self.is_paused:
      self.pause_timer += 1
      if self.pause_timer >= self.FPS:  # Pause d'une seconde
        self.is_paused = False
        self.pause_timer = 0
        self.current_line += 1
        self.displayed_text = ""
    else:
      if self.current_line < len(self.text_lines):
        current_text = self.text_lines[self.current_line]
        if len(self.displayed_text) < len(current_text):
          self.text_timer += 1
          if self.text_timer >= self.FPS / self.text_speed:
            self.text_timer = 0
            self.displayed_text += current_text[len(self.displayed_text)]
        else:
          # Si la ligne actuelle est complètement affichée et une pause est nécessaire
          if (self.current_line + 1) in self.pause_lines:
            self.is_paused = True
          else:
            self.current_line += 1
            self.displayed_text = ""

    # Vérifier si le texte est complètement affiché
    if self.current_line >= len(self.text_lines):
      self.finished_text = True

  def draw(self):
    # Affichage du texte lettre par lettre
    self.screen.fill((0, 0, 0))
    y_offset = 100  # Départ vertical du texte
    line_height = self.font.size("A")[1] + 5  # Hauteur d'une ligne + espacement

    for i in range(self.current_line):  # Affiche les lignes précédentes
      text_surface = self.font.render(self.text_lines[i], True, (255, 255, 255))
      self.screen.blit(text_surface, (50, y_offset + i * line_height))

    if self.current_line < len(self.text_lines):  # Affiche la ligne actuelle progressivement
      text_surface = self.font.render(self.displayed_text, True, (255, 255, 255))
      self.screen.blit(text_surface, (50, y_offset + self.current_line * line_height))

    # Affichage du message en bas à droite pour passer l'intro si le texte est en train de s'afficher
    if not self.finished_text:
      message = "PRESS SPACE TO SKIP"
      message_surface = self.font.render(message, True, (255, 0, 0))  # Texte rouge
      self.screen.blit(message_surface, (self.screen.get_width() - message_surface.get_width() - 20, 
                                        self.screen.get_height() - 40))  # Positionné en bas à droite

    # Affichage du message à la fin du texte
    if self.finished_text:
      message = "PRESS SPACE TO CONTINUE"
      message_surface = self.font.render(message, True, (255, 0, 0))  # Texte rouge
      self.screen.blit(message_surface, (self.screen.get_width() - message_surface.get_width() - 20, 
                                         self.screen.get_height() - 40))  # Positionné en bas à droite

  def run(self):
    clock = pygame.time.Clock()
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE and self.finished_text:  # Si espace est pressé et texte terminé
            running = False  # Ferme la fenêtre
          elif event.key == pygame.K_SPACE and not self.finished_text:
            self.finished_text = True  # Si l'utilisateur appuie sur espace pendant que le texte est en train de s'écrire
            running = False

      self.update()
      self.draw()
      pygame.display.flip()
      clock.tick(self.FPS)

    pygame.quit()


