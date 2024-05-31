import pygame

class Jetons:
  def __init__(self, dict_jeton, screen):
    self.dict_jeton = dict_jeton
    self.screen = screen

  def dep_addition(self, valeur_x, valeur_y):
    for nombre in self.dict_jeton.keys():
      name, x, y = self.dict_jeton[f"{nombre}"]
      self.dict_jeton[f"{nombre}"] = (name, x+valeur_x, y+valeur_y)

  def update_jeton(self):
    for items in self.dict_jeton.keys():
      name, x, y = self.dict_jeton[f"{items}"]
      self.screen.blit(pygame.image.load(f"res/sprite/{name}.png"), (x - 4000, y - 4000))

  def ajout_jeton(self, name, x, y):
    self.dict_jeton[f"{self.dict_jeton.keys}"] = name, x, y

  def supprime_jeton(self, key):
    if key in self.dict_jeton:
      del self.dict_jeton[key]

class Icon:
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

  def get_bar(self, screen, name, id=0, id2=0, x_bar=0, y_bar=0):
    """Affiche les barres de mécanique à l'écran

    Args:
        screen (var): écran de jeu
        name (str): nom du sprite sheet
        id (int): nombre de la dizaine   Min => 0, Max => 7
        id2 (int): nombre de l'unité - 1   Min => 0, Max => 9 (pour 10)
        x_bar (int): position de l'objet
        y_bar (int): position de l'objet
    """
    sprite_sheet = pygame.image.load(f"res/sprite/{name}.png")

    images = {
      '1': self.get_images(sprite_sheet, 0),   # 10 premières unités
      '11': self.get_images(sprite_sheet, 22),
      '21': self.get_images(sprite_sheet, 44), 
      '31': self.get_images(sprite_sheet, 66),
      '41': self.get_images(sprite_sheet, 88), 
      '51': self.get_images(sprite_sheet, 110),
      '61': self.get_images(sprite_sheet, 132), 
      '71': self.get_images(sprite_sheet, 154),
      }

    if id == 0:
      key = "1"
    elif id == 1:
      key = '11'
    elif id == 2:
      key = '21'
    elif id == 3:
      key = '31'
    elif id == 4:
      key = '41'
    elif id == 5:
      key = '51'
    elif id == 6:
      key = '61'
    elif id == 7:
      key = '71'
    else:
      print("Erreur d'affichage de barre de mécanique")
      key = '1'

    loop = 0
    for image in images[key]:
      if loop == id2:
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