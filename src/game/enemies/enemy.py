import pygame
import random
import math
from src.data_handling.load import *
from src.data_handling.read_data import *
from src.game.enemies.health_bar import *
from src.game.maps.awards_choice import *


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        zoom: int,
        screen: "pygame.Surface",
        name: str,
        player,
        icon,
        x: int,
        y: int,
        data: dict,
    ):
        super().__init__()
        self.read_data = ReadData()
        self.data = data
        self.params = self.data[name.lower()]
        self.zoom = zoom
        self.screen = screen
        self.name = name
        self.player = player
        self.animations = self.load_animations(
            self.params["sprite_sheet"],
            self.read_data.read_json(self.params["animation_specs"]),
        )
        self.size = self.params["size"]
        self.x = x
        self.y = y
        self.max_health = self.params["max_health"]
        self.health = self.max_health
        self.speed = self.params["speed"] * self.zoom * 0.5
        self.icon = icon
        self.current_animation = self.animations.get("idle", [])
        self.frame_index = 0
        self.image = self._resize_image(self.current_animation[self.frame_index])
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.animation_time = 0
        self.is_alive = True
        self.facing_left = False
        self.width = self.image.get_width()
        self.health_bar = HealthBar(
            self.zoom, self.x, self.y - 10, self.width, self.max_health
        )
        self.choice = Choice(self.name, self.params)

    def _resize_image(self, image: pygame.Surface) -> pygame.Surface:
        """Resize image based on zoom and size."""
        width = int(image.get_width() * self.size * 0.5 * self.zoom)
        height = int(image.get_height() * self.size * 0.5 * self.zoom)
        return pygame.transform.scale(image, (width, height))

    def update(self, dt: int, x_var: int, y_var: int, player_rect: "pygame.Rect"):
        """Update enemy state and animation."""
        self.x += (x_var / 2) * self.zoom
        self.y += (y_var / 2) * self.zoom
        self.rect.topleft = (self.x, self.y)
        self.check_collision(player_rect)

        if not self.is_alive and self.frame_index == len(self.current_animation) - 1:
            return

        self.animation_time += dt
        if self.animation_time >= 0.1:
            self.animation_time = 0
            if self.current_animation:
                self.frame_index = (self.frame_index + 1) % len(self.current_animation)
                self.image = self._resize_image(
                    self.current_animation[self.frame_index]
                )
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

        self.health_bar.rect.topleft = (self.x, self.y - 10)
        self.health_bar.update(self.health)

    def draw(self, screen: "pygame.Surface"):
        """Draw the enemy and its health bar on the screen."""
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.health_bar.image, self.health_bar.rect.topleft)

    def move(self, dx: int, dy: int):
        """Move the enemy and set its animation."""
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)
        self.set_animation("move")
        self.facing_left = dx < 0

    def attack(self):
        """Set attack animation."""
        self.icon.resource["health"] -= 1

    def damage(self, damage: int):
        """Apply damage to the enemy."""
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        """Handle enemy death."""
        self.is_alive = False
        self.player.add_object(
            "xp",
            self.params["reward"][1] * self.player.run.xp_multiplier,
            *self.rect.center,
        )
        self.player.add_object("ammo", self.params["reward"][2], *self.rect.center)
        award = self.choice.choose(*self.params["reward"][0])
        if award in ["energy", "metal", "food", "data"]:
            self.player.add_object(award, 25, *self.rect.center)
        if award == "weapon":
            award = self.choice.weapon(
                self.player.run.current_weapon_dict["id"],
                self.player.run.filtered_weapons.keys(),
            )
            self.player.add_weapon(
                self.player.run.data_weapons[f"{award}"]["name"],
                award,
                *self.rect.center,
            )
        self.delete()

    def delete(self):
        self.player.number_enemies -= 1
        self.kill()

    def set_animation(self, animation: str):
        """Set the current animation."""
        if self.current_animation != self.animations.get(animation, []):
            self.current_animation = self.animations.get(animation, [])
            self.frame_index = 0

    def follow(self, player_x: int, player_y: int):
        """Make the enemy follow the player."""
        direction = pygame.Vector2(player_x - self.x, player_y - self.y)
        distance = direction.length()
        if distance > 0:
            if random.randint(0, 1) >= 0.5:
                angle_deviation = random.uniform(-math.pi / 6, math.pi / 6)
                direction.rotate_ip(math.degrees(angle_deviation))
            direction.normalize_ip()
            self.x += direction.x * self.speed
            self.y += direction.y * self.speed
            self.rect.topleft = (self.x, self.y)
            self.set_animation("move")
            self.facing_left = direction.x < 0

    def check_collision(self, player_rect: "pygame.Rect"):
        """Check for collisions with player or bullets."""
        if self.rect.colliderect(player_rect):
            self.attack()

    def change_zoom(self, new_zoom: float):
        """Update the zoom level and resize relevant properties."""
        self.zoom = new_zoom
        self.speed = self.params["speed"] * self.zoom * 0.5
        self.image = self._resize_image(self.current_animation[self.frame_index])
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.health_bar.change_zoom(new_zoom)

    def load_animations(self, sprite_sheet_path: str, animation_specs):
        """Load animations from a sprite sheet."""
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        return {
            name: self.get_frames(sprite_sheet, *spec)
            for name, spec in animation_specs.items()
        }

    def get_frames(
        self,
        sprite_sheet: "pygame.Surface",
        row: int,
        num_frames: int,
        size_w: int,
        size_h: int,
    ):
        """Extract frames from a sprite sheet."""
        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((i * size_w, row * size_h, size_w, size_h))
            frame = frame.copy()
            frame = frame.subsurface(frame.get_bounding_rect())
            frames.append(frame)
        return frames
