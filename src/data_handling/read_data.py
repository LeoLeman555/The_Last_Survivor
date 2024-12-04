import ast

class ReadData:
  def get_thresholds(self, path: str) -> tuple:
    """Read and return thresholds from a file."""
    with open(path, "r") as file:
      thresholds = tuple(int(num) for line in file for num in line.split(','))
    return thresholds

  def read_resources_data(self, path: str) -> dict:
    """Read resources data from a file and return as a dictionary."""
    resources = {}
    with open(path, 'r') as file:
      for line in file:
        parts = line.strip().split(',')
        key = parts[0]
        value = int(parts[1])
        resources[key] = value
    return resources

  def read_bars_data(self, path: str) -> dict:
    """Read bars data from a file and return as a dictionary."""
    bars = {}
    with open(path, 'r') as file:
      for line in file:
        parts = line.strip().split(',')
        key = parts[0]
        value = int(parts[1])
        bars[key] = value
    return bars

  def read_animation_specs(self, filepath: str) -> dict:
    """Read animation specs from a file and return as a dictionary."""
    animation_specs = {}
    with open(filepath, 'r') as file:
      for line in file:
        key, value = line.strip().split(':')
        animation_specs[key] = tuple(map(int, value.strip("()").split(',')))
    return animation_specs
  
  def read_params(self, filepath: str, prefix: str) -> dict:
    """Generic method to read any parameter file by removing the specific prefix."""
    with open(filepath, 'r') as file:
      content = file.read()
    real_prefix = prefix.upper()
    content = content.replace(f"{real_prefix}_PARAMS = ", "", 1)
    params_dict = ast.literal_eval(content)
    return params_dict
