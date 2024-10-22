import pygame
import time
from load import *
from change_game_data import ChangeGameData

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

    self.data_weapons = self.load.process_data(self.game_data, "weapon_level", self.data_weapons)
    self.data_extras = self.load.process_data(self.game_data, "extras_level", self.data_extras)
    self.update_weapons_with_levels()
    self.update_extras_with_levels()

    # money icon
    self.icon_money = pygame.image.load("res/shop/icon_money.png")
    self.icon_money_rect = self.icon_money.get_rect()
    self.icon_money_rect.center = (80, 30)

    # return button
    self.button_return = pygame.image.load("res/shop/button_return.png").convert_alpha()
    self.button_return_click = pygame.image.load("res/shop/button_return_click.png").convert_alpha()
    self.button_return_rect = self.button_return.get_rect()
    self.button_return_rect.center = (975, 25)
    self.button_return_original_pos = self.button_return_rect.topleft
    #? maybe create a class for buttons
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
    self.shop_table_extras = self.create_table(self.data_extras, extras=True)
    self.extras_images = {}
    # todo create_extras_images()
    self.create_extras_images()

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

  def create_table(self, weapons_params, rows=2, cols=6, extras=False):
    shop_table_weapon = []
    if extras: 
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
    if self.step_shop_menu == 1:
      self.screen.blit(self.steps["step_1"]["cards"][0]['current_image'], self.steps["step_1"]["cards"][0]['rect'])
    
    if self.step_shop_menu == 2 or self.step_shop_menu == 3:
      self.screen.blit(self.icon_money, self.icon_money_rect)
      number_text = self.font.render(f"{self.game_data["money"]}", True, (255, 255, 255))
      text_rect = number_text.get_rect()
      text_rect.topleft = (self.icon_money_rect.centerx + 25, self.icon_money_rect.topleft[1])
      self.screen.blit(number_text, text_rect)

      if self.step_shop_menu == 3:
        self.screen.blit(self.button_left_arrow, self.button_left_arrow_rect)
        index_name = 0
        for line in range(2):
          for row in range(6):
            if self.shop_table_extras[line][row] != 0:
              name = self.extras_names[index_name]
            else:
              name = "LOCK"
            try:
              name_extra = list(self.data_extras.keys())[index_name]
              dict_extra = self.data_extras[name_extra]
            except IndexError:
              name_extra = None
            index_name += 1

            x = 40 + row * 160
            y = line
            self.back_weapon_rect.x = x
            self.back_weapon_rect.y = 60 + y * 260
            self.screen.blit(self.back_weapon, self.back_weapon_rect)

            number_text = self.font.render(name, True, (255, 255, 255))
            text_rect = number_text.get_rect()
            text_rect.center = (self.back_weapon_rect.x + self.back_weapon_rect.width // 2, 
                                self.back_weapon_rect.y + 25 + self.back_weapon_rect.height // 2)
            self.screen.blit(number_text, text_rect)

            if name != "LOCK":
              texts = {"DPS : ": ["damage", (254, 27, 0), 100], "LEVEL : ": ["level", (121, 248, 248), 80]}
              for name_text in texts.keys():
                text = self.font.render(name_text + str(dict_extra[texts[name_text][0]]), True, texts[name_text][1])
                text_rect = text.get_rect()
                text_rect.topleft = (self.back_weapon_rect.x, 
                                    self.back_weapon_rect.y + texts[name_text][2])
                self.screen.blit(text, text_rect)

            if name_extra != None:
              if dict_extra["level"] < 10:
                price = str(self.data_extras_price[f"{dict_extra["name"]}"][f"level_{dict_extra["level"]+1}"]) + "$"
              else: 
                price = "-- MAX --"
              text = self.font.render("PRICE", True, (255, 255, 255))
              text_rect = text.get_rect()
              text_rect.topleft = (self.back_weapon_rect.x, 
                                  self.back_weapon_rect.y + 180)
              self.screen.blit(text, text_rect)
              text = self.font.render(price, True, (255, 255, 255))
              text_rect = text.get_rect()
              text_rect.center = (self.back_weapon_rect.x + 35, 
                                  self.back_weapon_rect.y + 210)
              self.screen.blit(text, text_rect)

              if self.all_button_buy[f"buy_{index_name}"][0] == False:
                self.screen.blit(self.all_button_buy[f"buy_{index_name}"][1][0], self.all_button_buy[f"buy_{index_name}"][1][1])
              else:
                topleft = self.all_button_buy[f"buy_{index_name}"][1][3]
                topleft = (topleft[0] + 2, topleft[1] + 2)
                self.screen.blit(self.all_button_buy[f"buy_{index_name}"][1][2], topleft)

            rect = self.extras_images[name][1]
            rect.center = (self.back_weapon_rect.x + self.back_weapon_rect.width // 2, self.back_weapon_rect.y + self.back_weapon_rect.height // 2)
            self.screen.blit(self.extras_images[name][0], rect)

      if self.step_shop_menu == 2:
        self.screen.blit(self.button_right_arrow, self.button_right_arrow_rect)
        weapon_id = 0
        for line in range(2):
          for row in range(6):
            if self.shop_table_weapon[line][row] != 0:
              weapon_name_screen = self.weapon_names[weapon_id]
            else:
              weapon_name_screen = "LOCK"
            weapon_id += 1
            weapon_dict = self.data_weapons[f"{weapon_id}"]

            # Draw background
            x = 40 + row * 160
            y = line
            self.back_weapon_rect.x = x
            self.back_weapon_rect.y = 60 + y * 260
            self.screen.blit(self.back_weapon, self.back_weapon_rect)
            
            # Draw texts
            number_text = self.font.render(weapon_name_screen, True, (255, 255, 255))
            text_rect = number_text.get_rect()
            text_rect.center = (self.back_weapon_rect.x + self.back_weapon_rect.width // 2, 
                                self.back_weapon_rect.y + 25 + self.back_weapon_rect.height // 2)
            self.screen.blit(number_text, text_rect)

            if weapon_name_screen != "LOCK":
              texts = {"DPS : ": ["damage", (254, 27, 0), 100], "RANGE : ": ["range", (1, 215, 88), 120], "LEVEL : ": ["level", (121, 248, 248), 80]}
              for name_text in texts.keys():
                text = self.font.render(name_text + str(weapon_dict[texts[name_text][0]]), True, texts[name_text][1])
                text_rect = text.get_rect()
                text_rect.topleft = (self.back_weapon_rect.x, 
                                    self.back_weapon_rect.y + texts[name_text][2])
                self.screen.blit(text, text_rect)

            if weapon_dict["name"] != "knife":
              if weapon_dict["level"] < 10:
                price = str(self.data_weapons_price[f"{weapon_dict["name"]}"][f"level_{weapon_dict["level"]+1}"]) + "$"
              else: 
                price = "-- MAX --"
              text = self.font.render("PRICE", True, (255, 255, 255))
              text_rect = text.get_rect()
              text_rect.topleft = (self.back_weapon_rect.x, 
                                  self.back_weapon_rect.y + 180)
              self.screen.blit(text, text_rect)
              text = self.font.render(price, True, (255, 255, 255))
              text_rect = text.get_rect()
              text_rect.center = (self.back_weapon_rect.x + 35, 
                                  self.back_weapon_rect.y + 210)
              self.screen.blit(text, text_rect)

              if self.all_button_buy[f"buy_{weapon_id}"][0] == False:
                self.screen.blit(self.all_button_buy[f"buy_{weapon_id}"][1][0], self.all_button_buy[f"buy_{weapon_id}"][1][1])
              else:
                topleft = self.all_button_buy[f"buy_{weapon_id}"][1][3]
                topleft = (topleft[0] + 2, topleft[1] + 2)
                self.screen.blit(self.all_button_buy[f"buy_{weapon_id}"][1][2], topleft)

            # Draw weapon
            rect = self.weapon_images[weapon_name_screen][1]
            rect.center = (self.back_weapon_rect.x + self.back_weapon_rect.width // 2, self.back_weapon_rect.y + self.back_weapon_rect.height // 2)
            self.screen.blit(self.weapon_images[weapon_name_screen][0], rect)

    # Vérifier si la souris survole le bouton retour
    if self.button_return_rect.collidepoint(mouse_pos):
      # Afficher l'image survolée et déplacer le bouton légèrement
      self.screen.blit(self.button_return_click, self.button_return_rect)
      self.button_return_rect.topleft = (self.button_return_original_pos[0] + 1, self.button_return_original_pos[1] + 1)
    else:
      # Revenir à l'image normale et à la position originale
      self.screen.blit(self.button_return, self.button_return_rect)
      self.button_return_rect.topleft = self.button_return_original_pos

  def update(self, mouse_pos: tuple):
    self.step_return(mouse_pos)
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

    self.shop_table_extras = self.create_table(self.data_extras, extras=True)
    self.extras_images = {}
    self.create_extras_images()