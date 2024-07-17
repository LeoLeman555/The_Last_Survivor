import pygame, pytmx

class Load():
  def charge_image(self, zoom:int, chemin:str, name:str, extension:str, ratio:int =1):
    self.image = pygame.image.load(f"res/{chemin}/{name}.{extension}") # recuperation image
    self.image = self.image.copy()
    self.image = self.image.subsurface(self.image.get_bounding_rect())
    self.image = pygame.transform.scale(self.image, (self.image.get_width()*zoom*ratio, self.image.get_height()*zoom*ratio))
    return self.image
  
  def charge_tmx(self, chemin:str, name:str):
    self.map = pytmx.util_pygame.load_pygame(f"res/{chemin}/{name}.tmx")
    return self.map
  
  def save_animation_specs_to_file(filename:str, animation_specs):
    with open(filename, 'w') as file:
      for key, value in animation_specs.items():
        file.write(f"{key}:{value}\n")