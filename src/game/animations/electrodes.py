import pygame
import random

class ElectrodesManager:
  """Manage the animations of "electrodes" and their behavior."""
  def __init__(self, run):
    self.run = run
    self.background = pygame.image.load("res/power_up/background.png").convert_alpha()
    self.background = pygame.transform.scale(self.background, (1000, 600))
    self.background_rect = self.background.get_rect()
    
    # Load frames for the animation from a sprite sheet
    self.frames = self.run.load.load_frames_from_row(
      pygame.image.load("res/animations/electrodes.png").convert_alpha(),
      292, 292, num_frames=7, row=0, scale_size=(40, 40)
    )
    
    self.animations = []
    self.running = False
    self.spawn_rate = 5
    self.max_delay = 10
    self.num_animations = 5
    self.looping = True

  def _create_animations(self):
    """Create a set of initial animations with random delays."""
    for _ in range(self.num_animations):
      delay = random.uniform(0, 10 * self.max_delay)
      self.animations.append(ElectrodeAnimation(delay, self.frames))

  def update(self):
    """Update the state of all animations."""
    if self.running:
      for animation in self.animations:
        animation.update()
      
      # Remove animations that have finished
      self.animations = [anim for anim in self.animations if not anim.finished]
      
      # If in looping mode, ensure animations keep spawning
      if self.looping:
        while len(self.animations) < self.num_animations * self.spawn_rate:
          delay = random.uniform(0, 10 * self.max_delay)
          self.animations.append(ElectrodeAnimation(delay, self.frames))

  def draw(self, screen):
    """Draw the background and all active animations on the screen."""
    if self.animations:  # Draw background only if there are active animations
      screen.blit(self.background, self.background_rect)
    for animation in self.animations:
      animation.draw(screen)

  def stop(self):
    """Stop all animations and clear the list of active animations."""
    self.running = False
    self.animations = []

  def start(self):
    """Start or resume animations."""
    if not self.running:
      self.running = True
      self._create_animations()

class ElectrodeAnimation:
  """Represent an individual electrode animation with random delays and image updates."""
  def __init__(self, delay, frames):
    self.position = (random.randint(50, 1000 - 50), random.randint(50, 600 - 50))
    self.frames = frames
    self.delay = delay
    self.current_frame = 0
    self.timer = 0
    self.finished = False

  def update(self):
    """Update the animation's state by advancing frames once the delay is passed."""
    if self.timer >= self.delay:
      self.current_frame += 1
      if self.current_frame >= len(self.frames):
        self.finished = True
    else:
      self.timer += 1

  def draw(self, surface):
    """Draw the current frame of the animation on the provided surface."""
    if self.timer >= self.delay and not self.finished:
      frame = self.frames[self.current_frame]
      rect = frame.get_rect(center=self.position)
      surface.blit(frame, rect)
