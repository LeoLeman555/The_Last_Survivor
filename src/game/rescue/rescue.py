import pygame
import random
import math
from src.data_handling.load import *


class RescueShip:
    """Represents a rescue ship in the game."""

    def __init__(self, run):
        self.run = run
        self.original_image = Load.charge_image(
            self, self.run.zoom / 2, "rescue", "ship", "png", 1
        )

        # Load movement images
        self.move_images_right = [
            Load.charge_image(
                self, self.run.zoom / 2, "rescue", "ship_move1", "png", 1
            ),
            Load.charge_image(
                self, self.run.zoom / 2, "rescue", "ship_move2", "png", 1
            ),
            Load.charge_image(
                self, self.run.zoom / 2, "rescue", "ship_move3", "png", 1
            ),
        ]
        self.move_images_left = [
            pygame.transform.flip(img, True, False) for img in self.move_images_right
        ]

        self.current_move_frame = 0
        self.animation_delay = 75
        self.last_update = pygame.time.get_ticks()

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.position = self.random_position(1000)
        self.target_position = self.random_position(-500)
        self.rect.center = self.position
        self.ladder_rect = pygame.Rect(0, 0, 30, 15)

        self.rescue = False
        self.move = False
        self.show_ladder = False
        self.float_counter = 0

        self.facing_right = True
        self.moving_right = True

        self.arrive = False

    def random_position(self, interval: int) -> list[int]:
        """Generates a random position for the ship."""
        x_ranges = {
            1: (-1000 - interval, 500 + interval),
            2: (500 + interval, 1000 + interval),
            3: (1000 + interval, 1500 + interval),
            4: (1500 + interval, 2000 + interval),
        }
        y_ranges = {
            1: (-1000 - interval, 1900 + interval),
            2: [(-1000 - interval, 500 + interval), (1100 + interval, 1700 + interval)],
            3: [(-1000 - interval, 500 + interval), (1100 + interval, 1700 + interval)],
            4: (-1000 - interval, 1700 + interval),
        }
        choice = random.choice(list(x_ranges.keys()))
        x = random.randint(*x_ranges[choice])
        y_range = (
            random.choice(y_ranges[choice])
            if isinstance(y_ranges[choice], list)
            else y_ranges[choice]
        )
        y = random.randint(*y_range)
        return [x, y]

    def launch_rescue(self) -> None:
        """Activates the rescue operation."""
        self.rescue = True
        self.move = True

    def move_center(self) -> None:
        """Moves the ship towards the target position."""
        speed = 10
        delta_x = self.target_position[0] - self.position[0]
        delta_y = self.target_position[1] - self.position[1]

        if abs(delta_x) > speed:
            self.position[0] += speed if delta_x > 0 else -speed
            self.moving_right = delta_x > 0
        else:
            self.position[0] = self.target_position[0]

        if abs(delta_y) > speed:
            self.position[1] += speed if delta_y > 0 else -speed
        else:
            self.position[1] = self.target_position[1]

        self.rect.center = self.position

        if self.position == self.target_position:
            self.move = False
            if not self.arrive:
                self.arrive = True
                self.run.player.add_message(
                    "RESCUE SHIP ARRIVED", (500, 200), (500, 50), (0, 0, 0), 50, 1000
                )

    def update(self, x_var: int, y_var: int, player_rect: pygame.Rect) -> None:
        """Updates the ship's position and handles animations."""
        x = (x_var / 2) * self.run.zoom
        y = (y_var / 2) * self.run.zoom

        self.position[0] += x
        self.position[1] += y
        self.target_position[0] += x
        self.target_position[1] += y

        if not self.move:
            self.float_counter += 0.3
            floating_offset = math.sin(self.float_counter) * 2
            self.position[1] += floating_offset
            self.image = (
                self.original_image
                if self.facing_right
                else pygame.transform.flip(self.original_image, True, False)
            )
        else:
            self.move_center()

        current_time = pygame.time.get_ticks()
        if self.move and current_time - self.last_update > self.animation_delay:
            self.last_update = current_time
            self.current_move_frame = (self.current_move_frame + 1) % len(
                self.move_images_right
            )
            self.image = (
                self.move_images_right[self.current_move_frame]
                if self.facing_right
                else self.move_images_left[self.current_move_frame]
            )

        self.rect.center = self.position

        if not self.moving_right and self.facing_right:
            self.facing_right = False
            self.current_move_frame = 0
            self.image = self.move_images_left[self.current_move_frame]
        elif self.moving_right and not self.facing_right:
            self.facing_right = True
            self.current_move_frame = 0
            self.image = self.move_images_right[self.current_move_frame]

        self.check_collision(player_rect)

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the rescue ship on the screen."""
        if self.rescue or self.move:
            if self.show_ladder and not self.move:
                self.draw_ladder(screen)
            screen.blit(self.image, self.rect)

    def draw_ladder(self, screen: pygame.Surface) -> None:
        """Draws the rescue ladder."""
        ladder_x = (
            self.rect.x
            + self.image.get_width()
            - (100 if self.facing_right else 170) * self.run.zoom * 0.5
        )
        ladder_y_start = self.rect.y + 60 * self.run.zoom * 0.5
        ladder_height = int(100 * self.run.zoom * 0.5)
        bar_spacing = int(20 * self.run.zoom * 0.5)
        ladder_color = (0, 0, 0)

        pygame.draw.line(
            screen,
            ladder_color,
            (ladder_x, ladder_y_start),
            (ladder_x, ladder_y_start + ladder_height),
            int(3 * self.run.zoom * 0.5),
        )
        pygame.draw.line(
            screen,
            ladder_color,
            (ladder_x + 10 * self.run.zoom * 0.5, ladder_y_start),
            (ladder_x + 10 * self.run.zoom * 0.5, ladder_y_start + ladder_height),
            int(3 * self.run.zoom * 0.5),
        )
        for i in range(0, ladder_height // bar_spacing):
            y = ladder_y_start + i * bar_spacing
            pygame.draw.line(
                screen,
                ladder_color,
                (ladder_x, y),
                (ladder_x + 10 * self.run.zoom * 0.5, y),
                int(3 * self.run.zoom * 0.5),
            )
        self.ladder_rect.update(
            ladder_x - 10 * self.run.zoom * 0.5,
            ladder_y_start + ladder_height,
            30 * self.run.zoom * 0.5,
            15 * self.run.zoom * 0.5,
        )

    def check_collision(self, player_rect: pygame.Rect) -> None:
        """Checks for collision with the player."""
        if self.rect.colliderect(player_rect):
            self.show_ladder = True

        if self.ladder_rect.colliderect(player_rect):
            self.ladder_rect.size = (0, 0)
            self.show_ladder = False
            self.rescue = False
            self.run.win = True
            self.run.player.die()

    def change_zoom(self) -> None:
        """Recalculates visuals when zoom changes."""
        self.speed = 10 * self.run.zoom * 0.5
        self.original_image = Load.charge_image(
            self, self.run.zoom / 2, "rescue", "ship", "png", 1
        )
        self.move_images_right = [
            Load.charge_image(
                self, self.run.zoom / 2, "rescue", "ship_move1", "png", 1
            ),
            Load.charge_image(
                self, self.run.zoom / 2, "rescue", "ship_move2", "png", 1
            ),
            Load.charge_image(
                self, self.run.zoom / 2, "rescue", "ship_move3", "png", 1
            ),
        ]
        self.move_images_left = [
            pygame.transform.flip(img, True, False) for img in self.move_images_right
        ]
        self.image = (
            self.original_image
            if self.facing_right
            else pygame.transform.flip(self.original_image, True, False)
        )
        self.rect = self.image.get_rect()
