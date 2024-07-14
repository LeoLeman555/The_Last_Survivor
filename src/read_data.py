class ReadData():
  def get_paliers(self, path):
    with open(path, "r") as fichier:
        palier = tuple(int(num) for line in fichier for num in line.split(','))
    return palier
  
  def read_weapon_data(self, path):
    #?  numéro de l'arme:("nom de l'arme", (taille de l'arme), (position), portée, explosion?
    # TODO (type de mu, coût de mu, chargeur), (DPS, portée), (ME, EN, DF nécessaires))
    data_weapon = {}
    with open(path, 'r') as file:
      for line in file:
        parts = line.strip().split(',')
        key = int(parts[0])
        name = parts[1]
        dimensions = (int(parts[2]), int(parts[3]))
        position = (int(parts[4]), int(parts[5]))
        power = int(parts[6])
        special = int(parts[7])
        data_weapon[key] = (name, dimensions, position, power, special)
    return data_weapon
  
  def read_ressources_data(self, path):
    ressources = {}
    with open(path, 'r') as file:
      for line in file:
        parts = line.strip().split(',')
        key = parts[0]
        value = int(parts[1])
        ressources[key] = value
    return ressources

  def read_barres_data(self, path):
    barres = {}
    with open(path, 'r') as file:
      for line in file:
        parts = line.strip().split(',')
        key = parts[0]
        value = int(parts[1])
        barres[key] = value
    return barres
  
  def read_animation_specs(filename):
    animation_specs = {}
    with open(filename, 'r') as file:
      for line in file:
        key, value = line.strip().split(':')
        animation_specs[key] = tuple(map(int, value.strip("()").split(',')))
    return animation_specs