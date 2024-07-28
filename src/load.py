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

  def read_weapon_data(self, path: str):
    """Read weapon data from a file and return as a dictionary."""
    data_weapon = {}
    with open(path, 'r') as file:
      for line in file:
        parts = line.strip().split(',')
        key = int(parts[0])
        name = parts[1]
        dimensions = (int(parts[2]), int(parts[3]))
        position = (int(parts[4]), int(parts[5]))
        power = int(parts[6])
        explosion = int(parts[7])
        distance = int(parts[8])
        rate = int(parts[9])
        precision = int(parts[10])
        number_shoot = int(parts[11])
        delay = int(parts[12])
        dps = int(parts[13])
        data_weapon[key] = (name, dimensions, position, power, explosion, distance, rate, precision, number_shoot, delay, dps)
    return data_weapon

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
