def reset_game_save(save_params, filename="data/game_save.txt"):
  save_params['money'] = 0
  for resource in save_params['resource']:
    save_params['resource'][resource] = 0
  for weapon in save_params['weapon_level']:
    if weapon == 'pistol':
      save_params['weapon_level'][weapon] = 1
    else:
      save_params['weapon_level'][weapon] = 0
  for extra in save_params['extras_level']:
    save_params['extras_level'][extra] = 0
  for power_up in save_params['power_up_level']:
    if power_up == "care_kit" or power_up == "survival_ration" or power_up == "2nd_life":
      save_params['power_up_level'][power_up] = 1
    else:
      save_params['power_up_level'][power_up] = 0

  with open(filename, 'w') as file:
    file.write("GAME_SAVE_PARAMS = {\n")
    file.write(f'  "money": {save_params["money"]},\n')
    file.write('  "resource": {\n')
    for resource, value in save_params['resource'].items():
      file.write(f'    "{resource}": {value},\n')
    file.write('  },\n')
    file.write('  "weapon_level": {\n')
    for weapon, value in save_params['weapon_level'].items():
      file.write(f'    "{weapon}": {value},\n')
    file.write('  },\n')
    file.write('  "extras_level": {\n')
    for extra, value in save_params['extras_level'].items():
      file.write(f'    "{extra}": {value},\n')
    file.write('  },\n')
    file.write('  "power_up_level": {\n')
    for power_up, value in save_params['power_up_level'].items():
      file.write(f'    "{power_up}": {value},\n')
    file.write('  }\n')
    file.write('}\n')
  return save_params