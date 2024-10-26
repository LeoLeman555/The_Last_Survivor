import pygame
import time
from load import *
from change_game_data import ChangeGameData
from button import ReturnButton

class Shop:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("The Last Survivor - Shop")
    self.font = pygame.font.Font("res/texte/dialog_font.ttf", 18)

    # load all the data
    self.read_data = ReadData()
    self.load = Load()
    self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
    self.data_extras = self.read_data.read_params("data/extras.txt", "extras")
    self.data_extras_levels = self.read_data.read_params("data/extras_level.txt", "extras_level")
    self.data_extras_price = self.read_data.read_params("data/extras_price.txt", "price")
    self.data_weapons = self.read_data.read_params("data/weapons.txt", "weapons")
    self.data_weapons_levels = self.read_data.read_params("data/weapons_level.txt", "weapons_level")
    self.data_weapons_price = self.read_data.read_params("data/weapons_price.txt", "price")
    self.data_power_up = self.read_data.read_params("data/power_up.txt", "power_up")

    self.data_weapons = self.load.process_data(self.game_data, "weapon_level", self.data_weapons)
    self.data_extras = self.load.process_data(self.game_data, "extras_level", self.data_extras)
    self.data_power_up = self.load.process_data(self.game_data, "power_up_level", self.data_power_up)
    self.update_weapons_with_levels()
    self.update_extras_with_levels()

    # money icon
    self.icon_money = pygame.image.load("res/shop/icon_money.png")
    self.icon_money_rect = self.icon_money.get_rect()
    self.icon_money_rect.center = (80, 30)

    # return button
    self.button_return = ReturnButton(
      image_path="res/shop/button_return.png",
      click_image_path="res/shop/button_return_click.png",
      position=(975, 25)
    )

    # buy button
    self.button_buy = pygame.image.load("res/shop/button_buy.png").convert_alpha()
    self.button_buy_click = pygame.image.load("res/shop/button_buy_click.png").convert_alpha()
    self.button_buy_rect = self.button_buy.get_rect()
    self.button_buy_rect.center = (0, 0)
    self.button_buy_original_pos = self.button_buy_rect.topleft
    self.all_button_buy = {f"buy_{i}": [False, [], False] for i in range(1, 13)}
    i = 0
    for y in range(260, 780, 260):
      for x in range(160, 961, 160):
        i += 1
        self.all_button_buy[f"buy_{i}"][1].append(self.button_buy)
        self.all_button_buy[f"buy_{i}"][1].append(self.button_buy_rect.copy())
        self.all_button_buy[f"buy_{i}"][1][1].center = (x, y)
        self.all_button_buy[f"buy_{i}"][1].append(self.button_buy_click)
        element = self.all_button_buy[f"buy_{i}"][1][1].topleft
        self.all_button_buy[f"buy_{i}"][1].append(element)

    self.button_right_arrow = pygame.image.load("res/shop/right_arrow.png")
    self.button_right_arrow_rect = self.button_right_arrow.get_rect()
    self.button_right_arrow_rect.center = (980, 305)

    self.button_left_arrow = pygame.image.load("res/shop/left_arrow.png")
    self.button_left_arrow_rect = self.button_left_arrow.get_rect()
    self.button_left_arrow_rect.center = (20, 305)

    # background weapons
    self.back_weapon = pygame.image.load("res/shop/back_weapon.png").convert_alpha()
    self.back_weapon_rect = self.back_weapon.get_rect()

    self.weapon_names = ["Pistol", "Magnum", "Shotgun", "Sniper", "AK", "RPG", "Flamethrower", "Minigun", "G. Launcher", "Laser Gun", "Plasma Gun"]
    self.shop_table_weapon = self.create_table(self.data_weapons)
    self.weapon_images = {}
    self.create_weapon_images()

    self.extras_names = ["Grenade", "Toxic G.", "Drone", "Missile", "Laser Probe"]
    self.shop_table_extras = self.create_table(self.data_extras, str_key=True)
    self.extras_images = {}
    self.create_extras_images()

    self.power_up_names = ["Care kit", "Survival ration", "2nd life", "Critical hit", "Expert", "Boost", "Agile fingers", "Extra ammo", "Large range", "Magnetic", "Piercing", "Rapid fire", "Regeneration", "Zoom", "Strong stomach"]
    self.shop_tables_power_up = self.create_table(self.data_power_up, 3, 5, str_key=True)
    self.power_up_images = {}

    self.step_shop_menu = 1

    self.steps = {
      "step_1": {
        "cards": [],
        "positions": [(400, 100)],
        "names": ["card_weapon_extras"]
      }
    }
    self.create_cards_step_1()

    self.press_mouse = False
    self.last_click_times = [0] * (len(self.all_button_buy) + 1)
    self.last_click_time_arrow = [0, 0]
    self.cooldown = 0.5

  def create_cards_step_1(self):
    for i, name in enumerate(self.steps["step_1"]["names"]):
      left_image, right_image = self.get_image(name)
      position = self.steps["step_1"]["positions"][i]
      rect = left_image.get_rect(topleft=position)
      self.steps["step_1"]["cards"].append({
        'name': name,
        'left_image': left_image,
        'right_image': right_image,
        'current_image': left_image,
        'rect': rect,
      })

  def get_image(self, name):
    image_path = f"res/shop/{name}.png"
    image = pygame.image.load(image_path).convert_alpha()
    return Load.split_image(self, image) 

  def create_weapon_images(self):
    lock_image_path = "res/shop/lock.png"
    lock_image = pygame.image.load(lock_image_path).convert_alpha()
    lock_rect = lock_image.get_rect()
    self.weapon_images["LOCK"] = [lock_image, lock_rect]
    for index, weapon_name in enumerate(self.weapon_names, start=1):
      weapon_data = self.data_weapons.get(f"{index}", {})
      name = weapon_data.get("name", "")
      level = weapon_data.get("level", 0)
      if level >= 1:
        image_path = f"res/weapon/{name}/level_{level}.png"
      else:
        image_path = lock_image_path
      image = pygame.image.load(image_path).convert_alpha()
      rect = image.get_rect()
      self.weapon_images[weapon_name] = [image, rect]

  def create_extras_images(self):
    lock_image_path = "res/shop/lock.png"
    lock_image = pygame.image.load(lock_image_path).convert_alpha()
    lock_rect = lock_image.get_rect()
    self.extras_images["LOCK"] = [lock_image, lock_rect]

    for index, extras_name in enumerate(self.extras_names, start=0):
      name = list(self.data_extras.keys())[index]
      level = self.data_extras[name]["level"]
      if level >= 1:
        image_path = f"res/shop/{name}.png"
      else:
        image_path = lock_image_path
      image = pygame.image.load(image_path).convert_alpha()
      rect = image.get_rect()
      self.extras_images[extras_name] = [image, rect]

  def create_table(self, weapons_params, rows=2, cols=6, str_key=False):
    shop_table_weapon = []
    if str_key: 
      weapon_levels = [weapons_params[weapon_id]["level"] for weapon_id in weapons_params.keys()]
    else: 
      weapon_levels = [weapons_params[weapon_id]["level"] for weapon_id in sorted(weapons_params.keys(), key=int)]
    while len(weapon_levels) < rows * cols:
      weapon_levels.append(0)
    for i in range(rows):
      shop_table_weapon.append(weapon_levels[i * cols:(i + 1) * cols])
    return shop_table_weapon

  def update_weapons_with_levels(self):
    for weapon_id, weapon_data in self.data_weapons.items():
      weapon_name = weapon_data["name"]
      weapon_level = weapon_data["level"]
      if weapon_level > 0:
        level_upgrades = self.data_weapons_levels.get(weapon_name, {})
        for stat, upgrade_value in level_upgrades.items():
          if stat in weapon_data:
            if stat == "critical":
              weapon_data[stat] += upgrade_value * (weapon_level - 1)
            else:
              weapon_data[stat] += int(upgrade_value * (weapon_level - 1))
  
  def update_extras_with_levels(self):
    for extra_id, extra_data in self.data_extras.items():
      extra_name = extra_data["name"]
      extra_level = extra_data["level"]
      if extra_level > 0:
        level_upgrades = self.data_extras_levels.get(extra_name, {})
        for stat, upgrade_value in level_upgrades.items():
          if stat in extra_data:
            extra_data[stat] += upgrade_value * (extra_level - 1)
  
  def draw(self, mouse_pos):
    self.button_return.draw(self.screen, mouse_pos)
    self.screen.blit(self.icon_money, self.icon_money_rect)
    number_text = self.font.render(f"{self.game_data["money"]}", True, (255, 255, 255))
    text_rect = number_text.get_rect()
    text_rect.topleft = (self.icon_money_rect.centerx + 25, self.icon_money_rect.topleft[1])
    self.screen.blit(number_text, text_rect)

    if self.step_shop_menu == 1:
      self.screen.blit(self.steps["step_1"]["cards"][0]['current_image'], self.steps["step_1"]["cards"][0]['rect'])
    
    else:
      self.draw_step_2_3()
  
  def draw_elements(self, data: dict, data_price: dict, stats: dict, images: dict, shop_table: list[int], position: list[int], fake_names: list[str], data_names: list, number_line: int, number_row: int):
    x_start, x_interval, y_start, y_interval = position
    index_id = 0
    for line in range(number_line):
      for row in range(number_row):
        if shop_table[line][row] != 0:
          draw_name = fake_names[index_id]
        else: 
          draw_name = "LOCK"
        try:
          index_name = data_names[index_id]
          dict_element = data[index_name]
          if index_name == "12":
            index_name = None
        except:
          index_name = None
        index_id += 1
        # draw the background
        x = x_start + row * x_interval
        y = line
        self.back_weapon_rect.x = x
        self.back_weapon_rect.y = y_start + y * y_interval
        # todo change name of self.back_weapon
        self.screen.blit(self.back_weapon, self.back_weapon_rect)

        # draw the name
        text = self.font.render(draw_name, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.back_weapon_rect.x + self.back_weapon_rect.width // 2, 
                            self.back_weapon_rect.y + 25 + self.back_weapon_rect.height // 2)
        self.screen.blit(text, text_rect)

        # draw stats
        if draw_name != "LOCK":
          for name_text in stats.keys():
            text = self.font.render(name_text + str(dict_element[stats[name_text][0]]), True, stats[name_text][1])
            text_rect = text.get_rect()
            text_rect.topleft = (self.back_weapon_rect.x, self.back_weapon_rect.y + stats[name_text][2])
            self.screen.blit(text, text_rect)

        # draw price
        if index_name != None:
          if dict_element["level"] < 10:
            price = str(data_price[f"{dict_element["name"]}"][f"level_{dict_element["level"]+1}"]) + "$"
          else: 
            price = "-- MAX --"
          text = self.font.render("PRICE", True, (255, 255, 255))
          text_rect = text.get_rect()
          text_rect.topleft = (self.back_weapon_rect.x, self.back_weapon_rect.y + 180)
          self.screen.blit(text, text_rect)
          text = self.font.render(price, True, (255, 255, 255))
          text_rect = text.get_rect()
          text_rect.center = (self.back_weapon_rect.x + 35, self.back_weapon_rect.y + 210)
          self.screen.blit(text, text_rect)

          # draw buy button
          if self.all_button_buy[f"buy_{index_id}"][0] == False:
            self.screen.blit(self.all_button_buy[f"buy_{index_id}"][1][0], self.all_button_buy[f"buy_{index_id}"][1][1])
          else:
            topleft = self.all_button_buy[f"buy_{index_id}"][1][3]
            topleft = (topleft[0] + 2, topleft[1] + 2)
            self.screen.blit(self.all_button_buy[f"buy_{index_id}"][1][2], topleft)

        # draw the image
        rect = images[draw_name][1]
        rect.center = (self.back_weapon_rect.x + self.back_weapon_rect.width // 2, self.back_weapon_rect.y + self.back_weapon_rect.height // 2)
        self.screen.blit(images[draw_name][0], rect)

  
  def draw_step_2_3(self):
    if self.step_shop_menu == 2:
      self.screen.blit(self.button_right_arrow, self.button_right_arrow_rect)
      stats = {"DPS : ": ["damage", (254, 27, 0), 100], "RANGE : ": ["range", (1, 215, 88), 120], "LEVEL : ": ["level", (121, 248, 248), 80]}
      position = [40, 160, 60, 260]
      data_names = []
      for item in self.data_weapons:
        data_names.append(item)
      self.draw_elements(self.data_weapons, self.data_weapons_price, stats, self.weapon_images, self.shop_table_weapon, position, self.weapon_names, data_names, 2, 6)
      
    if self.step_shop_menu == 3:
      self.screen.blit(self.button_left_arrow, self.button_left_arrow_rect)
      stats = {"DPS : ": ["damage", (254, 27, 0), 100], "LEVEL : ": ["level", (121, 248, 248), 80]}
      position = [40, 160, 60, 260]
      data_names = list(self.data_extras.keys())
      self.draw_elements(self.data_extras, self.data_extras_price, stats, self.extras_images, self.shop_table_extras, position, self.extras_names, data_names, 2, 6)


  def update(self, mouse_pos: tuple):
    # Vérifier si le bouton retour est pressé
    if self.button_return.is_pressed(mouse_pos, self.press_mouse):
      current_time = time.time()
      return_button_index = len(self.all_button_buy)
      if current_time - self.last_click_times[return_button_index] > self.cooldown:
        if self.step_shop_menu == 3:
          self.step_shop_menu = 1
        else:
          self.step_shop_menu -= 1
        self.last_click_times[return_button_index] = current_time

    self.right_arrow(mouse_pos)
    self.left_arrow(mouse_pos)
    if self.step_shop_menu == 1:
      self.step_1(mouse_pos)
    elif self.step_shop_menu == 2 or self.step_shop_menu == 3:
      self.step_2_3(mouse_pos)

  def step_1(self, mouse_pos):
    for card in self.steps["step_1"]["cards"][:]:
      if card['rect'].collidepoint(mouse_pos):
        card['current_image'] = card['right_image']
        if self.press_mouse:
          # print(card["name"])
          self.step_shop_menu = 2
      else:
        card['current_image'] = card['left_image']

  def step_2_3(self, mouse_pos):
    i = 0
    current_time = time.time()
    for items in self.all_button_buy:
      button_key = f"buy_{i + 1}"
      button_info = self.all_button_buy[button_key]
      button_collider = button_info[1][1]
      if button_collider.collidepoint(mouse_pos):
        self.all_button_buy[button_key][0] = True
        if self.press_mouse and current_time - self.last_click_times[i] > self.cooldown:
          if self.step_shop_menu == 3:
            self.change_level_data_extras(i + 1)
          elif self.step_shop_menu == 2:
            self.change_level_data_weapon(i + 1)
          self.last_click_times[i] = current_time
      else:
        self.all_button_buy[button_key][0] = False
      i += 1

  def step_return(self, mouse_pos):
    current_time = time.time()
    return_button_index = len(self.all_button_buy)
    if self.button_return_rect.collidepoint(mouse_pos):
      if self.press_mouse and current_time - self.last_click_times[return_button_index] > self.cooldown:
        if self.step_shop_menu == 3:
          self.step_shop_menu = 1
        else:
          self.step_shop_menu -= 1
        self.last_click_times[return_button_index] = current_time

  def right_arrow(self, mouse_pos):
    current_time = time.time()
    index = 0
    if self.button_right_arrow_rect.collidepoint(mouse_pos):
      if self.press_mouse and current_time - self.last_click_time_arrow[index] > self.cooldown:
        if self.step_shop_menu == 2:
          self.step_shop_menu = 3
        self.last_click_time_arrow[index] = current_time

  def left_arrow(self, mouse_pos):
    current_time = time.time()
    index = 1
    if self.button_left_arrow_rect.collidepoint(mouse_pos):
      if self.press_mouse and current_time - self.last_click_time_arrow[index] > self.cooldown:
        if self.step_shop_menu == 3:
          self.step_shop_menu = 2
        self.last_click_time_arrow[index] = current_time

  def change_level_data_weapon(self, id):
    name = self.data_weapons[f"{id}"]["name"]
    level = self.data_weapons[f"{id}"]["level"] + 1
    if level <= 10:
      price = self.data_weapons_price[name][f"level_{level}"]
      if self.game_data["weapon_level"][name] < 10 and self.game_data["money"] >= price:
        rewards = {"money": -price, "weapon_level": {f"{name}": 1,}}
        change_game_data = ChangeGameData(rewards)
        change_game_data.change_params(change_game_data.reward, change_game_data.game_save_data)
        self.update_data()
  
  def change_level_data_extras(self, id):
    name = list(self.data_extras.keys())[id-1]
    level = self.data_extras[name]["level"] + 1
    if level <= 10:
      price = self.data_extras_price[name][f"level_{level}"]
      if self.game_data["extras_level"][name] < 10 and self.game_data["money"] >= price:
        rewards = {"money": -price, "extras_level": {name: 1,}}
        change_game_data = ChangeGameData(rewards)
        change_game_data.change_params(change_game_data.reward, change_game_data.game_save_data)
        self.update_data()

  def run(self):
    clock = pygame.time.Clock()
    self.running = True
    while self.running:
      mouse_pos = pygame.mouse.get_pos()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.press_mouse = True
        elif event.type == pygame.MOUSEBUTTONUP:
          self.press_mouse = False
      self.update(mouse_pos)
      self.screen.fill((0, 0, 0))
      self.draw(mouse_pos)
      pygame.display.flip()
      if self.step_shop_menu <= 0:
        self.running = False
      clock.tick(60)
    pygame.quit()

  def update_data(self):
    self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
    self.data_weapons = self.read_data.read_params("data/weapons.txt", "weapons")
    self.data_extras = self.read_data.read_params("data/extras.txt", "extras")
    self.data_weapons = self.load.process_data(self.game_data, "weapon_level", self.data_weapons)
    self.data_extras = self.load.process_data(self.game_data, "extras_level", self.data_extras)
    self.update_weapons_with_levels()
    self.update_extras_with_levels()

    self.shop_table_weapon = self.create_table(self.data_weapons)
    self.weapon_images = {}
    self.create_weapon_images()

    self.shop_table_extras = self.create_table(self.data_extras, str_key=True)
    self.extras_images = {}
    self.create_extras_images()