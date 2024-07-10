import pygame, random, math

class Enemy(pygame.sprite.Sprite):
  def __init__(self, screen, x, y):
    super().__init__()
    self.screen = screen
    self.x = x
    self.y = y
    self.sprite_sheet = pygame.image.load("res/enemy/shardsoul.png").convert_alpha()
    self.load_animations()
    self.current_animation = self.animations["idle"]
    self.frame_index = 0
    self.image = self.current_animation[self.frame_index]
    self.image = pygame.transform.scale(self.image, (64, 64))
    self.rect = self.image.get_rect(topleft=(self.x, self.y))
    self.animation_time = 0
    self.is_alive = True
    self.facing_left = False
    self.speed = 7

  def load_animations(self):
    self.animations = {
      "idle": self.get_frames(0, 5),
      "move": self.get_frames(1, 5),
      "attack": self.get_frames(2, 5),
      "die": self.get_frames(3, 5)
      }

  def get_frames(self, row, num_frames):
    frames = []
    for i in range(num_frames):
      frame = self.sprite_sheet.subsurface((i * 64, row * 64, 64, 64))
      frame = frame.copy()
      frame = frame.subsurface(frame.get_bounding_rect())
      frames.append(frame)
    return frames

  def update(self, dt, x, y):

    self.rect = self.image.get_rect(topleft=(self.x, self.y))
    self.x += x
    self.y += y

    if not self.is_alive and self.frame_index == len(self.current_animation) - 1:
      return
    self.animation_time += dt
    if self.animation_time >= 0.1:
      self.animation_time = 0
      self.frame_index = (self.frame_index + 1) % len(self.current_animation)
      self.image = self.current_animation[self.frame_index]
      self.image = pygame.transform.scale(self.image, (64, 64))
      if self.facing_left:
        self.image = pygame.transform.flip(self.image, True, False)

  def draw(self, screen):
    screen.blit(self.image, (self.x, self.y))

  def move(self, dx, dy):
    self.x += dx
    self.y += dy
    self.rect.topleft = (self.x, self.y)
    self.set_animation("move")
    self.facing_left = dx < 0

  def attack(self):
    self.set_animation("attack")

  def die(self):
    self.set_animation("die")
    self.is_alive = False

  def set_animation(self, animation):
    if self.current_animation != self.animations[animation]:
      self.current_animation = self.animations[animation]
      self.frame_index = 0

  def follow(self, player_x, player_y):
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