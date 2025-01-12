import pygame
import random

class Shooter:
  def __init__(self, run):
    self.run = run

  def test_shooting(self):
    """Manages player shots"""
    # Handle shooting
    if self.can_shoot():
      self.shoot()
      self.update_shot_state()
    
    # Handle reloading
    elif self.run.current_shot >= self.run.current_weapon_dict["charger_capacity"]:
      self.handle_reload()

  def can_shoot(self):
    """Check if the player can shoot"""
    return (self.run.mouse["press"] and 
            self.run.mouse["active_click"] and 
            self.run.current_shot < self.run.current_weapon_dict["charger_capacity"] and
            self.run.mouse["current_time"] - self.run.last_shot_time > self.run.mouse["shoot_delay"])

  def update_shot_state(self):
    """Update the state after shooting"""
    self.run.current_shot += self.run.current_weapon_dict["number_shoot"]
    self.run.last_shot_time = self.run.mouse["current_time"]

  def handle_reload(self):
    """Handle the reloading process"""
    if self.run.time >= self.run.current_weapon_dict["recharge_time"]:
      self.run.current_shot = 0
      self.run.icon.resource["ammo"] -= self.run.current_weapon_dict["charger_capacity"]
      self.run.time = 0
    else:
      self.run.time += 1
      self.draw_reload_bar()

  def shoot(self):
    """Perform the shooting action"""
    if self.run.current_weapon_dict["type"] == "flamethrower":
      self.run.player.add_fire(self.run.current_weapon_dict)

    elif self.can_shoot():
      if self.run.current_weapon_dict["type"] == "grenade_launcher":
        self.launch_grenade()

      else:
        self.launch_bullets()
        
      self.run.last_shot_time = self.run.mouse["current_time"]

  def launch_grenade(self):
    """Launch a grenade"""
    direction = 1 if self.run.mouse["position"][0] > 500 else -1
    self.run.player.launch_grenade(direction * self.run.zoom, self.run.data_extras["grenade"])

  def launch_bullets(self):
    """Launch bullets"""
    if self.run.current_weapon_dict["delay"] == 0:
      for position in range(-30, 10, 3):
        self.run.player.launch_bullet(
          (self.run.mouse["position"][0] + position, self.run.mouse["position"][1] + position),
          self.run.current_weapon_dict
        )
    else:
      for delay in range(0, self.run.current_weapon_dict["number_shoot"], self.run.current_weapon_dict["delay"]):
        x_offset = random.randint(-self.run.current_weapon_dict["precision"], self.run.current_weapon_dict["precision"])
        y_offset = random.randint(-self.run.current_weapon_dict["precision"], self.run.current_weapon_dict["precision"])
        self.run.player.launch_bullet(
          (self.run.mouse["position"][0] + x_offset, self.run.mouse["position"][1] + y_offset),
          self.run.current_weapon_dict, delay
        )

  def draw_reload_bar(self):
    """Draw the reload progress bar"""
    bar_width = 50 * self.run.zoom
    bar_height = 2 * self.run.zoom
    bar_x = 500 - bar_width / 2
    bar_y = 300 + bar_width / 2
    reload_progress = self.run.time / self.run.current_weapon_dict["recharge_time"]
    fill_width = int(bar_width * reload_progress)
    pygame.draw.rect(self.run.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(self.run.screen, (255, 255, 255), (bar_x, bar_y, fill_width, bar_height))