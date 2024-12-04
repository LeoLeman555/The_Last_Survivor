import pygame

class Slider:
  """A slider component for selecting values in a range."""
  def __init__(self, x: int, y: int, width: int, min_value: int, max_value: int, initial_value: int):
    self.x = x
    self.y = y
    self.width = width
    self.min_value = min_value
    self.max_value = max_value
    self.value = initial_value

    # Load images for slider bar and handle
    self.bar_image = pygame.image.load("res/options/bar_difficulty.png").convert_alpha()
    self.button_image = pygame.image.load("res/options/button_difficulty.png").convert_alpha()
    self.button_click_image = pygame.image.load("res/options/button_difficulty_click.png").convert_alpha()

    # Resize bar to match the given width
    self.bar_image = pygame.transform.scale(self.bar_image, (self.width, self.bar_image.get_height()))

    # Handle dimensions
    self.handle_width = self.button_image.get_width()
    self.handle_height = self.button_image.get_height()

    # Initial handle position
    self.handle_x = self.x + (self.value - self.min_value) / (self.max_value - self.min_value) * (self.width - self.handle_width)
    self.handle_y = self.y - (self.handle_height - self.bar_image.get_height()) // 2

    self.dragging = False

  def draw(self, screen: pygame.Surface) -> None:
    """Draws the slider bar and handle."""
    screen.blit(self.bar_image, (self.x, self.y))

    # Change handle image if dragging
    handle_image = self.button_click_image if self.dragging else self.button_image
    screen.blit(handle_image, (self.handle_x, self.handle_y))

  def update(self, event: pygame.event.Event) -> None:
    """Updates the slider state based on user input."""
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:  # Left click
        if (self.handle_x <= event.pos[0] <= self.handle_x + self.handle_width and
            self.handle_y <= event.pos[1] <= self.handle_y + self.handle_height):
          self.dragging = True

    elif event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:  # Release left click
        self.dragging = False

    elif event.type == pygame.MOUSEMOTION and self.dragging:
      # Update handle position and slider value
      self.handle_x = max(self.x, min(event.pos[0] - self.handle_width // 2, self.x + self.width - self.handle_width))
      self.value = self.min_value + ((self.handle_x - self.x) / (self.width - self.handle_width)) * (self.max_value - self.min_value)

  def get_value(self) -> int:
    """Returns the current slider value as an integer."""
    return round(self.value)
