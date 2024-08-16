import random

class Choice:
  def __init__(self, id_enemy, data_enemies):
    self.id_enemy = id_enemy
    self.data_enemies = data_enemies

  def choose(self, prob_A: int, prob_B: int, prob_Resource: int, prob_Food: int, prob_Weapon: int, prob_ESP: int, prob_Module: int) -> str:
    initial_choice = random.choices(['A', 'B'], [prob_A, prob_B])[0]

    if initial_choice == 'A':
      choice_A = random.choices(['resources', 'food'], [prob_Resource, prob_Food])[0]
      if choice_A == 'resources':
        choice_A = random.choices(['energy', 'metal', 'data'], [50, 50, 50])[0]
      return choice_A

    elif initial_choice == 'B':
      choice_B = random.choices(['weapon', 'ESP', 'module'], [prob_Weapon, prob_ESP, prob_Module])[0]

      if choice_B == 'module':
        rarity = random.choices(['Common', 'Rare'], [70, 30])[0]
        return f"module ({rarity})"

      return f"{choice_B}"
    
  def weapon(self, current_weapon):
    outcomes = [-1, 0, 1, 2, 3]
    probabilities = [0.10, 0.25, 0.50, 0.10, 0.05]
    result = random.choices(outcomes, probabilities)[0]
    futur_weapon = current_weapon + result
    if futur_weapon < 1:
      futur_weapon = 1
    if futur_weapon > 12:
      futur_weapon = 12
    return futur_weapon