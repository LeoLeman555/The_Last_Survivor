import pygame
import pytmx
import ast

class Load:
  def charge_image(self, zoom: int, path: str, name: str, extension: str, ratio: int = 1):
    """Load and scale an image from file."""
    self.image = pygame.image.load(f"res/{path}/{name}.{extension}")
    self.image = self.image.copy()
    self.image = self.image.subsurface(self.image.get_bounding_rect())
    self.image = pygame.transform.scale(self.image, (self.image.get_width() * zoom * ratio, self.image.get_height() * zoom * ratio))
    return self.image

  def charge_tmx(self, path: str, name: str):
    """Load a TMX map from file."""
    self.map = pytmx.util_pygame.load_pygame(f"res/{path}/{name}.tmx")
    return self.map
  
  def load_and_resize_image(self, image_path, new_width, new_height):
    image = pygame.image.load(image_path)
    resized_image = pygame.transform.scale(image, (new_width, new_height))
    return resized_image

  def split_image(self, image):
    original_width, original_height = image.get_size()
    left_half = image.subsurface((0, 0, original_width // 2, original_height))
    right_half = image.subsurface((original_width // 2, 0, original_width // 2, original_height))
    return left_half, right_half

  @staticmethod
  def save_animation_specs_to_file(filename: str, animation_specs):
    """Save animation specifications to a file."""
    with open(filename, 'w') as file:
      for key, value in animation_specs.items():
        file.write(f"{key}:{value}\n")

class ReadData:
  def get_thresholds(self, path: str):
    """Read and return thresholds from a file."""
    with open(path, "r") as file:
      thresholds = tuple(int(num) for line in file for num in line.split(','))
    return thresholds

  def read_resources_data(self, path: str):
    """Read resources data from a file and return as a dictionary."""
    resources = {}
    with open(path, 'r') as file:
      for line in file:
        parts = line.strip().split(',')
        key = parts[0]
        value = int(parts[1])
        resources[key] = value
    return resources

  def read_bars_data(self, path: str):
    """Read bars data from a file and return as a dictionary."""
    bars = {}
    with open(path, 'r') as file:
      for line in file:
        parts = line.strip().split(',')
        key = parts[0]
        value = int(parts[1])
        bars[key] = value
    return bars

  def read_animation_specs(self, filepath: str):
    """Read animation specs from a file and return as a dictionary."""
    animation_specs = {}
    with open(filepath, 'r') as file:
      for line in file:
        key, value = line.strip().split(':')
        animation_specs[key] = tuple(map(int, value.strip("()").split(',')))
    return animation_specs
  
  def read_enemy_params(self, filepath: str):
    with open(filepath, 'r') as file:
      content = file.read()
    content = content.replace("ENEMY_PARAMS = ", "", 1)
    enemy_params_dict = ast.literal_eval(content)
    return enemy_params_dict

  def read_weapon_params(self, filepath: str):
    with open(filepath, 'r') as file:
      content = file.read()
    content = content.replace("WEAPON_PARAMS = ", "", 1)
    enemy_params_dict = ast.literal_eval(content)
    return enemy_params_dict
  
  def read_extras_params(self, filepath: str):
    with open(filepath, 'r') as file:
      content = file.read()
    content = content.replace("EXTRAS_PARAMS = ", "", 1)
    enemy_params_dict = ast.literal_eval(content)
    return enemy_params_dict
  
  def read_power_up_params(self, filepath: str):
    with open(filepath, 'r') as file:
      content = file.read()
    content = content.replace("POWER_UP_PARAMS = ", "", 1)
    enemy_params_dict = ast.literal_eval(content)
    return enemy_params_dict
