import random


class EnemySelector:
    def __init__(self, data_enemies: dict):
        self.data_enemies = data_enemies

    def filter_by_id_suffix(self, suffix: str) -> list:
        """Filters enemies whose ID ends with a given suffix."""
        return [
            name
            for name, params in self.data_enemies.items()
            if str(params["id"]).endswith(suffix)
        ]

    def filter_by_id_prefix(self, prefix: str) -> list:
        """Filters enemies whose ID starts with a given prefix."""
        return [
            name
            for name, params in self.data_enemies.items()
            if str(int(params["id"])).startswith(prefix)
        ]

    def filter_by_exact_id(self, exact_id: float) -> list:
        """Filters enemies whose ID matches a given exact ID."""
        return [
            name
            for name, params in self.data_enemies.items()
            if params["id"] == exact_id
        ]

    def filter_by_type(self, exact_type: str) -> list:
        """Filters enemies by a specific type."""
        return [
            name
            for name, params in self.data_enemies.items()
            if params["type"] == exact_type
        ]

    def filter_by_speed(self, min_speed: int = None, max_speed: int = None) -> list:
        """Filters enemies by speed within a given range."""
        return [
            name
            for name, params in self.data_enemies.items()
            if (min_speed is None or params["speed"] >= min_speed)
            and (max_speed is None or params["speed"] <= max_speed)
        ]

    def filter_by_health(self, min_health: int = None, max_health: int = None) -> list:
        """Filters enemies by health within a given range."""
        return [
            name
            for name, params in self.data_enemies.items()
            if (min_health is None or params["max_health"] >= min_health)
            and (max_health is None or params["max_health"] <= max_health)
        ]

    def random_enemy(self, enemy_list: list) -> tuple:
        """Generates a random enemy position based on predefined x and y ranges."""
        x_ranges = {1: (-500, 0), 2: (0, 500), 3: (500, 1000), 4: (1000, 1500)}
        y_ranges = {
            1: (-500, 1400),
            2: [(-500, 0), (600, 1200)],
            3: [(-500, 0), (600, 1200)],
            4: (-500, 1200),
        }
        choice = random.choice(list(x_ranges.keys()))
        x = random.randint(*x_ranges[choice])

        # Handle multiple possible y-ranges
        if isinstance(y_ranges[choice], list):
            y_range = random.choice(y_ranges[choice])
        else:
            y_range = y_ranges[choice]
        y = random.randint(*y_range)

        return random.choice(enemy_list), x, y
