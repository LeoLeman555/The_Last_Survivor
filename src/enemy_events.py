import random

class EnemyEvent:
  def __init__(self, enemies_dict):
    self.enemies = enemies_dict

  def generate_enemy_events(self, difficulty):
    enemies = self.enemies
    total_enemies_target = min(1000, int(40 + (difficulty - 1) ** 1.5))
    current_enemies = 0

    events = []
    # Rank enemies by increasing danger
    enemy_danger = {}
    for enemy_name, data in enemies.items():
      danger = data["max_health"] * data["speed"]
      enemy_danger[enemy_name] = danger
    sorted_enemies = sorted(enemies.items(), key=lambda x: enemy_danger[x[0]])

    # Game phases
    early_phase = 60 # First phase (0 - 60 seconds)
    mid_phase = 120 # Intermediate phase (61 - 120 seconds)
    late_phase = 180 # Final phase (121 - 180 seconds)

    current_time = 0

    # Ajout des événements
    while current_time < late_phase:
      if current_time < early_phase:
        enemy_name, enemy_data = random.choice(sorted_enemies[:2])
        interval = 3
      elif current_time < mid_phase:
        enemy_name, enemy_data = random.choice(sorted_enemies[2:4])
        interval = 2
      elif 120 <= current_time <= 125 + difficulty // 10:
        enemy_name, enemy_data = random.choice([e for e in sorted_enemies if e[0] == "robot"])
        interval = 2
      else:
        enemy_name, enemy_data = random.choice(sorted_enemies[:4])
        interval = 1

      max_enemies_per_spawn = max(1, (difficulty // 4) + 1)
      nbre_ennemis = random.randint(1, min(difficulty // 4 + 1, max_enemies_per_spawn))

      spawn_interval = random.randint(interval, interval + 2)

      current_time += spawn_interval
      events.append((enemy_name, nbre_ennemis, current_time))
      current_enemies += nbre_ennemis

    while len(events) > total_enemies_target:
      event_to_remove = random.choice(events)
      events.remove(event_to_remove)

    return events