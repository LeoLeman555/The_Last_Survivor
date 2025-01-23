import pygame
import time
from itertools import islice
from src.data_handling.load import *
from src.data_handling.read_data import *
from src.data_handling.change_game_data import *
from src.UI.scenes.tutorial import *
from src.UI.widgets.button import *


class Shop:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 600))

        pygame.display.set_caption("The Last Survivor - Shop")
        pygame.display.set_icon(pygame.image.load("res/icons/official_logo.png"))

        self.font = pygame.font.Font("res/fonts/futurist_font.ttf", 18)
        self.title_font = pygame.font.Font("res/fonts/futurist_font.ttf", 25)

        # load all the data
        self.read_data = ReadData()
        self.load = Load()
        self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
        self.data_extras = self.read_data.read_params("data/extras.txt", "extras")
        self.data_extras_levels = self.read_data.read_params(
            "data/extras_level.txt", "extras_level"
        )
        self.data_extras_price = self.read_data.read_params(
            "data/extras_price.txt", "price"
        )
        self.data_weapons = self.read_data.read_params("data/weapons.txt", "weapons")
        self.data_weapons_levels = self.read_data.read_params(
            "data/weapons_level.txt", "weapons_level"
        )
        self.data_weapons_price = self.read_data.read_params(
            "data/weapons_price.txt", "price"
        )
        self.data_power_up = self.read_data.read_params("data/power_up.txt", "power_up")
        self.data_power_up_price = self.read_data.read_params(
            "data/power_up_price.txt", "price"
        )

        self.data_weapons = self.load.process_data(
            self.game_data, "weapon_level", self.data_weapons
        )
        self.data_extras = self.load.process_data(
            self.game_data, "extras_level", self.data_extras
        )
        self.data_power_up = self.load.process_data(
            self.game_data, "power_up_level", self.data_power_up
        )
        self.update_with_levels(self.data_weapons, self.data_weapons_levels)
        self.update_with_levels(self.data_extras, self.data_extras_levels)

        self.FPS = int(self.game_data["options"]["fps"])

        self.tutorial = Tutorial()

        # money icon
        self.icon_money = pygame.image.load("res/shop/icon_money.png")
        self.icon_money_rect = self.icon_money.get_rect()
        self.icon_money_rect.center = (80, 30)

        # return button
        self.button_return = Button("button_return", (975, 25))

        # buy button
        self.button_buy = pygame.image.load("res/shop/button_buy.png").convert_alpha()
        self.button_buy_click = pygame.image.load(
            "res/shop/button_buy_click.png"
        ).convert_alpha()
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
        self.back_object = pygame.image.load("res/shop/back_object.png").convert_alpha()
        self.back_object_rect = self.back_object.get_rect()

        self.weapon_names = [
            "Pistol",
            "Magnum",
            "Shotgun",
            "Sniper",
            "AK",
            "RPG",
            "Flamethrower",
            "Minigun",
            "G. Launcher",
            "Laser Gun",
            "Plasma Gun",
        ]
        self.shop_table_weapon = self.create_table(self.data_weapons)
        self.weapon_images = self.create_images(self.data_weapons, self.weapon_names, 1)

        self.extras_names = ["Grenade", "Toxic G.", "Drone", "Missile", "Laser Probe"]
        self.shop_table_extras = self.create_table(self.data_extras, str_key=True)
        self.extras_images = self.create_images(self.data_extras, self.extras_names, 2)

        self.power_up_names = [
            "Care kit",
            "Survival ration",
            "2nd life",
            "Critical hit",
            "Expert",
            "Boost",
            "Agile fingers",
            "Extra ammo",
            "Large range",
            "Magnetic",
            "Piercing",
            "Rapid fire",
            "Regeneration",
            "Zoom",
            "Strong stomach",
        ]
        self.shop_tables_power_up = [
            self.create_table(
                dict(islice(self.data_power_up.items(), 12)), str_key=True
            ),
            self.create_table(
                dict(islice(self.data_power_up.items(), 12, None)), str_key=True
            ),
        ]
        self.power_up_images = self.create_images(
            self.data_power_up, self.power_up_names, 3
        )

        self.shop_step = 1

        self.steps = {
            "step_1": {
                "cards": [],
                "positions": [(200, 100), (600, 100)],
                "names": ["card_weapon_extras", "card_power_up"],
                "effect": [2, 4],
            }
        }
        self.steps = self.create_cards(self.steps)

        self.press_mouse = False
        self.last_click_times = [0] * (len(self.all_button_buy) + 1)
        self.last_click_time_arrow = [0, 0]
        self.cooldown = 0.5

    def draw(self, mouse_pos):
        self.button_return.draw(self.screen, mouse_pos)
        self.screen.blit(self.icon_money, self.icon_money_rect)
        number_text = self.font.render(
            f"{self.game_data['money']}", True, (255, 255, 255)
        )
        text_rect = number_text.get_rect()
        text_rect.topleft = (
            self.icon_money_rect.centerx + 25,
            self.icon_money_rect.topleft[1],
        )
        self.screen.blit(number_text, text_rect)

        if self.shop_step <= 1:
            title_text = self.title_font.render("SHOP", True, (255, 255, 255))
            title_text_rect = title_text.get_rect()
            title_text_rect.center = (500, 30)
            self.screen.blit(title_text, title_text_rect)
            pygame.draw.line(self.screen, (255, 255, 255), (480, 45), (530, 45))
            self.screen.blit(
                self.steps["step_1"]["cards"][0]["current_image"],
                self.steps["step_1"]["cards"][0]["rect"],
            )
            self.screen.blit(
                self.steps["step_1"]["cards"][1]["current_image"],
                self.steps["step_1"]["cards"][1]["rect"],
            )
        else:
            self.draw_steps()

        if self.game_data["options"]["tutorial"] == "on":
            self.tutorial.draw_shop(self.screen, self.shop_step)

    def draw_elements(
        self,
        data: dict,
        data_price: dict,
        stats: dict,
        images: dict,
        shop_table: list[int],
        position: list[int],
        fake_names: list[str],
        data_names: list,
        number_line: int,
        number_row: int,
        max_level: int,
    ):
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
                self.back_object_rect.x = x
                self.back_object_rect.y = y_start + y * y_interval
                if index_name != None:
                    self.screen.blit(self.back_object, self.back_object_rect)

                # draw the name
                if index_name != None:
                    text = self.font.render(draw_name, True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.center = (
                        self.back_object_rect.x + self.back_object_rect.width // 2,
                        self.back_object_rect.y
                        + 25
                        + self.back_object_rect.height // 2,
                    )
                    self.screen.blit(text, text_rect)

                # draw stats
                if draw_name != "LOCK":
                    for name_text in stats.keys():
                        text = self.font.render(
                            name_text + str(dict_element[stats[name_text][0]]),
                            True,
                            stats[name_text][1],
                        )
                        text_rect = text.get_rect()
                        text_rect.topleft = (
                            self.back_object_rect.x,
                            self.back_object_rect.y + stats[name_text][2],
                        )
                        self.screen.blit(text, text_rect)

                # draw price
                if index_name != None:
                    if dict_element["level"] < max_level:
                        price = (
                            str(
                                data_price[f"{dict_element['name']}"][
                                    f"level_{dict_element['level']+1}"
                                ]
                            )
                            + "$"
                        )
                    else:
                        price = "-- MAX --"
                    text = self.font.render("PRICE", True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.topleft = (
                        self.back_object_rect.x,
                        self.back_object_rect.y + 180,
                    )
                    self.screen.blit(text, text_rect)
                    text = self.font.render(price, True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.center = (
                        self.back_object_rect.x + 35,
                        self.back_object_rect.y + 210,
                    )
                    self.screen.blit(text, text_rect)

                    # draw buy button
                    if self.all_button_buy[f"buy_{index_id}"][0] == False:
                        self.screen.blit(
                            self.all_button_buy[f"buy_{index_id}"][1][0],
                            self.all_button_buy[f"buy_{index_id}"][1][1],
                        )
                    else:
                        topleft = self.all_button_buy[f"buy_{index_id}"][1][3]
                        topleft = (topleft[0] + 2, topleft[1] + 2)
                        self.screen.blit(
                            self.all_button_buy[f"buy_{index_id}"][1][2], topleft
                        )

                # draw the image
                if index_name != None:
                    rect = images[draw_name][1]
                    rect.center = (
                        self.back_object_rect.x + self.back_object_rect.width // 2,
                        self.back_object_rect.y + self.back_object_rect.height // 2,
                    )
                    self.screen.blit(images[draw_name][0], rect)

    def draw_steps(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.shop_step % 2 == 0:
            if self.button_right_arrow_rect.collidepoint(mouse_pos):
                zoomed_arrow, zoomed_rect = self.zoom_image(
                    self.button_right_arrow, self.button_right_arrow_rect
                )
                self.screen.blit(zoomed_arrow, zoomed_rect)
            else:
                self.screen.blit(self.button_right_arrow, self.button_right_arrow_rect)
        else:
            if self.button_left_arrow_rect.collidepoint(mouse_pos):
                zoomed_arrow, zoomed_rect = self.zoom_image(
                    self.button_left_arrow, self.button_left_arrow_rect
                )
                self.screen.blit(zoomed_arrow, zoomed_rect)
            else:
                self.screen.blit(self.button_left_arrow, self.button_left_arrow_rect)

        if self.shop_step == 2:
            title_text = self.title_font.render("WEAPONS SHOP", True, (255, 255, 255))
            title_text_rect = title_text.get_rect()
            title_text_rect.center = (500, 30)
            self.screen.blit(title_text, title_text_rect)
            pygame.draw.line(self.screen, (255, 255, 255), (450, 45), (590, 45))

            stats = {
                "DPS : ": ["damage", (254, 27, 0), 100],
                "RANGE : ": ["range", (1, 215, 88), 120],
                "LEVEL : ": ["level", (121, 248, 248), 80],
            }
            position = [40, 160, 60, 260]
            data_names = []
            for item in self.data_weapons:
                data_names.append(item)
            self.draw_elements(
                self.data_weapons,
                self.data_weapons_price,
                stats,
                self.weapon_images,
                self.shop_table_weapon,
                position,
                self.weapon_names,
                data_names,
                2,
                6,
                10,
            )

        elif self.shop_step == 3:
            title_text = self.title_font.render("EXTRAS SHOP", True, (255, 255, 255))
            title_text_rect = title_text.get_rect()
            title_text_rect.center = (500, 30)
            self.screen.blit(title_text, title_text_rect)
            pygame.draw.line(self.screen, (255, 255, 255), (450, 45), (590, 45))

            stats = {
                "DPS : ": ["damage", (254, 27, 0), 100],
                "LEVEL : ": ["level", (121, 248, 248), 80],
            }
            position = [40, 160, 60, 260]
            data_names = list(self.data_extras.keys())
            self.draw_elements(
                self.data_extras,
                self.data_extras_price,
                stats,
                self.extras_images,
                self.shop_table_extras,
                position,
                self.extras_names,
                data_names,
                2,
                6,
                10,
            )

        elif self.shop_step == 4:
            title_text = self.title_font.render("POWER-UP SHOP", True, (255, 255, 255))
            title_text_rect = title_text.get_rect()
            title_text_rect.center = (500, 30)
            self.screen.blit(title_text, title_text_rect)
            pygame.draw.line(self.screen, (255, 255, 255), (450, 45), (600, 45))

            stats = {
                "LEVEL : ": ["level", (121, 248, 248), 80],
                "": ["effect", (254, 27, 0), 100],
            }
            position = [40, 160, 60, 260]
            data = dict(islice(self.data_power_up.items(), 12))
            prices = dict(islice(self.data_power_up_price.items(), 12))
            images = dict(
                islice(self.power_up_images.items(), 13)
            )  # +1 because of the "LOCK" in the first position
            data_names = list(self.data_power_up.keys())[:12]
            fake_names = self.power_up_names[:12]
            self.draw_elements(
                data,
                prices,
                stats,
                images,
                self.shop_tables_power_up[0],
                position,
                fake_names,
                data_names,
                2,
                6,
                1,
            )

        elif self.shop_step == 5:
            title_text = self.title_font.render("POWER-UP SHOP", True, (255, 255, 255))
            title_text_rect = title_text.get_rect()
            title_text_rect.center = (500, 30)
            self.screen.blit(title_text, title_text_rect)
            pygame.draw.line(self.screen, (255, 255, 255), (450, 45), (600, 45))

            stats = {
                "LEVEL : ": ["level", (121, 248, 248), 80],
                "": ["effect", (254, 27, 0), 100],
            }
            position = [40, 160, 60, 260]
            data = dict(islice(self.data_power_up.items(), 12, None))
            prices = dict(islice(self.data_power_up_price.items(), 12, None))
            images = dict(
                islice(self.power_up_images.items(), 13, None)
            )  # +1 because of the "LOCK" in the first position
            images["LOCK"] = self.power_up_images["LOCK"]
            data_names = list(self.data_power_up.keys())[12:]
            fake_names = self.power_up_names[12:]
            self.draw_elements(
                data,
                prices,
                stats,
                images,
                self.shop_tables_power_up[1],
                position,
                fake_names,
                data_names,
                2,
                6,
                1,
            )

    def update(self, mouse_pos: tuple):
        self.press_buttons(mouse_pos)
        if self.shop_step == 1:
            self.click_cards(mouse_pos)
        elif 2 <= self.shop_step <= 5:
            self.buy(mouse_pos)

    def press_buttons(self, mouse_pos):
        current_time = time.time()
        # Checks whether the back button is pressed
        return_button_index = len(self.all_button_buy)
        if self.button_return.is_pressed(mouse_pos, self.press_mouse):
            if (
                current_time - self.last_click_times[return_button_index]
                > self.cooldown
            ):
                if self.shop_step == 1:
                    self.shop_step = 0
                else:
                    self.shop_step = 1
                self.last_click_times[return_button_index] = current_time

        # Internal function for checking arrows
        def check_arrow_button(button_rect, index, from_step, to_step):
            if button_rect.collidepoint(mouse_pos) and self.press_mouse:
                if current_time - self.last_click_time_arrow[index] > self.cooldown:
                    if self.shop_step == from_step:
                        self.shop_step = to_step
                        self.last_click_time_arrow[index] = current_time

        # Checks the arrow buttons
        check_arrow_button(self.button_right_arrow_rect, 0, 2, 3)
        check_arrow_button(self.button_right_arrow_rect, 0, 4, 5)
        check_arrow_button(self.button_left_arrow_rect, 1, 3, 2)
        check_arrow_button(self.button_left_arrow_rect, 1, 5, 4)

    def click_cards(self, mouse_pos):
        for i, card in enumerate(self.steps["step_1"]["cards"][:], start=0):
            if card["rect"].collidepoint(mouse_pos):
                card["current_image"] = card["right_image"]
                if self.press_mouse:
                    self.shop_step = self.steps["step_1"]["effect"][i]
            else:
                card["current_image"] = card["left_image"]

    def buy(self, mouse_pos):
        i = 0
        current_time = time.time()
        for items in self.all_button_buy:
            button_key = f"buy_{i + 1}"
            button_info = self.all_button_buy[button_key]
            button_collider = button_info[1][1]
            if button_collider.collidepoint(mouse_pos):
                self.all_button_buy[button_key][0] = True
                if (
                    self.press_mouse
                    and current_time - self.last_click_times[i] > self.cooldown
                ):
                    if self.shop_step == 2:
                        self.change_level_data_weapon(i + 1)
                    elif self.shop_step == 3:
                        self.change_level_data_extras(i + 1)
                    elif self.shop_step == 4:
                        self.change_level_data_power_up(i + 1)
                    elif self.shop_step == 5:
                        self.change_level_data_power_up(i + 1 + 12)
                    self.last_click_times[i] = current_time
            else:
                self.all_button_buy[button_key][0] = False
            i += 1

    def change_level_data_weapon(self, id):
        name = self.data_weapons[f"{id}"]["name"]
        level = self.data_weapons[f"{id}"]["level"] + 1
        if level <= 10:
            price = self.data_weapons_price[name][f"level_{level}"]
            if (
                self.game_data["weapon_level"][name] < 10
                and self.game_data["money"] >= price
            ):
                rewards = {
                    "money": -price,
                    "weapon_level": {
                        f"{name}": 1,
                    },
                }
                change_game_data = ChangeGameData(rewards)
                change_game_data.change_params(
                    change_game_data.reward, change_game_data.game_save_data
                )
                self.update_data()

    def change_level_data_extras(self, id):
        name = list(self.data_extras.keys())[id - 1]
        level = self.data_extras[name]["level"] + 1
        if level <= 10:
            price = self.data_extras_price[name][f"level_{level}"]
            if (
                self.game_data["extras_level"][name] < 10
                and self.game_data["money"] >= price
            ):
                rewards = {
                    "money": -price,
                    "extras_level": {
                        name: 1,
                    },
                }
                change_game_data = ChangeGameData(rewards)
                change_game_data.change_params(
                    change_game_data.reward, change_game_data.game_save_data
                )
                self.update_data()

    def change_level_data_power_up(self, id):
        name = list(self.data_power_up.keys())[id - 1]
        level = self.data_power_up[name]["level"] + 1
        if level <= 1:
            price = self.data_power_up_price[name][f"level_{level}"]
            if (
                self.game_data["power_up_level"][name] < 1
                and self.game_data["money"] >= price
            ):
                rewards = {
                    "money": -price,
                    "power_up_level": {
                        name: 1,
                    },
                }
                change_game_data = ChangeGameData(rewards)
                change_game_data.change_params(
                    change_game_data.reward, change_game_data.game_save_data
                )
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            self.update(mouse_pos)
            self.screen.fill((0, 0, 0))
            self.draw(mouse_pos)
            pygame.display.flip()
            if self.shop_step <= 0:
                self.running = False
            clock.tick(self.FPS)

    def create_cards(self, dict_cards: dict):
        cards = dict_cards
        for i, name in enumerate(cards["step_1"]["names"]):
            left_image, right_image = self.get_image(name)
            position = cards["step_1"]["positions"][i]
            rect = left_image.get_rect(topleft=position)
            cards["step_1"]["cards"].append(
                {
                    "name": name,
                    "left_image": left_image,
                    "right_image": right_image,
                    "current_image": left_image,
                    "rect": rect,
                }
            )
        return cards

    def get_image(self, name: str):
        image_path = f"res/shop/{name}.png"
        image = pygame.image.load(image_path).convert_alpha()
        return Load.split_image(self, image)

    def create_images(self, data: dict, names: list, step: int):
        dict_images = {}
        lock_image_path = "res/shop/lock.png"
        lock_image = pygame.image.load(lock_image_path).convert_alpha()
        lock_rect = lock_image.get_rect()

        dict_images["LOCK"] = [lock_image, lock_rect]
        for index, key_name in enumerate(names, start=0):
            if step == 1:
                dict = data.get(f"{index+1}", {})
                name = dict.get("name", "")
                level = dict.get("level", 0)
            else:
                name = list(data.keys())[index]
                level = data[name]["level"]

            if level >= 1:
                if step == 1:
                    image_path = f"res/weapon/{name}/level_{level}.png"
                elif step == 2:
                    image_path = f"res/shop/extras/{name}.png"
                elif step == 3:
                    image_path = f"res/shop/power_up/{name}.png"
            else:
                image_path = lock_image_path

            image = pygame.image.load(image_path).convert_alpha()
            rect = image.get_rect()
            dict_images[key_name] = [image, rect]
        return dict_images

    def create_table(self, params, rows=2, cols=6, str_key=False):
        table = []
        if str_key:
            levels = [params[id]["level"] for id in params.keys()]
        else:
            levels = [params[id]["level"] for id in sorted(params.keys(), key=int)]
        while len(levels) < rows * cols:
            levels.append(0)
        for i in range(rows):
            table.append(levels[i * cols : (i + 1) * cols])
        return table

    def update_with_levels(self, dict, data_levels):
        for id, data in dict.items():
            name = data["name"]
            level = data["level"]
            if level > 0:
                level_upgrades = data_levels.get(name, {})
                for stat, upgrade_value in level_upgrades.items():
                    if stat in data:
                        if stat == "critical":
                            data[stat] += upgrade_value * (level - 1)
                        else:
                            data[stat] += int(upgrade_value * (level - 1))

    def zoom_image(self, image, rect, zoom_factor=1.1):
        width, height = image.get_size()
        new_size = (int(width * zoom_factor), int(height * zoom_factor))
        zoomed_image = pygame.transform.scale(image, new_size)
        new_rect = zoomed_image.get_rect(center=rect.center)
        return zoomed_image, new_rect

    def update_data(self):
        self.game_data = self.read_data.read_params("data/game_save.txt", "game_save")
        self.data_weapons = self.read_data.read_params("data/weapons.txt", "weapons")
        self.data_extras = self.read_data.read_params("data/extras.txt", "extras")
        self.data_power_up = self.read_data.read_params("data/power_up.txt", "power_up")
        self.data_weapons = self.load.process_data(
            self.game_data, "weapon_level", self.data_weapons
        )
        self.data_extras = self.load.process_data(
            self.game_data, "extras_level", self.data_extras
        )
        self.data_power_up = self.load.process_data(
            self.game_data, "power_up_level", self.data_power_up
        )
        self.update_with_levels(self.data_weapons, self.data_weapons_levels)
        self.update_with_levels(self.data_extras, self.data_extras_levels)

        self.shop_table_weapon = self.create_table(self.data_weapons)
        self.weapon_images = self.create_images(self.data_weapons, self.weapon_names, 1)

        self.shop_table_extras = self.create_table(self.data_extras, str_key=True)
        self.extras_images = self.create_images(self.data_extras, self.extras_names, 2)

        self.shop_tables_power_up = self.shop_tables_power_up = [
            self.create_table(
                dict(islice(self.data_power_up.items(), 12)), str_key=True
            ),
            self.create_table(
                dict(islice(self.data_power_up.items(), 12, None)), str_key=True
            ),
        ]
        self.power_up_images = self.create_images(
            self.data_power_up, self.power_up_names, 3
        )
