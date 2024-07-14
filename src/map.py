from dataclasses import dataclass
import pygame, pytmx, pyscroll
from load import Load

# Utilisation de la dataclass
@dataclass
class Map:
  name: str # nom de la carte
  walls: list[pygame.Rect]  # liste des murs de collisions
  sables: list[pygame.Rect]
  group: pyscroll.PyscrollGroup
  tmx_data: pytmx.TiledMap

class MapManager:
  def __init__(self, screen, player, run):
    self.run = run
    self.maps = dict()    #'house' -> map("house", walls, group)
    self.screen = screen
    self.player = player
    self.current_map = "carte_desert"

    self.register_map("carte_desert")
    
    self.teleport("start_player")

  def check_collision(self):
    """Vérifie si le joueur et en collision avec un mur
    """
    # collision
    for sprite in self.get_group().sprites():
      if sprite.feet.collidelist(self.get_walls()) > -1:
        sprite.move_back()
        self.run.collision(True)
      else:
        self.run.collision(False)

    # sables mouvants
  def check_sables(self):
    """Si collision avec sables réduit vitesse
    """
    for sprite in self.get_group().sprites():
      if sprite.feet.collidelist(self.get_sables()) > -1:
        self.run.collision_sables(True)
      else:
        self.run.collision_sables(False)

  def teleport(self, name):
    """Téléporte le personage aux coordonnées indiqués sur Tiled

    Args:
        name (str): nom de l'objet 
    """
    point = self.get_object(name)
    self.player.position[0] = point.x
    self.player.position[1] = point.y
    self.player.save_location()

  def register_map(self, name):
    """Charge les différentes cartes

    Args:
        name (str): nom de la carte à charger
    """
    tmx_data = Load.charge_tmx(self, chemin="map", name=name)
    map_data = pyscroll.data.TiledMapData(tmx_data)
    map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
    map_layer.zoom = 2
    
    # rectangles de collision
    walls = []
    sables = []

    for obj in tmx_data.objects:
      if obj.type == "collision": # ajoute un rectangle à la liste si objet collision
        walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
      elif obj.type == "sables":
        sables.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    # dessiner les groupes de calques
    group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
    group.add(self.player)

    self.maps[name] = Map(name, walls, sables, group, tmx_data) # Créer un objet map dictionnaire

    # Affiche dans la console la liste maps
    # print(f"- Rectangles de collisions : {walls}")
    # print(f"- Sables mouvant : {sables}")
    # print(f"- Calques : {group}")
    # print(f"- Carte : {name} / - Chemin d’accès : {tmx_data}")

  # retourne les information de la carte
  def get_map(self):
    return self.maps[self.current_map]
  
  def get_group(self):
    return self.get_map().group
  
  def get_walls(self):
    return self.get_map().walls
  
  def get_sables(self):
    return self.get_map().sables
  
  def get_object(self, name):
    return self.get_map().tmx_data.get_object_by_name(name)
  
  # créer une méthode pour centrer le joueur et pour récupérer les collisions

  def draw(self):
    self.get_group().draw(self.screen)
    self.get_group().center(self.player.rect.center)

  def update(self):
    self.get_group().update()
    self.check_collision()
    self.check_sables()