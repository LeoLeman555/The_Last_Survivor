import pygame

class Icon:
  def __init__(self, ressource:dict,  barres:dict):
    self.ressource = ressource
    self.barres = barres

  def ajout_ressource(self, name:str, valeur:int):
    self.ressource[f"{name}"] += valeur

  def change_palier(self, name:str, valeur:int):
    self.barres[f"{name}_max"] = valeur

  def ajout_barres(self, name:str, valeur:int):
    self.barres[f"{name}"] += valeur

  def get_icon(self, screen:'pygame.surface.Surface', name:str, x_pos:int, y_pos:int, x_text:int, y_text:int, width:int, height:int, valeur=0):
    """Affiche un icon"""

    image = pygame.image.load(f"res/sprite/{name}.png")
    image = pygame.transform.scale(image, (width, height))
    screen.blit(image, (x_pos, y_pos))
    police = pygame.font.Font("res/texte/dialog_font.ttf", 18)
    self.get_score(screen, police, valeur, x_pos + x_text, y_pos + y_text)
    
  def get_score(self, screen:'pygame.surface.Surface', police , valeur, x, y):
      msg_score = police.render(f"{valeur}", True, (0, 0, 0) )
      screen.blit(msg_score, (x, y))

  def get_bar(self, screen:'pygame.surface.Surface', name:str, x_bar:int, y_bar:int, valeur:int =0):
    """Affiche les barres de mécanique à l'écran (0=>79)"""

    sprite_sheet = pygame.image.load(f"res/sprite/{name}.png")

    images = {
      '0': self.get_images(sprite_sheet, 0),   # 10 premières unités
      '10': self.get_images(sprite_sheet, 22),  # 10 suivantes unités (décalé de 22 pixels en y)
      '20': self.get_images(sprite_sheet, 44), 
      '30': self.get_images(sprite_sheet, 66),
      '40': self.get_images(sprite_sheet, 88), 
      '50': self.get_images(sprite_sheet, 110),
      '60': self.get_images(sprite_sheet, 132), 
      '70': self.get_images(sprite_sheet, 154),
    }

    if valeur < 10:
      key = "0"
    elif valeur < 20:
      key = '10'
    elif valeur < 30:
      key = '20'
    elif valeur < 40:
      key = '30'
    elif valeur < 50:
      key = '40'
    elif valeur < 60:
      key = '50'
    elif valeur < 70:
      key = '60'
    elif valeur < 80:
      key = '70'
    else:
      print(f"Erreur d'affichage de barre de mécanique : valeur = {valeur}")
      key = '0'

    loop = 0
    for image in images[key]:
      if loop == valeur % 10:
        barre = image
        barre.set_colorkey([0, 0 , 0])
        screen.blit(barre, (x_bar, y_bar))
        break
      else:
        loop += 1

  def get_image(self, sheet:'pygame.surface.Surface', x:int, y:int):
      image = pygame.Surface([186, 22])
      image.blit(sheet, (0, 0), (x, y, 186, 22))
      return image

  def get_images(self, sheet:'pygame.surface.Surface', y:int):
    images = []
    for i in range(0, 10):
      x = i*186
      image = self.get_image(sheet, x, y)
      images.append(image)
    return images