import pygame
from weapon import Bullet, Weapon
from extras import Grenade
from load import Load

class Player(pygame.sprite.Sprite):
  def __init__(self, zoom:int, screen:'pygame.surface.Surface', name:str ="jim", x:int =0, y:int =0):
    super().__init__()
    self.zoom = zoom
    self.screen = screen
    self.sprite_sheet = Load.charge_image(self, 1, "sprite", name, "png")
    self.animation_index = 0
    self.clock = 0
    self.images = {
      'right': self.get_images(0),
      'left': self.get_images(38)
    }
    self.speed = 0
    self.image = self.get_image(0, 0)
    self.image.set_colorkey((0, 0, 0))
    self.rect = self.image.get_rect()

    self.rect_collision = self.rect.copy()
    self.rect_collision.x = 483
    self.rect_collision.y = 262
    self.rect_collision.width = 34
    self.rect_collision.height = 76
    
    self.position = [x, y]
    self.feet = pygame.Rect(0, 0, self.rect.width * 0.4, 10)
    self.old_position = self.position.copy()
    self.attack = 10
    self.bullets = pygame.sprite.Group()
    self.weapons = pygame.sprite.Group()
    self.grenades = pygame.sprite.Group()
    self.explosions = pygame.sprite.Group()

    #TODO change self.ammo_images + his management
    self.ammo_images = {
      1: "res/weapon/ammo1.png",
      2: "res/weapon/ammo1.png",
      3: "res/weapon/ammo2.png",
      4: "res/weapon/ammo3.png",
      5: "res/weapon/ammo1.png",
      6: "res/weapon/ammo4.png",
      7: "lance_flammes",
      8: "res/weapon/ammo1.png",
      9: "res/weapon/ammo5.png",
      10: "res/weapon/ammo6.png",
      11: "res/weapon/ammo6.png",
      12: "res/weapon/ammo1.png",
    }
    self.grenade_image = "res/weapon/ammo5.png"

  def change_animation(self, name:str, speed:int):
    self.speed = speed
    self.image = self.images[name][self.animation_index]
    self.image.set_colorkey((0, 0, 0))
    self.clock += self.speed * 10

    if self.clock >= 100:
      self.animation_index = (self.animation_index + 1) % len(self.images[name])
      self.clock = 0

  def get_images(self, y:int):
    images = []
    for i in range(8):
      x = i * 17
      image = self.get_image(x, y)
      images.append(image)
    return images

  def get_image(self, x:int, y:int):
    image = pygame.Surface([17, 38], pygame.SRCALPHA)
    image.blit(self.sprite_sheet, (0, 0), (x, y, 17, 38))
    return image

  def save_location(self):
    self.old_position = self.position.copy()

  def move_right(self, diagonale:int, speed:int):
    self.change_animation('right', speed)
    self.position[0] += self.speed / diagonale

  def move_left(self, diagonale:int, speed:int):
    self.change_animation('left', speed)
    self.position[0] -= self.speed / diagonale

  def move_up(self, diagonale:int, speed:int):
    if diagonale == 1:
      self.change_animation('right', speed)
    self.position[1] -= self.speed / diagonale

  def move_down(self, diagonale:int, speed:int):
    if diagonale == 1:
      self.change_animation('left', speed)
    self.position[1] += self.speed / diagonale

  def update(self):
    # pygame.draw.rect(self.screen, (0, 0, 0), self.rect_collision)
    self.rect.topleft = self.position
    self.feet.midbottom = self.rect.midbottom

  def move_back(self):
    self.position = self.old_position
    self.rect.topleft = self.position
    self.feet.midbottom = self.rect.midbottom

  def launch_bullet(self, goal:tuple, weapon_id:int, data_weapon:dict):
    ammo_image = self.ammo_images.get(weapon_id)
    weapon_range = data_weapon[weapon_id][3]
    explosive = data_weapon[weapon_id][4] == 1
    self.bullets.add(Bullet(self.screen, self, goal, ammo_image, weapon_range, explosive))

  def display_weapon(self, zoom:int, name:str, size:tuple, position:tuple):
    self.weapons.add(Weapon(zoom, self, name, size, position))

  def launch_grenade(self, speed:int):
    self.grenades.add(Grenade(self.screen, self, self.grenade_image, speed))