import pygame

class ReturnButton:
  def __init__(self, image_path, click_image_path, position):
    self.image = pygame.image.load(image_path).convert_alpha()
    self.click_image = pygame.image.load(click_image_path).convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.center = position
    self.original_pos = self.rect.topleft
    self.is_clicked = False

  def draw(self, screen, mouse_pos):
    if self.rect.collidepoint(mouse_pos):
      screen.blit(self.click_image, (self.rect.x + 1, self.rect.y + 1))
    else:
      screen.blit(self.image, self.rect)

  def is_pressed(self, mouse_pos, press_mouse):
    return self.rect.collidepoint(mouse_pos) and press_mouse