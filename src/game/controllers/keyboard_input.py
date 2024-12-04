import pygame
import time
import math
from itertools import islice

class KeyboardInput:
  def __init__(self, run):
    """Initialize KeyboardInput with key mappings and game state."""
    self.run = run
    self.commands = dict(islice(self.run.game_data["options"].items(), 7))
    self.key_mappings = self._map_keys()

  def _map_keys(self) -> dict:
    """Map actions to their corresponding pygame key codes."""
    key_map = {}
    for action, key in self.commands.items():
      if not key.startswith("MOUSE"):  # Ignore mouse commands
        key_map[action] = pygame.key.key_code(key)
    return key_map

  def check_input(self):
    """Handle keyboard input for player movement and actions."""
    press = pygame.key.get_pressed()
    
    # Handle player movement
    if press[self.key_mappings["up"]] and press[self.key_mappings["left"]]:
      self.run.player.move_up(1.5, self.run.speed)
      self.run.player.move_left(1.5, self.run.speed)
      self.run.mouvement = [math.ceil(self.run.speed * 1.33), math.ceil(self.run.speed * 1.33)]
    elif press[self.key_mappings["up"]] and press[self.key_mappings["right"]]:
      self.run.player.move_up(1.5, self.run.speed)
      self.run.player.move_right(1.5, self.run.speed)
      self.run.mouvement = [math.ceil(self.run.speed * 1.33) * -1, math.ceil(self.run.speed * 1.33)]
    elif press[self.key_mappings["down"]] and press[self.key_mappings["right"]]:
      self.run.player.move_down(1.5, self.run.speed)
      self.run.player.move_right(1.5, self.run.speed)
      self.run.mouvement = [math.ceil(self.run.speed * 1.33) * -1, math.ceil(self.run.speed * 1.33) * -1]
    elif press[self.key_mappings["down"]] and press[self.key_mappings["left"]]:
      self.run.player.move_down(1.5, self.run.speed)
      self.run.player.move_left(1.5, self.run.speed)
      self.run.mouvement = [math.ceil(self.run.speed * 1.33), math.ceil(self.run.speed * 1.33) * -1]
    elif press[self.key_mappings["up"]]:
      self.run.player.move_up(1, self.run.speed)
      self.run.mouvement = [0, self.run.speed * 2]
    elif press[self.key_mappings["down"]]:
      self.run.player.move_down(1, self.run.speed)
      self.run.mouvement = [0, self.run.speed * -2]
    elif press[self.key_mappings["left"]]:
      self.run.player.move_left(1, self.run.speed)
      self.run.mouvement = [self.run.speed * 2, 0]
    elif press[self.key_mappings["right"]]:
      self.run.player.move_right(1, self.run.speed)
      self.run.mouvement = [self.run.speed * -2, 0]
    else:
      self.run.mouvement = [0, 0]

    # Handle collision effect
    if self.run.collision_caillou:
      self.run.mouvement = [0, 0]

    # Handle grenade launch
    if press[self.key_mappings["launch"]]:
      self._handle_grenade_launch()

  def _handle_grenade_launch(self):
    """Handle the logic for launching grenades."""
    grenade_data = None
    if self.run.data_extras["toxic_grenade"]["activate"]:
      grenade_data = self.run.data_extras["toxic_grenade"]
    elif self.run.data_extras["grenade"]["activate"]:
      grenade_data = self.run.data_extras["grenade"]

    if grenade_data and self.run.mouse["current_time"] - grenade_data["last_shot_time"] > grenade_data["rate"]:
      direction = grenade_data["speed"] * self.run.zoom
      if self.run.mouse["position"][0] > 500:
        self.run.player.launch_grenade(direction, grenade_data)
      else:
        self.run.player.launch_grenade(-direction, grenade_data)
      grenade_data["last_shot_time"] = self.run.mouse["current_time"]

  def get_pause(self):
    """Toggle game pause state."""
    press = pygame.key.get_pressed()
    if press[self.key_mappings["pause"]]:
      self.run.pause = not self.run.pause
      time.sleep(0.1)
