import pygame
import pytmx

class Load:
  def charge_image(self, zoom: int, path: str, name: str, extension: str, ratio: int = 1) -> pygame.Surface:
    """Load and scale an image from file."""
    image = pygame.image.load(f"res/{path}/{name}.{extension}")
    image = image.copy()
    image = image.subsurface(image.get_bounding_rect())
    image = pygame.transform.scale(
      image,
      (image.get_width() * zoom * ratio, image.get_height() * zoom * ratio)
    )
    return image

  def charge_tmx(self, path: str, name: str) -> pytmx.TiledMap:
    """Load a TMX map from file."""
    map = pytmx.util_pygame.load_pygame(f"res/{path}/{name}.tmx")
    return map

  def split_image(self, image: pygame.Surface) -> tuple[pygame.Surface, pygame.Surface]:
    """Split an image into two halves."""
    original_width, original_height = image.get_size()
    left_half = image.subsurface((0, 0, original_width // 2, original_height))
    right_half = image.subsurface((original_width // 2, 0, original_width // 2, original_height))
    return left_half, right_half

  @staticmethod
  def save_animation_specs_to_file(filename: str, animation_specs: dict):
    """Save animation specifications to a file."""
    with open(filename, 'w') as file:
      for key, value in animation_specs.items():
        file.write(f"{key}:{value}\n")

  def load_power_up(self, data_power_up: dict):
    """Load power-up images and split them into left and right parts."""
    for power_up_name, power_up_data in data_power_up.items():
      image_path = f"res/power_up/power_up/{power_up_name}.png"
      image = pygame.image.load(image_path)
      left_image, right_image = self.split_image(image)
      power_up_data["left_image"] = left_image
      power_up_data["right_image"] = right_image

  def process_data(self, game_data: dict, level_key: str, data: dict) -> dict:
    """Process and update game data with levels and lock status."""
    for name, level in game_data[level_key].items():
      for item_id, item_info in data.items():
        if item_info["name"] == name:
          item_info["level"] = level
          item_info["locked"] = (level == 0)
          break
    return {key: value for key, value in data.items()}
