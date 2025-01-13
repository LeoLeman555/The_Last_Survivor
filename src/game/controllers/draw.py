class Draw:
    def __init__(self, run) -> None:
        self.run = run
        self.particles_list = []

    def draw_all(self) -> None:
        """Displays all game elements."""
        self.run.map_manager.draw()
        self._draw_collection(self.run.player.objects)
        self._draw_collection(self.run.player.missiles)
        self._draw_collection(self.run.player.bullets)
        self._draw_collection(self.run.player.enemies)
        self._draw_collection(self.run.player.particles)
        self.run.weapon.draw(self.run.screen)
        self.run.player.grenades.draw(self.run.screen)
        self.run.player.explosions.draw(self.run.screen)
        self._draw_collection(self.run.player.lasers)
        self._draw_collection(self.run.player.toxic_particles)

        if self.run.data_extras["drone"].get("activate", False):
            self.run.drone.draw(self.run.screen)

        self.run.rescue_ship.draw(self.run.screen)
        self._draw_collection(self.run.player.messages)
        self.run.countdown.draw()
        self.run.arrow_indicator.draw(self.run.screen)

        if self.run.game_data["options"]["tutorial"] == "on":
            self.run.tutorial.draw_play(self.run.screen)
            if self.run.rescue_ship.rescue or self.run.rescue_ship.move:
                self.run.tutorial.draw_arrow(self.run.screen)

        self.run.icon.draw(self.run.screen)

        self.run.electrodes_manager.draw(self.run.screen)

        self._draw_collection(
            [self.run.power_up, self.run.weapons_cards, self.run.extras_cards]
        )

    def _draw_collection(self, collection: list) -> None:
        """Draws all elements in a given collection."""
        for element in collection:
            element.draw(self.run.screen)
