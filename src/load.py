import pygame, pytmx

class Load():
  def charge_image(self, chemin, name, extension):
    self.image = pygame.image.load(f"res/{chemin}/{name}.{extension}") # recuperation image
    return self.image
  
  def charge_tmx(self, chemin, name):
    self.map = pytmx.util_pygame.load_pygame(f"res/{chemin}/{name}.tmx")
    return self.map
  
  def save_animation_specs_to_file(filename, animation_specs):
    with open(filename, 'w') as file:
      for key, value in animation_specs.items():
        file.write(f"{key}:{value}\n")