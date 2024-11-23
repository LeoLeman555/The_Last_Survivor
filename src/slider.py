import pygame

class Slider:
  def __init__(self, x, y, width, min_value, max_value, initial_value):
    self.x = x
    self.y = y
    self.width = width
    self.min_value = min_value
    self.max_value = max_value
    self.value = initial_value

    self.bar_image = pygame.image.load("res/options/bar_difficulty.png").convert_alpha()
    self.button_image = pygame.image.load("res/options/button_difficulty.png").convert_alpha()
    self.button_click_image = pygame.image.load("res/options/button_difficulty_click.png").convert_alpha()

    # Redimensionner la barre pour correspondre à la largeur donnée
    self.bar_image = pygame.transform.scale(self.bar_image, (self.width, self.bar_image.get_height()))

    # Dimensions du bouton
    self.handle_width = self.button_image.get_width()
    self.handle_height = self.button_image.get_height()

    # Calcul de la position initiale du bouton
    self.handle_x = self.x + (self.value - self.min_value) / (self.max_value - self.min_value) * (self.width - self.handle_width)
    self.handle_y = self.y - (self.handle_height - self.bar_image.get_height()) // 2

    self.dragging = False

  def draw(self, screen):
    screen.blit(self.bar_image, (self.x, self.y))

    if self.dragging:
      screen.blit(self.button_click_image, (self.handle_x, self.handle_y))
    else:
      screen.blit(self.button_image, (self.handle_x, self.handle_y))

  def update(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:  # Clique gauche
        if (self.handle_x <= event.pos[0] <= self.handle_x + self.handle_width and
            self.handle_y <= event.pos[1] <= self.handle_y + self.handle_height):
          self.dragging = True

    elif event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:  # Relâchement du clique gauche
        self.dragging = False

    elif event.type == pygame.MOUSEMOTION:
      if self.dragging:
        self.handle_x = max(self.x, min(event.pos[0] - self.handle_width // 2, self.x + self.width - self.handle_width))
        self.value = self.min_value + ((self.handle_x - self.x) / (self.width - self.handle_width)) * (self.max_value - self.min_value)

  def get_value(self):
    return round(self.value)