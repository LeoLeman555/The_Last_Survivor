import pygame

class CountDown:
  def __init__(self, run, duration):
    self.run = run
    self.duration = duration
    self.remaining_time = duration
    self.start_time = pygame.time.get_ticks()

  def update(self, pause):
    if not self.is_finished():
      if not pause:
        current_time = pygame.time.get_ticks()  # Get the current time
        elapsed_time = (current_time - self.start_time) // 1000  # Calculate elapsed time in seconds

        if elapsed_time > 0:  # If at least one second has passed
          self.remaining_time -= elapsed_time  # Decrease the remaining time
          self.start_time = current_time  # Reset the start time
      else:
        self.start_time = pygame.time.get_ticks()
    else:
      self.run.rescue_ship.launch_rescue()

  def get_time(self):
    minutes, seconds = divmod(self.remaining_time, 60)
    return f"{minutes}:{seconds:02d}"

  def is_finished(self):
    return self.remaining_time <= 0
  
  def draw(self):
    time_display = self.get_time()
    font = pygame.font.Font("res/texte/dialog_font.ttf", 20)
    text = font.render(time_display, True, (0, 0, 0))
    text_rect = text.get_rect(center=(self.run.WIDTH_SCREEN//2, 20))
    self.run.screen.blit(text, text_rect)
