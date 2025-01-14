from dataclasses import dataclass
import pygame, pytmx, pyscroll
from src.data_handling.load import *


@dataclass
class Map:
    name: str  # Name of the map
    walls: list[pygame.Rect]  # List of collision walls
    sables: list[pygame.Rect]  # List of quicksand areas
    group: pyscroll.PyscrollGroup  # Pyscroll group for map layers
    tmx_data: pytmx.TiledMap  # TMX map data


class MapManager:
    def __init__(self, run, screen: "pygame.surface.Surface", player, zoom: int):
        """Initialize the map manager with game context."""
        self.run = run
        self.maps = {}  # Map name -> Map object
        self.screen = screen
        self.zoom = zoom
        self.player = player
        self.current_map = "map_desert"
        self.register_map("map_desert")
        self.teleport("start_player")

    def check_collision(self):
        """Check if player collides with walls."""
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
                self.run.manager.rock_collision(True)
            else:
                self.run.manager.rock_collision(False)

    def check_sables(self):
        """Check if player is in quicksand and reduce speed."""
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_sables()) > -1:
                self.run.manager.collision_sables(True)
            else:
                self.run.manager.collision_sables(False)

    def teleport(self, name: str):
        """Teleport the player to specified coordinates."""
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name: str):
        """Load the map data and set up collision and quicksand areas."""
        tmx_data = Load.charge_tmx(self, "map", name)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size()
        )
        map_layer.zoom = self.zoom

        # * no trees => more post-apocalyptic

        walls = []
        sables = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "sables":
                sables.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        group.add(self.player)

        self.maps[name] = Map(name, walls, sables, group, tmx_data)

    def get_map(self):
        """Return the current map object."""
        return self.maps[self.current_map]

    def get_group(self):
        """Return the Pyscroll group of the current map."""
        return self.get_map().group

    def get_walls(self):
        """Return the list of collision walls for the current map."""
        return self.get_map().walls

    def get_sables(self):
        """Return the list of quicksand areas for the current map."""
        return self.get_map().sables

    def get_object(self, name: str):
        """Return the map object by name."""
        return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        """Draw the current map and center the player."""
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        """Update the map group and check for collisions."""
        self.get_group().update()
        self.check_collision()
        self.check_sables()

    def change_map_size(self, new_zoom: float):
        """Change the size of the map by updating the zoom level."""
        self.zoom = new_zoom

        # Recreate the map layer with the new zoom level
        map_data = pyscroll.data.TiledMapData(self.get_map().tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size()
        )
        map_layer.zoom = self.zoom

        # Update the group with the new map layer
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        group.add(self.player)

        # Update the current map's group with the new group
        self.maps[self.current_map] = Map(
            self.current_map,
            self.get_walls(),
            self.get_sables(),
            group,
            self.get_map().tmx_data,
        )
