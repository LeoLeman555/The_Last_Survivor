import pygame

class Icon:
  def __init__(self, run, resource: dict, bars: dict):
    """Initialize the Icon class with resources"""
    self.resource = resource
    self.bars = bars
    self.run = run

  def update(self):
    if self.resource["food"] > self.bars["food_max"]:
      self.resource["food"] = self.bars["food_max"]
    elif self.resource["food"] < 0:
      self.resource["food"] = 0

    if self.resource["health"] > self.bars["health_max"]:
      self.resource["health"] = self.bars["health_max"]
    elif self.resource["health"] < 0:
      self.resource["health"] = 0

    if self.resource["xp"] > self.bars["xp_max"]:
      self.resource["xp"] = 0
      self.run.manager.change_max_xp(self.run.index_palier_xp + 1)
      self.run.manager.launch_power_up()

  def draw(self, screen):
    def calculate_bar_length(current, maximum):
      return round(current * 79 / maximum)
    
    def draw_resource_icon(name, x, y, width, height, shift_x, shift_y, value):
      self.draw_icon(screen, name, x, y, width, height, shift_x, shift_y, value)

    self.bars["xp_bar"] = calculate_bar_length(self.resource["xp"], self.bars["xp_max"])
    self.bars["health_bar"] = calculate_bar_length(self.resource["health"], self.bars["health_max"])
    self.bars["food_bar"] = calculate_bar_length(self.resource["food"], self.bars["food_max"])

    self.draw_bar(screen, "xp_bar", 20, 20, self.bars["xp_bar"])
    self.draw_bar(screen, "health_bar", 20, 45, self.bars["health_bar"])
    self.draw_bar(screen, "food_bar", 20, 70, self.bars["food_bar"])

    draw_resource_icon("energy_icon", 130, 100, 25, -3, 22, 20, self.resource["energy"])
    draw_resource_icon("metal_icon", 20, 100, 25, -3, 22, 20, self.resource["metal"])
    # draw_resource_icon("ammo_icon", 134, 125, 21, 1, 15, 29, self.resource["ammo"])
    draw_resource_icon("data_icon", 20, 127, 30, -1, 30, 21, self.resource["data"])

  def add_resource(self, name: str, value: int):
    """Add a value to a resource."""
    self.run.player.add_message(f"+{value} {name}", (500, 200), (500, 125), (0, 0, 0), 20, 750)
    try :
      self.resource[f"{name}"] += value
    except KeyError:
      self.add_bars(name, value)

  def change_threshold(self, name: str, value: int):
    """Change the maximum value for a bar."""
    self.bars[f"{name}_max"] = value

  def add_bars(self, name: str, value: int):
    """Add a value to a bar."""
    self.bars[f"{name}"] += value

  def draw_icon(self, screen: pygame.Surface, name: str, x_pos: int, y_pos: int, x_text: int, y_text: int, width: int, height: int, value=0):
    """Draw an icon on the screen."""
    image = pygame.image.load(f"res/sprite/{name}.png")
    image = pygame.transform.scale(image, (width, height))
    screen.blit(image, (x_pos, y_pos))
    font = pygame.font.Font("res/texte/dialog_font.ttf", 18)
    self.draw_score(screen, font, value, x_pos + x_text, y_pos + y_text)

  def draw_score(self, screen: pygame.Surface, font, value, x, y):
    """Draw the score value on the screen."""
    score_text = font.render(f"{value}", True, (0, 0, 0))
    screen.blit(score_text, (x, y))

  def draw_bar(self, screen: pygame.Surface, name: str, x_bar: int, y_bar: int, value: int = 0):
    """Draw mechanical bars on the screen based on the given value."""
    sprite_sheet = pygame.image.load(f"res/sprite/{name}.png")

    images = {
      '0': self.get_images(sprite_sheet, 0),
      '10': self.get_images(sprite_sheet, 22),
      '20': self.get_images(sprite_sheet, 44),
      '30': self.get_images(sprite_sheet, 66),
      '40': self.get_images(sprite_sheet, 88),
      '50': self.get_images(sprite_sheet, 110),
      '60': self.get_images(sprite_sheet, 132),
      '70': self.get_images(sprite_sheet, 154),
    }

    if value < 10:
      key = "0"
    elif value < 20:
      key = '10'
    elif value < 30:
      key = '20'
    elif value < 40:
      key = '30'
    elif value < 50:
      key = '40'
    elif value < 60:
      key = '50'
    elif value < 70:
      key = '60'
    elif value < 80:
      key = '70'
    else:
      print(f"Error displaying mechanical bar: value = {value}")
      key = '70'

    loop = 0
    for image in images[key]:
      if loop == value % 10:
        bar = image
        bar.set_colorkey([0, 0, 0])
        screen.blit(bar, (x_bar, y_bar))
        break
      else:
        loop += 1

  def get_image(self, sheet: pygame.Surface, x: int, y: int):
    """Extract a single image from the sprite sheet."""
    image = pygame.Surface([186, 22])
    image.blit(sheet, (0, 0), (x, y, 186, 22))
    return image

  def get_images(self, sheet: pygame.Surface, y: int):
    """Extract a series of images from the sprite sheet."""
    images = []
    for i in range(0, 10):
      x = i * 186
      image = self.get_image(sheet, x, y)
      images.append(image)
    return images
