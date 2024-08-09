import pygame

class Message(pygame.sprite.Sprite):
  def __init__(self, text: str, start_position: list, end_position: list, color: tuple, font_size: int, duration: int):
    super().__init__()
    self.text = text
    self.start_position = start_position
    self.end_position = end_position
    self.color = color
    self.font_size = font_size
    self.duration = duration
    self.start_time = pygame.time.get_ticks()
    self.font = pygame.font.Font(None, font_size)
    self.image = self.font.render(text, True, color)
    self.rect = self.image.get_rect(center=start_position)
  
  def update(self):
    """Update the text sprite's position and appearance."""
    elapsed_time = pygame.time.get_ticks() - self.start_time
    if elapsed_time >= self.duration:
      self.kill()  # Remove the sprite after the effect is finished
      return

    progress = elapsed_time / self.duration

    # Calculate intermediate position for the movement effect
    current_x = self.start_position[0] + (self.end_position[0] - self.start_position[0]) * progress
    current_y = self.start_position[1] + (self.end_position[1] - self.start_position[1]) * progress
    self.rect.center = (current_x, current_y)

    # Apply transparency effect
    alpha = int(255 * (1 - progress))  # Alpha goes from 255 to 0
    self.image.set_alpha(alpha)

    self.rect = self.image.get_rect(center=(current_x, current_y))

  def draw(self, screen: 'pygame.surface.Surface'):
    screen.blit(self.image, self.rect)