import pygame
import math
import time

class KeyboardInput:
  def __init__(self, run):
    self.run = run
    self.commands = self.run.game_data["options"]
    self.key_mappings = self._map_keys()

  def _map_keys(self):
    # todo faire pour tirer du mouse1, 2, 3 ou 4, ou 5
    key_map = {}
    for action, key in self.commands.items():
      if not key.startswith("MOUSE"):  # Exclure les commandes de souris ici
        key_map[action] = pygame.key.key_code(key)
    return key_map

  def check_input(self):
    press = pygame.key.get_pressed()

    # Mouvement du joueur
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

    # Gestion de collision
    if self.run.collision_caillou:
      self.run.mouvement = [0, 0]

    # Lancer de grenade
    if press[self.key_mappings["launch"]]:
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

    if press[pygame.K_g]:
      self.run.manager.launch_power_up()

  def get_pause(self):
    press = pygame.key.get_pressed()
    if press[self.key_mappings["pause"]]:
      self.run.pause = not self.run.pause
      time.sleep(0.1)
