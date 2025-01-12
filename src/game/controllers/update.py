import pygame
import random

class Update:
  """Handles updates and rendering of all game elements."""

  def __init__(self, run) -> None:
    self.run = run
    self.particles_list = []

  def update_all(self) -> None:
    """Central update loop for the game."""
    if not self.run.pause:
      self.update_map()
      self.update_objects()
      self.update_bullets()
      self.update_enemies()
      self.update_weapon()
      self.update_toxic()

      if self.run.data_extras["missile"].get("activate", False):
        self.update_missile()

      if self.run.data_extras["laser_probe"].get("activate", False):
        self.update_laser()

      if self.run.data_extras["drone"].get("activate", False):
        self.update_drone()

      self.update_rescue()
      self.update_messages()

    self.update_electrodes()
    self.update_countdown()
    self.update_icon()
    self.update_cards()

  def update_cards(self) -> None:
    """Updates and draws all card-related elements."""
    for card_type in [self.run.power_up, self.run.weapons_cards, self.run.extras_cards]:
      card_type.update(self.run.mouse["position"], self.run.mouse["press"])

  def update_electrodes(self) -> None:
    self.run.electrodes_manager.update()

  def update_rescue(self) -> None:
    """Updates the rescue ship."""
    self.run.rescue_ship.update(*self.run.mouvement, self.run.player.rect_collision)

  def update_toxic(self) -> None:
    """Updates toxic particles."""
    self.particles_list = sorted(self.run.player.toxic_particles, key=lambda p: p.creation_time, reverse=True)
    for particle in self.particles_list:
      particle.update(*self.run.mouvement)

  def update_weapon(self) -> None:
    """Updates weapon-related elements."""
    self.run.weapon.rotate_to_cursor(self.run.mouse["position"])
    self.run.player.grenades.update(*self.run.mouvement)
    self.run.player.explosions.update()

  def update_bullets(self) -> None:
    """Updates bullets or specific particles based on the current weapon."""
    if self.run.current_weapon_dict["id"] == 7:
      self._update_collection(self.run.player.particles)
    else:
      self._update_collection(self.run.player.bullets)

  def update_enemies(self) -> None:
    """Updates all enemies."""
    for enemy in self.run.player.enemies:
      enemy.follow(475, 281)
      enemy.update(0.05, *self.run.mouvement, self.run.player.rect_collision)

  def update_objects(self) -> None:
    """Updates all objects."""
    self._update_collection(self.run.player.objects, *self.run.mouvement, self.run.player.rect_collision)

  def update_countdown(self) -> None:
    """Updates the countdown timer."""
    self.run.countdown.update(self.run.pause)

  def update_messages(self) -> None:
    """Updates in-game messages."""
    self._update_collection(self.run.player.messages)

  def update_map(self) -> None:
    """Updates the game map."""
    self.run.map_manager.update()

  def update_icon(self) -> None:
    """Updates and draws the game icon."""
    self.run.icon.update()
    self.run.arrow_indicator.update()

  def update_laser(self) -> None:
    """Handles laser-related updates."""
    if random.random() < self.run.data_extras["laser_probe"]["rarity"]:
      self.run.player.add_laser()
    self._update_collection(self.run.player.lasers)

  def update_missile(self) -> None:
    """Handles missile-related updates."""
    if random.random() < self.run.data_extras["missile"]["rarity"]:
      self.run.player.add_missile()
    self._update_collection(self.run.player.missiles, *self.run.mouvement)

  def update_drone(self) -> None:
    """Updates the drone."""
    self.run.drone.update()

  def _update_collection(self, collection: list, *args, **kwargs) -> None:
    """Updates all elements in a given collection."""
    for element in collection:
      element.update(*args, **kwargs)
