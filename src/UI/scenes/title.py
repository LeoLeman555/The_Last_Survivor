import pygame
import time

class TitleScreen:
  def __init__(self, screen):
    """Initialisation avec partage d'écran."""
    self.screen = screen
    
    # Chargement de la police
    self.base_font_size = 100  # Taille initiale pour les mots séparés
    self.impact_font_size = 150  # Taille lors de l'impact
    self.impact_color = (38, 255, 186)  # Couleur de l'impact
    self.bg_color = (0, 0, 0)  # Couleur de fond
    
    self.words = ["THE", "LAST", "SURVIVOR"]  # Les trois mots à afficher

  def draw_text(self, text, font_size, position, color):
    """Dessine un texte centré sur la position donnée."""
    font = pygame.font.Font("res/texte/dialog_font.ttf", font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    self.screen.blit(text_surface, text_rect)

  def hammer_effect(self, word, position):
    """Effet de marteau : apparition avec un impact rapide."""
    # Impact rapide (grand et rouge)
    self.screen.fill(self.bg_color)
    self.draw_text(word, self.impact_font_size, position, (38, 255, 186))
    pygame.display.flip()
    time.sleep(0.1)  # Pause pour l'effet

    # Réduction à la taille normale
    self.screen.fill(self.bg_color)
    self.draw_text(word, self.base_font_size, position, (255, 255, 255))
    pygame.display.flip()
    time.sleep(0.6)  # Pause pour rester affiché

    # Disparition
    self.screen.fill(self.bg_color)
    pygame.display.flip()
    time.sleep(0.2)

  def display_title(self):
    """Affiche les mots séquentiellement avec effet de marteau."""
    center_position = (self.screen.get_width() // 2, self.screen.get_height() // 2)
    for word in self.words[:-1]:
      self.hammer_effect(word, center_position)

    self.hammer_effect(self.words[-1], center_position)
  def run(self):
    """Boucle principale pour exécuter l'animation."""
    self.display_title()
