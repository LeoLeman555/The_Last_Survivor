import yaml
import os

class GameDataManager:
    def __init__(self, filepath="data/game_save.yaml"):
        """Initialize the game data manager with a default save file path."""
        self.filepath = filepath
        self.game_data = self._read_params()

    def _read_params(self) -> dict:
        """Read the game save data from the YAML file."""
        if not os.path.exists(self.filepath):
            print("Save file not found, initializing with default values.")
            return self.reset_game_save()

        try:
            with open(self.filepath, "r") as file:
                return yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            print(f"Error reading YAML file: {e}")
            return {}

    def save_params(self) -> None:
        """Write the game data to the YAML save file."""
        try:
            with open(self.filepath, "w") as file:
                yaml.dump(self.game_data, file, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"Error writing to YAML file: {e}")

    def change_params(self, updates: dict, target_dict: dict = None) -> None:
        """Recursively update game parameters while preserving values correctly."""
        if target_dict is None:
            target_dict = self.game_data  # Start at root if no target is specified

        for key, value in updates.items():
            if isinstance(value, dict) and key in target_dict and isinstance(target_dict[key], dict):
                self.change_params(value, target_dict[key])  # Update nested dictionaries
            else:
                # Si la clé existe et est un nombre, on additionne la valeur
                if key in target_dict and isinstance(target_dict[key], (int, float)) and isinstance(value, (int, float)):
                    target_dict[key] += value
                else:
                    target_dict[key] = value  # Sinon, on remplace normalement

        self.save_params()

    def reset_game_save(self) -> dict:
        """Reset the game save to default values and save to the file."""
        self.game_data = {
            "money": 500,
            "resource": {key: 0 for key in ["energy", "metal", "data", "ammo"]},
            "weapon_level": {key: (1 if key == "pistol" else 0) for key in [
                "pistol", "magnum", "shotgun", "sniper", "ak", "rpg", "flamethrower",
                "minigun", "grenade_launcher", "laser", "plasma_gun", "knife"
            ]},
            "extras_level": {key: 0 for key in ["grenade", "toxic_grenade", "drone", "missile", "laser_probe"]},
            "power_up_level": {key: (1 if key in ["care_kit", "survival_ration", "2nd_life"] else 0) for key in [
                "care_kit", "survival_ration", "2nd_life", "critical_hit", "expert", "boost", "agile_fingers",
                "extra_ammo", "large_range", "magnetic", "piercing", "rapid_fire", "regeneration", "zoom",
                "strong_stomach"
            ]},
            "options": {
                "up": "W", "left": "A", "down": "S", "right": "D", "shoot": "MOUSE1",
                "launch": "SPACE", "pause": "P", "sound": "off", "music": "off",
                "language": "english", "fps": "60", "screen size": "1000x600",
                "difficulty": "1", "tutorial": "on"
            }
        }
        self.save_params()
        return self.game_data
