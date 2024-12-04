import random

class EnemyEvent:
  def __init__(self, enemies_dict: dict):
    """Initialize the EnemyEvent with the given dictionary of enemies."""
    self.enemies = enemies_dict

  def generate_enemy_events(self, difficulty: int) -> list:
    """Generate a list of enemy events based on difficulty and game phases."""
    enemies = self.enemies
    total_enemies_target = min(1000, int(40 + (difficulty - 1) ** 1.5))
    current_enemies = 0

    events = []
    # Rank enemies by increasing danger (calculated as max_health * speed)
    enemy_danger = {}
    for enemy_name, data in enemies.items():
      danger = data["max_health"] * data["speed"]
      enemy_danger[enemy_name] = danger

    # Sort enemies by their danger level
    sorted_enemies = sorted(enemies.items(), key=lambda x: enemy_danger[x[0]])

    # Define game phases with time limits
    early_phase = 60  # First phase (0 - 60 seconds)
    mid_phase = 120   # Intermediate phase (61 - 120 seconds)
    late_phase = 180  # Final phase (121 - 180 seconds)

    current_time = 0

    # Generate events based on the game phases
    while current_time < late_phase:
      if current_time < early_phase:
        # Early phase: Randomly select from the least dangerous enemies
        enemy_name, enemy_data = random.choice(sorted_enemies[:2])
        interval = 3  # Spawn interval (in seconds)
      elif current_time < mid_phase:
        # Mid phase: Select from moderately dangerous enemies
        enemy_name, enemy_data = random.choice(sorted_enemies[2:4])
        interval = 2
      elif 120 <= current_time <= 125 + difficulty // 10:
        # Late phase: Special condition for robots with adjusted interval
        enemy_name, enemy_data = random.choice([e for e in sorted_enemies if e[0] == "robot"])
        interval = 2
      else:
        # Final phase: Select from the most dangerous enemies
        enemy_name, enemy_data = random.choice(sorted_enemies[:4])
        interval = 1

      # Randomly decide how many enemies to spawn based on difficulty
      max_enemies_per_spawn = max(1, (difficulty // 4) + 1)
      number_enemies = random.randint(1, min(difficulty // 4 + 1, max_enemies_per_spawn))

      # Random spawn interval
      spawn_interval = random.randint(interval, interval + 2)

      # Update the current time and add the event
      current_time += spawn_interval
      events.append((enemy_name, number_enemies, current_time))
      current_enemies += number_enemies

    # Remove excess events if there are too many enemies
    while len(events) > total_enemies_target:
      event_to_remove = random.choice(events)
      events.remove(event_to_remove)

    return events
