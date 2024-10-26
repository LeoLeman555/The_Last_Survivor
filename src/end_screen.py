import pygame
from change_game_data import ChangeGameData

class GameOverScreen:
  def __init__(self, width, height, rewards, victory):
    # Initialize Pygame and screen attributes
    pygame.init()
    self.width = width
    self.height = height
    self.victory = victory
    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption("The Last Survivor - Game Over")

    # Define colors
    self.black = (0, 0, 0)
    self.color = (255, 255, 255)
    self.shadow_color = (64, 64, 64)

    self.background_image = self.load_image(f"res/end/screen_{self.victory}.png", (self.width, self.height))

    # Load the "GAME OVER" image instead of rendering text
    self.game_over_image = self.load_image(f"res/end/text_{self.victory}.png", (461, 164))
    self.game_over_rect = self.game_over_image.get_rect(center=(self.width // 2, 125))

    self.rewards_font = pygame.font.Font("res/texte/dialog_font.ttf", 30)

    # Rewards (passed as a dictionary)
    self.rewards = rewards
    self.change_game_data = ChangeGameData(self.rewards)
    self.rewards = self.rewards["resource"]
    self.rewards["money"] = rewards["money"]

    # Load reward icons
    self.energy_icon = self.load_image("res/sprite/energy_icon.png", (44, 40))
    self.metal_icon = self.load_image("res/sprite/metal_icon.png", (44, 40))
    self.data_icon = self.load_image("res/sprite/data_icon.png", (44, 32))
    self.money_icon = self.load_image("res/shop/icon_money.png", (38, 26))

    # Animation variables
    self.scale = 1.0
    self.growing = True
    self.animation_speed = 0.017

    # Rewards animation variables
    self.temp_rewards = {key: 0 for key in self.rewards}  # Temporary rewards start at 0
    self.current_reward = "energy"  # Start with energy reward
    self.max_duration = 60  # Total frames over which animation should complete per reward

    # Delay between reward animations (in seconds)
    self.delay_between_rewards = 0  # 60 frames (1 second at 60 FPS)
    self.delay_counter = 0  # Counter to keep track of delay between animations

    # Frame rate management
    self.clock = pygame.time.Clock()

    # Easing factor to control how slow the animation becomes at the end
    self.easing_factor = 3

  def load_image(self, path, size):
    """Helper function to load and scale images."""
    try:
      image = pygame.image.load(path)
      return pygame.transform.scale(image, size)
    except pygame.error as e:
      print(f"Failed to load image {path}: {e}")
      return None

  def animate_game_over_image(self):
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
    scaled_image = pygame.transform.scale(self.game_over_image, (scaled_width, scaled_height))
    
    # Recenter the image
    scaled_rect = scaled_image.get_rect(center=self.game_over_rect.center)
    return scaled_image, scaled_rect

  def animate_current_reward(self, frame):
    """Anime la récompense actuelle en réduisant la vitesse d'incrémentation progressivement."""
    # Ordre des récompenses à afficher
    reward_order = ["energy", "metal", "data", "money"]

    current_index = reward_order.index(self.current_reward)
    next_reward = reward_order[current_index + 1] if current_index + 1 < len(reward_order) else None

    # Valeur finale de la récompense actuelle
    final_value = self.rewards[self.current_reward]

    # Calcul du progrès actuel basé sur le nombre de frames
    progress = frame / self.max_duration
    if progress > 1:
      progress = 1  # S'assurer qu'on ne dépasse pas

    # Utilisation d'une fonction d'easing pour ralentir la progression vers la fin
    eased_progress = 1 - (1 - progress) ** self.easing_factor  # Utilise self.easing_factor pour contrôler la lenteur

    # Mise à jour de la récompense temporaire en fonction du progrès eased
    self.temp_rewards[self.current_reward] = int(eased_progress * final_value)

    # Si la récompense actuelle a terminé son animation
    if self.temp_rewards[self.current_reward] >= final_value:
      if self.delay_counter >= self.delay_between_rewards:
        # Passer à la récompense suivante après le délai
        if next_reward:
          self.current_reward = next_reward  # Passer à la récompense suivante
          self.delay_counter = 0  # Réinitialiser le compteur de délai pour la prochaine récompense
          return 0  # Réinitialiser le compteur de frames pour la nouvelle récompense
      else:
        # Incrémenter le compteur de délai (pour créer la pause de 1 seconde)
        self.delay_counter += 1

    return frame  # Continuer avec la récompense actuelle
  def display_rewards(self):
    """Display rewards with icons and animated values."""
    # Définir la couleur de l'ombre rouge

    rewards = [
      (self.energy_icon, f"{int(self.temp_rewards['energy'])}"),
      (self.metal_icon, f"{int(self.temp_rewards['metal'])}"),
      (self.data_icon, f"{int(self.temp_rewards['data'])}"),
      (self.money_icon, f"{int(self.temp_rewards['money'])}")
    ]

    for i, (icon, text) in enumerate(rewards):
      if self.temp_rewards[list(self.rewards.keys())[i]] > 0:
        # Créer l'ombre (en rouge) avec un léger décalage
        shadow_text = self.rewards_font.render(text, True, self.shadow_color)
        shadow_text_rect = shadow_text.get_rect(topleft=(170 + 2, 250 + i * 60 + 2 - 3))  # Décalé de 2px à droite et en bas

        # Créer le texte principal (en blanc)
        reward_text = self.rewards_font.render(text, True, self.color)
        reward_text_rect = reward_text.get_rect(topleft=(170, 250 + i * 60 - 3))

        self.screen.blit(icon, (100, 250 + i * 60))
        self.screen.blit(shadow_text, shadow_text_rect)  # Afficher l'ombre
        self.screen.blit(reward_text, reward_text_rect)  # Afficher le texte principal

  def run(self):
    running = True
    frame = 0  # Keep track of the frame count for animation
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.save_awards()
          running = False

      self.screen.fill(self.black)
      if self.background_image:
        self.screen.blit(self.background_image, (0, 0))

      # Animate and draw the scaled "GAME OVER" image
      scaled_image, scaled_rect = self.animate_game_over_image()
      self.screen.blit(scaled_image, scaled_rect)

      # Animate the current reward
      frame = self.animate_current_reward(frame)
      frame += 1
      self.display_rewards()

      pygame.display.flip()
      self.clock.tick(60)

    pygame.quit()

  def save_awards(self):
    self.change_game_data.change_params(self.change_game_data.reward, self.change_game_data.game_save_data)
