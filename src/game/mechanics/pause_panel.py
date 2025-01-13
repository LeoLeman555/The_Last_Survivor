import pygame
from src.UI.widgets.button import *


class PausePanel:
    def __init__(self, run):
        self.run = run

        self.button_return = Button("button_pause", (975, 25))

        self.panel = pygame.image.load("res/pause/panel.png")
        self.panel_rect = self.panel.get_rect()
        self.panel_rect.center = (500, 300)

        self.button_play = pygame.image.load("res/pause/button_play.png")
        self.button_play_click = pygame.image.load("res/pause/button_play_click.png")
        self.button_play_rect = self.button_play.get_rect()
        self.button_play_rect.center = (500, 300)

        self.button_quit = pygame.image.load("res/pause/button_quit.png")
        self.button_quit_click = pygame.image.load("res/pause/button_quit_click.png")
        self.button_quit_rect = self.button_quit.get_rect()
        self.button_quit_rect.center = (500, 370)

        self.mouse_press = False

    def press_pause(self) -> None:
        """Handle button presses"""
        self.button_return.draw(self.run.screen, self.run.mouse["position"])
        if self.button_return.is_pressed(
            self.run.mouse["position"], self.run.mouse["press"]
        ):
            self.run.pause = True

    def draw(self):
        self.run.screen.blit(self.panel, self.panel_rect)

        if self.button_play_rect.collidepoint(self.run.mouse["position"]):
            self.run.screen.blit(self.button_play_click, self.button_play_rect)
            if self.run.mouse["press"]:
                self.run.pause = False
        else:
            self.run.screen.blit(self.button_play, self.button_play_rect)

        if self.button_quit_rect.collidepoint(self.run.mouse["position"]):
            self.run.screen.blit(self.button_quit_click, self.button_quit_rect)
            if self.run.mouse["press"]:
                self.run.running = False
        else:
            self.run.screen.blit(self.button_quit, self.button_quit_rect)
