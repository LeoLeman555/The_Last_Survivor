import pygame
import time


class CardManager:
    def __init__(self, run, text_path: str, data: dict, image_folder: str):
        self.run = run
        self.cards = []
        self.positions = [(274, 200), (590, 200)]
        self.text_image = pygame.image.load(f"res/power_up/{text_path}.png")
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = (500, 120)
        self.data = data
        self.image_folder = image_folder

        self.last_click_times = 0
        self.cooldown = 0.5

        self.cooldown_start_time = None

        self.blink_timer = 0
        self.blink_interval = 0.5

    def get_image(self, name, level):
        image_path = f"res/power_up/{self.image_folder}/{name}_{level}.png"
        image = pygame.image.load(image_path)
        return self.run.load.split_image(image)

    def launch_cards(self, names: list):
        self.cards = []
        for i, name in enumerate(names):
            if name in self.data:
                card_data = self.data[name]
                left_image, right_image = self.get_image(name, card_data[1])
                position = self.positions[i]
                rect = left_image.get_rect(topleft=position)
                self.cards.append(
                    {
                        "name": name,
                        "left_image": left_image,
                        "right_image": right_image,
                        "current_image": left_image,
                        "rect": rect,
                        "id": card_data[0],
                        "level": card_data[1],
                    }
                )

        self.cooldown_start_time = pygame.time.get_ticks() / 1000

    def draw(self, screen: pygame.Surface):
        if self.run.power_up_launch:
            current_time = pygame.time.get_ticks() / 1000  # Temps en secondes
            if (current_time - self.blink_timer) % (
                2 * self.blink_interval
            ) < self.blink_interval:
                screen.blit(self.text_image, self.text_image_rect)

        for card in self.cards:
            screen.blit(card["current_image"], card["rect"])

    def update(self, mouse_pos: tuple, mouse_click: bool):
        if self.cooldown_start_time is not None:
            current_time = pygame.time.get_ticks() / 1000
            if current_time - self.cooldown_start_time < self.cooldown:
                return
            else:
                self.cooldown_start_time = None

        for card in self.cards[:]:
            if card["rect"].collidepoint(mouse_pos):
                card["current_image"] = card["right_image"]
                current_time = time.time()
                if mouse_click:
                    if current_time - self.last_click_times > self.cooldown:
                        self.last_click_times = current_time
                        self.on_card_click(card)
                        self.cards = []
                        self.run.pause = False
                        self.run.power_up_launch = False
                        self.run.active_panel = None
                        self.run.electrodes_manager.stop()
                        self.run.mouse["active_click"] = False
                        self.run.mouse["cooldown_active_click"] = (
                            pygame.time.get_ticks() / 1000
                        )
            else:
                card["current_image"] = card["left_image"]
