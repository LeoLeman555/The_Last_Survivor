import random


class Choice:
    def __init__(self, id_enemy: int, data_enemies: dict):
        """Initialize with enemy ID and data of enemies."""
        self.id_enemy = id_enemy
        self.data_enemies = data_enemies

    def choose(
        self,
        prob_A: int,
        prob_B: int,
        prob_Resource: int,
        prob_Food: int,
        prob_Weapon: int,
        prob_ESP: int,
        prob_Module: int,
    ) -> str:
        """Choose an option based on provided probabilities."""
        initial_choice = random.choices(["A", "B"], [prob_A, prob_B])[0]

        if initial_choice == "A":
            choice_A = random.choices(
                ["resources", "food"], [prob_Resource, prob_Food]
            )[0]
            if choice_A == "resources":
                choice_A = random.choices(["energy", "metal", "data"], [50, 50, 50])[0]
            return choice_A

        elif initial_choice == "B":
            choice_B = random.choices(
                ["weapon", "ESP", "module"], [prob_Weapon, prob_ESP, prob_Module]
            )[0]

            if choice_B == "module":
                rarity = random.choice(
                    ["Common", "Rare"]
                )  # Simplified choice with two options
                return f"module ({rarity})"

            return f"{choice_B}"

    def weapon(self, current_weapon: int, unlock_weapons: list) -> int:
        """Generate a new weapon ID based on probabilities and unlock status."""
        unlocked_weapons = set(
            int(weapon_id) for weapon_id in unlock_weapons
        )  # Use set for faster look-up
        outcomes = [-1, 0, 1, 2]
        probabilities = [0.10, 0.35, 0.50, 0.05]
        result = random.choices(outcomes, probabilities)[0]
        future_weapon = current_weapon + result

        if future_weapon not in unlocked_weapons:
            future_weapon = current_weapon

        return future_weapon
