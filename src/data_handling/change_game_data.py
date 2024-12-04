import ast

class ChangeGameData:
  def __init__(self, reward: int, as_string: bool = False):
    """Initialize with reward and flag for string conversion."""
    self.reward = reward
    self.as_string = as_string
    self.game_save_data = self._read_params()

  def _read_params(self) -> dict:
    """Read game save data from the file."""
    try:
      with open("data/game_save.txt", 'r') as file:
        content = file.read()
      content = content.replace(f"GAME_SAVE_PARAMS = ", "", 1)
      params_dict = ast.literal_eval(content)
      return params_dict
    except (FileNotFoundError, SyntaxError) as e:
      print(f"Error reading game save file: {e}")
      return {}

  def change_params(self, dict1: dict, dict2: dict) -> None:
    """Update game data parameters based on two dictionaries."""
    for key, value in dict1.items():
      if key in dict2:
        if isinstance(value, dict) and isinstance(dict2[key], dict):
          self.change_params(value, dict2[key])
        else:
          if self.as_string:
            dict2[key] = str(value)
          else:
            dict2[key] += value
    self.write_params(self.game_save_data)

  def write_params(self, save_params: dict) -> None:
    """Write updated parameters back to the game save file."""
    try:
      with open("data/game_save.txt", 'w') as file:
        file.write("GAME_SAVE_PARAMS = {\n")
        file.write(f'  "money": {save_params["money"]},\n')
        file.write('  "resource": {\n')
        for resource, value in save_params['resource'].items():
          file.write(f'    "{resource}": {value},\n')
        file.write('  },\n')
        file.write('  "weapon_level": {\n')
        for weapon, value in save_params['weapon_level'].items():
          file.write(f'    "{weapon}": {value},\n')
        file.write('  },\n')
        file.write('  "extras_level": {\n')
        for extra, value in save_params['extras_level'].items():
          file.write(f'    "{extra}": {value},\n')
        file.write('  },\n')
        file.write('  "power_up_level": {\n')
        for power_up, value in save_params['power_up_level'].items():
          file.write(f'    "{power_up}": {value},\n')
        file.write('  },\n')
        file.write('  "options": {\n')
        for option, value in save_params['options'].items():
          file.write(f'    "{option}": "{value}",\n')
        file.write('  }\n')
        file.write('}\n')
    except Exception as e:
      print(f"Error writing to game save file: {e}")
