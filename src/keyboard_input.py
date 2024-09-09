import pygame
import math

class KeyboardInput:
  def __init__(self, run):
    self.run = run

  def check_input(self):
    press = pygame.key.get_pressed()

    if press[pygame.K_w] and press[pygame.K_a]:
      self.run.player.move_up(1.5, self.run.speed)
      self.run.player.move_left(1.5, self.run.speed)
      self.run.mouvement = [math.ceil(self.run.speed*1.33), math.ceil(self.run.speed*1.33)]
    elif press[pygame.K_w] and press[pygame.K_d]:
      self.run.player.move_up(1.5, self.run.speed)
      self.run.player.move_right(1.5, self.run.speed)
      self.run.mouvement = [math.ceil(self.run.speed*1.33)*-1, math.ceil(self.run.speed*1.33)]
    elif press[pygame.K_s] and press[pygame.K_d]:
      self.run.player.move_down(1.5, self.run.speed)
      self.run.player.move_right(1.5, self.run.speed)
      self.run.mouvement = [math.ceil(self.run.speed*1.33)*-1, math.ceil(self.run.speed*1.33)*-1]
    elif press[pygame.K_s] and press[pygame.K_a]:
      self.run.player.move_down(1.5, self.run.speed)
      self.run.player.move_left(1.5, self.run.speed)
      self.run.mouvement = [math.ceil(self.run.speed*1.33), math.ceil(self.run.speed*1.33)*-1]
    elif press[pygame.K_w]:
      self.run.player.move_up(1, self.run.speed)
      self.run.mouvement = [0, self.run.speed*2]
    elif press[pygame.K_s]:
      self.run.player.move_down(1, self.run.speed)
      self.run.mouvement = [0, self.run.speed*-2]
    elif press[pygame.K_a]:
      self.run.player.move_left(1, self.run.speed)
      self.run.mouvement = [self.run.speed*2, 0]
    elif press[pygame.K_d]:
      self.run.player.move_right(1, self.run.speed)
      self.run.mouvement = [self.run.speed*-2, 0]
    else:
      self.run.mouvement = [0, 0]
    
    if self.run.collision_caillou:
      self.run.mouvement = [0, 0]

    if press[pygame.K_SPACE]:
      if self.run.data_extras["toxic_grenade"]["activate"] == True:
        if self.run.mouse["current_time"] - self.run.data_extras["toxic_grenade"]["last_shot_time"] > self.run.data_extras["toxic_grenade"]["rate"]:
          if self.run.mouse["position"][0] > 500:
            self.run.player.launch_grenade(self.run.data_extras["toxic_grenade"]["speed"]*self.run.zoom, self.run.data_extras["toxic_grenade"])
          else:
            self.run.player.launch_grenade(-self.run.data_extras["toxic_grenade"]["speed"]*self.run.zoom, self.run.data_extras["toxic_grenade"])
          self.run.data_extras["toxic_grenade"]["last_shot_time"] = self.run.mouse["current_time"]
      elif self.run.data_extras["grenade"]["activate"] == True and self.run.mouse["current_time"] - self.run.data_extras["grenade"]["last_shot_time"] > self.data_extras["grenade"]["rate"]:
        if self.run.mouse["position"][0] > 500:
          self.run.player.launch_grenade(self.run.data_extras["grenade"]["speed"]*self.run.zoom, self.run.data_extras["grenade"])
        else:
          self.run.player.launch_grenade(-self.run.data_extras["grenade"]["speed"]*self.run.zoom, self.run.data_extras["grenade"])
        self.run.data_extras["grenade"]["last_shot_time"] = self.run.mouse["current_time"]