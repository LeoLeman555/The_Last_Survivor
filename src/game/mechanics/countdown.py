import pygame

class CountDown:
  def __init__(self, run: object, duration: int):
    """Initialize countdown with a duration and reference to the run object."""
    self.run = run
    self.duration = duration
    self.remaining_time = duration
    self.start_time = pygame.time.get_ticks()

  def update(self, pause: bool) -> None:
    """Update the countdown timer, pause if necessary, and launch rescue when finished."""
    if not self.is_finished():
      if not pause:
        self._update_time()
      else:
        self._reset_start_time()
    else:
      self.run.rescue_ship.launch_rescue()

  def _update_time(self) -> None:
    """Update remaining time based on elapsed seconds."""
    current_time = pygame.time.get_ticks()  # Get the current time
    elapsed_time = (current_time - self.start_time) // 1000  # Calculate elapsed time in seconds

    if elapsed_time > 0:  # If at least one second has passed
      self.remaining_time -= elapsed_time  # Decrease the remaining time
      self.start_time = current_time  # Reset the start time

  def _reset_start_time(self) -> None:
    """Reset start time when the countdown is paused."""
    self.start_time = pygame.time.get_ticks()

  def get_time(self) -> str:
    """Return the formatted countdown time as 'minutes:seconds'."""
    minutes, seconds = divmod(self.remaining_time, 60)
    return f"{minutes}:{seconds:02d}"

  def is_finished(self) -> bool:
    """Return whether the countdown has finished."""
    return self.remaining_time <= 0
  
  def draw(self) -> None:
    """Draw the countdown timer on the screen."""
    time_display = self.get_time()
    font = pygame.font.Font("res/texte/dialog_font.ttf", 20)
    text = font.render(time_display, True, (0, 0, 0))
    text_rect = text.get_rect(center=(self.run.WIDTH_SCREEN//2, 20))
    self.run.screen.blit(text, text_rect)
