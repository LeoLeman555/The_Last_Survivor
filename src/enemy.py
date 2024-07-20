import pygame, random, math
from read_data import ReadData

class Enemy(pygame.sprite.Sprite):
  def __init__(self, zoom, screen:'pygame.surface.Surface', name:str, animations:dict, size:float, x:int, y:int, speed:int, life:int =100):
    super().__init__()
    self.zoom = zoom
    self.screen = screen
    self.x = x
    self.y = y
    self.name = name
    self.animations = animations
    self.size = size
    self.life = life
    self.current_animation = self.animations["idle"]
    self.frame_index = 0
    self.image = self.current_animation[self.frame_index]
    self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.size*0.5*self.zoom, self.image.get_height()*self.size*0.5*self.zoom))
    self.rect = self.image.get_rect(topleft=(self.x, self.y))
    self.animation_time = 0
    self.is_alive = True
    self.facing_left = False
    self.speed = speed

  def update(self, dt:int, x_var:int, y_var:int, player_rect:'pygame.Rect', bullets_rect:list):
    x = (x_var/2) * self.zoom
    y = (y_var/2) * self.zoom
    self.x += x
    self.y += y
    self.rect = self.image.get_rect(topleft=(self.x, self.y))
    self.check_collision(player_rect, bullets_rect)

    if not self.is_alive and self.frame_index == len(self.current_animation) - 1:
      return
    self.animation_time += dt
    if self.animation_time >= 0.1:
      self.animation_time = 0
      self.frame_index = (self.frame_index + 1) % len(self.current_animation)
      self.image = self.current_animation[self.frame_index]
      self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.size*0.5*self.zoom, self.image.get_height()*self.size*0.5*self.zoom))
      if self.facing_left:
        self.image = pygame.transform.flip(self.image, True, False)
    
  def draw(self, screen:'pygame.surface.Surface'):
    # pygame.draw.rect(screen, (0, 0, 0), self.rect)
    screen.blit(self.image, (self.x, self.y))

  def move(self, dx:int, dy:int):
    self.x += dx
    self.y += dy
    self.rect.topleft = (self.x, self.y)
    self.set_animation("move")
    self.facing_left = dx < 0

  def attack(self):
    self.set_animation("attack")

  def damage(self, damage:int):
    self.life -= damage
    print(self.life)
    if self.life <= 0:
      self.die()

  def die(self):
    self.is_alive = False
    self.kill()

  def set_animation(self, animation:str):
    if self.current_animation != self.animations[animation]:
      self.current_animation = self.animations[animation]
      self.frame_index = 0

  def follow(self, player_x:int, player_y:int):
    direction = pygame.Vector2(player_x - self.x, player_y - self.y)
    distance = direction.length()
    if distance > 0:
      if random.randint(0, 1) >= 0.5:
        angle_deviation = random.uniform(-math.pi / 6, math.pi / 6)  # déviation de +/- 30 degrés
        direction.rotate_ip(math.degrees(angle_deviation))

      direction.normalize_ip()
      self.x += direction.x * self.speed
      self.y += direction.y * self.speed
      self.rect.topleft = (self.x, self.y)
      self.set_animation("move")
      self.facing_left = direction.x < 0

  def check_collision(self, player_rect:'pygame.Rect', bullets_rect:list):
    if self.rect.colliderect(player_rect):
      self.die()

  def load_animations(self, sprite_sheet_path:str, animation_specs):
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    animations = {name: self.get_frames(sprite_sheet, *spec) for name, spec in animation_specs.items()}
    return animations

  def get_frames(self, sprite_sheet:'pygame.surface.Surface', row:int, num_frames:int, size_w:int, size_h:int):
    frames = []
    for i in range(num_frames):
      frame = sprite_sheet.subsurface((i * size_w, row * size_h, size_w, size_h))
      frame = frame.copy()
      frame = frame.subsurface(frame.get_bounding_rect())
      frames.append(frame)
    return frames

class Shardsoul(Enemy):
  def __init__(self, zoom:int, screen:'pygame.surface.Surface', x:int, y:int, speed:int =3):
    animation_specs = ReadData.read_animation_specs("data/shardsoul_animations.txt")
    animations = self.load_animations("res/enemy/shardsoul.png", animation_specs)
    super().__init__(zoom, screen, "shardsoul", animations, 2, x, y, speed/zoom)

class Sprout(Enemy):
  def __init__(self, zoom:int, screen:'pygame.surface.Surface', x:int, y:int, speed:int =5):
    animation_specs = ReadData.read_animation_specs("data/sprout_animations.txt")
    animations = self.load_animations("res/enemy/sprout.png", animation_specs)
    super().__init__(zoom, screen, "sprout", animations, 2, x, y, speed/zoom)

class Worm(Enemy):
  def __init__(self, zoom:int, screen:'pygame.surface.Surface', x:int, y:int, speed:int =5):
    animation_specs = ReadData.read_animation_specs("data/worm_animations.txt")
    animations = self.load_animations("res/enemy/worm.png", animation_specs)
    super().__init__(zoom, screen, "worm", animations, 1.5, x, y, speed/zoom)

class Wolf(Enemy):
  def __init__(self, zoom:int, screen:'pygame.surface.Surface', x:int, y:int, speed:int =5):
    animation_specs = ReadData.read_animation_specs("data/wolf_animations.txt")
    animations = self.load_animations("res/enemy/wolf.png", animation_specs)
    super().__init__(zoom, screen, "wolf", animations, 1.5, x, y, speed/zoom)

class Robot(Enemy):
  def __init__(self, zoom:int, screen:'pygame.surface.Surface', x:int, y:int, speed:int =5):
    animation_specs = ReadData.read_animation_specs("data/robot_animations.txt")
    animations = self.load_animations("res/enemy/robot.png", animation_specs)
    super().__init__(zoom, screen, "robot", animations, 1.5, x, y, speed/zoom)