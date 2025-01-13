import pygame


class UsePowerUp:
    def __init__(self, run):
        self.run = run

    def use_power_up(self):
        if self.run.data_power_up["care_kit"]["activate"]:
            self.run.icon.resource["health"] += self.run.data_power_up["care_kit"][
                "value"
            ]
            self.run.data_power_up["care_kit"]["activate"] = False

        if self.run.data_power_up["survival_ration"]["activate"]:
            self.run.icon.resource["food"] += self.run.data_power_up["survival_ration"][
                "value"
            ]
            self.run.data_power_up["survival_ration"]["activate"] = False

        if self.run.data_power_up["critical_hit"]["activate"]:
            for weapon_id, weapon_data in self.run.data_weapons.items():
                if "critical" in weapon_data:
                    weapon_data["critical"] *= self.run.data_power_up["critical_hit"][
                        "value"
                    ]
            self.run.data_power_up["critical_hit"]["activate"] = False

        if self.run.data_power_up["2nd_life"]["activate"]:
            self.run.life = 2
            self.run.data_power_up["2nd_life"]["activate"] = False

        if self.run.data_power_up["expert"]["activate"]:
            self.run.xp_multiplier *= self.run.data_power_up["expert"]["value"]
            self.run.data_power_up["expert"]["activate"] = False

        if self.run.data_power_up["boost"]["activate"]:
            self.run.speed_init *= self.run.data_power_up["boost"]["value"]
            self.run.data_power_up["boost"]["activate"] = False

        if self.run.data_power_up["agile_fingers"]["activate"]:
            for weapon_id, weapon_data in self.run.data_weapons.items():
                if "recharge_time" in weapon_data:
                    weapon_data["recharge_time"] *= self.run.data_power_up[
                        "agile_fingers"
                    ]["value"]
            self.run.data_power_up["agile_fingers"]["activate"] = False

        if self.run.data_power_up["extra_ammo"]["activate"]:
            for weapon_id, weapon_data in self.run.data_weapons.items():
                if "charger_capacity" in weapon_data:
                    weapon_data["charger_capacity"] += self.run.data_power_up[
                        "extra_ammo"
                    ]["value"]
            self.run.data_power_up["extra_ammo"]["activate"] = False

        if self.run.data_power_up["large_range"]["activate"]:
            for weapon_id, weapon_data in self.run.data_weapons.items():
                if "range" in weapon_data:
                    weapon_data["range"] *= self.run.data_power_up["large_range"][
                        "value"
                    ]
            self.run.data_power_up["large_range"]["activate"] = False

        if self.run.data_power_up["magnetic"]["activate"]:
            self.run.range_obj *= self.run.data_power_up["magnetic"]["value"]
            self.run.data_power_up["magnetic"]["activate"] = False

        if self.run.data_power_up["rapid_fire"]["activate"]:
            for weapon_id, weapon_data in self.run.data_weapons.items():
                if "rate" in weapon_data:
                    weapon_data["rate"] *= self.run.data_power_up["rapid_fire"]["value"]
            self.run.data_power_up["rapid_fire"]["activate"] = False

        if self.run.data_power_up["strong_stomach"]["activate"]:
            self.run.hunger_resistance *= self.run.data_power_up["strong_stomach"][
                "value"
            ]
            self.run.data_power_up["strong_stomach"]["activate"] = False

        if self.run.data_power_up["zoom"]["activate"]:
            self.run.zoom = 1.5
            self.run.manager.change_zoom()
            self.run.data_power_up["zoom"]["activate"] = False

        if self.run.data_power_up["regeneration"]["activate"]:
            self.run.regeneration += self.run.data_power_up["regeneration"]["value"]
            self.run.data_power_up["regeneration"]["activate"] = False

        if self.run.data_power_up["piercing"]["activate"]:
            self.run.piercing += self.run.data_power_up["piercing"]["value"]
            self.run.data_power_up["piercing"]["activate"] = False
