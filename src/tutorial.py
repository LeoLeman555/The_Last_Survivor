import pygame

class Tutorial:
  def __init__(self):
    self.font = pygame.font.Font("res/texte/dialog_font.ttf", 18)

  def draw_play(self, screen):
    text = self.font.render("Metal", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (100, 120)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, (0, 0, 0), (95, 130), (65, 115))

    text = self.font.render("Energy", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (210, 120)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, (0, 0, 0), (205, 130), (175, 115))

    text = self.font.render("Data", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (100, 147)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, (0, 0, 0), (95, 157), (65, 142))

    text = self.font.render("Your experience", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (250, 10)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, (0, 0, 0), (245, 20), (205, 25))

    screen.blit(text, text_rect)
    text = self.font.render("Your health", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (250, 40)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, (0, 0, 0), (245, 50), (205, 55))

    screen.blit(text, text_rect)
    text = self.font.render("Your food bar", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (250, 70)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, (0, 0, 0), (245, 80), (205, 85))

    screen.blit(text, text_rect)
    text = self.font.render("Time remaining before end of mission", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (560, 10)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, (0, 0, 0), (560, 23), (533, 20))

  def draw_arrow(self, screen):
    text = self.font.render("Direction of the recovery ship", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (560, 40)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, (0, 0, 0), (558, 53), (533, 50))

  def draw_shop(self, screen, step):
    if step <= 1:
      text = self.font.render("Click here to buy weapons or extras", True, (255, 255, 255))
      text_rect = text.get_rect()
      text_rect.topleft = (100, 350)
      screen.blit(text, text_rect)
      pygame.draw.line(screen, (255, 255, 255), (200, 350), (250, 240))

      text = self.font.render("Or here to unlock the power ups", True, (255, 255, 255))
      text_rect = text.get_rect()
      text_rect.topleft = (500, 400)
      screen.blit(text, text_rect)
      pygame.draw.line(screen, (255, 255, 255), (570, 400), (640, 240))
    else:
      text = self.font.render("Your money :)", True, (255, 255, 255))
      text_rect = text.get_rect()
      text_rect.topleft = (150, 15)
      screen.blit(text, text_rect)
      pygame.draw.line(screen, (255, 255, 255), (145, 25), (130, 27))

      text = self.font.render("To buy or upgrade", True, (255, 255, 255))
      text_rect = text.get_rect()
      text_rect.center = (200, 300)
      screen.blit(text, text_rect)
      pygame.draw.line(screen, (255, 255, 255), (215, 290), (185, 270))
      pygame.draw.line(screen, (255, 255, 255), (220, 290), (295, 270))
    
      if step % 2 == 0:
        text = self.font.render("Go to next", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topright = (965, 290)
        screen.blit(text, text_rect)


  def draw_options(self, screen):
    text = self.font.render("Reset all progress", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topright = (700, 520)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, (255, 255, 255), (705, 532), (800, 550))

    text = self.font.render("Disable tutorial", True, (255, 255, 255))
    text_rect.topleft = (810, 425)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, (255, 255, 255), (805, 437), (760, 450))

    text = self.font.render("Change controls", True, (255, 255, 255))
    text_rect.topleft = (400, 110)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, (255, 255, 255), (text_rect.topleft[0] - 5, text_rect.topleft[1] + 12), (350, 150))

  def draw_main_menu(self, screen, name):
    if name == "play":
      text = self.font.render("Start a game", True, (255, 255, 255))
      text_rect = text.get_rect()
      text_rect.topleft = (700, 100)
      screen.blit(text, text_rect)
      pygame.draw.line(screen, (255, 255, 255), (695, 112), (610, 125))

    if name == "shop":
      text = self.font.render("Display the store", True, (255, 255, 255))
      text_rect = text.get_rect()
      text_rect.topleft = (700, 200)
      screen.blit(text, text_rect)
      pygame.draw.line(screen, (255, 255, 255), (695, 212), (610, 225))
    
    if name == "options":
      text = self.font.render("Change settings", True, (255, 255, 255))
      text_rect = text.get_rect()
      text_rect.topleft = (700, 300)
      screen.blit(text, text_rect)
      pygame.draw.line(screen, (255, 255, 255), (695, 312), (610, 325))


  def draw(self, screen, title, name):
    pass