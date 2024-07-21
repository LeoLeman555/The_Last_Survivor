import pygame
import random
import math
import items
from load import ReadData

class Enemy(pygame.sprite.Sprite):
  def __init__(self, zoom: int, screen: 'pygame.surface.Surface', name: str, animations: dict, size: float, x: int, y: int, speed: int, icon : 'items.Icon', life: int = 100):
    super().__init__()
    self.zoom = zoom
    self.screen = screen
    self.name = name
    self.animations = animations
    self.size = size
    self.x = x
    self.y = y
    self.life = life
    self.speed = speed
    self.icon = icon
    self.current_animation = self.animations.get("idle", [])
    self.frame_index = 0
    self.image = self._resize_image(self.current_animation[self.frame_index])
    self.rect = self.image.get_rect(topleft=(self.x, self.y))
    self.animation_time = 0
    self.is_alive = True
    self.facing_left = False

  def _resize_image(self, image: pygame.Surface) -> pygame.Surface:
    """Resize image based on zoom and size."""
    width = int(image.get_width() * self.size * 0.5 * self.zoom)
    height = int(image.get_height() * self.size * 0.5 * self.zoom)
    return pygame.transform.scale(image, (width, height))

  def update(self, dt: int, x_var: int, y_var: int, player_rect: 'pygame.Rect'):
    """Update enemy state and animation."""
    self.x += (x_var / 2) * self.zoom
    self.y += (y_var / 2) * self.zoom
    self.rect.topleft = (self.x, self.y)
    self.check_collision(player_rect)

    if not self.is_alive and self.frame_index == len(self.current_animation) - 1:
      return

    self.animation_time += dt
    if self.animation_time >= 0.1:
      self.animation_time = 0
      if not len(self.current_animation) == 0 :
        self.frame_index = (self.frame_index + 1) % len(self.current_animation)
        self.image = self._resize_image(self.current_animation[self.frame_index])
      if self.facing_left:
        self.image = pygame.transform.flip(self.image, True, False)

  def draw(self, screen: 'pygame.surface.Surface'):
    """Draw the enemy on the screen."""
    # pygame.draw.rect(screen, (0, 0, 0,), self.rect)
    screen.blit(self.image, (self.x, self.y))

  def move(self, dx: int, dy: int):
    """Move the enemy and set its animation."""
    self.x += dx
    self.y += dy
    self.rect.topleft = (self.x, self.y)
    self.set_animation("move")
    self.facing_left = dx < 0

  def attack(self):
    """Set attack animation."""
    self.set_animation("attack")

  def damage(self, damage: int):
    """Apply damage to the enemy."""
    self.life -= damage
    if self.life <= 0:
      self.die()

  def die(self):
    """Handle enemy death."""
    self.is_alive = False
    self.icon.add_resource("me", 5)
    self.kill()

  def set_animation(self, animation: str):
    """Set the current animation."""
    if self.current_animation != self.animations.get(animation, []):
      self.current_animation = self.animations.get(animation, [])
      self.frame_index = 0

  def follow(self, player_x: int, player_y: int):
    """Make the enemy follow the player."""
    direction = pygame.Vector2(player_x - self.x, player_y - self.y)
    distance = direction.length()
    if distance > 0:
      if random.randint(0, 1) >= 0.5:
        angle_deviation = random.uniform(-math.pi / 6, math.pi / 6)
        direction.rotate_ip(math.degrees(angle_deviation))
      direction.normalize_ip()
      self.x += direction.x * self.speed
      self.y += direction.y * self.speed
      self.rect.topleft = (self.x, self.y)
      self.set_animation("move")
      self.facing_left = direction.x < 0

  def check_collision(self, player_rect: 'pygame.Rect'):
    """Check for collisions with player or bullets."""
    if self.rect.colliderect(player_rect):
      self.attack()

  def load_animations(self, sprite_sheet_path: str, animation_specs):
    """Load animations from a sprite sheet."""
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    return {name: self.get_frames(sprite_sheet, *spec) for name, spec in animation_specs.items()}

  def get_frames(self, sprite_sheet:'pygame.surface.Surface', row:int, num_frames:int, size_w:int, size_h:int):
    """Extract frames from a sprite sheet."""
    frames = []
    for i in range(num_frames):
      frame = sprite_sheet.subsurface((i * size_w, row * size_h, size_w, size_h))
      frame = frame.copy()
      frame = frame.subsurface(frame.get_bounding_rect())
      frames.append(frame)
    return frames

# Enemy subclasses
class Shardsoul(Enemy):
  def __init__(self, zoom: int, screen: 'pygame.surface.Surface', icon :'items.Icon', x: int, y: int, speed: int = 3):
    animation_specs = ReadData.read_animation_specs("data/shardsoul_animations.txt")
    animations = self.load_animations("res/enemy/shardsoul.png", animation_specs)
    super().__init__(zoom, screen, "shardsoul", animations, 2, x, y, speed * zoom * 0.5, icon)

class Sprout(Enemy):
  def __init__(self, zoom: int, screen: 'pygame.surface.Surface', icon :'items.Icon', x: int, y: int, speed: int = 6):
    animation_specs = ReadData.read_animation_specs("data/sprout_animations.txt")
    animations = self.load_animations("res/enemy/sprout.png", animation_specs)
    super().__init__(zoom, screen, "sprout", animations, 2, x, y, speed  * zoom * 0.5, icon)

class Worm(Enemy):
  def __init__(self, zoom: int, screen: 'pygame.surface.Surface', icon :'items.Icon', x: int, y: int, speed: int = 2):
    animation_specs = ReadData.read_animation_specs("data/worm_animations.txt")
    animations = self.load_animations("res/enemy/worm.png", animation_specs)
    super().__init__(zoom, screen, "worm", animations, 1.5, x, y, speed  * zoom * 0.5, icon)

class Wolf(Enemy):
  def __init__(self, zoom: int, screen: 'pygame.surface.Surface', icon :'items.Icon', x: int, y: int, speed: int = 5):
    animation_specs = ReadData.read_animation_specs("data/wolf_animations.txt")
    animations = self.load_animations("res/enemy/wolf.png", animation_specs)
    super().__init__(zoom, screen, "wolf", animations, 1.5, x, y, speed  * zoom * 0.5, icon)

class Robot(Enemy):
  def __init__(self, zoom: int, screen: 'pygame.surface.Surface', icon :'items.Icon', x: int, y: int, speed: int = 1):
    animation_specs = ReadData.read_animation_specs("data/robot_animations.txt")
    animations = self.load_animations("res/enemy/robot.png", animation_specs)
    super().__init__(zoom, screen, "robot", animations, 1.5, x, y, speed  * zoom * 0.5, icon)
