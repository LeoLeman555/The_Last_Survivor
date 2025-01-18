import pygame
import time
from src.data_handling.load import *
from src.data_handling.read_data import *
from src.data_handling.change_game_data import *
from src.UI.widgets.button import *


class GameOverScreen:
    def __init__(self, width: int, height: int, rewards: dict, victory: bool):
        """Initialize the game over screen with necessary data and assets."""
        self.width = width
        self.height = height
        self.victory = victory
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The Last Survivor - Game Over")
        pygame.display.set_icon(pygame.image.load("res/icons/official_logo.png"))

        self.read_data = ReadData()
        self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
        self.FPS = int(self.game_data["options"]["fps"])

        self.button_return = Button("button_return", (975, 25))

        # Animation setup
        self.end_screen_step = 1
        self.mouse_pos = 0
        self.mouse_press = False
        self.last_click_times = [0] * 1
        self.cooldown = 0.5

        # Colors
        self.black = (0, 0, 0)
        self.color = (255, 255, 255)
        self.shadow_color = (64, 64, 64)

        # Load images and fonts
        self.background_image = self.load_image(
            f"res/end/screen_{self.victory}.png", (self.width, self.height)
        )
        self.game_over_image = self.load_image(
            f"res/end/text_{self.victory}.png", (461, 164)
        )
        self.game_over_rect = self.game_over_image.get_rect(
            center=(self.width // 2, 125)
        )

        self.rewards_font = pygame.font.Font("res/fonts/futurist_font.ttf", 30)

        # Initialize rewards
        self.rewards = rewards
        self.change_game_data = ChangeGameData(self.rewards)
        self.rewards = self.rewards["resource"]
        self.rewards["money"] = rewards["money"]

        # Load reward icons
        self.energy_icon = self.load_image("res/sprite/energy_icon.png", (44, 40))
        self.metal_icon = self.load_image("res/sprite/metal_icon.png", (44, 40))
        self.data_icon = self.load_image("res/sprite/data_icon.png", (44, 32))
        self.money_icon = self.load_image("res/shop/icon_money.png", (38, 26))

        # Animation state
        self.scale = 1.0
        self.growing = True
        self.animation_speed = 0.017
        self.temp_rewards = {key: 0 for key in self.rewards}
        self.current_reward = "energy"
        self.max_duration = 60
        self.delay_between_rewards = 0
        self.delay_counter = 0

        # Frame rate management
        self.clock = pygame.time.Clock()
        self.easing_factor = 3

    def load_image(self, path: str, size: tuple[int, int]) -> pygame.Surface:
        """Helper function to load and scale images."""
        try:
            image = pygame.image.load(path)
            return pygame.transform.scale(image, size)
        except pygame.error as e:
            print(f"Failed to load image {path}: {e}")
            return None

    def animate_game_over_image(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Animate the 'GAME OVER' image with scaling."""
        if self.growing:
            self.scale += self.animation_speed
            if self.scale >= 1.5:
                self.growing = False
        else:
            self.scale -= self.animation_speed
            if self.scale <= 1.0:
                self.growing = True

        # Scale the image
        scaled_width = int(self.game_over_image.get_width() * self.scale)
        scaled_height = int(self.game_over_image.get_height() * self.scale)
        scaled_image = pygame.transform.scale(
            self.game_over_image, (scaled_width, scaled_height)
        )

        # Recenter the image
        scaled_rect = scaled_image.get_rect(center=self.game_over_rect.center)
        return scaled_image, scaled_rect

    def animate_current_reward(self, frame: int) -> int:
        """Animate the current reward with easing to slow down towards the end."""
        reward_order = ["energy", "metal", "data", "money"]
        current_index = reward_order.index(self.current_reward)
        next_reward = (
            reward_order[current_index + 1]
            if current_index + 1 < len(reward_order)
            else None
        )

        final_value = self.rewards[self.current_reward]
        progress = frame / self.max_duration
        progress = min(progress, 1)

        # Easing function to slow down the animation towards the end
        eased_progress = 1 - (1 - progress) ** self.easing_factor
        self.temp_rewards[self.current_reward] = int(eased_progress * final_value)

        if self.temp_rewards[self.current_reward] >= final_value:
            if self.delay_counter >= self.delay_between_rewards:
                if next_reward:
                    self.current_reward = next_reward
                    self.delay_counter = 0
                    return 0  # Reset the frame count for the next reward
            else:
                self.delay_counter += 1
        return frame

    def display_rewards(self) -> None:
        """Display the rewards with animations on the screen."""
        self.button_return.draw(self.screen, self.mouse_pos)
        rewards = [
            (self.energy_icon, f"{int(self.temp_rewards['energy'])}"),
            (self.metal_icon, f"{int(self.temp_rewards['metal'])}"),
            (self.data_icon, f"{int(self.temp_rewards['data'])}"),
            (self.money_icon, f"{int(self.temp_rewards['money'])}"),
        ]

        for i, (icon, text) in enumerate(rewards):
            if self.temp_rewards[list(self.rewards.keys())[i]] > 0:
                shadow_text = self.rewards_font.render(text, True, self.shadow_color)
                shadow_text_rect = shadow_text.get_rect(
                    topleft=(170 + 2, 250 + i * 60 + 2 - 3)
                )
                reward_text = self.rewards_font.render(text, True, self.color)
                reward_text_rect = reward_text.get_rect(topleft=(170, 250 + i * 60 - 3))
                self.screen.blit(icon, (100, 250 + i * 60))
                self.screen.blit(shadow_text, shadow_text_rect)
                self.screen.blit(reward_text, reward_text_rect)

    def update(self) -> None:
        """Update the screen and handle user inputs."""
        self.press_buttons()

    def press_buttons(self) -> None:
        """Handle button presses with cooldown."""
        current_time = time.time()
        return_button_index = 0
        if self.button_return.is_pressed(self.mouse_pos, self.mouse_press):
            if (
                current_time - self.last_click_times[return_button_index]
                > self.cooldown
            ):
                self.end_screen_step = 0 if self.end_screen_step == 1 else 1
                self.last_click_times[return_button_index] = current_time

    def run(self) -> None:
        """Main game loop for the game over screen."""
        running = True
        frame = 0
        while running:
            self.mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.end_screen_step <= 0:
                    self.save_awards()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_press = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_press = False
            self.update()
            self.screen.fill(self.black)
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))

            scaled_image, scaled_rect = self.animate_game_over_image()
            self.screen.blit(scaled_image, scaled_rect)

            frame = self.animate_current_reward(frame)
            frame += 1
            self.display_rewards()

            pygame.display.flip()
            self.clock.tick(self.FPS)

    def save_awards(self) -> None:
        """Save the updated rewards to the game save data."""
        self.change_game_data.change_params(
            self.change_game_data.reward, self.change_game_data.game_save_data
        )
