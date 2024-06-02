import pygame

class Icon:
  def __init__(self, ressource,  barres):
    self.ressource = ressource
    self.barres = barres

  def ajout_ressource(self, name, valeur):
    self.ressource[f"{name}"] += valeur

  def change_palier(self, name, valeur):
    self.barres[f"{name}_max"] = valeur

  def ajout_barres(self, name, valeur):
    self.barres[f"{name}"] += valeur

  def get_icon(self, screen, name, x_pos, y_pos, x_text, y_text, width, height, valeur=0):
    """Affiche un icon

    Args:
        name (str): nom de l'icon
        x_pos (int): x de l'icon
        y_pos (int): y de l'icon
        x_text (int): x du texte
        y_text (int): y du texte
        width (int): largeur voulue
        height (int): hauteur voulue
        valeur (int): score a afficher
    """
    image = pygame.image.load(f"res/sprite/{name}.png")
    image = pygame.transform.scale(image, (width, height))
    screen.blit(image, (x_pos, y_pos))
    police = pygame.font.Font("res/texte/dialog_font.ttf", 18)
    self.get_score(screen, police, valeur, x_pos + x_text, y_pos + y_text)
    
  def get_score(self, screen, police , valeur, x, y):
      msg_score = police.render(f"{valeur}", True, (0, 0, 0) )
      screen.blit(msg_score, (x, y))

  def get_bar(self, screen, name, x_bar, y_bar, valeur=0):
    """Affiche les barres de mécanique à l'écran (0=>79)

    Args:
        screen (var): écran de jeu
        name (str): nom du sprite sheet
        x_bar (int): position de l'objet
        y_bar (int): position de l'objet
        valeur (int): valeur de l'objet
    """
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

  def get_image(self, sheet, x, y):
      image = pygame.Surface([186, 22])
      image.blit(sheet, (0, 0), (x, y, 186, 22))
      return image

  def get_images(self, sheet, y):
    images = []
    for i in range(0, 10):
      x = i*186
      image = self.get_image(sheet, x, y)
      images.append(image)
    return images