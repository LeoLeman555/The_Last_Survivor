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

  def load_power_up(self, data_power_up):
    for power_up_name, power_up_data in data_power_up.items():
      image_path = f"res/power_up/power_up/{power_up_name}.png"
      image = pygame.image.load(image_path)
      left_image, right_image = self.split_image(image)
      power_up_data["left_image"] = left_image
      power_up_data["right_image"] = right_image

  def process_data(self, game_data: dict, level_key: str, data: dict) -> dict:
    for name, level in game_data[level_key].items():
      for item_id, item_info in data.items():
        if item_info["name"] == name:
          item_info["level"] = level
          item_info["locked"] = (level == 0)
          break
    return {key: value for key, value in data.items()}

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
  
  def read_params(self, filepath: str, prefix: str):
    """Generic method to read any parameter file by removing the specific prefix."""
    with open(filepath, 'r') as file:
      content = file.read()
    real_prefix = prefix.upper()
    content = content.replace(f"{real_prefix}_PARAMS = ", "", 1)
    params_dict = ast.literal_eval(content)
    return params_dict
