import pygame

def get_icon(screen, name, x_pos, y_pos, x_text, y_text, width, height, valeur=0):
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
  get_score(screen, police, valeur, x_pos + x_text, y_pos + y_text)
  
def get_score(screen, police , valeur, x, y):
    msg_score = police.render(f"{valeur}", True, (0, 0, 0) )
    screen.blit(msg_score, (x, y))

def get_bar(screen, name, id=0, id2=0, x_bar=0, y_bar=0):
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
    '1': get_images(sprite_sheet, 0),   # 10 premières unités
    '11': get_images(sprite_sheet, 22),  # 10 suivantes unités (décalé de 22 pixels en y)
    '21': get_images(sprite_sheet, 44), 
    '31': get_images(sprite_sheet, 66),
    '41': get_images(sprite_sheet, 88), 
    '51': get_images(sprite_sheet, 110),
    '61': get_images(sprite_sheet, 132), 
    '71': get_images(sprite_sheet, 154),
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

def get_image(sheet, x, y):
    image = pygame.Surface([186, 22])
    image.blit(sheet, (0, 0), (x, y, 186, 22))
    return image

def get_images(sheet, y):
  images = []
  for i in range(0, 10):
    x = i*186
    image = get_image(sheet, x, y)
    images.append(image)
  return images