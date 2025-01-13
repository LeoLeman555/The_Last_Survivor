import pygame


class Icon:
    def __init__(self, run, resource: dict, bars: dict):
        """Initialize the Icon class with resources and bars."""
        self.resource = resource
        self.bars = bars
        self.run = run

    def update(self):
        """Update resources and trigger actions if limits are reached."""
        # Clamp resource values within their maximum and minimum bounds
        self.resource["food"] = max(
            0, min(self.resource["food"], self.bars["food_max"])
        )
        self.resource["health"] = max(
            0, min(self.resource["health"], self.bars["health_max"])
        )

        # Handle XP logic: reset if max is reached, trigger power-up
        if self.resource["xp"] >= self.bars["xp_max"]:
            self.resource["xp"] = 0
            self.run.manager.change_max_xp(self.run.index_palier_xp + 1)
            self.run.manager.launch_power_up()

    def draw(self, screen: pygame.Surface):
        """Draw resource bars and icons on the screen."""

        def calculate_bar_length(current, maximum):
            return round(current * 79 / maximum)

        def draw_resource_icon(name, x, y, width, height, shift_x, shift_y, value):
            self.draw_icon(screen, name, x, y, width, height, shift_x, shift_y, value)

        # Calculate bar lengths based on resource values
        self.bars["xp_bar"] = calculate_bar_length(
            self.resource["xp"], self.bars["xp_max"]
        )
        self.bars["health_bar"] = calculate_bar_length(
            self.resource["health"], self.bars["health_max"]
        )
        self.bars["food_bar"] = calculate_bar_length(
            self.resource["food"], self.bars["food_max"]
        )

        # Draw resource bars
        self.draw_bar(screen, "xp_bar", 20, 20, self.bars["xp_bar"])
        self.draw_bar(screen, "health_bar", 20, 45, self.bars["health_bar"])
        self.draw_bar(screen, "food_bar", 20, 70, self.bars["food_bar"])

        # Draw resource icons
        draw_resource_icon(
            "energy_icon", 130, 100, 25, -3, 22, 20, self.resource["energy"]
        )
        draw_resource_icon(
            "metal_icon", 20, 100, 25, -3, 22, 20, self.resource["metal"]
        )
        draw_resource_icon("data_icon", 20, 127, 30, -1, 30, 21, self.resource["data"])
        # draw_resource_icon("ammo_icon", 134, 125, 21, 1, 15, 29, self.resource["ammo"])

    def add_resource(self, name: str, value: int):
        """Add a value to a resource."""
        self.run.player.add_message(
            f"+{value} {name}", (500, 200), (500, 125), (0, 0, 0), 20, 750
        )
        try:
            self.resource[name] += value
        except KeyError:
            self.add_bars(name, value)

    def change_threshold(self, name: str, value: int):
        """Change the maximum value for a bar."""
        self.bars[f"{name}_max"] = value

    def add_bars(self, name: str, value: int):
        """Add a value to a bar."""
        self.bars[name] += value

    def draw_icon(
        self,
        screen: pygame.Surface,
        name: str,
        x_pos: int,
        y_pos: int,
        x_text: int,
        y_text: int,
        width: int,
        height: int,
        value=0,
    ):
        """Draw an icon and its value on the screen."""
        image = pygame.image.load(f"res/sprite/{name}.png")
        image = pygame.transform.scale(image, (width, height))
        screen.blit(image, (x_pos, y_pos))
        font = pygame.font.Font("res/texte/dialog_font.ttf", 18)
        self.draw_score(screen, font, value, x_pos + x_text, y_pos + y_text)

    def draw_score(
        self, screen: pygame.Surface, font: pygame.font.Font, value: int, x: int, y: int
    ):
        """Draw the score value near the icon."""
        score_text = font.render(f"{value}", True, (0, 0, 0))
        screen.blit(score_text, (x, y))

    def draw_bar(
        self, screen: pygame.Surface, name: str, x_bar: int, y_bar: int, value: int = 0
    ):
        """Draw mechanical bars based on the given value."""
        sprite_sheet = pygame.image.load(f"res/sprite/{name}.png")
        images = {f"{i * 10}": self.get_images(sprite_sheet, i * 22) for i in range(8)}

        # Determine key based on value range
        key = str((value // 10) * 10)
        key = key if key in images else "70"  # Default to max range if key is invalid

        for i, image in enumerate(images[key]):
            if i == value % 10:
                image.set_colorkey([0, 0, 0])
                screen.blit(image, (x_bar, y_bar))
                break

    def get_image(self, sheet: pygame.Surface, x: int, y: int) -> pygame.Surface:
        """Extract a single image from the sprite sheet."""
        image = pygame.Surface((186, 22))
        image.blit(sheet, (0, 0), (x, y, 186, 22))
        return image

    def get_images(self, sheet: pygame.Surface, y: int) -> list[pygame.Surface]:
        """Extract a series of images from a specific row in the sprite sheet."""
        return [self.get_image(sheet, i * 186, y) for i in range(10)]
